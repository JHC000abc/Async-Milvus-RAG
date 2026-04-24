使用 VectorETL 将数据高效加载到 Milvus 中
在本教程中，我们将探讨如何使用专为向量数据库设计的轻量级 ETL 框架
VectorETL
将数据高效地加载到 Milvus 中。VectorETL 简化了从各种来源提取数据的过程，利用人工智能模型将数据转化为向量 Embeddings，并将其存储到 Milvus 中，以便进行快速、可扩展的检索。在本教程结束时，你将拥有一个可正常工作的 ETL 管道，让你轻松集成和管理向量搜索系统。让我们开始吧！
准备工作
依赖性和环境
$
pip install --upgrade vector-etl pymilvus
如果你使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
VectorETL 支持多种数据源，包括亚马逊 S3、谷歌云存储、本地文件等。你可以
在这里
查看支持数据源的完整列表。在本教程中，我们将以亚马逊 S3 作为数据源示例。
我们将从亚马逊 S3 加载文档。因此，你需要准备
AWS_ACCESS_KEY_ID
和
AWS_SECRET_ACCESS_KEY
作为环境变量，以便安全访问 S3 存储桶。此外，我们将使用 OpenAI 的
text-embedding-ada-002
embedding 模型为数据生成 embeddings。您还应将
api 密钥
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"your-openai-api-key"
os.environ[
"AWS_ACCESS_KEY_ID"
] =
"your-aws-access-key-id"
os.environ[
"AWS_SECRET_ACCESS_KEY"
] =
"your-aws-secret-access-key"
工作流程
定义数据源（亚马逊 S3）
在本例中，我们从亚马逊 S3 存储桶中提取文档。VectorETL 允许我们指定数据桶名称、文件路径和数据类型。
source = {
"source_data_type"
:
"Amazon S3"
,
"bucket_name"
:
"my-bucket"
,
"key"
:
"path/to/files/"
,
"file_type"
:
".csv"
,
"aws_access_key_id"
: os.environ[
"AWS_ACCESS_KEY_ID"
],
"aws_secret_access_key"
: os.environ[
"AWS_SECRET_ACCESS_KEY"
],
}
配置嵌入模型（OpenAI）
设置好数据源后，我们需要定义嵌入模型，将文本数据转换为向量嵌入。在本例中，我们使用 OpenAI 的
text-embedding-ada-002
。
embedding = {
"embedding_model"
:
"OpenAI"
,
"api_key"
: os.environ[
"OPENAI_API_KEY"
],
"model_name"
:
"text-embedding-ada-002"
,
}
将 Milvus 设置为目标数据库
我们需要将生成的嵌入模型存储在 Milvus 中。在此，我们使用 Milvus Lite 定义 Milvus 连接参数。
target = {
"target_database"
:
"Milvus"
,
"host"
:
"./milvus.db"
,
# os.environ["ZILLIZ_CLOUD_PUBLIC_ENDPOINT"] if using Zilliz Cloud
"api_key"
:
""
,
# os.environ["ZILLIZ_CLOUD_TOKEN"] if using Zilliz Cloud
"collection_name"
:
"my_collection"
,
"vector_dim"
:
1536
,
# 1536 for text-embedding-ada-002
}
对于
host
和
api_key
：
将
host
设置为本地文件，如
./milvus.db
，并将
api_key
留空，这是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果数据规模较大，可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器 uri（如
http://localhost:19530
）作为
host
，并将
api_key
留空。
如果您想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
host
和
api_key
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
指定 Embeddings 的列
现在，我们需要指定 CSV 文件中的哪些列应转换为 Embeddings。这样可以确保只处理相关的文本字段，优化效率和存储。
embed_columns = [
"col_1"
,
"col_2"
,
"col_3"
]
创建并执行 VectorETL 管道
所有配置就绪后，我们现在要初始化 ETL 管道、设置数据流并执行它。
from
vector_etl
import
create_flow

flow = create_flow()
flow.set_source(source)
flow.set_embedding(embedding)
flow.set_target(target)
flow.set_embed_columns(embed_columns)
# Execute the flow
flow.execute()
通过本教程的学习，我们已经成功地建立了一个端到端的 ETL 管道，使用 VectorETL 将文档从亚马逊 S3 转移到 Milvus。VectorETL 的数据源非常灵活，你可以根据自己的具体应用需求选择任何数据源。借助 VectorETL 的模块化设计，你可以轻松扩展这个管道，支持其他数据源，嵌入模型，使其成为人工智能和数据工程工作流的强大工具！