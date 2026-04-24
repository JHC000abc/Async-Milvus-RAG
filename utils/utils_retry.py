# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: utils_retry.py
@time: 2026/4/21 21:16 
@desc: 

"""
import functools
import traceback
import asyncio
import time


def retry(**params):
    """
    同步重试装饰器
    """
    limit = params.get("limit", 3)

    def decorate(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            c_limit = limit  # 使用 nonlocal 修改闭包内的变量
            while c_limit > 0:
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    c_limit -= 1
                    print(f"发生错误:{func.__name__} 剩余重试次数:{c_limit}\n{traceback.format_exc()}")
                    if c_limit <= 0:
                        raise e  # 耗尽次数后抛出异常
                finally:
                    time.sleep(3)

        return inner

    return decorate


def async_retry(**params):
    """
    异步重试装饰器
    """
    limit = params.get("limit", 3)

    def decorate(func):
        @functools.wraps(func)
        async def inner(*args, **kwargs):
            c_limit = limit
            while c_limit > 0:
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    c_limit -= 1
                    print(f"发生错误:{func.__name__} 剩余重试次数:{c_limit}\n{traceback.format_exc()}")
                    if c_limit <= 0:
                        raise e
                finally:
                    await asyncio.sleep(3)

        return inner

    return decorate
