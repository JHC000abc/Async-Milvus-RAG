安装 Milvus Python SDK
本主题介绍如何为 Milvus 安装 Milvus python SDK pymilvus。
当前版本的 Milvus 支持 Python、Node.js、GO 和 Java SDK。
要求
需要 Python 3.7 或更高版本。
已安装 Google protobuf。可以使用
pip3 install protobuf==3.20.0
命令安装。
已安装 grpcio-tools。可以使用
pip3 install grpcio-tools
命令安装。
通过 pip 安装 PyMilvus
PyMilvus 可在
Python 包索引
中找到。
建议安装与所安装 Milvus 服务器版本相匹配的 PyMilvus 版本。更多信息，请参阅
发行说明
。
$
python3 -m pip install pymilvus==
2.6
.
10
验证安装
如果 PyMilvus 安装正确，运行以下命令时不会出现异常。
$
python3 -c
"from pymilvus import Collection"
下一步
安装 PyMilvus 后，您可以
学习 Milvus 的基本操作：
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
探索
PyMilvus API 参考