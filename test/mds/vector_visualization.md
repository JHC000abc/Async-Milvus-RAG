向量可视化
在本例中，我们将展示如何使用
t-SNE
可视化 Milvus 中的嵌入（向量）。
减维技术（如 t-SNE）对于在二维或三维空间中可视化复杂的高维数据，同时保留局部结构来说非常宝贵。这可以实现模式识别，增强对特征关系的理解，并方便解释机器学习模型的结果。此外，它还能通过直观地比较聚类结果来帮助算法评估，简化向非专业受众的数据展示，并通过使用低维表示来降低计算成本。通过这些应用，t-SNE 不仅有助于深入了解数据集，还能支持更明智的决策过程。
准备工作
依赖和环境
$
pip install --upgrade pymilvus openai requests tqdm matplotlib seaborn
我们将在本例中使用 OpenAI 的 Embeddings 模型。你需要准备 OPENAI_API_KEY 作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
准备数据
我们使用 Milvus
文档 2.4.x
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
准备嵌入模型
我们初始化 OpenAI 客户端，准备嵌入模型。
from
openai
import
OpenAI

openai_client = OpenAI()
定义一个函数，使用 OpenAI 客户端生成文本嵌入。我们以
text-embedding-3-large
模型为例。
def
emb_text
(
text
):
return
(
        openai_client.embeddings.create(
input
=text, model=
"text-embedding-3-large"
)
        .data[
0
]
        .embedding
    )
生成一个测试嵌入，并打印其尺寸和前几个元素。
test_embedding = emb_text(
"This is a test"
)
embedding_dim =
len
(test_embedding)
print
(embedding_dim)
print
(test_embedding[:
10
])
3072
[-0.015370666049420834, 0.00234124343842268, -0.01011690590530634, 0.044725317507982254, -0.017235849052667618, -0.02880779094994068, -0.026678944006562233, 0.06816216558218002, -0.011376636102795601, 0.021659553050994873]
将数据载入 Milvus
创建 Collections
from
pymilvus
import
MilvusClient

milvus_client = MilvusClient(uri=
"./milvus_demo.db"
)

collection_name =
"my_rag_collection"
至于
MilvusClient
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
检查 Collections 是否已存在，如果存在则删除。
if
milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)
使用指定参数创建新 Collections。
如果我们不指定任何字段信息，Milvus 会自动创建一个主键的默认
id
字段，以及一个存储向量数据的
vector
字段。保留的 JSON 字段用于存储非 Schema 定义的字段及其值。
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=embedding_dim,
    metric_type=
"IP"
,
# Inner product distance
consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
)
插入数据
遍历文本行，创建 Embeddings，然后将数据插入 Milvus。
这里有一个新字段
text
，它是 Collections Schema 中的一个非定义字段。它会自动添加到预留的 JSON 动态字段中，在高层次上可将其视为普通字段。
from
tqdm
import
tqdm

data = []
for
i, line
in
enumerate
(tqdm(text_lines, desc=
"Creating embeddings"
)):
    data.append({
"id"
: i,
"vector"
: emb_text(line),
"text"
: line})

milvus_client.insert(collection_name=collection_name, data=data)
Creating embeddings: 100%|██████████| 72/72 [00:20<00:00,  3.60it/s]





{'insert_count': 72, 'ids': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71], 'cost': 0}
向量搜索中的可视化 Embeddings
在本节中，我们将执行一次 milvus 搜索，然后将查询向量和检索向量一起进行降维可视化。
检索查询数据
让我们为搜索准备一个问题。
# Modify the question to test it with your own query!
question =
"How is data stored in Milvus?"
在 Collections 中搜索该问题，并检索语义前 10 个匹配项。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=[
        emb_text(question)
    ],
# Use the `emb_text` function to convert the question to an embedding vector
limit=
10
,
# Return top 10 results
search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
# Inner product distance
output_fields=[
"text"
],
# Return the text field
)
让我们看看查询的搜索结果
import
json

