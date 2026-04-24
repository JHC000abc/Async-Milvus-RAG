使用 ColPali 与 Milvus 一起进行多模式检索
现代检索模型通常使用单一嵌入来表示文本或图像。而 ColBERT 是一种神经模型，它利用每个数据实例的嵌入列表，并采用 "MaxSim "操作来计算两个文本之间的相似度。除文本数据外，图、表和图表也包含丰富的信息，而这些信息在基于文本的信息检索中往往被忽略。
MaxSim 函数通过查看查询和文档（你要搜索的内容）的标记嵌入来比较它们。对于查询中的每个单词，它都会从文档中挑选出最相似的单词（使用余弦相似度或平方 L2 距离），并将查询中所有单词的最大相似度相加。
ColPali 是一种将 ColBERT 的多向量表示法与 PaliGemma（多模态大语言模型）相结合的方法，可充分利用其强大的理解能力。这种方法可以使用统一的多向量嵌入来表示同时包含文本和图像的页面。这种多向量表示法中的嵌入可以捕捉详细信息，提高多模态数据的检索增强生成（RAG）性能。
在本笔记本中，我们将这种多向量表示法称为 "ColBERT embeddings"，以示通用。不过，实际使用的模型是
ColPali 模型
。我们将演示如何使用 Milvus 进行多向量检索。在此基础上，我们将介绍如何使用 ColPali 根据给定查询检索网页。
准备工作
$
pip install pdf2image
$
pip install pymilvus
$
pip install colpali_engine
$
pip install tqdm
$
pip install pillow
准备数据
我们将以 PDF RAG 为例。你可以下载
ColBERT
论文并将其放入
./pdf
。ColPali 不直接处理文本，而是将整个页面光栅化为图像。ColPali 模型擅长理解这些图像中包含的文本信息。因此，我们将把每个 PDF 页面转换成图像进行处理。
from
pdf2image
import
convert_from_path

pdf_path =
"pdfs/2004.12832v2.pdf"
images = convert_from_path(pdf_path)
for
i, image
in
enumerate
(images):
    image.save(
f"pages/page_
{i +
1
}
.png"
,
"PNG"
)
接下来，我们将使用 Milvus Lite 初始化数据库。只需将 uri 设置为 Milvus 服务托管的相应地址，就能轻松切换到完整的 Milvus 实例。
from
pymilvus
import
MilvusClient, DataType
import
numpy
as
np
import
concurrent.futures

client = MilvusClient(uri=
"milvus.db"
)
如果你只需要一个本地向量数据库用于小规模数据或原型设计，将 uri 设置为一个本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在这个文件中。
如果你有大规模数据，比如超过一百万个向量，你可以在
Docker 或 Kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器地址和端口作为 uri，例如
http://localhost:19530
。如果在 Milvus 上启用了身份验证功能，请使用 "
:
" 作为令牌，否则不要设置令牌。
如果您使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 API 密钥
相对应。
我们将定义一个 MilvusColbertRetriever 类，用于围绕 Milvus 客户端进行多向量数据检索。该实现将 ColBERT embeddings 扁平化并插入 Collections，其中每一行代表 ColBERT embedding 列表中的单个 embedding。它还会记录 doc_id 和 seq_id，以追踪每个嵌入的来源。
使用 ColBERT 嵌入列表进行搜索时，会进行多次搜索--每次搜索一个 ColBERT 嵌入。然后对检索到的 doc_ids 进行重复。然后将执行重新排序过程，即获取每个 doc_id 的完整 Embeddings，并计算 MaxSim 分数，得出最终排序结果。
class
MilvusColbertRetriever
:
def
__init__
(
self, milvus_client, collection_name, dim=
128
):
# Initialize the retriever with a Milvus client, collection name, and dimensionality of the vector embeddings.
# If the collection exists, load it.
self
.collection_name = collection_name
self
.client = milvus_client
if
self
.client.has_collection(collection_name=
self
.collection_name):
self
.client.load_collection(collection_name)
self
.dim = dim
def
create_collection
(
self
):
# Create a new collection in Milvus for storing embeddings.
# Drop the existing collection if it already exists and define the schema for the collection.
if
self
.client.has_collection(collection_name=
self
.collection_name):
self
.client.drop_collection(collection_name=
self
.collection_name)
        schema =
