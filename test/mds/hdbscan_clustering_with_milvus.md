利用 Milvus 进行 HDBSCAN 聚类
使用深度学习模型可以将数据转化为 Embeddings，从而捕捉到原始数据的有意义表征。通过应用无监督聚类算法，我们可以根据固有模式将相似的数据点归类到一起。HDBSCAN（基于密度的有噪声应用空间分层聚类）是一种广泛使用的聚类算法，它通过分析数据点的密度和距离对数据点进行有效分组。它对于发现不同形状和大小的聚类特别有用。在本笔记本中，我们将使用 HDBSCAN 与高性能向量数据库 Milvus，根据数据点的 Embeddings 将其聚类为不同的组。
HDBSCAN （Hierarchical Density-Based Spatial Clustering of Applications with Noise）是一种聚类算法，它依赖于计算嵌入空间中数据点之间的距离。这些由深度学习模型创建的嵌入以高维形式表示数据。为了对相似数据点进行分组，HDBSCAN 要确定它们之间的距离和密度，但高效计算这些距离，尤其是对大型数据集而言，可能具有挑战性。
Milvus 是一种高性能向量数据库，它通过存储和索引嵌入来优化这一过程，从而可以快速检索相似向量。HDBSCAN 和 Milvus 配合使用时，可以在嵌入空间中对大规模数据集进行高效聚类。
在本笔记本中，我们将使用 BGE-M3 嵌入模型从新闻标题数据集中提取嵌入，利用 Milvus 高效计算嵌入之间的距离以帮助 HDBSCAN 进行聚类，然后使用 UMAP 方法将结果可视化以进行分析。本笔记本是 Milvus 对
Dylan Castillo 文章的
改编。
准备工作
从 https://www.kaggle.com/datasets/dylanjcastillo/news-headlines-2024/ 下载新闻数据集
$
pip install
"pymilvus[model]"
$
pip install hdbscan
$
pip install plotly
$
pip install umap-learn
下载数据
从 https://www.kaggle.com/datasets/dylanjcastillo/news-headlines-2024/ 下载新闻数据集，提取
news_data_dedup.csv
并将其放入当前目录。
或通过 curl 下载：
%%bash
curl -L -o ~/Downloads/news-headlines-2024.zip\
  https://www.kaggle.com/api/v1/datasets/download/dylanjcastillo/news-headlines-2024
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:--  0:00:02 --:--:--     0 --:--:--     0
100  225k  100  225k    0     0  33151      0  0:00:06  0:00:06 --:--:-- 62160:03  114k  0:00:07  0:00:06  0:00:01 66615    0  30519      0  0:00:07  0:00:06  0:00:01 61622
提取 Embeddings 至 Milvus
我们将使用 Milvus 创建一个 Collections，并使用 BGE-M3 模型提取密集嵌入。
import
pandas
as
pd
from
dotenv
import
load_dotenv
from
pymilvus.model.hybrid
import
BGEM3EmbeddingFunction
from
pymilvus
import
FieldSchema, Collection, connections, CollectionSchema, DataType

load_dotenv()

df = pd.read_csv(
"news_data_dedup.csv"
)


docs = [
f"
{title}
\n
{description}
"
for
title, description
in
zip
(df.title, df.description)
]
ef = BGEM3EmbeddingFunction()

embeddings = ef(docs)[
"dense"
]

connections.connect(uri=
"milvus.db"
)
如果你只需要一个本地向量数据库，用于小规模数据或原型设计，那么将 uri 设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储到这个文件中。
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
fields = [
    FieldSchema(
        name=
"id"
, dtype=DataType.INT64, is_primary=
True
, auto_id=
True
),
# Primary ID field
FieldSchema(
        name=
"embedding"
, dtype=DataType.FLOAT_VECTOR, dim=
1024
),
# Float vector field (embedding)
FieldSchema(
        name=
"text"
, dtype=DataType.VARCHAR, max_length=
65535
),
# Float vector field (embedding)
]

schema = CollectionSchema(fields=fields, description=
"Embedding collection"
)

collection = Collection(name=
"news_data"
, schema=schema)
for
doc, embedding
in
zip
(docs, embeddings):
    collection.insert({
"text"
: doc,
"embedding"
: embedding})
print
(doc)

index_params = {
"index_type"
:
"FLAT"
,
"metric_type"
:
"L2"
,
"params"
: {}}

collection.create_index(field_name=
"embedding"
, index_params=index_params)

collection.flush()
为 HDBSCAN 构建距离矩阵
HDBSCAN 需要计算点与点之间的距离来进行聚类，这可能需要大量计算。由于远处的点对聚类分配的影响较小，我们可以通过计算前 k 个近邻来提高效率。在本例中，我们使用的是 FLAT 索引，但对于大规模数据集，Milvus 支持更高级的索引方法来加速搜索过程。 首先，我们需要获取一个迭代器来迭代之前创建的 Milvus Collections。
import
hdbscan
import
numpy
as
np
import
pandas
as
pd
import
plotly.express
as
px
from
umap
import
UMAP
from
pymilvus
import
Collection

