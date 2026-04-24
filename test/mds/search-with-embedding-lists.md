使用 Embeddings 列表进行检索
本页介绍如何使用 Milvus 中的结构数组建立 ColBERT 文本检索系统和 ColPali 文本检索系统，这样就可以在嵌入列表中存储文档及其向量块。
概述
在构建文本检索系统时，您可能需要将文档分割成块，并将每个块及其嵌入作为一个实体存储在向量数据库中，以确保精确度和准确性，尤其是对于长文档而言，全文嵌入可能会削弱语义特异性或超出模型输入限制。
不过，以块为单位存储数据会导致以块为单位的搜索结果，这意味着检索最初识别的是相关
片段
，而不是连贯的
文档
。为了解决这个问题，你应该执行额外的搜索后处理。
ColBERT（arXiv:
2004.12832
）是一个文本-文本检索系统，它通过 BERT 上的上下文化后期交互提供高效的段落搜索。它能对查询和文档进行独立的标记化编码，并计算它们的相似性。
令牌编码
在ColBERT的数据摄取过程中，每个文档都会被分割成令牌，然后被向量化并存储为一个
Embedding
列表，如
d
→
Ed=
[
ed1
,
ed2
,
..
.
edn
]
∈Rn×dd
\rightarrow E_d = [e_{d1}, e_{d2}, \dots, e_{dn}] ∈ \R^{n×d}
d
→
E
d
=
[e
d1
,
e
d2
,
..
.
,
e
dn
]
∈
R
n
×d。当一个查询到达时，它也会被标记化、向量化，并以嵌入列表的形式存储，如
q→Eq=
[
eq1
,
eq2
,
...
,
eqm
]
∈Rm×dq
\rightarrow E_q = [e_{q1}, e_{q2}, \dots, e_{qm}] ∈ \R^{m×d}
q
→
E
q
=
[e
q1
,
e
q2
,
..
.
,
e
qm
]
∈
R
m
×d。
在上述公式中
dd
d：文档
qq
q：查询
EdE_d
E
d
：表示文档的嵌入列表。
EqE_q
E
q
：表示查询的嵌入列表。
[
ed1
,
ed2
,
...
,
edn
]
∈Rn×d[e_{d1}, e_{d2}, \dots, e_{dn}] ∈ \R^{n×d}
[e
d1
,
e
d2
,
.
.
.
,
e
dn
]
∈
R
n
×d：嵌入列表中代表文档的向量嵌入数在
Rn×d\R^{n×d}
R
n×d
的范围内。
[
eq1
,
eq2
,
.
..
,
eqm
]
∈Rm×d[e_{q1}, e_{q2}, \dots, e_{qm}] ∈ \R^{m×d}
[e
q1
,
e
q2
,
.
.
.
,
e
qm
]
∈
R
m
×d：嵌入列表中代表查询的向量嵌入数在
Rm×d\R^{m×d}
R
m×d
范围内。
后期交互
向量化完成后，将查询嵌入列表与每个文档嵌入列表逐个令牌进行比较，以确定最终的相似度得分。
后期交互
如上图所示，查询包含两个标记，即
machine
和
learning
，而窗口中的文档有四个标记：
neural
,
network
,
python
, 和
tutorial
。这些令牌被向量化后，每个查询令牌的向量嵌入与文档中的向量嵌入进行比较，得到一个相似度分数列表。然后将每个分数列表中的最高分相加，得出最终分数。确定文档最终得分的过程称为最大相似度
(MAX_SIM
)。有关最大相似度的详细信息，请参阅
最大相似度
。
在 Milvus 中实施类似 ColBERT 的文本检索系统时，并不局限于将文档分割成标记。
相反，你可以将文档分割成任何适当大小的片段，嵌入每个片段以创建一个嵌入列表，并将文档连同其嵌入的片段一起存储在一个实体中。
ColPali 扩展
在 ColBERT 的基础上，ColPali（arXiv:
2407.01449
）提出了一种利用视觉语言模型（VLMs）的视觉丰富文档检索新方法。在数据摄取过程中，每个文档页面都会被渲染成高分辨率图像，然后被分割成片段，而不是标记化。例如，448 x 448 像素的文档页面图像可产生 1,024 个补丁，每个补丁的大小为 14 x 14 像素。
这种方法保留了非文本信息，如文档布局、图像和表格结构，这些信息在使用纯文本检索系统时会丢失。
Copali 扩展
ColPali 中使用的 VLM 被称为 PaliGemma（arXiv:
2407.07726
），它由一个图像编码器
（SigLIP-400M
）、一个纯解码器语言模型
（Gemma2-2B
）和一个线性层组成，线性层将图像编码器的输出投射到语言模型的向量空间中，如上图所示。
在数据摄取过程中，以原始图像表示的文档页面会被分割成多个视觉斑块，对每个斑块进行嵌入，生成向量嵌入列表。然后将它们投射到语言模型的向量空间，得到最终的嵌入列表，如
d→Ed=
[
ed1
,
ed2
,
...
edn
]
∈Rn×dd
\rightarrow E_d = [e_{d1}, e_{d2}, \dots, e_{dn}] ∈ \R^{n×d}
d
→
E
d
=
[e
d1
,
e
d2
,
..
.
,
e
dn
]
∈
R
n
×d。当一个查询到达时，它被标记化，每个标记被嵌入以生成一个向量嵌入列表，如
q
→
Eq=
[
eq1
,
eq2
,
...
,
eqm
]
∈Rm×dq
\rightarrow E_q = [e_{q1}, e_{q2}, \dots, e_{qm}] ∈ \R^{m×d}
q
→
E
q
=
[e
q1
,
e
q2
,
..
.
,
e
qm
]
∈
R
m
×d。然后，应用
MAX_SIM
对两个嵌入列表进行比较，得到查询和文档页面之间的最终得分。
ColBERT 文本检索系统
在本节中，我们将使用 Milvus 的结构阵列建立一个 ColBERT 文本检索系统。在此之前，先建立一个兼容 Milvus v2.6.x 实例的 Zilliz 云集群，获取一个 Cohere 访问令牌。
第 1 步：安装依赖项
运行以下命令安装依赖项。
pip install --upgrade huggingface-hub transformers datasets pymilvus cohere
第 2 步：加载 Cohere 数据集
在本例中，我们将使用 Cohere 的维基百科数据集，并检索前 10,000 条记录。有关该数据集的信息，请参见
本页
。
from
datasets
import
load_dataset

