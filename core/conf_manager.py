# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: conf_manager.py
@time: 2026/4/4 12:28 
@desc: 

"""
import yaml

class LoadConfig:
    """
    配置加载管理器
    """
    def load_yaml_config(self, file_path: str) -> dict:
        """加载 YAML 配置文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                # 使用 safe_load 避免任意代码执行的安全风险
                config = yaml.safe_load(f)
                return config
        except Exception as e:
            print(f"加载 YAML 失败: {e}")
            return {}