collection = Collection(name=
"news_data"
)
collection.load()

iterator = collection.query_iterator(
    batch_size=
10
, expr=
"id > 0"
, output_fields=[
"id"
,
"embedding"
]
)

search_params = {
"metric_type"
:
"L2"
,
"params"
: {
"nprobe"
:
10
},
}
# L2 is Euclidean distance
ids = []
dist = {}

embeddings = []
我们将遍历 Milvus Collections 中的所有嵌入。对于每个 Embeddings，我们将搜索其在同一 Collections 中的前 k 个邻居，获取它们的 id 和距离。然后，我们还需要创建一个字典，将原始 ID 映射到距离矩阵中的连续索引。完成后，我们需要创建一个初始化所有元素为无穷大的距离矩阵，并填充我们搜索到的元素。这样，远距离点之间的距离将被忽略。最后，我们使用 HDBSCAN 库，利用我们创建的距离矩阵对点进行聚类。我们需要将度量值设置为 "预计算"，以表明数据是距离矩阵而非原始嵌入。
while
True
:
    batch = iterator.
next
()
    batch_ids = [data[
"id"
]
for
data
in
batch]
    ids.extend(batch_ids)

    query_vectors = [data[
"embedding"
]
for
data
in
batch]
    embeddings.extend(query_vectors)

    results = collection.search(
        data=query_vectors,
        limit=
50
,
        anns_field=
"embedding"
,
        param=search_params,
        output_fields=[
"id"
],
    )
for
i, batch_id
in
enumerate
(batch_ids):
        dist[batch_id] = []
for
result
in
results[i]:
            dist[batch_id].append((result.
id
, result.distance))
if
len
(batch) ==
0
:
break
ids2index = {}
for
id
in
dist:
    ids2index[
id
] =
len
(ids2index)

dist_metric = np.full((
len
(ids),
len
(ids)), np.inf, dtype=np.float64)
for
id
in
dist:
for
result
in
dist[
id
]:
        dist_metric[ids2index[
id
]][ids2index[result[
0
]]] = result[
1
]

h = hdbscan.HDBSCAN(min_samples=
3
, min_cluster_size=
3
, metric=
"precomputed"
)
hdb = h.fit(dist_metric)
之后，HDBSCAN 聚类就完成了。我们可以获取一些数据并显示其聚类结果。请注意，有些数据不会被分配到任何聚类中，这意味着它们是噪音，因为它们位于某些稀疏区域。
使用 UMAP 进行聚类可视化
我们已经使用 HDBSCAN 对数据进行了聚类，并获得了每个数据点的标签。不过，利用一些可视化技术，我们可以获得聚类的全貌，以便进行直观分析。现在，我们将使用 UMAP 对聚类进行可视化。UMAP 是一种用于降维的高效方法，它在保留高维数据结构的同时，将其投影到低维空间，以便进行可视化或进一步分析。有了它，我们就能在二维或三维空间中可视化原始高维数据，并清楚地看到聚类。 在这里，我们再次遍历数据点，获取原始数据的 ID 和文本，然后使用 ploty 将数据点与这些元信息绘制成图，并用不同的颜色代表不同的聚类。
import
plotly.io
as
pio

pio.renderers.default =
"notebook"
umap = UMAP(n_components=
2
, random_state=
42
, n_neighbors=
80
, min_dist=
0.1
)

df_umap = (
    pd.DataFrame(umap.fit_transform(np.array(embeddings)), columns=[
"x"
,
"y"
])
    .assign(cluster=
lambda
df: hdb.labels_.astype(
str
))
    .query(
'cluster != "-1"'
)
    .sort_values(by=
"cluster"
)
)
iterator = collection.query_iterator(
    batch_size=
10
, expr=
"id > 0"
, output_fields=[
"id"
,
"text"
]
)

ids = []
texts = []
while
True
:
    batch = iterator.
next
()
if
len
(batch) ==
0
:
break
batch_ids = [data[
"id"
]
for
data
in
batch]
    batch_texts = [data[
"text"
]
for
data
in
batch]
    ids.extend(batch_ids)
    texts.extend(batch_texts)

show_texts = [texts[i]
for
i
in
df_umap.index]

df_umap[
"hover_text"
] = show_texts
fig = px.scatter(
    df_umap, x=
"x"
, y=
"y"
, color=
"cluster"
, hover_data={
"hover_text"
:
True
}
)
fig.show()
图像
在这里，我们展示了数据的良好聚类，你可以将鼠标悬停在点上查看它们所代表的文本。通过本笔记本，我们希望您能学会如何使用 HDBSCAN 对 Milvus 的嵌入数据进行高效聚类，这也可以应用于其他类型的数据。结合大型语言模型，这种方法可以对您的数据进行大规模的深入分析。