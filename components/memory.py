# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: memory.py
@time: 2026/4/4 12:30 
@desc: 

"""


class Messages:
    """
    ai 消息类组件
    """

    def __init__(self, system, limit=20):
        self.system = system
        self.limit = limit
        self._messages = []
        self.add_system_msg(system)

    def add_user_msg(self, msg):
        """

        :param msg:
        :return:
        """
        self._clear_old_messages()
        self._messages.append({
            "role": "user",
            "content": msg
        })

    def add_assistant_msg(self, msg):
        """

        :param msg:
        :return:
        """
        self._clear_old_messages()
        self._messages.append({
            "role": "assistant",
            "content": msg
        })

    def add_system_msg(self, msg):
        """

        :param msg:
        :return:
        """
        self._clear_old_messages()
        self._messages.append({
            "role": "system",
            "content": msg
        })

    def _clear_old_messages(self):
        """

        :return:
        """
        while self.get_msg_len() > self.limit:
            message_deleted = False
            for i in range(len(self._messages)):
                if self._messages[i]["role"] != "system":
                    self._messages.pop(i)
                    message_deleted = True
                    break
            if not message_deleted:
                break

    def get_msg_len(self):
        """

        :return:
        """
        return len(self.get_msg())

    def get_msg(self):
        """

        :return:
        """
        return self._messages

    def clear_msg(self):
        """

        :return:
        """
        self._messages = []

    def set_messages(self, messages):
        """

        :param messages:
        :return:
        """
        self._messages = messages
