使用 Milvus 和 Cognee 构建 RAG
Cognee
是一个以开发人员为先的平台，可通过可扩展的模块化 ECL（提取、认知、加载）管道简化人工智能应用程序开发。通过与 Milvus 无缝集成，Cognee 可实现对话、文档和转录的高效连接和检索，减少幻觉并优化操作符。
凭借对 Milvus、图数据库和 LLMs 等向量存储的强大支持，Cognee 为构建检索增强生成（RAG）系统提供了一个灵活且可定制的框架。其生产就绪的架构可确保提高人工智能应用的准确性和效率。
在本教程中，我们将向您展示如何使用 Milvus 和 Cognee 构建 RAG（检索增强生成）管道。
$
pip install pymilvus git+https://github.com/topoteretes/cognee.git
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
默认情况下，本例中使用 OpenAI 作为 LLM。您应准备好
api 密钥
，并在配置
set_llm_api_key()
函数中进行设置。
要将 Milvus 配置为向量数据库，请将
VECTOR_DB_PROVIDER
设置为
milvus
，并指定
VECTOR_DB_URL
和
VECTOR_DB_KEY
。由于我们在本演示中使用 Milvus Lite 存储数据，因此只需提供
VECTOR_DB_URL
。
import
os
import
cognee

cognee.config.set_llm_api_key(
"YOUR_OPENAI_API_KEY"
)


os.environ[
"VECTOR_DB_PROVIDER"
] =
"milvus"
os.environ[
"VECTOR_DB_URL"
] =
"./milvus.db"
至于环境变量
VECTOR_DB_URL
和
VECTOR_DB_KEY
：
将
VECTOR_DB_URL
设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果数据规模较大，可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器 uri，例如
http://localhost:19530
，作为您的
VECTOR_DB_URL
。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
VECTOR_DB_URL
和
VECTOR_DB_KEY
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
准备数据
我们使用
Milvus 文档 2.4.x
中的常见问题页面作为 RAG 中的私有知识，这对于简单的 RAG 管道来说是一个很好的数据源。
下载 zip 文件并将文档解压缩到
milvus_docs
文件夹中。
$
wget https://github.com/milvus-io/milvus-docs/releases/download/v2.4.6-preview/milvus_docs_2.4.x_en.zip
$
unzip -q milvus_docs_2.4.x_en.zip -d milvus_docs
我们从
milvus_docs/en/faq
文件夹中加载所有标记文件。对于每个文档，我们只需简单地使用 "#"来分隔文件中的内容，这样就能大致分隔出 markdown 文件中每个主要部分的内容。
from
glob
import
glob

text_lines = []
for
file_path
in
glob(
"milvus_docs/en/faq/*.md"
, recursive=
True
):
with
open
(file_path,
"r"
)
as
file:
        file_text = file.read()

    text_lines += file_text.split(
"# "
)
构建 RAG
重置 Cognee 数据
await
cognee.prune.prune_data()
await
cognee.prune.prune_system(metadata=
True
)
现在，我们可以添加数据集并将其处理成知识图谱。
添加数据和认知
await
cognee.add(data=text_lines, dataset_name=
"milvus_faq"
)
await
cognee.cognify()
# [DocumentChunk(id=UUID('6889e7ef-3670-555c-bb16-3eb50d1d30b0'), updated_at=datetime.datetime(2024, 12, 4, 6, 29, 46, 472907, tzinfo=datetime.timezone.utc), text='Does the query perform in memory? What are incremental data and historical data?\n\nYes. When ...
# ...
add
方法将数据集（Milvus 常见问题解答）加载到 Cognee 中，
cognify
方法对数据进行处理，提取实体、关系和摘要，构建知识图谱。
查询摘要
数据处理完成后，我们来查询知识图谱。
from
cognee.api.v1.search
import
SearchType

query_text =
"How is data stored in milvus?"
search_results =
await
cognee.search(SearchType.SUMMARIES, query_text=query_text)
print
(search_results[
0
])
{'id': 'de5c6713-e079-5d0b-b11d-e9bacd1e0d73', 'text': 'Milvus stores two data types: inserted data and metadata.'}
该查询会在知识图谱中搜索与查询文本相关的摘要，并打印出最相关的候选摘要。
查询摘要块
摘要提供了高层次的见解，但对于更细化的细节，我们可以直接从处理过的数据集中查询特定的数据块。这些数据块来自知识图谱创建过程中添加和分析的原始数据。
from
cognee.api.v1.search
import
SearchType