lang =
"simple"
docs = load_dataset(
"Cohere/wikipedia-2023-11-embed-multilingual-v3"
, 
    lang, 
    split=
"train[:10000]"
)
如果本地没有该数据集，运行上述脚本将下载该数据集。数据集中的每条记录都是维基百科页面中的一个段落。下表显示了该数据集的结构。
列名
说明
_id
记录 ID
url
当前记录的 URL。
title
源文件的标题。
text
源文件的段落。
emb
源文档中文本的 Embeddings。
步骤 3：按标题分组段落
要搜索文档而不是段落，我们应该按标题对段落进行分组。
df = docs.to_pandas()
groups = df.groupby(
'title'
)

data = []
for
title, group
in
groups:
  data.append({
"title"
: title,
"paragraphs"
: [{
"text"
: row[
'text'
],
'emb'
: row[
'emb'
]
      }
for
_, row
in
group.iterrows()]
  })
在此代码中，我们将分组后的段落存储为文档，并将其包含在
data
列表中。每个文档都有一个
paragraphs
键，这是一个段落列表；每个段落对象都包含一个
text
和
emb
键。
步骤 4：为 Cohere 数据集创建 Collections
数据准备就绪后，我们将创建一个 Collection。在 Collection 中，有一个名为
paragraphs
的字段，它是一个 Structs 数组。
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)
# Create collection schema
schema = client.create_schema()

schema.add_field(
'id'
, DataType.INT64, is_primary=
True
, auto_id=
True
)
schema.add_field(
'title'
, DataType.VARCHAR, max_length=
512
)
# Create struct schema
struct_schema = client.create_struct_field_schema()
struct_schema.add_field(
'text'
, DataType.VARCHAR, max_length=
65535
)
struct_schema.add_field(
'emb'
, DataType.FLOAT_VECTOR, dim=
512
)

schema.add_field(
'paragraphs'
, DataType.ARRAY,
                 element_type=DataType.STRUCT,
                 struct_schema=struct_schema, max_capacity=
200
)
# Create index parameters
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"paragraphs[emb]"
,
    index_type=
"AUTOINDEX"
,
    metric_type=
