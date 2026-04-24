使用 Matryoshka 嵌入进行漏斗搜索
在构建高效的向量搜索系统时，一个关键的挑战是管理存储成本，同时保持可接受的延迟和召回率。现代嵌入模型输出的向量有成百上千个维度，这给原始向量和索引带来了巨大的存储和计算开销。
传统方法是在建立索引前应用量化或降维方法来降低存储需求。例如，我们可以使用乘积量化（PQ）降低精度，或使用主成分分析（PCA）降低维数，从而节省存储空间。这些方法会对整个向量集进行分析，以找到一个能保持向量间语义关系的更紧凑的向量集。
这些标准方法虽然有效，但只能在单一尺度上降低一次精度或维度。但是，如果我们能同时保持多层细节，就像一座精确度越来越高的金字塔呢？
这就是 Matryoshka Embeddings。这些巧妙的构造以俄罗斯嵌套娃娃命名（见插图），将多级表示嵌入到单个向量中。与传统的后处理方法不同，Matryoshka 嵌入在初始训练过程中就能学习这种多尺度结构。结果非常显著：不仅完整的 Embeddings 能够捕捉输入语义，而且每个嵌套的子集前缀（前半部分、前四分之一等）都提供了一个连贯的、即使不那么详细的表示。
在本笔记本中，我们将研究如何将 Matryoshka 嵌入与 Milvus 一起用于语义搜索。我们展示了一种名为 "漏斗搜索 "的算法，它允许我们在嵌入维度的一小部分子集上执行相似性搜索，而不会导致召回率急剧下降。
准备工作
$
pip install datasets numpy pandas pymilvus sentence-transformers tqdm
仅用于 CPU：
$
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
用于 CUDA 11.8
$
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
CUDA 11.8 的安装命令只是一个示例。安装 PyTorch 时，请确认您的 CUDA 版本。
import
functools
from
datasets
import
load_dataset
import
numpy
as
np
import
pandas
as
pd
import
pymilvus
from
pymilvus
import
MilvusClient
from
pymilvus
import
FieldSchema, CollectionSchema, DataType
from
sentence_transformers
import
SentenceTransformer
import
torch
import
torch.nn.functional
as
F
from
tqdm
import
tqdm
加载 Matryoshka 嵌入模型
我们不使用标准的嵌入模型，如
sentence-transformers/all-MiniLM-L12-v2
等标准嵌入
模型
，而是使用
Nomic
专门为生成 Matryoshka 嵌入而训练
的模型
。
model = SentenceTransformer(
# Remove 'device='mps' if running on non-Mac device
"nomic-ai/nomic-embed-text-v1.5"
,
    trust_remote_code=
True
,
    device=
"mps"
,
)
<All keys matched successfully>
加载数据集、嵌入项目和构建向量数据库
以下代码是对文档页面
"使用句子变形器和 Milvus 进行电影搜索 "中
的代码的修改
。
首先，我们从 HuggingFace 加载数据集。它包含约 35k 个条目，每个条目对应一部有维基百科文章的电影。我们将在本例中使用
Title
和
PlotSummary
字段。
ds = load_dataset(
"vishnupriyavr/wiki-movie-plots-with-summaries"
, split=
"train"
)
print
(ds)
Dataset({
    features: ['Release Year', 'Title', 'Origin/Ethnicity', 'Director', 'Cast', 'Genre', 'Wiki Page', 'Plot', 'PlotSummary'],
    num_rows: 34886
})
接下来，我们连接到 Milvus Lite 数据库，指定数据 Schema，并用此 Schema 创建一个 Collections。我们将在不同字段中存储非规范化嵌入和嵌入的前六分之一。这样做的原因是，我们需要前 1/6 的 Matryoshka 嵌入来执行相似性搜索，而其余 5/6 的嵌入则用于重新排序和改进搜索结果。
embedding_dim =
768
search_dim =
128
collection_name =
"movie_embeddings"
client = MilvusClient(uri=
"./wiki-movie-plots-matryoshka.db"
)

fields = [
    FieldSchema(name=
"id"
, dtype=DataType.INT64, is_primary=
True
, auto_id=
True
),
    FieldSchema(name=
"title"
, dtype=DataType.VARCHAR, max_length=
256
),
# First sixth of unnormalized embedding vector
FieldSchema(name=
"head_embedding"
, dtype=DataType.FLOAT_VECTOR, dim=search_dim),
# Entire unnormalized embedding vector
FieldSchema(name=
"embedding"
, dtype=DataType.FLOAT_VECTOR, dim=embedding_dim),
]

