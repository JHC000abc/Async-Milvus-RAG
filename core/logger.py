# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: logger.py
@time: 2026/4/5 11:32 
@desc: 

"""
import sys
from loguru import logger


def setup_logger():
    """
    配置日志器格式与输出
    """
    # 移除默认配置
    logger.remove()

    # 添加控制台输出：包含时间、等级、文件名、行号及消息
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        enqueue=True  # 异步安全
    )

    # 如果需要，可以添加文件输出
    logger.add("logs/rag_system.log", rotation="10 MB", retention="7 days", level="DEBUG")

    return logger


# 全局单例
sys_logger = setup_logger()