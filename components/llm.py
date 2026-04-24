# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: llm.py
@time: 2026/4/4 12:30 
@desc: 

"""
from openai import AsyncOpenAI
from components import Messages
from schemas import LLMResponseParse
from utils import async_retry

class LLM:
    """
    LLM 插件组件
    """

    def __init__(self, url, api_key, system, ai_model, limit_loop_num, **kwargs):
        self.url = url
        self.system = system
        self.limit_loop_num = limit_loop_num
        self.ai_model = ai_model
        self.api_key = api_key
        self.message = Messages(system, limit_loop_num)
        self._client = self._init_llm_plugin()

    def _init_llm_plugin(self):
        """根据配置的 type 加载对应的 LLM 客户端插件"""
        return AsyncOpenAI(
            base_url=self.url,
            api_key=self.api_key
        )

    @async_retry()
    async def chat(self, messages, **kwargs):
        """

        :param messages:
        :return:
        """
        return await self._client.chat.completions.create(
            model=self.ai_model,
            messages=messages,
            **kwargs
        )

    async def parse_chat_response(self, response) -> LLMResponseParse:
        """

        :param response:
        :return:
        """

        response_txt = ""
        think_txt = ""
        stop = False

        if hasattr(response, "choices"):
            for choice in response.choices:
                # print("choice", choice)
                stop = False if choice.finish_reason is None else True
                if hasattr(choice, "message"):
                    message = choice.message
                    # 仅提取 content，忽略 reasoning 等非必要字段以保证 JSON 纯净
                    content = getattr(message, "content", "") or ""
                    content_think = getattr(message, "reasoning_content", "") or getattr(message, "reasoning", "") or ""
                    response_txt += content
                    think_txt += content_think
                else:
                    raise ValueError(f"ai 返回异常:{choice}")
        else:
            # 2. 处理流式响应
            async for chunk in response:
                if hasattr(chunk, "choices"):
                    for choice in chunk.choices:
                        # print("choice", choice)
                        stop = False if choice.finish_reason is None else True
                        if hasattr(choice, "delta"):
                            delta = choice.delta
                            content = getattr(delta, "content", "") or ""
                            content_think = getattr(delta, "reasoning_content", "") or getattr(delta, "reasoning",
                                                                                               "") or ""
                        elif hasattr(choice, "messages"):
                            messages = choice.messages
                            content = getattr(messages, "content", "") or ""
                            content_think = getattr(messages, "reasoning_content", "") or getattr(messages, "reasoning",
                                                                                                  "") or ""
                        else:
                            raise ValueError(f"ai 返回异常:{choice}")
                        response_txt += content
                        think_txt += content_think

        return LLMResponseParse(response=response_txt, think=think_txt, stop=stop)

    async def close(self):
        """

        :return:
        """
        if self._client:
            await self._client.close()

    def __getattr__(self, item):
        """代理转发底层的 OpenAI Client 方法"""
        return getattr(self._client, item)
