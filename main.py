# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: main.py
@time: 2026/4/4 12:30 
@desc: 异步优化版业务实现 - 增强资源管理与生命周期控制
"""
import asyncio
import copy
import json
import os
import traceback
import re
import hashlib
from pipeline import RAGPipeline
from pymilvus import DataType, Function, FunctionType, AnnSearchRequest, RRFRanker
from schemas import LLMResponse
from concurrent.futures import ThreadPoolExecutor
from components import Messages


class MilvusTest(RAGPipeline):
    """
    Milvus 业务实现类
    """

    def __init__(self, collection_name):
        super().__init__()
        self.collection_name = collection_name

    async def find_answer_from_db(self, question, limit=5, distance_threshold=0.6):
        """
        异步检索知识库
        """
        # 确保使用异步向量转换
        query_vector = await self.embedding.aembed_query(question)

        # 异步搜索数据库
        search_result = await self.client_db.search(
            self.collection_name,
            data=[query_vector],
            limit=limit,
            output_fields=["content", "path"]
        )
        contexts = []
        if search_result and len(search_result) > 0:
            for sr in search_result[0]:
                distance = sr["distance"]
                if distance < distance_threshold:
                    continue
                content = sr["entity"]["content"]
                path = sr["entity"]["path"]
                if content:
                    # 仅收集相关背景，不污染全局对话记忆
                    contexts.append(f"【来源: {path}】(相似度: {distance:.4f})\n{content}")

        if not contexts:
            return ""
        self.logger.info(f"contexts:{len(contexts)}")
        sim = await self.reranker.infinity_search(contexts, question)
        if not sim:
            return ""
        self.logger.info(f"sim:{len(sim)}")
        new_contexts = [f"{i} 重排相似度:{j:.4f}" for i, j in sim]
        print("new_contexts", new_contexts)
        return "\n\n".join(new_contexts)

    async def insert_db(self):
        """
        异步入库，利用线程池分流计算密集型的切片任务
        """
        # 严格读取 config.yaml 中的正确字段名
        chunk_size = self.normal_config.get("doc_chunk_size")
        chunk_overlap = self.normal_config.get("doc_chunk_overlap")
        batch_size = self.normal_config.get("batch_size")

        loop = asyncio.get_running_loop()
        # 将同步的 Markdown 切片逻辑交给线程池
        docs = await loop.run_in_executor(
            self.executor,
            self.load_docs.split_documents_by_mhts,
            chunk_size,
            chunk_overlap
        )
        total_docs = len(docs)
        for i in range(0, total_docs, batch_size):
            self.logger.info(f"正在处理入库批次: {min(i + batch_size, total_docs)}/{total_docs}")
            batch_docs = docs[i:i + batch_size]
            text_list = [doc.page_content.strip() for doc in batch_docs]
            path_list = [doc.metadata.get("source", "unknown") for doc in batch_docs]

            # 异步方法批量计算向量
            eb_list = await self.embedding.aembed_documents(text_list)

            data = []
            data_hash_set = set()
            for text, path, eb in zip(text_list, path_list, eb_list):
                doc_hash = hashlib.md5(f"{path}_{text}".encode('utf-8')).hexdigest()
                if doc_hash not in data_hash_set:
                    data.append({
                        "id": doc_hash,
                        "content": text,
                        "path": path,
                        "content_emb": eb
                    })
                    data_hash_set.add(doc_hash)
            if data:
                await self.client_db.upsert(collection_name=self.collection_name, data=data)

    async def _clear_old_collections(self):
        """
        异步删除旧集合
        """
        if await self.client_db.has_collection(self.collection_name):
            await self.client_db.drop_collection(self.collection_name)

    async def _build_schema(self):
        """
        构建数据模型 Schema
        """
        schema = self.client_db.create_schema()
        schema.add_field("id", DataType.VARCHAR, max_length=64, is_primary=True)
        schema.add_field("content", DataType.VARCHAR, max_length=65535)
        schema.add_field("path", DataType.VARCHAR, max_length=1000)
        schema.add_field("content_emb", DataType.FLOAT_VECTOR, dim=768)
        return schema

    async def _build_index(self):
        """
        构建向量索引
        """
        index_params = self.client_db.prepare_index_params()
        index_params.add_index("content_emb", index_name="content_emb_idx", index_type="AUTOINDEX")
        return index_params

    async def create_collections(self):
        """
        异步创建集合
        """
        if not await self.client_db.has_collection(self.collection_name):
            schema = await self._build_schema()
            index_params = await self._build_index()
            await self.client_db.create_collection(
                collection_name=self.collection_name,
                schema=schema,
                index_params=index_params
            )

    async def insert_init_db(self):
        """
        初始化数据库
        """
        await self.create_collections()
        await self.insert_db()

    async def normal_search(self, question, use_db=True, external_context=None):
        """
        异步标准检索增强生成流程
        """
        status = False
        limit_loop_num = self.llm_config.get("limit_loop_num")
        _loop_nums = 0
        while not status and limit_loop_num > 0:
            _loop_nums += 1
            self.logger.info(f"当前第 {_loop_nums} 轮")
            try:
                db_context = external_context or ""
                if use_db and not db_context:
                    db_context = await self.find_answer_from_db(question=question)

                # 将检索内容包装在临时 Prompt 中，不污染上下文
                if db_context:
                    query_prompt = f"请基于以下知识库片段回答问题：\n\n{db_context}\n\n我的问题是：{question}"
                else:
                    query_prompt = question

                temp_messages = self.messages.get_msg().copy()
                temp_messages.append({"role": "user", "content": query_prompt})

                chat_config = {
                    "stream": True,
                    "temperature": 0.9
                }
                # 调用异步 LLM 客户端
                chat_response = await self.client_llm.chat(temp_messages, **chat_config)
                chat_parse_obj = await self.client_llm.parse_chat_response(chat_response)

                if not chat_parse_obj:
                    raise ValueError("ai 响应结果解析异常")

                # 正则清洗，确保提取 JSON 结构
                raw_text = chat_parse_obj.response
                json_match = re.search(r'\{[\s\S]*\}', raw_text)
                if not json_match:
                    raise ValueError(f"大模型未返回合法的JSON结构。原始输出：{raw_text}")

                chat_response_json = json.loads(json_match.group(0))
                self.logger.info(f"ai json结果:{chat_response_json}")
                LLMResponse(**chat_response_json)

                status = chat_parse_obj.stop
                if status:
                    # 仅在最终成功后持久化记忆
                    self.messages.add_user_msg(question)
                    self.messages.add_assistant_msg(json.dumps(chat_response_json, ensure_ascii=False))
                    return chat_response_json
            except Exception as e:
                traceback.self.logger.info_exc()
                msg = f"{traceback.format_exc()}, {e.__traceback__.tb_lineno}"
                if limit_loop_num > 1:
                    self.messages.add_assistant_msg(f"解析失败，请确保格式正确: {msg}")
            finally:
                limit_loop_num -= 1

    async def pre_search(self, question):
        """
        异步预识别检索逻辑
        """
        self.messages.add_user_msg(question)
        prompt = "请先不使用向量数据库查询的相关知识自行生成预识别回复"
        self.messages.add_user_msg(prompt)
        pre_response_json = await self.normal_search(prompt, use_db=False)
        pre_ans = pre_response_json.get("response", "")
        db_context = await self.find_answer_from_db(pre_ans)
        prompt_result = "请基于上述结果分析并输出最终答案"
        response_json = await self.normal_search(prompt_result, use_db=False, external_context=db_context)
        return response_json

    async def plan_and_execute_search(self, question):
        """
        核心优化：并发执行子问题拆解与并行检索
        """
        cp_messages = copy.deepcopy(self.messages).get_msg()
        self.messages.clear_msg()

        # 1. 规划阶段 (Plan)
        plan_system_prompt = """你是一个任务拆解专家。为了全面回答用户的问题，请将其拆解为2到3个核心的搜索子问题。
        【严格指令】你必须且只能输出一个合法的 JSON 格式的字符串数组，绝不能包含任何其他解释性文本。"""

        self.messages.add_system_msg(plan_system_prompt)
        plan_prompt = f"请拆解此问题：{question}"
        self.messages.add_user_msg(plan_prompt)

        try:
            plan_response = await self.client_llm.chat(self.messages.get_msg(), stream=False, temperature=0.1)
            plan_parse_obj = await self.client_llm.parse_chat_response(plan_response)

            array_match = re.search(r'\[[\s\S]*\]', plan_parse_obj.response)
            if array_match:
                sub_questions = json.loads(array_match.group(0))
            else:
                raise ValueError("未能提取出合法的 JSON 数组")
            self.logger.info("【规划阶段】AI 返回的拆解结果:", sub_questions)
        except Exception as e:
            self.logger.error(f"⚠️ 规划阶段异常: {e}，已降级为直接检索原问题。")
            sub_questions = [question]

        self.messages.set_messages(cp_messages)

        # 2. 执行阶段 (Execute) - 缺陷修复：通过 asyncio.gather 并发检索所有子问题
        self.logger.info(f"【执行阶段】正在并发检索 {len(sub_questions)} 个子问题...")
        search_tasks = [self.find_answer_from_db(question=sub_q) for sub_q in sub_questions]
        search_results = await asyncio.gather(*search_tasks)

        all_contexts = []
        for sub_q, sub_ctx in zip(sub_questions, search_results):
            if sub_ctx:
                all_contexts.append(f"<{sub_q} 专项检索结果>\n{sub_ctx}")

        merged_context = "\n\n".join(all_contexts)

        # 3. 综合总结阶段 (Synthesize)
        final_prompt = f"请综合上述所有的规划拆解思路，以及检索到的知识，完整地回答最初的问题：'{question}'"
        self.logger.info("【综合阶段】开始生成最终答案...")
        final_response_json = await self.normal_search(final_prompt, use_db=False, external_context=merged_context)
        return final_response_json

    async def build_test(self):
        """

        :return:
        """
        schema = self.client_db.create_schema()
        schema.add_field(
            "id",
            DataType.INT64,
            is_primary=True,
            auto_id=True
        )
        schema.add_field(
            "text",
            DataType.VARCHAR,
            max_length=1000,
            enable_analyzer=True
        )
        schema.add_field(
            "sparse",
            DataType.SPARSE_FLOAT_VECTOR
        )

        bm25_func = Function(
            name="text_bm25_emb",
            input_field_names=["text"],
            output_field_names=[
                "sparse"
            ],
            function_type=FunctionType.BM25,
        )
        schema.add_function(
            bm25_func
        )

        index = self.client_db.prepare_index_params()
        index.add_index(field_name="sparse", index_type="AUTOINDEX", metric_type="BM25")

        collection_name = "test9"
        # if await self.client_db.has_collection(collection_name):
        #     await self.client_db.drop_collection(collection_name)
        await self.client_db.create_collection(collection_name, schema=schema, index_params=index)

        data_list = [
            {
                "text": "Information retrieval helps users find relevant documents in large datasets."
            },
            {
                "text": "Search engines use information retrieval techniques to index and rank web pages."
            },
            {
                "text": "The core of IR is matching user queries with the most relevant content."
            },
            {
                "text": "Vector search is revolutionising modern information retrieval systems."
            },
            {
                "text": "Machine learning improves ranking algorithms in information retrieval."
            },
            {
                "text": "IR techniques include keyword-based search, semantic search, and vector search."
            },
            {
                "text": "Boolean retrieval is one of the earliest information retrieval methods."
            },
            {"text": "TF-IDF is a classic method used to score document relevance in IR."},
            {
                "text": "Modern IR systems integrate deep learning for better contextual understanding."
            },
            {
                "text": "Milvus is an open-source vector database designed for AI-powered search."
            },
            {
                "text": "Milvus enables fast and scalable similarity search on high-dimensional data."
            },
            {
                "text": "With Milvus, developers can build applications that support image, text, and video retrieval."
            },
            {
                "text": "Milvus integrates well with deep learning frameworks like PyTorch and TensorFlow."
            },
            {
                "text": "The core of Milvus is optimised for approximate nearest neighbour (ANN) search."
            },
            {
                "text": "Milvus supports hybrid search combining structured and unstructured data."
            },
            {
                "text": "Large-scale AI applications rely on Milvus for efficient vector retrieval."
            },
            {"text": "Milvus makes it easy to perform high-speed similarity searches."},
            {"text": "Cloud-native by design, Milvus scales effortlessly with demand."},
            {
                "text": "Milvus powers applications in recommendation systems, fraud detection, and genomics."
            },
            {
                "text": "The latest version of Milvus introduces faster indexing and lower latency."
            },
            {"text": "Milvus supports HNSW, IVF_FLAT, and other popular ANN algorithms."},
            {
                "text": "Vector embeddings from models like OpenAI’s CLIP can be indexed in Milvus."
            },
            {
                "text": "Milvus has built-in support for multi-tenancy in enterprise use cases."
            },
            {
                "text": "The Milvus community actively contributes to improving its performance."
            },
            {
                "text": "Milvus integrates with data pipelines like Apache Kafka for real-time updates."
            },
            {
                "text": "Using Milvus, companies can enhance search experiences with vector search."
            },
            {
                "text": "Milvus plays a crucial role in powering AI search in medical research."
            },
            {"text": "Milvus integrates with LangChain for advanced RAG pipelines."},
            {
                "text": "Open-source contributors continue to enhance Milvus’ search performance."
            },
            {
                "text": "Multi-modal search in Milvus enables applications beyond text and images."
            },
            {"text": "Milvus has an intuitive REST API for easy integration."},
            {"text": "Milvus’ FAISS and HNSW backends provide flexibility in indexing."},
            {
                "text": "The architecture of Milvus ensures fault tolerance and high availability."
            },
            {"text": "Milvus integrates seamlessly with LLM-based applications."},
            {"text": "Startups leverage Milvus to build next-gen AI-powered products."},
            {"text": "Milvus Cloud offers a managed solution for vector search at scale."},
            {
                "text": "The future of AI search is being shaped by Milvus and similar vector databases."
            }
        ]
        # await self.client_db.insert(
        #     collection_name,
        #     data_list
        # )

        search_params = {"metric_type": "BM25", "params": {"drop_ratio_search": 0.2}}

        query_text = "what is Milvus?"
        # Execute search with text query
        results = await self.client_db.search(
            collection_name=collection_name,
            data=[query_text],
            anns_field="sparse",
            limit=10,
            search_params=search_params,
            output_fields=["text"],
        )
        self.logger.info(f"results:{results[0]}")
        docs = [i["entity"]["text"] for i in results[0]]
        infinity_search = await self.reranker.infinity_search(docs, query_text, 2)
        self.logger.info(f"infinity_search:{infinity_search}")

    async def insert_milvus_md(self):
        """

        """
        schema = self.client_db.create_schema()
        schema.add_field(
            "id",
            DataType.VARCHAR,
            max_length=512,
            is_primary=True
        )
        schema.add_field(
            "text",
            DataType.VARCHAR,
            max_length=65535,
            enable_analyzer=True
        )
        schema.add_field(
            "text_emb",
            DataType.FLOAT_VECTOR,
            dim=768
        )

        schema.add_field(
            "sparse",
            DataType.SPARSE_FLOAT_VECTOR
        )

        bm25_func = Function(
            name="text_bm25_emb",
            input_field_names=["text"],
            output_field_names=[
                "sparse"
            ],
            function_type=FunctionType.BM25,
        )
        schema.add_function(bm25_func)

        index_params = self.client_db.prepare_index_params()
        index_params.add_index(field_name="sparse", index_type="AUTOINDEX", metric_type="BM25")
        index_params.add_index(field_name="text_emb", index_type="AUTOINDEX")
        collection_name = "milvus_desc"

        if await self.client_db.has_collection(collection_name):
            await self.client_db.drop_collection(collection_name)
        await self.client_db.create_collection(collection_name, schema=schema, index_params=index_params)

        base_path = "/home/jhc/Projects/Python/ai/rag/milvue_stand/test/mds"
        chunk_size = self.normal_config.get("doc_chunk_size")
        chunk_overlap = self.normal_config.get("doc_chunk_overlap")
        batch_size = self.normal_config.get("batch_size")

        loop = asyncio.get_running_loop()

        # [精准修改 1]: 移除导致 O(N^2) 灾难性重复计算的 get_all_files 外层循环，仅执行一次全量切分
        print("开始全量加载并切分文档...")
        docs = self.load_docs.split_documents_by_mhts(chunk_size, chunk_overlap)
        print("开始执行全局文本去重...")
        unique_docs = []
        hash_set = set()
        for doc in docs:
            text = doc.page_content
            source = doc.metadata.get("source", "unknown_file")
            doc_id = hashlib.md5(f"{source}_{text}".encode('utf-8')).hexdigest()
            if doc_id not in hash_set:
                hash_set.add(doc_id)
                unique_docs.append((doc_id, text))

        len_unique_docs = len(unique_docs)
        print(f"去重完成：原始片段 {len(docs)} 个，有效唯一片段 {len_unique_docs} 个")

        max_concurrency = 500
        executor = ThreadPoolExecutor(max_workers=max_concurrency)
        semaphore = asyncio.Semaphore(max_concurrency)

        async def process_batch(_batch_idx):
            async with semaphore:
                start_idx = _batch_idx * batch_size
                end_idx = (_batch_idx + 1) * batch_size
                batch_tuples = unique_docs[start_idx: end_idx]

                if not batch_tuples:
                    return

                # 解包获取当前批次的 ids 和纯文本
                doc_ids = [t[0] for t in batch_tuples]
                texts = [t[1] for t in batch_tuples]

                # 仅对去重后的文本进行向量化推理
                mock_text_emb_ts = await loop.run_in_executor(
                    executor,
                    self.embedding.embed_documents,
                    texts
                )

                batch_data = []
                for doc_id, text, text_emb in zip(doc_ids, texts, mock_text_emb_ts):
                    batch_data.append({
                        "id": doc_id,
                        "text": text,
                        "text_emb": text_emb
                    })

                if batch_data:
                    await self.client_db.insert(collection_name=collection_name, data=batch_data)
                    print(f"批次 {_batch_idx} 写入完成，成功插入 {len(batch_data)} 条数据")

        tasks = []
        total_batches = (len_unique_docs // batch_size) + 1
        for _batch in range(total_batches):
            tasks.append(asyncio.create_task(process_batch(_batch)))

        if tasks:
            await asyncio.gather(*tasks)

        executor.shutdown(wait=True)
        print("所有数据向量化及插入任务极限提速完成。")

    async def get_all_files(self, path):
        """

        """
        for base_path, folders, names in os.walk(path):
            if names:
                for name in names:
                    abs_file = os.path.join(base_path, name)
                    yield abs_file

    async def hybrid_search_milvus(self, query_text: str, top_k: int = 10):
        """
        执行 Milvus 混合检索 (Dense + Sparse)

        :param query_text: 用户查询文本
        :param top_k: 返回的相似文档数量
        """
        print(query_text)
        query_dense_vector = self.embedding.embed_query(query_text)
        print("query_dense_vector", query_dense_vector)

        # 2. 构造【语义路】查询请求
        dense_search_req = AnnSearchRequest(
            data=[query_dense_vector],  # 查询向量
            anns_field="text_emb",  # 对应 Schema 里的稠密向量字段
            param={"metric_type": "COSINE"},  # 搜索参数
            limit=top_k
        )
        print("dense_search_req", dense_search_req)

        # 3. 构造【全文路】查询请求 (Sparse/BM25)
        # ⚠️ 关键点：因为你配置了 BM25 Function，这里 data 直接传原始字符串！
        sparse_search_req = AnnSearchRequest(
            data=[query_text],  # 直接传查询字符串
            anns_field="sparse",  # 对应 Schema 里的稀疏向量字段
            param={"metric_type": "BM25"},
            limit=top_k
        )
        print("sparse_search_req", sparse_search_req)

        try:
            # 2. 第一阶段：使用 Milvus 内部 RRF 进行多路融合与初步过滤（粗排）
            res = await self.client_db.hybrid_search(
                collection_name=collection_name,
                reqs=[dense_search_req, sparse_search_req],
                ranker=RRFRanker(),
                limit=top_k,
                output_fields=["id", "text"]
            )

            # 提取候选文档文本，并建立与原始 ID 的哈希映射字典
            docs_for_rerank = []
            text_to_id_map = {}

            for hits in res:
                for hit in hits:
                    doc_text = hit.entity.get('text').replace('\n', '')
                    doc_id = hit.entity.get("id")
                    # ⚠️ 确保在提取时去重
                    if doc_text not in text_to_id_map:
                        docs_for_rerank.append(doc_text)
                        text_to_id_map[doc_text] = doc_id

            if not docs_for_rerank:
                print("[-] 粗排未召回任何结果")
                return []

            print(f"[>>>] Milvus 粗排召回 {len(docs_for_rerank)} 个候选文档，开始通过 Cross-Encoder 进行精排计算...")

            # 3. 第二阶段：将候选文档交由自己的 Reranker 模型进行语义交叉验证（精排）
            # ⚠️ 这里直接传入 top_k 参数限制其最终返回数量
            reranked_scores = await self.reranker.infinity_search(
                docs_for_rerank,
                query_text,
                3
            )

            print("\n[<<<] 二次精排完成，最终结果:")
            final_results = []

            # 解析重排结果，通过之前缓存的 map 将得分、文本和 ID 重新缝合
            for rank_item in reranked_scores:
                # ⚠️ 根据上下文，reranked_scores 返回的是 [(text, score), ...]
                r_text = rank_item[0]
                r_score = rank_item[1]
                r_id = text_to_id_map.get(r_text, "unknown_id")

                print(f"最终得分: {r_score:.4f} | ID: {r_id} | 内容: {r_text[:60]}...")

                final_results.append({
                    "id": r_id,
                    "text": r_text,
                    "score": r_score
                })

            return final_results

        except Exception as e:
            print(f"[-] 混合检索或模型重排执行失败: {e}")
            traceback.print_exc()
            return []

    def get_file_hash(self, file):
        """

        :param file:
        :return:
        """
        with open(file, "r", encoding="utf-8") as f:
            file_data = f.read()
        file_hash = hashlib.md5(file_data.encode()).hexdigest()
        return file_hash, file_data

    async def contextualSearchPreAgent(self):
        """

        :return:
        """
        pages_cache = {}

        system = ('你是一个高级架构师并且是个文档阅读分析高手，能够 阅读文档，并iqe总结文档内容，而且还能根据传入的文本片段，自动为片段加上合适的上下文，'
                  '并且将结果以json形式输出，输出格式如下：'
                  '{"question":"","knowledge":"","response":""}'
                  '字段解释：'
                  'question:用户问题'
                  'knowledge:知识库检索结果,如果没有可以是空字符串'
                  'response:ai结论'
                  '所有回复,思考过程 必须用中文'
                  )
        contextual_message = Messages(
            system,
            self.llm_config.get("memory_size")
        )
        contextual_message_cp = copy.deepcopy(contextual_message)

        file = r"/home/jhc/Projects/Python/ai/rag/milvue_stand/test/mds/release_notes.md"
        file_hash, file_data = self.get_file_hash(file)
        if not pages_cache:
            contextual_message.add_user_msg(f"这是文档全文，基于此分析总结文档 {file_data}")
            llm_response = await self.client_llm.chat(contextual_message.get_msg())
            llm_response_obj = await self.client_llm.parse_chat_response(llm_response)
            print("llm_response_obj", llm_response_obj.response)
            pages_cache[file_hash] = llm_response_obj.response

        split_res = self.load_docs.split_documents_by_mhts(1000, 100)
        contextual_message_cp.add_user_msg(f"{pages_cache[file_hash]} 这是文档的总体分析，请基于此为文档片段加上上下文 ")
        cp_pre_contextual_message_cp = copy.deepcopy(contextual_message_cp)
        for sp in split_res:
            # print(sp.__dict__)
            cp_pre_contextual_message_cp.add_user_msg(f"{sp.page_content} 这是文档片段，请添加上下文")
            chat_resp = await self.client_llm.chat(cp_pre_contextual_message_cp.get_msg())
            chat_obj = await self.client_llm.parse_chat_response(chat_resp)
            print(sp.page_content.replace("\n",""))
            print(chat_obj.response.replace("\n",""))
            print("*" * 50)
            # print(sp)

        # contextual_message.add_user_msg()

    async def process(self, *args, **kwargs):
        """
        异步主处理逻辑入口
        """
        try:
            # 首次运行时取消注释进行全量构建
            # await self.insert_init_db()

            # await self.insert_milvus_md()

            # query = "Milvus schema 相关的所有参数及详细解释"
            #
            # self.messages.add_user_msg(query)
            # # 执行混合搜索模式
            # result = await self.hybrid_search_milvus(query)
            # for res in result:
            #     self.messages.add_user_msg(f"向量数据库检索结果：{res['text']} 相关性分数:{res['score']}")
            #
            # print(self.messages.get_msg())
            # llm_res = await self.client_llm.chat(self.messages.get_msg())
            # print("llm_res", llm_res)
            # plan_parse_obj = await self.client_llm.parse_chat_response(llm_res)
            # print("plan_parse_obj", plan_parse_obj)
            #
            # array_match = re.search(r'\{[\s\S]*\}', plan_parse_obj.response)
            # if array_match:
            #     sub_questions = json.loads(array_match.group(0))
            # else:
            #     raise ValueError("未能提取出合法的 JSON 数组")
            #
            # print("sub_questions", sub_questions)

            # query = "http1.0和http2.0异同"
            #
            # # 执行 Plan-and-Solve 搜索模式
            # result = await self.plan_and_execute_search(query)
            # self.logger.info("Final Result:", result)

            # await self.build_test()
            await self.contextualSearchPreAgent()
        finally:
            # 无论成功失败，确保资源释放
            await self.close()


if __name__ == '__main__':
    collection_name = "milvus_desc"
    mt = MilvusTest(collection_name)
    # 启动异步事件循环控制中心
    try:
        asyncio.run(mt.process())
    except KeyboardInterrupt:
        pass
