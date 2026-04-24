# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: vectory_store.py
@time: 2026/4/4 12:30 
@desc: 

"""

from pymilvus import AsyncMilvusClient


class MilvusDB:
    """
    向量数据库插件组件
    """

    def __init__(self, uri, type="milvus", **kwargs):
        self.type = type
        self.uri = uri
        # 将实例声明为受保护的属性
        self._client = self._init_db_plugin()

    def _init_db_plugin(self):
        """根据配置加载对应的向量数据库插件"""
        if self.type == "milvus":
            return AsyncMilvusClient(uri=self.uri)
        else:
            raise ValueError(f"不支持的 VectorDB 插件类型: {self.type}")

    async def close(self):
        """

        :return:
        """
        if self._client:
            await self._client.close()

    def __getattr__(self, item):
        """
        魔法方法代理转发：
        当调用 self.client_db.search() 等原生方法时，自动转发给底层的 MilvusClient 实例
        """
        return getattr(self._client, item)