"MAX_SIM_COSINE"
)
# Create a collection
client.create_collection(
    collection_name=
'wiki_documents'
, 
    schema=schema, 
    index_params=index_params
)
第 5 步：将 Cohere 数据集插入 Collections
现在，我们可以将准备好的数据插入到上面创建的 Collection 中。
client.insert(
    collection_name=
'wiki_documents'
, 
    data=data
)
第 6 步：在 Cohere 数据集中搜索
根据 ColBERT 的设计，查询文本应经过标记化处理，然后嵌入到 EmbeddingList 中。在这一步中，我们将使用与 Cohere 为维基百科数据集中的段落生成 Embeddings 所使用的相同模型。
import
cohere

co = cohere.ClientV2(
"COHERE_API_KEY"
)

query_inputs = [
    {
'content'
: [
            {
'type'
:
'text'
,
'text'
:
'Adobe'
},
        ]
    },
    {
'content'
: [
            {
'type'
:
'text'
,
'text'
:
'software'
}
        ]
    }
]

embeddings = co.embed(
    inputs=query_inputs,
    model=
'embed-multilingual-v3.0'
,
    input_type=
"classification"
,
    embedding_types=[
"float"
],
)
在代码中，查询文本被组织成
query_inputs
中的 token，并嵌入到浮点向量列表中。然后就可以使用 Milvus 的 EmbeddingList 进行相似性搜索，如下所示。
from
pymilvus.client.embedding_list
import
EmbeddingList

query_emb_list = EmbeddingList()
if
(embeddings.embeddings.
float
):
  query_emb_list.add_batch(embeddings.embeddings.
float
)

results = client.search(
    collection_name=
"wiki_documents"
,
    data=[query_emb_list],
    anns_field=
"paragraphs[emb]"
,
    search_params={
"metric_type"
:
"MAX_SIM_COSINE"
},
    limit=
10
,
    output_fields=[
"title"
]
)
for
hit
in
results[
0
]:
print
(
f"Document
{hit[
'entity'
][
'title'
]}
:
{hit[
'distance'
]:
.4
f}
"
)
上述代码的输出类似于下图：
# Document Software: 2.3035
# Document Application: 2.1875
# Document Adobe Illustrator: 2.1167
# Document Open source: 2.0542
# Document Computer: 1.9811
# Document Microsoft: 1.9784
# Document Web browser: 1.9655
# Document Program: 1.9627
# Document Website: 1.9594
# Document Computer science: 1.9460
余弦相似度得分从
-1
到
1
，上述输出中的相似度得分清楚地显示了多个令牌级相似度得分的总和。
ColPali 文本检索系统
在本节中，我们将使用 Milvus 的结构数组（Array of Structs）建立一个基于 ColPali 的文本检索系统。在此之前，请设置一个与 Milvus v2.6.x 兼容的 Milvus v2.6.x 实例Zilliz 云集群。
第 1 步：安装依赖项
pip install --upgrade huggingface-hub transformers datasets pymilvus 'colpali-engine>=0.3.0,<0.4.0'
第 2 步：加载 Vidore 数据集
在本节中，我们将使用名为
vidore_v2_finance_en 的
Vidore 数据集。该数据集是一个银行业年度报告语料库，用于长文档理解任务。它是 ViDoRe v3 Benchmark 的 10 个语料库之一。有关该数据集的详细信息，请访问
本页
。
from
datasets
import
load_dataset

ds = load_dataset(
"vidore/vidore_v3_finance_en"
,
"corpus"
)
df = ds[
'test'
].to_pandas()
如果本地没有该数据集，运行上述脚本即可下载该数据集。数据集中的每条记录都是财务报告中的一页。下表显示了该数据集的结构。
列名
说明
corpus_id
语料库中的一条记录
image
以字节为单位的页面图像。
doc_id
描述性文档 ID。
page_number_in_doc
文档中当前页面的页码。
步骤 3：生成页面图像的 Embeddings
如
概述
部分所述，ColPali 模型是一种 VLM，可将图像投射到文本模型的向量空间中。在本步骤中，我们将使用最新的 ColPali 模型
vidore/colpali-v1.3
。有关该模型的详细信息，请参见
本页
。
import
torch
from
typing
import
cast
from
colpali_engine.models
import
ColPali, ColPaliProcessor