retrieved_lines_with_distances = [
    (res[
"entity"
][
"text"
], res[
"distance"
])
for
res
in
search_res[
0
]
]
print
(json.dumps(retrieved_lines_with_distances, indent=
4
))
[
    [
        " Where does Milvus store data?\n\nMilvus deals with two types of data, inserted data and metadata. \n\nInserted data, including vector data, scalar data, and collection-specific schema, are stored in persistent storage as incremental log. Milvus supports multiple object storage backends, including [MinIO](https://min.io/), [AWS S3](https://aws.amazon.com/s3/?nc1=h_ls), [Google Cloud Storage](https://cloud.google.com/storage?hl=en#object-storage-for-companies-of-all-sizes) (GCS), [Azure Blob Storage](https://azure.microsoft.com/en-us/products/storage/blobs), [Alibaba Cloud OSS](https://www.alibabacloud.com/product/object-storage-service), and [Tencent Cloud Object Storage](https://www.tencentcloud.com/products/cos) (COS).\n\nMetadata are generated within Milvus. Each Milvus module has its own metadata that are stored in etcd.\n\n###",
        0.7675539255142212
    ],
    [
        "How does Milvus handle vector data types and precision?\n\nMilvus supports Binary, Float32, Float16, and BFloat16 vector types.\n\n- Binary vectors: Store binary data as sequences of 0s and 1s, used in image processing and information retrieval.\n- Float32 vectors: Default storage with a precision of about 7 decimal digits. Even Float64 values are stored with Float32 precision, leading to potential precision loss upon retrieval.\n- Float16 and BFloat16 vectors: Offer reduced precision and memory usage. Float16 is suitable for applications with limited bandwidth and storage, while BFloat16 balances range and efficiency, commonly used in deep learning to reduce computational requirements without significantly impacting accuracy.\n\n###",
        0.6210848689079285
    ],
    [
        "Does the query perform in memory? What are incremental data and historical data?\n\nYes. When a query request comes, Milvus searches both incremental data and historical data by loading them into memory. Incremental data are in the growing segments, which are buffered in memory before they reach the threshold to be persisted in storage engine, while historical data are from the sealed segments that are stored in the object storage. Incremental data and historical data together constitute the whole dataset to search.\n\n###",
        0.585393488407135
    ],
    [
        "Why is there no vector data in etcd?\n\netcd stores Milvus module metadata; MinIO stores entities.\n\n###",
        0.579704999923706
    ],
    [
        "How does Milvus flush data?\n\nMilvus returns success when inserted data are loaded to the message queue. However, the data are not yet flushed to the disk. Then Milvus' data node writes the data in the message queue to persistent storage as incremental logs. If `flush()` is called, the data node is forced to write all data in the message queue to persistent storage immediately.\n\n###",
        0.5777501463890076
    ],
    [
        "What is the maximum dataset size Milvus can handle?\n\n  \nTheoretically, the maximum dataset size Milvus can handle is determined by the hardware it is run on, specifically system memory and storage:\n\n- Milvus loads all specified collections and partitions into memory before running queries. Therefore, memory size determines the maximum amount of data Milvus can query.\n- When new entities and and collection-related schema (currently only MinIO is supported for data persistence) are added to Milvus, system storage determines the maximum allowable size of inserted data.\n\n###",
        0.5655910968780518
    ],
    [
        "Does Milvus support inserting and searching data simultaneously?\n\nYes. Insert operations and query operations are handled by two separate modules that are mutually independent. From the client's perspective, an insert operation is complete when the inserted data enters the message queue. However, inserted data are unsearchable until they are loaded to the query node. For growing segments with incremental data, Milvus automatically builds interim indexes to ensure efficient search performance, even when the segment size does not reach the index-building threshold, calculated as `dataCoord.segment.maxSize` × `dataCoord.segment.sealProportion`. You can control this behavior through the configuration parameter `queryNode.segcore.interimIndex.enableIndex` in the [Milvus configuration file](https://github.com/milvus-io/milvus/blob/master/configs/milvus.yaml#L440) - setting it to `true` enables temporary indexing (default) while setting it to `false` disables it.\n\n###",
        0.5618637204170227
    ],
    [
        "What data types does Milvus support on the primary key field?\n\nIn current release, Milvus supports both INT64 and string.\n\n###",
        0.5561620593070984
    ],
    [
        "Is Milvus available for concurrent search?\n\nYes. For queries on the same collection, Milvus concurrently searches the incremental and historical data. However, queries on different collections are conducted in series. Whereas the historical data can be an extremely huge dataset, searches on the historical data are relatively more time-consuming and essentially performed in series.\n\n###",
        0.529681921005249
    ],
    [
        "Can vectors with duplicate primary keys be inserted into Milvus?\n\nYes. Milvus does not check if vector primary keys are duplicates.\n\n###",
        0.528809666633606
    ]
]
通过 t-SNE 将维度降低到 2-d
让我们通过 t-SNE 将 Embeddings 的维度降为 2-d。我们将使用
sklearn
库来执行 t-SNE 变换。
import
pandas
as
pd
import
numpy
as
np
from
sklearn.manifold
import
TSNE

