# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: embeddings.py
@time: 2026/4/4 12:29
@desc:

"""
import traceback
from langchain_ollama import OllamaEmbeddings
import httpx
import os
import asyncio


class Embeddings:
    """
    Embedding 插件组件
    """

    def __init__(self, model, base_url, type="ollama", **kwargs):
        self.type = type
        self.model = model
        self.base_url = base_url
        self._embedding_model = self._init_embedding_plugin()

    def _init_embedding_plugin(self):
        """根据配置的 type 加载对应的 Embedding 插件"""
        if self.type == "ollama":
            return OllamaEmbeddings(
                model=self.model,
                base_url=self.base_url
            )
        else:
            raise ValueError(f"不支持的 Embedding 插件类型: {self.type}")

    async def close(self):
        """

        :return:
        """
        if hasattr(self._embedding_model, "close"):
            await self._embedding_model.close()
        elif hasattr(self._embedding_model, "client") and hasattr(self._embedding_model.client, "close"):
            await self._embedding_model.client.close()

    def __getattr__(self, item):
        """代理转发：使得外部可以直接调用 embed_query 等底层方法"""
        return getattr(self._embedding_model, item)


class CLIPEmbeddings:
    """

    """

    def __init__(self, url, dimension=768, **kwargs):
        self.dimension = dimension
        self.base_url = url
        self.client = httpx.AsyncClient()

    def _get_api_url(self, endpoint: str) -> str:
        """
        辅助方法：自动兼容传入的 base_url，提取根域名并拼接目标接口
        （防止之前传入的是具体的 /api/v1/embedding/image 路径）
        """
        # ⚠️ 将完整的 URL 按照后端 API 的共同前缀截断，获取根域名地址
        root_url = self.base_url.split("/api/v")[0]
        return f"{root_url}{endpoint}"

    async def get_embedding(self, image_path: str) -> list:
        """
        获取图像向量 (用于图搜图或图文混合检索)
        :param image_path:
        :return:
        """
        api_url = self._get_api_url("/api/v1/embedding/image")
        try:
            with open(image_path, "rb") as f:
                file_bytes = f.read()
                files = {"file": (os.path.basename(image_path), file_bytes, f"image/{image_path.split('.')[-1]}")}
                response = await self.client.post(api_url, files=files)
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "success":
                        return data["embedding"]
                    else:
                        raise ValueError(f"接口返回状态异常: {data}")
                else:
                    raise RuntimeError(f"HTTP 请求失败, 状态码: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"提取 {image_path} 向量失败: {traceback.format_exc()} ")
            return None

    async def get_text_embedding(self, text: str) -> list:
        """
        获取文本向量 (用于纯文本搜图或图文混合检索)
        :param text: 查询文本
        :return:
        """
        api_url = self._get_api_url("/api/v1/embedding/text")
        try:
            # ⚠️ 依据 FastAPI 后端的 TextEmbeddingRequest 模型要求，通过 JSON Body 发送
            payload = {
                "text": text,
                "target_dim": self.dimension
            }
            response = await self.client.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return data["embedding"]
                else:
                    raise ValueError(f"接口返回状态异常: {data}")
            else:
                raise RuntimeError(f"HTTP 请求失败, 状态码: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"提取文本 '{text}' 向量失败: {traceback.format_exc()} ")
            return None

    async def match_image_text(self, image_path: str, texts: str) -> list:
        """
        零样本图文分类概率匹配
        :param image_path: 图像本地路径
        :param texts: 候选文本列表 (逗号分隔，如 "a dog, a cat")
        :return: 返回包含匹配概率字典的列表
        """
        api_url = self._get_api_url("/api/v1/match/image_text")
        try:
            with open(image_path, "rb") as f:
                file_bytes = f.read()
                files = {"file": (os.path.basename(image_path), file_bytes, f"image/{image_path.split('.')[-1]}")}
                # ⚠️ 依据 FastAPI 后端要求，文本字段通过 Form 表单数据传输
                data = {"texts": texts}
                response = await self.client.post(api_url, files=files, data=data)
                if response.status_code == 200:
                    res_data = response.json()
                    if res_data.get("status") == "success":
                        return res_data["results"]
                    else:
                        raise ValueError(f"接口返回状态异常: {res_data}")
                else:
                    raise RuntimeError(f"HTTP 请求失败, 状态码: {response.status_code}, {response.text}")
        except Exception as e:
            print(f"图文匹配请求失败: {traceback.format_exc()} ")
            return None

    async def close(self):
        """

        :return:
        """
        if hasattr(self, "client") and not self.client.is_closed:
            await self.client.aclose()