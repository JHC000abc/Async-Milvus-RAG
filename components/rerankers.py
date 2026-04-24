import asyncio
import httpx
from typing import List, Tuple, Optional


class Rerankers:
    """
    Infinity 重排服务异步客户端封装
    """

    def __init__(self, host: str, port: int = 7997, model: str = "BAAI/bge-reranker-v2-m3"):
        self.host = host
        self.port = port
        self.model = model
        self.base_url = f"http://{self.host}:{self.port}/rerank"
        # 延迟初始化 client，建议在异步环境中使用单个 client 复用连接
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """
        获取或初始化异步 HTTP 客户端
        """
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=60.0)
        return self._client

    async def gen_payload(self, documents: List[str], query_text: str, top_n=None):
        """

        :param documents:
        :param query_text:
        :param top_n:
        :return:
        """
        return {
            "model": self.model,
            "query": query_text,
            "documents": documents,
            "top_n": min(top_n, len(documents)) if top_n else len(documents),
            "return_documents": False
        }

    async def infinity_search(self, documents: List[str], query_text: str, limit: int = 10,
                              score_threshold: float = 0.5) -> List[
        Tuple[str, float]]:
        """

        :param documents:
        :param query_text:
        :param limit:
        :param score_threshold:
        :return:
        """
        if not documents:
            return []

        payload = await self.gen_payload(documents, query_text, limit)
        client = await self._get_client()

        try:
            response = await client.post(self.base_url, json=payload)
            response.raise_for_status()
            rerank_response = response.json()

            results = rerank_response.get("results", [])

            # 构造排序后的结果列表
            # Infinity 返回的 results 已经是按分数降序排列的
            sorted_results = []
            for item in results:
                original_index = item["index"]
                score = item["relevance_score"]
                if score_threshold is not None and score < score_threshold:
                    continue
                original_doc = documents[original_index]
                sorted_results.append((original_doc, score))

            return sorted_results

        except Exception as e:
            print(f"❌ Rerank 异步过程发生错误: {e}")
            # 出错时返回原始顺序及零分，确保业务流不中断
            return [(doc, 0.0) for doc in documents]

    async def close(self):
        """
        关闭异步客户端连接
        """
        if self._client and not self._client.is_closed:
            await self._client.aclose()


# --- 测试逻辑 ---
async def main():
    query_text = "What event in 1956 marked the official birth of artificial intelligence as a discipline?"

    documents = [
        "In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence.",
        "The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals.",
        "In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy.",
        "The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems."
    ]

    # 初始化客户端 (指向您的 Docker GPU 容器)
    client_reranker = Rerankers(host="172.17.0.1", port=7997)

    try:
        # 异步调用重排方法
        print(f"正在异步请求重排服务: {client_reranker.base_url}...")
        sorted_data = await client_reranker.infinity_search(documents, query_text, 2)

        # 输出结果
        print("\n--- 异步推理结果（已按分数排序）---")
        for doc, score in sorted_data:
            print(f"分数: {score:.4f} | 文档: {doc}")

    finally:
        # 确保关闭连接池
        await client_reranker.close()


if __name__ == "__main__":
    # 使用 asyncio 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
