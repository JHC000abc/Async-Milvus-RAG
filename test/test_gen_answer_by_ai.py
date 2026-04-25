# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: test_gen_answer_by_ai.py
@time: 2026/4/20 22:25 
@desc: 

"""
import asyncio
import copy
import json
from pymilvus import DataType, Function, FunctionType, AnnSearchRequest, RRFRanker

from pipeline import RAGPipeline


class GenAnswer(RAGPipeline):
    """

    """

    def __init__(self):
        super(GenAnswer, self).__init__()

    async def build_mysql(self):
        """

        :return:
        """
        await self.client_mysql.init_pool()
        sql = """select *
                 from rag_qa \
                 where id >= 117;"""
        results = await self.client_mysql.execute_select(sql)
        system = """你是一个Python资深开发工程师，特别擅长分析处理异步问题，能够用最简单的语言解答问题，能够让人很直接的看懂 并且回复格式参照如下格式
                    {"question":"","response":""}
                    字段解释：
                        question:用户问题
                        response:ai生成的最终结论
                    所有回复必须用中文"""
        self.messages.clear_msg()
        self.messages.add_system_msg(system)
        cp_msg = copy.deepcopy(self.messages)
        for result in results:
            print(result)
            id = result["id"]
            question = result["question"]
            print("--->", self.messages.get_msg())
            self.messages.add_user_msg(question)
            llm_response = await self.client_llm.chat(self.messages.get_msg())
            llm_obj = await self.client_llm.parse_chat_response(llm_response)
            # print(llm_obj.response)
            answer = json.loads(llm_obj.response)['response']
            print("answer", answer)
            self.messages = cp_msg
            sql_update = """update rag_qa
                            set answer=%s
                            where id = %s """
            await self.client_mysql.execute_update(sql_update, (answer, id))

            await asyncio.sleep(10)

    async def create_qa(self, collection_name):
        """

        :param collection_name:
        :return:
        """
        schema = self.client_db.create_schema()
        schema.add_field("id", DataType.INT64, auto_id=True, is_primary=True)
        chinese_analyzer = {
            "type": "chinese"
        }
        schema.add_field("question", DataType.VARCHAR, max_length=1000, enable_analyzer=True,
                         analyzer_params=chinese_analyzer, enable_match=True)
        schema.add_field("answer", DataType.VARCHAR, max_length=5000, enable_analyzer=True,
                         analyzer_params=chinese_analyzer, enable_match=True)
        schema.add_field("question_dense", DataType.FLOAT_VECTOR, dim=self.embedding_clip.dimension)
        schema.add_field("answer_dense", DataType.FLOAT_VECTOR, dim=self.embedding_clip.dimension)
        schema.add_field("question_sparse", DataType.SPARSE_FLOAT_VECTOR, is_function_output=True)
        schema.add_field("answer_sparse", DataType.SPARSE_FLOAT_VECTOR, is_function_output=True)

        bm25_function_question = Function(
            name="question_to_vector",
            function_type=FunctionType.BM25,
            input_field_names=["question"],
            output_field_names=["question_sparse"]
        )
        schema.add_function(bm25_function_question)

        bm25_function_answer = Function(
            name="answer_to_vector",
            function_type=FunctionType.BM25,
            input_field_names=["answer"],
            output_field_names=["answer_sparse"]
        )
        schema.add_function(bm25_function_answer)

        index_params = self.client_db.prepare_index_params()
        index_params.add_index(field_name="question", index_name="question_txt_idx", index_type="INVERTED")
        index_params.add_index(field_name="answer", index_name="answer_txt_idx", index_type="INVERTED")
        index_params.add_index(field_name="question_dense", index_name="question_idx", index_type="AUTOINDEX",
                               metric_type="IP")
        index_params.add_index(field_name="answer_dense", index_name="answer_idx", index_type="AUTOINDEX",
                               metric_type="IP")
        index_params.add_index(field_name="question_sparse", index_name="question_sparse_idx",
                               index_type="SPARSE_INVERTED_INDEX",
                               metric_type="BM25")
        index_params.add_index(field_name="answer_sparse", index_name="answer_sparse_idx",
                               index_type="SPARSE_INVERTED_INDEX",
                               metric_type="BM25")

        if await self.client_db.has_collection(collection_name):
            await self.client_db.drop_collection(collection_name)
        await self.client_db.create_collection(collection_name, schema=schema, index_params=index_params)

    async def insert_data(self, collection_name):
        """

        :param collection_name:
        :return:
        """
        await self.client_mysql.init_pool()
        res = await self.client_mysql.execute_select("select * from rag_qa;")
        _res = []
        for i in res:
            _res.append({
                "question": i['question'],
                "answer": i['answer'],
                "question_dense": await self.embedding_clip.get_text_embedding(i['question']),
                "answer_dense": await self.embedding_clip.get_text_embedding(i['answer'])
            })

        await self.client_db.insert(collection_name, _res)

    async def search(self, collection_name, query, limit=10):
        """

        :param collection_name:
        :param query:
        :param limit:
        :return:
        """
        query_dense_vector = await self.embedding_clip.get_text_embedding(query)

        req_dense = AnnSearchRequest(
            data=[query_dense_vector],
            anns_field="question_dense",
            param={"metric_type": "IP", "params": {"nprobe": 10}},
            limit=limit
        )

        req_sparse = AnnSearchRequest(
            data=[query],
            anns_field="question_sparse",
            param={"metric_type": "BM25", "params": {}},
            limit=limit
        )
        res = await self.client_db.hybrid_search(
            collection_name=collection_name,
            reqs=[req_dense, req_sparse],
            ranker=RRFRanker(),
            limit=limit,
            output_fields=["question", "answer"]
        )

        search_results = {}
        docs_for_rerank = []
        for hit in res[0]:
            print(hit)
            docs_for_rerank.append(hit.entity.get("question"))
            search_results.update({f"{hit.entity.get('question')}": {
                "id": hit.id,
                "score": hit.distance,
                "question": hit.entity.get("question"),
                "answer": hit.entity.get("answer")
            }})
        print(len(docs_for_rerank), docs_for_rerank)
        # 精排
        reranked_scores = await self.reranker.infinity_search(
            docs_for_rerank,
            query,
            3,
            score_threshold=None
        )
        print(reranked_scores)

    async def process(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        collection_name = "qa"
        # await self.create_qa(collection_name)
        # await self.insert_data(collection_name)

        # 等待数据加载
        await asyncio.sleep(3)

        query = "核心概念"
        q_res = await self.client_db.query(collection_name, filter=f"TEXT_MATCH(question, '{query}')",
                                           output_fields=["question"])
        print(q_res)

        s_res=  await self.search(collection_name, query=query)
        print(s_res)


if __name__ == '__main__':
    asyncio.run(GenAnswer().process())