schema = CollectionSchema(fields=fields, enable_dynamic_field=
False
)
client.create_collection(collection_name=collection_name, schema=schema)
Milvus 目前不支持对嵌入式子集进行搜索，因此我们将嵌入式分成两部分：头部代表要索引和搜索的向量的初始子集，尾部是剩余部分。该模型是为余弦距离相似性搜索而训练的，因此我们对头部嵌入进行了归一化处理。不过，为了以后计算更大子集的相似性，我们需要存储头部嵌入的规范，因此可以在连接到尾部之前对其进行非规范化处理。
为了通过前 1/6 的嵌入执行搜索，我们需要在
head_embedding
字段上创建一个向量搜索索引。稍后，我们将比较 "漏斗搜索 "和常规向量搜索的结果，因此也要在全嵌入上建立一个搜索索引。
重要的是，我们使用的是
COSINE
而不是
IP
距离度量，因为否则我们就需要跟踪嵌入规范，这将使实现过程变得复杂（一旦介绍了漏斗搜索算法，这一点将更有意义）。
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"head_embedding"
, index_type=
"FLAT"
, metric_type=
"COSINE"
)
index_params.add_index(field_name=
"embedding"
, index_type=
"FLAT"
, metric_type=
"COSINE"
)
client.create_index(collection_name, index_params)
最后，我们对所有 35k 部电影的情节摘要进行编码，并将相应的 Embeddings 输入数据库。
for
batch
in
tqdm(ds.batch(batch_size=
512
)):
# This particular model requires us to prefix 'search_document:' to stored entities
plot_summary = [
"search_document: "
+ x.strip()
for
x
in
batch[
"PlotSummary"
]]
# Output of embedding model is unnormalized
embeddings = model.encode(plot_summary, convert_to_tensor=
True
)
    head_embeddings = embeddings[:, :search_dim]

    data = [
        {
"title"
: title,
"head_embedding"
: head.cpu().numpy(),
"embedding"
: embedding.cpu().numpy(),
        }
for
title, head, embedding
in
zip
(batch[
"Title"
], head_embeddings, embeddings)
    ]
    res = client.insert(collection_name=collection_name, data=data)
100%|██████████| 69/69 [05:57<00:00,  5.18s/it]
执行漏斗搜索
现在，让我们使用 Matryoshka 嵌入维数的前 1/6 来执行 "漏斗搜索"。我有三部要检索的电影，并制作了自己的情节摘要用于查询数据库。我们嵌入查询，然后在
head_embedding
字段上执行向量搜索，检索出 128 个结果候选。
queries = [
"An archaeologist searches for ancient artifacts while fighting Nazis."
,
"A teenager fakes illness to get off school and have adventures with two friends."
,
"A young couple with a kid look after a hotel during winter and the husband goes insane."
,
]
# Search the database based on input text
def
embed_search
(
data
):
    embeds = model.encode(data)
return
[x
for
x
in
embeds]
# This particular model requires us to prefix 'search_query:' to queries
instruct_queries = [
"search_query: "
+ q.strip()
for
q
in
queries]
search_data = embed_search(instruct_queries)
# Normalize head embeddings
head_search = [x[:search_dim]
for
x
in
search_data]
# Perform standard vector search on first sixth of embedding dimensions
res = client.search(
    collection_name=collection_name,
    data=head_search,
    anns_field=
"head_embedding"
,
    limit=
128
,
    output_fields=[
"title"
,
"head_embedding"
,
"embedding"
],
)
此时，我们已经在更小的向量空间上执行了搜索，因此相对于在完整空间上的搜索，可能会降低延迟并减少对索引的存储要求。让我们来看看每个查询的前 5 个匹配结果：
for
query, hits
in
zip
(queries, res):
    rows = [x[
"entity"
]
for
x
in
hits][:
5
]
print
(
"Query:"
, query)
print
(
"Results:"
)
for
row
in
rows:
print
(row[
"title"
].strip())
print
()
Query: An archaeologist searches for ancient artifacts while fighting Nazis.
Results:
"Pimpernel" Smith
Black Hunters
The Passage
Counterblast
Dominion: Prequel to the Exorcist

