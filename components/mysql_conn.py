# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: mysql_conn.py
@time: 2026/4/19 20:57 
@desc: 

"""
import aiomysql
from typing import List, Dict, Any, Optional, Union, Tuple


class AsyncMysqlClient:
    """
    异步 MySQL 客户端，封装了连接池、查询、插入、更新及关闭接口。
    """

    def __init__(
            self,
            host: str = '127.0.0.1',
            port: int = 3306,
            user: str = 'root',
            password: str = '',
            db: str = 'test_db',
            minsize: int = 1,
            maxsize: int = 10,
            charset: str = 'utf8mb4'
    ):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.minsize = minsize
        self.maxsize = maxsize
        self.charset = charset
        self.pool: Optional[aiomysql.Pool] = None

    async def init_pool(self) -> None:
        """
        初始化异步数据库连接池。
        """
        if self.pool is None:
            self.pool = await aiomysql.create_pool(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                db=self.db,
                minsize=self.minsize,
                maxsize=self.maxsize,
                charset=self.charset,
                autocommit=False,  # 默认关闭自动提交，在操作接口中手动控制
                cursorclass=aiomysql.DictCursor  # 查询结果以字典形式返回
            )
            print("MySQL 连接池初始化成功。")

    async def close(self) -> None:
        """
        优雅地关闭连接池，释放所有资源。
        """
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None
            print("MySQL 连接池已关闭。")

    async def execute_insert(self, sql: str, args: Union[Tuple, List] = ()) -> int:
        """
        执行插入操作 (DML)。

        :param sql: 要执行的 SQL 语句
        :param args: SQL 语句中的参数
        :return: 影响的行数
        """
        if self.pool is None:
            raise RuntimeError("连接池未初始化，请先调用 init_pool()。")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(sql, args)
                    affected_rows = cursor.rowcount
                    await conn.commit()
                    return affected_rows
                except Exception as e:
                    await conn.rollback()
                    print(f"执行插入操作时发生错误，已回滚: {e}")
                    raise e

    async def execute_insert_many(self, sql: str, args: List[Union[Tuple, List]]) -> int:
        """
        执行批量插入操作 (DML)。

        :param sql: 要执行的 SQL 语句，例如 "INSERT INTO table (col1) VALUES (%s)"
        :param args: 参数列表，例如 [("val1",), ("val2",), ("val3",)]
        :return: 影响的行数
        """
        if self.pool is None:
            raise RuntimeError("连接池未初始化，请先调用 init_pool()。")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    # 使用 executemany 进行批量插入，底层会进行优化
                    await cursor.executemany(sql, args)
                    affected_rows = cursor.rowcount
                    await conn.commit()
                    return affected_rows
                except Exception as e:
                    await conn.rollback()
                    print(f"执行批量插入操作时发生错误，已回滚: {e}")
                    raise e

    async def execute_update(self, sql: str, args: Union[Tuple, List] = ()) -> int:
        """
        执行更新操作 (DML)。

        :param sql: 要执行的 SQL 语句，例如 "UPDATE table SET col1=%s WHERE id=%s"
        :param args: SQL 语句中的参数
        :return: 影响的行数
        """
        if self.pool is None:
            raise RuntimeError("连接池未初始化，请先调用 init_pool()。")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(sql, args)
                    affected_rows = cursor.rowcount
                    await conn.commit()
                    return affected_rows
                except Exception as e:
                    await conn.rollback()
                    print(f"执行更新操作时发生错误，已回滚: {e}")
                    raise e

    async def execute_update_many(self, sql: str, args: List[Union[Tuple, List]]) -> int:
        """
        执行批量更新操作 (DML)。

        :param sql: 要执行的 SQL 语句，例如 "UPDATE table SET status=%s WHERE id=%s"
        :param args: 参数列表，例如 [("active", 1), ("disabled", 2)]
        :return: 影响的行数
        """
        if self.pool is None:
            raise RuntimeError("连接池未初始化，请先调用 init_pool()。")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    # executemany 同样适用于批量更新
                    await cursor.executemany(sql, args)
                    affected_rows = cursor.rowcount
                    await conn.commit()
                    return affected_rows
                except Exception as e:
                    await conn.rollback()
                    print(f"执行批量更新操作时发生错误，已回滚: {e}")
                    raise e

    async def execute_select(self, sql: str, args: Union[Tuple, List] = ()) -> List[Dict[str, Any]]:
        """
        执行查询操作 (DQL)。

        :param sql: 要执行的 SQL 语句
        :param args: SQL 语句中的参数
        :return: 包含查询结果字典的列表
        """
        if self.pool is None:
            raise RuntimeError("连接池未初始化，请先调用 init_pool()。")

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                try:
                    await cursor.execute(sql, args)
                    result = await cursor.fetchall()
                    return result
                except Exception as e:
                    print(f"执行查询操作时发生错误: {e}")
                    raise e