data.append({
"id"
:
len
(data),
"vector"
: emb_text(question),
"text"
: question})
embeddings = []
for
gp
in
data:
    embeddings.append(gp[
"vector"
])

X = np.array(embeddings, dtype=np.float32)
tsne = TSNE(random_state=
0
, max_iter=
1000
)
tsne_results = tsne.fit_transform(X)

df_tsne = pd.DataFrame(tsne_results, columns=[
"TSNE1"
,
"TSNE2"
])
df_tsne
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
TSNE1
TSNE2
0
-3.877362
0.866726
1
-5.923084
0.671701
2
-0.645954
0.240083
3
0.444582
1.222875
4
6.503896
-4.984684
...
...
...
69
6.354055
1.264959
70
6.055961
1.266211
71
-1.516003
1.328765
72
3.971772
-0.681780
73
3.971772
-0.681780
74 行 × 2 列
在二维平面上可视化 Milvus 搜索结果
我们将用绿色绘制查询向量，用红色绘制检索向量，用蓝色绘制剩余向量。
import
matplotlib.pyplot
as
plt
import
seaborn
as
sns
# Extract similar ids from search results
similar_ids = [gp[
"id"
]
for
gp
in
search_res[
0
]]

df_norm = df_tsne[:-
1
]

df_query = pd.DataFrame(df_tsne.iloc[-
1
]).T
# Filter points based on similar ids
similar_points = df_tsne[df_tsne.index.isin(similar_ids)]
# Create the plot
fig, ax = plt.subplots(figsize=(
8
,
6
))
# Set figsize
# Set the style of the plot
sns.set_style(
"darkgrid"
, {
"grid.color"
:
".6"
,
"grid.linestyle"
:
":"
})
# Plot all points in blue
sns.scatterplot(
    data=df_tsne, x=
"TSNE1"
, y=
"TSNE2"
, color=
"blue"
, label=
"All knowledge"
, ax=ax
)
# Overlay similar points in red
sns.scatterplot(
    data=similar_points,
    x=
"TSNE1"
,
    y=
"TSNE2"
,
    color=
"red"
,
    label=
"Similar knowledge"
,
    ax=ax,
)

sns.scatterplot(
    data=df_query, x=
"TSNE1"
, y=
"TSNE2"
, color=
"green"
, label=
"Query"
, ax=ax
)
# Set plot titles and labels
plt.title(
"Scatter plot of knowledge using t-SNE"
)
plt.xlabel(
"TSNE1"
)
plt.ylabel(
"TSNE2"
)
# Set axis to be equal
plt.axis(
"equal"
)
# Display the legend
plt.legend()
# Show the plot
plt.show()
图
我们可以看到，查询向量与检索向量很接近。虽然检索到的向量并不在以查询为中心、半径固定的标准圆内，但我们可以看到，它们在二维平面上仍然非常接近查询向量。
使用降维技术可以促进对向量的理解和故障排除。希望你能通过本教程更好地理解向量。