# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: pipeline.py
@time: 2026/4/4 12:30 
@desc: 

"""
import os

os.environ["TRANSFORMERS_NO_ADAPTER_WARNING"] = "1"
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ['GRPC_VERBOSITY'] = 'NONE'
os.environ['GLOG_minloglevel'] = '3'
os.environ['PYTHON_GRPC_FORK_SUPPORT_ENABLED'] = '0'

import asyncio
from pathlib import Path
from abc import ABC, abstractmethod
from core import LoadConfig
from components import MilvusDB, LocalMdSpliter, LLM, Embeddings, Messages, Rerankers, CLIPEmbeddings, AsyncMysqlClient
from core import sys_logger
from typing import Union
from pymilvus import AsyncMilvusClient
from langchain_ollama import OllamaEmbeddings
from concurrent.futures import ThreadPoolExecutor

import nest_asyncio

# 允许 asyncio 内部嵌套事件才循环
nest_asyncio.apply()


class RAGPipeline(ABC):
    """
    RAG 核心调度管道
    """

    def __init__(self):
        # 初始化线程池用于处理同步阻塞的文本切片任务
        self.executor = ThreadPoolExecutor(max_workers=4)
        config_path = Path(__file__).parent / "conf" / "config.yaml"
        self.config = LoadConfig().load_yaml_config(str(config_path))
        self.logger = sys_logger
        # 拆解插件化配置 (保留这些属性以供子类直接调用，例如 main.py 中的 normal_config)
        self.milvus_config = self.config.get('Milvus', {})
        self.normal_config = self.config.get('Normal', {})
        self.llm_config = self.config.get('LLM', {})
        self.reranker_config = self.config.get('Reranker', {})
        self.reranker_config_bge = self.reranker_config.get("BGE", {})
        self.embedding_config = self.config.get('Embedding', {})
        self.embedding_clip_config = self.config.get('CLIP', {})
        self.mysql_config = self.config.get('Mysql', {})

        # 精准修改：去除冗余的 _assemble_components 内部方法，直接在初始化阶段完成组装，减少代码层级
        self.client_db: Union[MilvusDB, AsyncMilvusClient] = MilvusDB(**self.milvus_config)
        self.load_docs = LocalMdSpliter(self.normal_config.get("docs_path"))
        self.client_llm = LLM(**self.llm_config)
        self.embedding: Union[Embeddings, OllamaEmbeddings] = Embeddings(**self.embedding_config)
        self.embedding_clip = CLIPEmbeddings(**self.embedding_clip_config)

        self.reranker = Rerankers(**self.reranker_config_bge)
        self.client_mysql = AsyncMysqlClient(**self.mysql_config)

        self.messages = Messages(
            self.llm_config.get("system"),
            self.llm_config.get("memory_size")
        )

    async def close(self):
        """
        严谨释放所有占用的资源
        """
        self.logger.info("正在释放系统资源...")
        # 关闭线程池
        self.executor.shutdown(wait=True)
        tasks = []
        if hasattr(self.client_db, "close"):
            tasks.append(self.client_db.close())
        if hasattr(self.client_llm, "close"):
            tasks.append(self.client_llm.close())
        if hasattr(self.embedding, "close"):
            tasks.append(self.embedding.close())
        if hasattr(self.embedding_clip, "close"):
            tasks.append(self.embedding_clip.close())
        if hasattr(self.client_mysql, "close"):
            tasks.append(self.client_mysql.close())

        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
            self.logger.info("底层客户端连接已安全关闭")

    @abstractmethod
    async def process(self, *args, **kwargs):
        """流程执行入口"""
        pass
