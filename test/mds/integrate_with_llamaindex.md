使用 Milvus 和 LlamaIndex 的检索增强生成（RAG）
本指南演示了如何使用 LlamaIndex 和 Milvus 构建检索-增强生成（RAG）系统。
RAG 系统结合了检索系统和生成模型，可根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
LlamaIndex
是一个简单、灵活的数据框架，用于将自定义数据源连接到大型语言模型（LLMs）。
Milvus
是世界上最先进的开源向量数据库，专为支持嵌入式相似性搜索和人工智能应用而构建。
在本笔记本中，我们将快速演示如何使用 MilvusVectorStore。
开始之前
安装依赖项
本页面上的代码片段需要 pymilvus 和 llamaindex 依赖项。您可以使用以下命令安装它们：
$ pip install pymilvus>=
2.4
.2
milvus-lite
$ pip install llama-index-vector-stores-milvus
$ pip install llama-index
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
。(点击屏幕上方的 "Runtime（运行时）"菜单，从下拉菜单中选择 "Restart session（重新启动会话）"）。
设置 OpenAI
首先让我们添加 openai api 密钥。这将允许我们访问 chatgpt。
import
openai

openai.api_key =
"sk-***********"
准备数据
您可以使用以下命令下载样本数据：
! mkdir -p
'data/'
! wget
'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt'
-O
'data/paul_graham_essay.txt'
! wget
'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/10k/uber_2021.pdf'
-O
'data/uber_2021.pdf'
开始
生成数据
作为第一个例子，让我们从文件
paul_graham_essay.txt
中生成一个文档。这是保罗-格雷厄姆（Paul Graham）的一篇题为
What I Worked On
的文章。我们将使用 SimpleDirectoryReader 生成文档。
from
llama_index.core
import
SimpleDirectoryReader
# load documents
documents = SimpleDirectoryReader(
    input_files=[
"./data/paul_graham_essay.txt"
]
).load_data()
print
(
"Document ID:"
, documents[
0
].doc_id)
Document ID: 95f25e4d-f270-4650-87ce-006d69d82033
创建数据索引
现在我们有了文档，可以创建索引并插入文档。对于索引，我们将使用 MilvusVectorStore。MilvusVectorStore 需要几个参数：
基本参数
uri (str, optional)
:要连接的 URI，对于 Milvus 或 Zilliz Cloud 服务，其形式为 "https://address:port"；对于本地的精简版 Milvus，其形式为 "path/to/local/milvus.db"。默认为"./milvus_llamaindex.db"。
token (str, optional)
:登录令牌。不使用 rbac 时为空，使用 rbac 时很可能是 "username:password"。
collection_name (str, optional)
:用于存储数据的 Collection 的名称。默认为 "llamalection"。
overwrite (bool, optional)
:是否覆盖同名的现有 Collection。默认为 "假"。
标量字段，包括 doc id 和文本
doc_id_field (str, optional)
:Collections 的 doc_id 字段名称。默认为 DEFAULT_DOC_ID_KEY。
text_key (str, optional)
:在传递的 Collections 中存储什么键文本。在使用自己的 Collections 时使用。默认为 DEFAULT_TEXT_KEY。
scalar_field_names (list, optional)
:要包含在 Collections Schema 中的额外标量字段的名称。
scalar_field_types (list, optional)
:额外标量字段的类型。
密集字段
enable_dense (bool)
:布尔标志，用于启用或禁用密集嵌入。默认为 True。
dim (int, optional)
:Collections 的嵌入向量维度。创建新 Collections 时必须使用，且 enable_sparse 为 False。
embedding_field (str, optional)
:Collections 的密集嵌入字段名称，默认为 DEFAULT_EMBEDDING_KEY。
index_config (dict, optional)
:用于构建密集嵌入索引的配置。默认为 "无"。
search_config (dict, optional)
:用于搜索 Milvus 密集索引的配置。注意必须与
index_config
指定的索引类型兼容。默认为无。
similarity_metric (str, optional)
:用于高密度 Embeddings 的相似度量，目前支持 IP、COSINE 和 L2。
稀疏字段
enable_sparse (bool)
:布尔标志，用于启用或禁用稀疏嵌入。默认为假。
sparse_embedding_field (str)
:稀疏嵌入字段的名称，默认为 DEFAULT_SPARSE_EMBEDDING_KEY。
sparse_embedding_function (Union[BaseSparseEmbeddingFunction, BaseMilvusBuiltInFunction], optional)
:如果 enable_sparse 为 True，则应提供此对象将文本转换为稀疏嵌入。如果为 None，将使用默认的稀疏嵌入函数（BGEM3SparseEmbeddingFunction）。
sparse_index_config (dict, optional)
:用于构建稀疏嵌入索引的配置。默认为 "无"。
混合排序器
hybrid_ranker (str)
:指定混合搜索查询中使用的排名器类型。目前仅支持["RRFRanker", "WeightedRanker"]。默认为 "RRFRanker"。
hybrid_ranker_params (dict, optional)
:混合排名器的配置参数。该字典的结构取决于所使用的特定排名器：
对于 "RRFRanker"，它应包括
"k"（int）：互易排序融合（RRF）中使用的参数。该值用于计算 RRF 算法中的排名分数，该算法将多种排名策略合并为一个分数，以提高搜索相关性。
对于 "WeightedRanker"（加权排名器），它的期望值是
"权重"（浮点数列表）：一个包含两个权重的列表：
密集嵌入组件的权重。
稀疏嵌入成分的权重。 这些权重用于调整混合检索过程中嵌入的密集和稀疏成分的重要性。 默认为空字典，这意味着排名器将以其预定义的默认设置进行操作。
其他
collection_properties (dict, optional)
:Collections 属性，如 TTL（生存时间）和 MMAP（内存映射）。默认为 "无"。可以包括
"collection.ttl.seconds"（int）：设置此属性后，当前 Collections 中的数据将在指定时间内过期。Collection 中过期的数据将被清理，不会参与搜索或查询。
"mmap.enabled"（bool）：是否在 Collections 级别启用内存映射存储。
index_management (IndexManagement)
:指定要使用的索引管理策略。默认为 "create_if_not_exists"。
batch_size (int)
:配置向 Milvus 插入数据时一个批次中处理的文档数量。默认为 DEFAULT_BATCH_SIZE。
consistency_level (str, optional)
:对新创建的 Collections 使用哪种一致性级别。默认为 "Session"。
# Create an index over the documents
from
llama_index.core
import
VectorStoreIndex, StorageContext
from
llama_index.vector_stores.milvus
import
MilvusVectorStore


vector_store = MilvusVectorStore(uri=
"./milvus_demo.db"
, dim=
1536
, overwrite=
True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
对于
MilvusVectorStore
的参数：
将
uri
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
uri
。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
查询数据
现在我们已经将文档存储在索引中，可以针对索引提出问题。索引会将自身存储的数据作为 chatgpt 的知识库。
query_engine = index.as_query_engine()
res = query_engine.query(
"What did the author learn?"
)
print
(res)
The author learned that philosophy courses in college were boring to him, leading him to switch his focus to studying AI.
res = query_engine.query(
"What challenges did the disease pose for the author?"
)
print
(res)
The disease posed challenges for the author as it affected his mother's health, leading to a stroke caused by colon cancer. This resulted in her losing her balance and needing to be placed in a nursing home. The author and his sister were determined to help their mother get out of the nursing home and back to her house.
下一个测试显示覆盖会删除之前的数据。
from
llama_index.core
import
Document


vector_store = MilvusVectorStore(uri=
"./milvus_demo.db"
, dim=
1536
, overwrite=
True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    [Document(text=
"The number that is being searched for is ten."
)],
    storage_context,
)
query_engine = index.as_query_engine()
res = query_engine.query(
"Who is the author?"
)
print
(res)
The author is the individual who created the context information.
下一个测试显示的是向已有索引添加额外数据。
del
index, vector_store, storage_context, query_engine

vector_store = MilvusVectorStore(uri=
"./milvus_demo.db"
, overwrite=
False
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
query_engine = index.as_query_engine()
res = query_engine.query(
"What is the number?"
)
print
(res)
The number is ten.
res = query_engine.query(
"Who is the author?"
)
print
(res)
Paul Graham
元数据过滤
我们可以通过过滤特定来源生成结果。下面的示例说明了从目录中加载所有文档，然后根据元数据对其进行过滤。
from
llama_index.core.vector_stores
import
ExactMatchFilter, MetadataFilters
# Load all the two documents loaded before
documents_all = SimpleDirectoryReader(
"./data/"
).load_data()

vector_store = MilvusVectorStore(uri=
"./milvus_demo.db"
, dim=
1536
, overwrite=
True
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents_all, storage_context)
我们只想检索文件
uber_2021.pdf
中的文档。
filters = MetadataFilters(
    filters=[ExactMatchFilter(key=
"file_name"
, value=
"uber_2021.pdf"
)]
)
query_engine = index.as_query_engine(filters=filters)
res = query_engine.query(
"What challenges did the disease pose for the author?"
)
print
(res)
The disease posed challenges related to the adverse impact on the business and operations, including reduced demand for Mobility offerings globally, affecting travel behavior and demand. Additionally, the pandemic led to driver supply constraints, impacted by concerns regarding COVID-19, with uncertainties about when supply levels would return to normal. The rise of the Omicron variant further affected travel, resulting in advisories and restrictions that could adversely impact both driver supply and consumer demand for Mobility offerings.
当从文件
paul_graham_essay.txt
中检索时，我们会得到不同的结果。
filters = MetadataFilters(
    filters=[ExactMatchFilter(key=
"file_name"
, value=
"paul_graham_essay.txt"
)]
)
query_engine = index.as_query_engine(filters=filters)
res = query_engine.query(
"What challenges did the disease pose for the author?"
)
print
(res)
The disease posed challenges for the author as it affected his mother's health, leading to a stroke caused by colon cancer. This resulted in his mother losing her balance and needing to be placed in a nursing home. The author and his sister were determined to help their mother get out of the nursing home and back to her house.