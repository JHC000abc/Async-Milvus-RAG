使用 Milvus 和 HayStack 的检索增强生成（RAG）
本指南演示了如何使用 HayStack 和 Milvus 建立一个检索-增强生成（RAG）系统。
RAG 系统将检索系统与生成模型相结合，根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
HayStack
是 deepset 公司推出的开源 Python 框架，用于使用大型语言模型（LLMs）构建定制应用程序。
Milvus
是世界上最先进的开源向量数据库，用于支持嵌入式相似性搜索和人工智能应用。
前提条件
在运行本笔记本之前，请确保您已安装以下依赖项：
! pip install --upgrade --quiet pymilvus milvus-lite milvus-haystack markdown-it-py mdit_plain
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重新启动会话"）。
我们将使用 OpenAI 的模型。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备数据
我们使用关于
达芬奇
的在线内容作为 RAG 管道的私人知识库，这对于简单的 RAG 管道来说是一个很好的数据源。
下载并保存为本地文本文件。
import
os
import
urllib.request

url =
"https://www.gutenberg.org/cache/epub/7785/pg7785.txt"
file_path =
"./davinci.txt"
if
not
os.path.exists(file_path):
    urllib.request.urlretrieve(url, file_path)
创建索引管道
创建一个索引管道，将文本转换成文档，分割成句子并嵌入其中。然后将文档写入 Milvus 文档存储。
from
haystack
import
Pipeline
from
haystack.components.converters
import
MarkdownToDocument
from
haystack.components.embedders
import
OpenAIDocumentEmbedder, OpenAITextEmbedder
from
haystack.components.preprocessors
import
DocumentSplitter
from
haystack.components.writers
import
DocumentWriter
from
haystack.utils
import
Secret
from
milvus_haystack
import
MilvusDocumentStore
from
milvus_haystack.milvus_embedding_retriever
import
MilvusEmbeddingRetriever


document_store = MilvusDocumentStore(
    connection_args={
"uri"
:
"./milvus.db"
},
# connection_args={"uri": "http://localhost:19530"},
# connection_args={"uri": YOUR_ZILLIZ_CLOUD_URI, "token": Secret.from_env_var("ZILLIZ_CLOUD_API_KEY")},
drop_old=
False
,
)
连接参数
将
uri
设置为本地文件，例如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储到这个文件中。
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
indexing_pipeline = Pipeline()
indexing_pipeline.add_component(
"converter"
, MarkdownToDocument())
indexing_pipeline.add_component(
"splitter"
, DocumentSplitter(split_by=
"sentence"
, split_length=
2
)
)
indexing_pipeline.add_component(
"embedder"
, OpenAIDocumentEmbedder())
indexing_pipeline.add_component(
"writer"
, DocumentWriter(document_store))
indexing_pipeline.connect(
"converter"
,
"splitter"
)
indexing_pipeline.connect(
"splitter"
,
"embedder"
)
indexing_pipeline.connect(
"embedder"
,
"writer"
)
indexing_pipeline.run({
"converter"
: {
"sources"
: [file_path]}})
print
(
"Number of documents:"
, document_store.count_documents())
Converting markdown files to Documents: 100%|█| 1/
Calculating embeddings: 100%|█| 9/9 [00:05<00:00, 
E20240516 10:40:32.945937 5309095 milvus_local.cpp:189] [SERVER][GetCollection][] Collecton HaystackCollection not existed
E20240516 10:40:32.946677 5309095 milvus_local.cpp:189] [SERVER][GetCollection][] Collecton HaystackCollection not existed
E20240516 10:40:32.946704 5309095 milvus_local.cpp:189] [SERVER][GetCollection][] Collecton HaystackCollection not existed
E20240516 10:40:32.946725 5309095 milvus_local.cpp:189] [SERVER][GetCollection][] Collecton HaystackCollection not existed


Number of documents: 277
创建检索管道
创建一个检索管道，使用向量相似性搜索引擎从 Milvus 文档存储中检索文档。
question =
'Where is the painting "Warrior" currently stored?'
retrieval_pipeline = Pipeline()
retrieval_pipeline.add_component(
"embedder"
, OpenAITextEmbedder())
retrieval_pipeline.add_component(
"retriever"
, MilvusEmbeddingRetriever(document_store=document_store, top_k=
3
)
)
retrieval_pipeline.connect(
"embedder"
,
"retriever"
)

retrieval_results = retrieval_pipeline.run({
"embedder"
: {
"text"
: question}})
for
doc
in
retrieval_results[
"retriever"
][
"documents"
]:
print
(doc.content)
print
(
"-"
*
10
)
). The
composition of this oil-painting seems to have been built up on the
second cartoon, which he had made some eight years earlier, and which
was apparently taken to France in 1516 and ultimately lost.
----------

This "Baptism of Christ," which is now in the Accademia in Florence
and is in a bad state of preservation, appears to have been a
comparatively early work by Verrocchio, and to have been painted
in 1480-1482, when Leonardo would be about thirty years of age.

To about this period belongs the superb drawing of the "Warrior," now
in the Malcolm Collection in the British Museum.
----------
" Although he
completed the cartoon, the only part of the composition which he
eventually executed in colour was an incident in the foreground
which dealt with the "Battle of the Standard." One of the many
supposed copies of a study of this mural painting now hangs on the
south-east staircase in the Victoria and Albert Museum.
----------
创建 RAG 管道
创建 RAG 管道，结合 MilvusEmbeddingRetriever 和 OpenAIGenerator，使用检索到的文档回答问题。
from
haystack.utils
import
Secret
from
haystack.components.builders
import
PromptBuilder
from
haystack.components.generators
import
OpenAIGenerator

prompt_template =
"""Answer the following query based on the provided context. If the context does
                     not include an answer, reply with 'I don't know'.\n
                     Query: {{query}}
                     Documents:
                     {% for doc in documents %}
                        {{ doc.content }}
                     {% endfor %}
                     Answer:
                  """
rag_pipeline = Pipeline()
rag_pipeline.add_component(
"text_embedder"
, OpenAITextEmbedder())
rag_pipeline.add_component(
"retriever"
, MilvusEmbeddingRetriever(document_store=document_store, top_k=
3
)
)
rag_pipeline.add_component(
"prompt_builder"
, PromptBuilder(template=prompt_template))
rag_pipeline.add_component(
"generator"
,
    OpenAIGenerator(
        api_key=Secret.from_token(os.getenv(
"OPENAI_API_KEY"
)),
        generation_kwargs={
"temperature"
:
0
},
    ),
)
rag_pipeline.connect(
"text_embedder.embedding"
,
"retriever.query_embedding"
)
rag_pipeline.connect(
"retriever.documents"
,
"prompt_builder.documents"
)
rag_pipeline.connect(
"prompt_builder"
,
"generator"
)

results = rag_pipeline.run(
    {
"text_embedder"
: {
"text"
: question},
"prompt_builder"
: {
"query"
: question},
    }
)
print
(
"RAG answer:"
, results[
"generator"
][
"replies"
][
0
])
RAG answer: The painting "Warrior" is currently stored in the Malcolm Collection in the British Museum.
有关如何使用 milvus-hayStack 的更多信息，请参阅
milvus-haystack Readme
。