Query: A teenager fakes illness to get off school and have adventures with two friends.
Results:
How to Deal
Shorts
Blackbird
Valentine
Unfriended

Query: A young couple with a kid look after a hotel during winter and the husband goes insane.
Results:
Ghostkeeper
Our Vines Have Tender Grapes
The Ref
Impact
The House in Marsh Road
我们可以看到，由于在搜索过程中截断了 Embeddings，因此召回率受到了影响。漏斗搜索通过一个巧妙的技巧解决了这一问题：我们可以利用剩余的嵌入维度对候选列表进行重新排序和修剪，从而恢复检索性能，而无需运行任何额外的昂贵向量搜索。
为了便于说明漏斗搜索算法，我们将每个查询的 Milvus 搜索命中率转换为 Pandas 数据帧。
def
hits_to_dataframe
(
hits: pymilvus.client.abstract.Hits
) -> pd.DataFrame:
"""
    Convert a Milvus search result to a Pandas dataframe. This function is specific to our data schema.

    """
rows = [x[
"entity"
]
for
x
in
hits]
    rows_dict = [
        {
"title"
: x[
"title"
],
"embedding"
: torch.tensor(x[
"embedding"
])}
for
x
in
rows
    ]
return
pd.DataFrame.from_records(rows_dict)


dfs = [hits_to_dataframe(hits)
for
hits
in
res]
现在，为了执行漏斗搜索，我们对嵌入的越来越大的子集进行迭代。在每次迭代中，我们都会根据新的相似度对候选项进行重新排序，并删除部分排序最低的候选项。
具体来说，在上一步中，我们使用 1/6 的嵌入维度和查询维度检索到 128 个候选项。执行漏斗搜索的第一步是使用
前 1/3 维度
重新计算查询和候选项之间的相似度。我们会剪切掉最下面的 64 个候选项。然后，我们使用
前 2/3 个维度
重复这一过程，然后使用
所有维度
，依次剪切到 32 个和 16 个候选
维度
。
# An optimized implementation would vectorize the calculation of similarity scores across rows (using a matrix)
def
calculate_score
(
row, query_emb=
None
, dims=
768
):
    emb = F.normalize(row[
"embedding"
][:dims], dim=-
1
)
return
(emb @ query_emb).item()
# You could also add a top-K parameter as a termination condition
def
funnel_search
(
df: pd.DataFrame, query_emb, scales=[
256
,
512
,
768
], prune_ratio=
0.5
) -> pd.DataFrame:
# Loop over increasing prefixes of the embeddings
for
dims
in
scales:
# Query vector must be normalized for each new dimensionality
emb = torch.tensor(query_emb[:dims] / np.linalg.norm(query_emb[:dims]))
# Score
scores = df.apply(
            functools.partial(calculate_score, query_emb=emb, dims=dims), axis=
1
)
        df[
"scores"
] = scores
# Re-rank
df = df.sort_values(by=
"scores"
, ascending=
False
)
# Prune (in our case, remove half of candidates at each step)
df = df.head(
int
(prune_ratio *
len
(df)))
return
df


dfs_results = [
    {
"query"
: query,
"results"
: funnel_search(df, query_emb)}
for
query, df, query_emb
in
zip
(queries, dfs, search_data)
]
for
d
in
dfs_results:
print
(d[
"query"
],
"\n"
, d[
"results"
][:
5
][
"title"
],
"\n"
)
An archaeologist searches for ancient artifacts while fighting Nazis. 
 0           "Pimpernel" Smith
1               Black Hunters
29    Raiders of the Lost Ark
34             The Master Key
51            My Gun Is Quick
Name: title, dtype: object 

A teenager fakes illness to get off school and have adventures with two friends. 
 21               How I Live Now
32     On the Edge of Innocence
77             Bratz: The Movie
4                    Unfriended
108                  Simon Says
Name: title, dtype: object 

A young couple with a kid look after a hotel during winter and the husband goes insane. 
 9         The Shining