self
.client.create_schema(
            auto_id=
True
,
            enable_dynamic_fields=
True
,
        )
        schema.add_field(field_name=
"pk"
, datatype=DataType.INT64, is_primary=
True
)
        schema.add_field(
            field_name=
"vector"
, datatype=DataType.FLOAT_VECTOR, dim=
self
.dim
        )
        schema.add_field(field_name=
"seq_id"
, datatype=DataType.INT16)
        schema.add_field(field_name=
"doc_id"
, datatype=DataType.INT64)
        schema.add_field(field_name=
"doc"
, datatype=DataType.VARCHAR, max_length=
65535
)
self
.client.create_collection(
            collection_name=
self
.collection_name, schema=schema
        )
def
create_index
(
self
):
# Create an index on the vector field to enable fast similarity search.
# Releases and drops any existing index before creating a new one with specified parameters.
self
.client.release_collection(collection_name=
self
.collection_name)
self
.client.drop_index(
            collection_name=
self
.collection_name, index_name=
"vector"
)
        index_params =
self
.client.prepare_index_params()
        index_params.add_index(
            field_name=
"vector"
,
            index_name=
"vector_index"
,
            index_type=
"HNSW"
,
# or any other index type you want
metric_type=
"IP"
,
# or the appropriate metric type
params={
"M"
:
16
,
"efConstruction"
:
500
,
            },
# adjust these parameters as needed
)
self
.client.create_index(
            collection_name=
self
.collection_name, index_params=index_params, sync=
True
)
def
create_scalar_index
(
self
):
# Create a scalar index for the "doc_id" field to enable fast lookups by document ID.
self
.client.release_collection(collection_name=
self
.collection_name)

        index_params =
self
.client.prepare_index_params()
        index_params.add_index(
            field_name=
"doc_id"
,
            index_name=
"int32_index"
,
            index_type=
"INVERTED"
,
# or any other index type you want
)
self
.client.create_index(
            collection_name=
self
.collection_name, index_params=index_params, sync=
True
)
def
search
(
self, data, topk
):
# Perform a vector search on the collection to find the top-k most similar documents.
search_params = {
"metric_type"
:
"IP"
,
"params"
: {}}
        results =
self
.client.search(
self
.collection_name,
            data,
            limit=
int
(
50
),
            output_fields=[
"vector"
,
"seq_id"
,
"doc_id"
],
            search_params=search_params,
        )
        doc_ids =
set
()
for
r_id
in
range
(
len
(results)):
for
r
in
range
(
len
(results[r_id])):
                doc_ids.add(results[r_id][r][
"entity"
][
"doc_id"
])

        scores = []
def
rerank_single_doc
(
doc_id, data, client, collection_name
):
# Rerank a single document by retrieving its embeddings and calculating the similarity with the query.
doc_colbert_vecs = client.query(
                collection_name=collection_name,
filter
=
f"doc_id in [
{doc_id}
]"
,
                output_fields=[
"seq_id"
,
"vector"
,
"doc"
],
                limit=
1000
,
            )
            doc_vecs = np.vstack(
                [doc_colbert_vecs[i][
"vector"
]
for
i
in
range
(
len
(doc_colbert_vecs))]
            )
            score = np.dot(data, doc_vecs.T).
max
(
1
).
sum
()
return
(score, doc_id)
with
concurrent.futures.ThreadPoolExecutor(max_workers=
300
)
as
executor:
            futures = {
                executor.submit(
                    rerank_single_doc, doc_id, data, client,
self
.collection_name
                ): doc_id
for
doc_id
in
doc_ids
            }
for
future
in
concurrent.futures.as_completed(futures):
                score, doc_id = future.result()
                scores.append((score, doc_id))

        scores.sort(key=
lambda
x: x[
0
], reverse=
True
)
if
len
(scores) >= topk:
return
scores[:topk]
else
:
return
scores
def
insert
(
self, data
):
# Insert ColBERT embeddings and metadata for a document into the collection.
colbert_vecs = [vec
for
vec
in
data[
"colbert_vecs"
]]
        seq_length =
