# Async-Milvus-RAG
基于 Python 异步框架 构建的增强型 RAG（检索增强生成）系统。它深度集成了 Milvus 向量数据库（支持混合检索）、Ollama 嵌入模型、BGE Reranker 精排以及 DeepSeek 等大模型，并针对文档处理实现了高效的异步并发优化。
# MilvueStand: 异步高性能增强型 RAG 系统

MilvueStand 是一个基于 Python 异步架构设计的检索增强生成（RAG）管道。本项目旨在解决传统 RAG 系统在处理大规模文档入库时的效率瓶颈，并利用混合检索（Hybrid Search）与重排序（Reranking）技术显著提升问答的精准度。

## 🌟 核心特性

- **极致异步优化**：全链路采用 `asyncio` 驱动，包括异步 Milvus 客户端、异步 LLM 调用及异步数据库操作。
- **混合检索方案**：支持 Milvus 2.4+ 的多路召回技术，结合了基于文本语义的稠密向量检索（Dense Vector）和基于 BM25 的稀疏向量检索（Sparse Vector）。
- **智能任务拆解 (Plan-and-Solve)**：内置子问题并行拆解逻辑，通过并发检索多个专项子问题，构建更全面的上下文背景。
- **极致入库性能**：通过线程池（ThreadPoolExecutor）分流计算密集型的文档切片，配合信号量控制并发，实现海量 Markdown 文档的极限提速入库与去重。
- **精排验证 (Reranking)**：集成了 BGE 或 Jina 等精排模型，对初筛结果进行二次语义交叉验证，确保提供给 LLM 的知识片段高度相关。
- **灵活的模型适配**：支持 Ollama 本地 Embedding 以及 CLIP 多模态嵌入，兼容 OpenAI 格式的各种 LLM API（如 DeepSeek）。

## 🏗️ 系统架构


## 🛠️ 技术栈

- **Vector Database**: Milvus (Async Client)
- **LLM Engine**: DeepSeek / OpenAI API
- **Embedding**: Ollama (Gemma) / CLIP
- **Reranker**: BAAI/BGE-Reranker-V2-M3
- **Framework**: Python 3.9+ / Asyncio / Pydantic

## 🚀 快速开始

### 1. 环境准备
确保您的开发环境已安装 Docker，并启动了以下服务：
- **Milvus**: 监听 `19530` 端口
- **Ollama**: 监听 `11434` 端口，并下载了 `embeddinggemma` 模型
- **BGE Reranker Service**: 监听 `7997` 端口



