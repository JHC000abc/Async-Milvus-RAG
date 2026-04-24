# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: models.py
@time: 2026/4/4 12:29 
@desc: 

"""
from pydantic import BaseModel, Field


class LLMResponse(BaseModel):
    """
    Response model for the LLM output.
    """
    question: str = Field(..., description="用户提问")
    knowledge: str = Field(..., description="知识库查询结果")
    response: str = Field(..., description="ai 最终返回结果")


class LLMResponseParse(BaseModel):
    """
    Response model for the LLM output.
    """
    response: str = Field(description="文本答案", default="")
    think: str = Field(description="思考", default="")
    stop: bool = Field(description="是否输出结束", default=False)
