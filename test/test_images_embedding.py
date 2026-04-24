# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: test_images_embedding.py
@time: 2026/4/16 21:54 
@desc: 

"""
import os
import asyncio
from pipeline import RAGPipeline
from pymilvus import DataType


class ImageEmbedding(RAGPipeline):
    """

    """

    def __init__(self):
        super(ImageEmbedding, self).__init__()

    async def init_collections(self, name):
        """

        :param name:
        :return:
        """
        schema = self.client_db.create_schema()
        schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True)
        schema.add_field("file", DataType.VARCHAR, max_length=1000)
        schema.add_field("meta", DataType.JSON)
        schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=self.embedding_clip.dimension)

        index_params = self.client_db.prepare_index_params()
        index_params.add_index(
            field_name="embedding",
            metric_type="COSINE",
            index_type="HNSW",
            params={"M": 32, "efConstruction": 512}
        )
        # index_params.add_index("embedding", metric_type="COSINE", index_type="IVF_FLAT", params={"nlist": 128})

        if await self.client_db.has_collection(name):
            await self.client_db.drop_collection(name)
        await self.client_db.create_collection(name, schema=schema, index_params=index_params, num_shards=2,
                                               consistency_level="Bounded")

    async def insert_data(self, images_folder, collection_name):
        """

        :param images_folder:
        :param collection_name:
        :return:
        """
        data = []
        for img_name in os.listdir(images_folder):
            abs_img_file = os.path.join(images_folder, img_name)
            eb = await self.embedding_clip.get_embedding(abs_img_file)
            data.append(
                {
                    "file": abs_img_file,
                    "embedding": eb
                }
            )
        await self.client_db.insert(collection_name, data)

    async def search_images(self, img_file, collection_name, top_k=5):
        """

        :param img_file:
        :param collection_name:
        :param top_k:
        :return:
        """
        emb = await self.embedding_clip.get_embedding(img_file)

        search_results = await self.client_db.search(
            collection_name,
            data=[emb],
            anns_field="embedding",
            metric_type="COSINE",
            params={"nprobe": 10},
            limit=top_k,
            output_fields=["file"]
        )
        if search_results:
            print(search_results)
            for search_result in search_results:
                # print(search_result)
                # for id, res in enumerate(sorted(search_result, key=lambda x: x['distance'], reverse=True), 1):
                for id, res in enumerate(search_result, 1):
                    distance = f'{res["distance"] * 100:.2f}'
                    entity = res["entity"]
                    print(id, f"{distance} %", entity['file'])

    async def search_mixed(self, text, img_file, collection_name, top_k=5, text_weight=0.5):
        """
        文本和图像混合检索接口（多模态联合检索）
        将文本向量和图像向量按权重融合后进行检索
        :param text: 查询的补充文本描述
        :param img_file: 查询的基准图像路径
        :param collection_name: 集合名称
        :param top_k: 返回数量
        :param text_weight: 文本向量所占权重(0~1)，图像权重则为 1 - text_weight
        :return:
        """
        # ⚠️此处同样假设您的 embedding_clip 具有 get_text_embedding 方法获取文本向量
        text_emb = await self.embedding_clip.get_text_embedding(text)
        img_emb = await self.embedding_clip.get_embedding(img_file)

        # 向量加权融合计算
        img_weight = 1.0 - text_weight
        mixed_emb = [
            (t * text_weight) + (i * img_weight)
            for t, i in zip(text_emb, img_emb)
        ]

        search_results = await self.client_db.search(
            collection_name,
            data=[mixed_emb],
            anns_field="embedding",
            metric_type="COSINE",
            params={"nprobe": 10},
            limit=top_k,
            output_fields=["file"]
        )
        if search_results:
            print(f"\n图文混合 (文本:'{text}', 图像:'{os.path.basename(img_file)}') 的检索结果:")
            for search_result in search_results:
                for id, res in enumerate(search_result, 1):
                    distance = f'{res["distance"] * 100:.2f}'
                    entity = res["entity"]
                    print(id, f"{distance} %", entity['file'])

    async def process(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        images_folder = r"/home/jhc/Projects/Python/ai/rag/milvue_stand/test/images"
        collection_name = "images"
        await self.init_collections(collection_name)
        await self.insert_data(images_folder, collection_name)
        stand_image_file = r"/home/jhc/Projects/Python/ai/rag/milvue_stand/test/images/3aa7d3d1-06e3-46f3-b44e-bd3960a872a6.jpeg"
        # await self.search_images(stand_image_file, collection_name)
        await self.search_mixed("black girl", stand_image_file, collection_name, text_weight=0.9)


if __name__ == '__main__':
    asyncio.run(ImageEmbedding().process())
