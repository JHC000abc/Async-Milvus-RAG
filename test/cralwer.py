# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: cralwer.py
@time: 2026/4/18 22:06 
@desc: 

"""
import hashlib
from curl_cffi import requests
from lxml import etree
import asyncio
import nest_asyncio

nest_asyncio.apply()

from pipeline import RAGPipeline


class Crawler(RAGPipeline):
    """

    """

    def __init__(self, urls):
        super(Crawler, self).__init__()
        self.urls = urls

    async def parse_html(self, html):
        """

        :param html:
        :return:
        """
        with open("1.html", "w", encoding="utf-8") as f:
            f.write(html)
        tree = etree.HTML(html)
        lis = tree.xpath('//table[@cellpadding="4"]/tr[1]/td[@colspan="2"]')
        for li in lis:
            question = li.xpath('./div//span/a/span/text()|./div//span/span/text()')
            print(question)
            # print(question[0].replace("\n ",""))
            if question:
                if len(question) >= 2:
                    question = question[1]
                else:
                    question = question[0]
                yield question.replace("\n ", "").replace("?", "").strip()

    async def calculate_hash(self, text):
        """

        :param text:
        :return:
        """
        return hashlib.md5(text.encode()).hexdigest()

    async def process(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        await self.client_mysql.init_pool()
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "dnt": "1",
            "pragma": "no-cache",
            "priority": "u=0, i",
            "referer": "https://www.chaojimake.cn/user_login_web.html",
            "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }
        cookies = {
            "PHPSESSID": "33qfadmqqr5n352n1djvr0ccd4"
        }
        args = []
        hash_set = set()
        for url in self.urls:
            print(url)
            response = requests.get(url, headers=headers, cookies=cookies)
            async for question in self.parse_html(response.content.decode()):
                question_hash = await self.calculate_hash(question)
                if question_hash not in hash_set:
                    print(question, question_hash)
                    args.append((question, question_hash))
                    hash_set.add(question_hash)

            print(len(args))
            sql = """ insert into rag_qa (question, question_hash)
                      values (%s, %s)"""
            await self.client_mysql.execute_insert_many(sql, args)
            args = []


if __name__ == '__main__':
    base_lis = [
        # 'https://www.chaojimake.cn/question_16_154.html/p{i}',
                'https://www.chaojimake.cn/question_16_868.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_782.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_574.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_153.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_856.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_857.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_451.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_155.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_858.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_598.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_859.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_157.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_202.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_651.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_650.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_657.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_482.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_701.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_702.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_159.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_370.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_652.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_653.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_654.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_655.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_656.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_459.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_703.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_404.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_860.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_861.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_862.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_863.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_864.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_865.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_866.html/p{i}',
                # 'https://www.chaojimake.cn/question_16_867.html/p{i}'
                ]

    urls = []
    for base in base_lis:
        for i in range(1, 9):
            _url = base.format(i=i)
            urls.append(_url)
    crawler = Crawler(urls)
    asyncio.run(crawler.process())
