# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: documents_loader.py
@time: 2026/4/4 12:29 
@desc: 

"""

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter,MarkdownHeaderTextSplitter


class LocalMdSpliter:
    """
    文档加载与切片组件
    """

    def __init__(self, path):
        self.docs = self._load_documents(path)

    def _load_documents(self, path):
        """

        :param path:
        :return:
        """
        loader = DirectoryLoader(
            path=path,
            glob="*.md",
            loader_cls=TextLoader,
            show_progress=True
        )
        return loader.load()

    def split_documents_by_rcts(self, chunk_size, chunk_overlap):
        """

        :param chunk_size:
        :param chunk_overlap:
        :return:
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(self.docs)

    def split_documents_by_mhts(self, chunk_size, chunk_overlap):
        """

        :param chunk_size:
        :param chunk_overlap:
        :return:
        """
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

        md_docs = []
        for doc in self.docs:
            splits = markdown_splitter.split_text(doc.page_content)
            for split in splits:
                header_context = " > ".join([v for k, v in split.metadata.items() if k.startswith("Header")])
                if header_context:
                    split.page_content = f"【文档脉络: {header_context}】\n{split.page_content}"

                # 保留原文件的 metadata，确保后续入库能溯源 path
                split.metadata.update(doc.metadata)
            md_docs.extend(splits)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return text_splitter.split_documents(md_docs)