0         Ghostkeeper
11     Fast and Loose
7      Killing Ground
12         Home Alone
Name: title, dtype: object
我们已经能够在不执行任何额外向量搜索的情况下恢复召回率！从质量上看，这些结果对 "夺宝奇兵 "和 "闪灵 "
的
召回率似乎高于教程 "
使用 Milvus 和 Sentence Transformers 进行电影搜索
"中的标准向量搜索，后者使用了不同的嵌入模型。然而，它却无法找到我们将在本手册稍后讨论的 "Ferris Bueller's Day Off"（《Ferris Bueller's Day Off》）。(有关更多定量实验和基准测试，请参阅论文
Matryoshka Representation Learning
）。
比较漏斗搜索和常规搜索
让我们比较一下我们的漏斗搜索和标准向量搜索
在相同数据集上使用相同嵌入模型
的结果。我们对全嵌入进行搜索。
# Search on entire embeddings
res = client.search(
    collection_name=collection_name,
    data=search_data,
    anns_field=
"embedding"
,
    limit=
5
,
    output_fields=[
"title"
,
"embedding"
],
)
for
query, hits
in
zip
(queries, res):
    rows = [x[
"entity"
]
for
x
in
hits]
print
(
"Query:"
, query)
print
(
"Results:"
)
for
row
in
rows:
print
(row[
"title"
].strip())
print
()
Query: An archaeologist searches for ancient artifacts while fighting Nazis.
Results:
"Pimpernel" Smith
Black Hunters
Raiders of the Lost Ark
The Master Key
My Gun Is Quick

Query: A teenager fakes illness to get off school and have adventures with two friends.
Results:
A Walk to Remember
Ferris Bueller's Day Off
How I Live Now
On the Edge of Innocence
Bratz: The Movie

Query: A young couple with a kid look after a hotel during winter and the husband goes insane.
Results:
The Shining
Ghostkeeper
Fast and Loose
Killing Ground
Home Alone
除了 "一名青少年为逃学而装病...... "的搜索结果外，漏斗搜索的结果与完全搜索的结果几乎完全相同，尽管漏斗搜索是在 128 维的搜索空间上进行的，而普通搜索是在 768 维的搜索空间上进行的。
调查《费里斯-布勒的一天》漏斗搜索召回失败的原因
为什么漏斗搜索没有成功检索到《费里斯-布勒的一天》？让我们来看看它是否在原始候选列表中，还是被错误地过滤掉了。
queries2 = [
"A teenager fakes illness to get off school and have adventures with two friends."
]
# Search the database based on input text
def
embed_search
(
data
):
    embeds = model.encode(data)
return
[x
for
x
in
embeds]


instruct_queries = [
"search_query: "
+ q.strip()
for
q
in
queries2]
search_data2 = embed_search(instruct_queries)
head_search2 = [x[:search_dim]
for
x
in
search_data2]
# Perform standard vector search on subset of embeddings
res = client.search(
    collection_name=collection_name,
    data=head_search2,
    anns_field=
"head_embedding"
,
    limit=
256
,
    output_fields=[
"title"
,
"head_embedding"
,
"embedding"
],
)
for
query, hits
in
zip
(queries, res):
    rows = [x[
"entity"
]
for
x
in
hits]
print
(
"Query:"
, queries2[
0
])
for
idx, row
in
enumerate
(rows):
if
row[
"title"
].strip() ==
"Ferris Bueller's Day Off"
:
print
(
f"Row
{idx}
: Ferris Bueller's Day Off"
)
Query: A teenager fakes illness to get off school and have adventures with two friends.
Row 228: Ferris Bueller's Day Off
我们发现，问题在于初始候选列表不够大，或者说，在最高粒度级别上，所需的点击与查询不够相似。把它从
128
改为
256
，结果检索成功。
我们应该形成一条经验法则，即通过经验评估召回率和延迟之间的权衡，来设定保留集上的候选项数量。
dfs = [hits_to_dataframe(hits)
for
hits
in
res]

dfs_results = [
    {
"query"
: query,
"results"
: funnel_search(df, query_emb)}
for
query, df, query_emb
in
zip
(queries2, dfs, search_data2)
]
for
d
in
dfs_results:
print
(d[
"query"
],
"\n"
, d[
"results"
][:
7
][
"title"
].to_string(index=
False
),
"\n"
)
A teenager fakes illness to get off school and have adventures with two friends. 
       A Walk to Remember
Ferris Bueller's Day Off
          How I Live Now
On the Edge of Innocence
        Bratz: The Movie
              Unfriended
              Simon Says
顺序重要吗？前缀与后缀嵌入。
经过训练，该模型能够很好地匹配递归较小的前缀嵌入。我们使用的维度顺序是否重要？例如，我们是否也可以提取后缀嵌入的子集？在本实验中，我们颠倒了 Matryoshka 嵌入中维度的顺序，并进行漏斗搜索。
client = MilvusClient(uri=
"./wikiplots-matryoshka-flipped.db"
)

fields = [
    FieldSchema(name=
"id"
, dtype=DataType.INT64, is_primary=
True
, auto_id=
True
),
    FieldSchema(name=
"title"
, dtype=DataType.VARCHAR, max_length=
256
),
    FieldSchema(name=
"head_embedding"
, dtype=DataType.FLOAT_VECTOR, dim=search_dim),
    FieldSchema(name=
"embedding"
, dtype=DataType.FLOAT_VECTOR, dim=embedding_dim),
]

schema = CollectionSchema(fields=fields, enable_dynamic_field=
False
)
client.create_collection(collection_name=collection_name, schema=schema)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"head_embedding"
, index_type=
"FLAT"
, metric_type=
"COSINE"
)
client.create_index(collection_name, index_params)
huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
To disable this warning, you can either:
    - Avoid using `tokenizers` before the fork if possible
    - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