model_name =
"vidore/colpali-v1.3"
model = ColPali.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map=
"cuda:0"
,
# or "mps" if on Apple Silicon
).
eval
()

processor = ColPaliProcessor.from_pretrained(model_name)
模型准备就绪后，您可以尝试为特定图像生成补丁，具体方法如下。
from
PIL
import
Image
from
io
import
BytesIO
# Use the iterrow() generator to get the first row
row =
next
(df.iterrows())[
1
]
# Include the image in the above row in a list
images = [ Image.
open
(row[
'image'
][
'bytes'
] ]
patches = processor.process_images(images).to(model.device)
patches_embeddings = model(**patches_in_pixels)[
0
]
# Check the shape of the embeddings generated for the patches
print
(patches_embeddings.shape)
# [1031, 128]
在上面的代码中，ColPali 模型将图像大小调整为 448 x 448 像素，然后将其分割为多个补丁，每个补丁的大小为 14 x 14 像素。最后，这些斑块会被嵌入到 1031 个嵌入项中，每个嵌入项有 128 个维度。
你可以使用如下循环生成所有图像的嵌入：
data = []
for
index, row
in
df.iterrows():
  row =
next
(df.iterrows())[
1
]
  corpus_id = row[
'corpus_id'
]
  
  images = [Image.
open
(BytesIO(row[
'image'
][
'bytes'
]))]
  batch_images = processor.process_images(images).to(model.device)
  patches = model(**batch_images)[
0
]

  doc_id = row[
'doc_id'
]
  markdown = row[
'markdown'
]
  page_number_in_doc = row[
'page_number_in_doc'
]

  data.append({
"corpus_id"
: corpus_id,
"patches"
: [ {
"emb"
: emb}
for
emb
in
patches ],
"doc_id"
: markdown,
"page_number_in_doc"
: row[
'page_number_in_doc'
]
  })
由于需要嵌入的数据量较大，这一步相对耗时。
步骤 4：为财务报告数据集创建 Collections
数据准备就绪后，我们将创建一个 Collection。在 Collection 中，名为
patches
的字段是一个 Structs 数组。
from
pymilvus
import
MilvusClient, DataType

client = MilvusClient(
    uri=YOUR_CLUSTER_ENDPOINT,
    token=YOUR_API_KEY
)

schema = client.create_schema()

schema.add_field(
    field_name=
"corpus_id"
,
    datatype=DataType.INT64,
    is_primary=
True
)

patch_schema = client.create_struct_field_schema()

patch_schema.add_field(
    field_name=
"emb"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
128
)

schema.add_field(
    field_name=
"patches"
,
    datatype=DataType.ARRAY,
    element_type=DataType.STRUCT,
    struct_schema=patch_schema,
    max_capacity=
1031
)

schema.add_field(
    field_name=
"doc_id"
,
    datatype=DataType.VARCHAR,
    max_length=
512
)

schema.add_field(
    field_name=
"page_number_in_doc"
,
    datatype=DataType.INT64
)

index_params = client.prepare_index_params()

index_params.add_index(
    field_name=
"patches[emb]"
,
    index_type=
"AUTOINDEX"
,
    metric_type=
"MAX_SIM_COSINE"
)

client.create_collection(
    collection_name=
"financial_reports"
,
    schema=schema,
    index_params=index_params
)
第 5 步：将财务报告插入 Collections
现在，我们可以将准备好的财务报告插入 Collections 中。
client.insert(
    collection_name=
"financial_reports"
,
    data=data
)
从输出结果可以看出，Vidore 数据集中的所有页面都已插入。
第 6 步：在财务报告中搜索
数据准备就绪后，我们就可以对集合中的数据进行搜索，具体操作如下：
from
pymilvus.client.embedding_list
import
EmbeddingList

queries = [
"quarterly revenue growth chart"
]

batch_queries = processor.process_queries(queries).to(model.device)
with
torch.no_grad():
  query_embeddings = model(**batch_queries)

query_emb_list = EmbeddingList()
query_emb_list.add_batch(query_embeddings[
0
].cpu())

results = client.search(
    collection_name=
"financial_reports"
,
    data=[query_emb_list],
    anns_field=
"patches[emb]"
,
    search_params={
"metric_type"
:
"MAX_SIM_COSINE"
},
    limit=
10
,
    output_fields=[
"doc_id"
,
"page_number_in_doc"
]
)