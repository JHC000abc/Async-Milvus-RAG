# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: test_crawl_pages.py
@time: 2026/4/12 13:41
@desc:

"""
import json
import os
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

md_list = []

with open("./md.json", "r", encoding="utf-8") as f:
    data = f.read()
    md_list = json.loads(data)

os.makedirs("mds", exist_ok=True)


def get_html(md):
    """

    """
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        "cache-control": "no-cache",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "purpose": "prefetch",
        "referer": f"https://milvus.io/docs/zh/{md}",
        "sec-ch-ua": "\"Google Chrome\";v=\"147\", \"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"147\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Linux\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
        "x-nextjs-data": "1"
    }
    url = f"https://milvus.io/_next/data/4gjcCGBjB35vsvuMKg5fP/docs/zh/{md}.json"
    params = {
        "id": f"{md}"
    }
    response = requests.get(url, headers=headers, params=params)
    return parse_result(response.json()), md


def parse_result(html):
    """

    """

    new_html = html["pageProps"]["homeData"]["tree"]

    data = f"""<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <title>Title</title>
                </head>
                <body>
                {new_html}
                </body>
                </html>
                    """

    tree = etree.HTML(data)

    # 接口返回的 "tree" 是正文的所有元素，没有诸如 div 的包裹层，
    # 因此我们通过 '//body//text()' 捕获由 etree 自动包入的 body 标签下所有文本。
    lis = tree.xpath('//body//text()')

    # 清洗文本，去除无意义的空行和首尾空格

    _lis = []
    for i in lis:
        line = i.strip()
        if line == "下一步计划":
            break
        if line:
            _lis.append(line)
    print(_lis)
    return "\n".join(_lis)


with ThreadPoolExecutor(max_workers=20) as tp:
    for html, md in tp.map(get_html, [md for md in md_list if md != "__N_SSG"]):
        with open(f"./mds/{md}", "w", encoding="utf-8") as f:
            f.write(html)
#
# for md in md_list:
#     if md in ("__N_SSG"):
#         continue
#
#     html = get_html(md)
#     with open(f"./mds/{md}", "w", encoding="utf-8") as f:
#         f.write(html)