for
batch
in
tqdm(ds.batch(batch_size=
512
)):
    plot_summary = [
"search_document: "
+ x.strip()
for
x
in
batch[
"PlotSummary"
]]
# Encode and flip embeddings
embeddings = model.encode(plot_summary, convert_to_tensor=
True
)
    embeddings = torch.flip(embeddings, dims=[-
1
])
    head_embeddings = embeddings[:, :search_dim]

    data = [
        {
"title"
: title,
"head_embedding"
: head.cpu().numpy(),
"embedding"
: embedding.cpu().numpy(),
        }
for
title, head, embedding
in
zip
(batch[
"Title"
], head_embeddings, embeddings)
    ]
    res = client.insert(collection_name=collection_name, data=data)
100%|██████████| 69/69 [05:50<00:00,  5.08s/it]
# Normalize head embeddings
flip_search_data = [
    torch.flip(torch.tensor(x), dims=[-
1
]).cpu().numpy()
for
x
in
search_data
]
flip_head_search = [x[:search_dim]
for
x
in
flip_search_data]
# Perform standard vector search on subset of embeddings
res = client.search(
    collection_name=collection_name,
    data=flip_head_search,
    anns_field=
"head_embedding"
,
    limit=
128
,
    output_fields=[
"title"
,
"head_embedding"
,
"embedding"
],
)
dfs = [hits_to_dataframe(hits)
for
hits
in
res]

dfs_results = [
    {
"query"
: query,
"results"
: funnel_search(df, query_emb)}
for
query, df, query_emb
in
zip
(queries, dfs, flip_search_data)
]
for
d
in
dfs_results:
print
(
        d[
"query"
],
"\n"
,
        d[
"results"
][:
7
][
"title"
].to_string(index=
False
, header=
False
),
"\n"
,
    )
An archaeologist searches for ancient artifacts while fighting Nazis. 
       "Pimpernel" Smith
          Black Hunters
Raiders of the Lost Ark
         The Master Key
        My Gun Is Quick
            The Passage
        The Mole People 

A teenager fakes illness to get off school and have adventures with two friends. 
                       A Walk to Remember
                          How I Live Now
                              Unfriended
Cirque du Freak: The Vampire's Assistant
                             Last Summer
                                 Contest
                                 Day One 

A young couple with a kid look after a hotel during winter and the husband goes insane. 
         Ghostkeeper
     Killing Ground
Leopard in the Snow
              Stone
          Afterglow
         Unfaithful
     Always a Bride
正如预期的那样，召回率比漏斗搜索或常规搜索要差得多（嵌入模型是通过对嵌入维度的前缀而非后缀进行对比学习来训练的）。
总结
下面是各种方法的搜索结果对比：
我们展示了如何使用 Matryoshka 嵌入和 Milvus 来执行一种更高效的语义搜索算法，即 "漏斗搜索"。我们还探讨了该算法的 Rerankers 和剪枝步骤的重要性，以及当初始候选列表太小时的失败模式。最后，我们讨论了在形成子嵌入时，维度的顺序是如何重要的--它必须与模型训练时的顺序一致。或者说，只有因为模型是以某种方式训练的，嵌入的前缀才有意义。现在你知道如何实现 Matryoshka 嵌入和漏斗搜索，以降低语义搜索的存储成本，同时又不会牺牲太多检索性能了吧！