query_text =
"How is data stored in milvus?"
search_results =
await
cognee.search(SearchType.CHUNKS, query_text=query_text)
让我们将其格式化并显示出来，以提高可读性！
def
format_and_print
(
data
):
print
(
"ID:"
, data[
"id"
])
print
(
"\nText:\n"
)
    paragraphs = data[
"text"
].split(
"\n\n"
)
for
paragraph
in
paragraphs:
print
(paragraph.strip())
print
()


format_and_print(search_results[
0
])
ID: 4be01c4b-9ee5-541c-9b85-297883934ab3

Text:

Where does Milvus store data?

Milvus deals with two types of data, inserted data and metadata.

Inserted data, including vector data, scalar data, and collection-specific schema, are stored in persistent storage as incremental log. Milvus supports multiple object storage backends, including [MinIO](https://min.io/), [AWS S3](https://aws.amazon.com/s3/?nc1=h_ls), [Google Cloud Storage](https://cloud.google.com/storage?hl=en#object-storage-for-companies-of-all-sizes) (GCS), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), [Alibaba Cloud OSS](https://www.alibabacloud.com/product/object-storage-service), and [Tencent Cloud Object Storage](https://www.tencentcloud.com/products/cos) (COS).

Metadata are generated within Milvus. Each Milvus module has its own metadata that are stored in etcd.

###
在前面的步骤中，我们查询了 Milvus FAQ 数据集，以获取摘要和特定的数据块。虽然这提供了详细的见解和细粒度信息，但由于数据集很大，要清晰可视化知识图谱中的依赖关系非常困难。
为了解决这个问题，我们将重新设置 Cognee 环境，并使用更小、更集中的数据集。这将使我们能够更好地展示在认知过程中提取的关系和依赖性。通过简化数据，我们可以清楚地看到 Cognee 如何组织和构建知识图谱中的信息。
重置 Cognee
await
cognee.prune.prune_data()
await
cognee.prune.prune_system(metadata=
True
)
添加重点数据集
在这里，我们添加并处理了一个只有一行文本的较小数据集，以确保知识图谱重点突出、易于解读。
# We only use one line of text as the dataset, which simplifies the output later
text =
"""
    Natural language processing (NLP) is an interdisciplinary
    subfield of computer science and information retrieval.
    """
await
cognee.add(text)
await
cognee.cognify()
查询洞察
通过关注这个较小的数据集，我们现在可以清楚地分析知识图谱中的关系和结构。
query_text =
"Tell me about NLP"
search_results =
await
cognee.search(SearchType.INSIGHTS, query_text=query_text)
for
result_text
in
search_results:
print
(result_text)
# Example output:
# ({'id': UUID('bc338a39-64d6-549a-acec-da60846dd90d'), 'updated_at': datetime.datetime(2024, 11, 21, 12, 23, 1, 211808, tzinfo=datetime.timezone.utc), 'name': 'natural language processing', 'description': 'An interdisciplinary subfield of computer science and information retrieval.'}, {'relationship_name': 'is_a_subfield_of', 'source_node_id': UUID('bc338a39-64d6-549a-acec-da60846dd90d'), 'target_node_id': UUID('6218dbab-eb6a-5759-a864-b3419755ffe0'), 'updated_at': datetime.datetime(2024, 11, 21, 12, 23, 15, 473137, tzinfo=datetime.timezone.utc)}, {'id': UUID('6218dbab-eb6a-5759-a864-b3419755ffe0'), 'updated_at': datetime.datetime(2024, 11, 21, 12, 23, 1, 211808, tzinfo=datetime.timezone.utc), 'name': 'computer science', 'description': 'The study of computation and information processing.'})
# (...)
#
# It represents nodes and relationships in the knowledge graph:
# - The first element is the source node (e.g., 'natural language processing').
# - The second element is the relationship between nodes (e.g., 'is_a_subfield_of').
# - The third element is the target node (e.g., 'computer science').
该输出代表了知识图谱查询的结果，展示了从处理过的数据集中提取的实体（节点）及其关系（边）。每个元组包括源实体、关系类型和目标实体，以及唯一 ID、描述和时间戳等元数据。图突出显示了关键概念及其语义联系，提供了对数据集的结构化理解。
恭喜您，您已经学会了 cognee 与 Milvus 的基本用法。如果想了解更多 cognee 的高级用法，请参阅其官方
页面
。