len
(colbert_vecs)
        doc_ids = [data[
"doc_id"
]
for
i
in
range
(seq_length)]
        seq_ids =
list
(
range
(seq_length))
        docs = [
""
] * seq_length
        docs[
0
] = data[
"filepath"
]
# Insert the data as multiple vectors (one for each sequence) along with the corresponding metadata.
self
.client.insert(
self
.collection_name,
            [
                {
"vector"
: colbert_vecs[i],
"seq_id"
: seq_ids[i],
"doc_id"
: doc_ids[i],
"doc"
: docs[i],
                }
for
i
in
range
(seq_length)
            ],
        )
我们将使用
colpali_engine
提取两个查询的嵌入列表，并从 PDF 页面检索相关信息。
from
colpali_engine.models
import
ColPali
from
colpali_engine.models.paligemma.colpali.processing_colpali
import
ColPaliProcessor
from
colpali_engine.utils.processing_utils
import
BaseVisualRetrieverProcessor
from
colpali_engine.utils.torch_utils
import
ListDataset, get_torch_device
from
torch.utils.data
import
DataLoader
import
torch
from
typing
import
List
, cast

device = get_torch_device(
"cpu"
)
model_name =
"vidore/colpali-v1.2"
model = ColPali.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map=device,
).
eval
()

queries = [
"How to end-to-end retrieval with ColBert?"
,
"Where is ColBERT performance table?"
,
]

processor = cast(ColPaliProcessor, ColPaliProcessor.from_pretrained(model_name))

dataloader = DataLoader(
    dataset=ListDataset[
str
](queries),
    batch_size=
1
,
    shuffle=
False
,
    collate_fn=
lambda
x: processor.process_queries(x),
)

qs:
List
[torch.Tensor] = []
for
batch_query
in
dataloader:
with
torch.no_grad():
        batch_query = {k: v.to(model.device)
for
k, v
in
batch_query.items()}
        embeddings_query = model(**batch_query)
    qs.extend(
list
(torch.unbind(embeddings_query.to(
"cpu"
))))
此外，我们还需要提取每个页面的嵌入列表，它显示每个页面有 1030 个 128 维嵌入。
from
tqdm
import
tqdm
from
PIL
import
Image
import
os

images = [Image.
open
(
"./pages/"
+ name)
for
name
in
os.listdir(
"./pages"
)]

dataloader = DataLoader(
    dataset=ListDataset[
str
](images),
    batch_size=
1
,
    shuffle=
False
,
    collate_fn=
lambda
x: processor.process_images(x),
)

ds:
List
[torch.Tensor] = []
for
batch_doc
in
tqdm(dataloader):
with
torch.no_grad():
        batch_doc = {k: v.to(model.device)
for
k, v
in
batch_doc.items()}
        embeddings_doc = model(**batch_doc)
    ds.extend(
list
(torch.unbind(embeddings_doc.to(
"cpu"
))))
print
(ds[
0
].shape)
0%|          | 0/10 [00:00<?, ?it/s]

100%|██████████| 10/10 [01:22<00:00,  8.24s/it]

torch.Size([1030, 128])
我们将使用 MilvusColbertRetriever 创建一个名为 "colpali "的 Collections。
retriever = MilvusColbertRetriever(collection_name=
"colpali"
, milvus_client=client)
retriever.create_collection()
retriever.create_index()
我们将向 Milvus 数据库插入嵌入列表。
filepaths = [
"./pages/"
+ name
for
name
in
os.listdir(
"./pages"
)]
for
i
in
range
(
len
(filepaths)):
    data = {
"colbert_vecs"
: ds[i].
float
().numpy(),
"doc_id"
: i,
"filepath"
: filepaths[i],
    }
    retriever.insert(data)
现在，我们可以使用查询嵌入列表搜索最相关的页面。
for
query
in
qs:
    query = query.
float
().numpy()
    result = retriever.search(query, topk=
1
)
print
(filepaths[result[
0
][
1
]])
./pages/page_5.png
./pages/page_7.png
最后，我们检索原始页面名称。利用 ColPali，我们可以检索多模态文档，而无需复杂的处理技术来提取文档中的文本和图像。通过利用大型视觉模型，可以在不损失大量信息的情况下分析更多信息，如表格和数字。