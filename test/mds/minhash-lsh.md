MINHASH_LSH
高效的重复数据删除和相似性搜索对于大规模机器学习数据集来说至关重要，尤其是在为大型语言模型（LLMs）清理训练语料库等任务中。在处理数百万或数十亿文档时，传统的精确匹配会变得过于缓慢和昂贵。
Milvus 中的
MINHASH_LSH
索引通过结合两种强大的技术，实现了快速、可扩展和精确的近似重复数据删除：
MinHash
快速生成紧凑的签名（或 "指纹"），以估计文档的相似性。
位置敏感散列（LSH）
：根据 MinHash 签名快速查找相似文档组。
本指南将引导您了解在 Milvus 中使用 MINHASH_LSH 的概念、前提条件、设置和最佳实践。
概述
杰卡德相似性
Jaccard 相似性度量两个集合 A 和 B 之间的重叠程度，正式定义如下：
J
(
A
,
B
)
=
∣
A
∩
B
∣
∣
A
∪
B
∣
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
J
(
A
,
B
)
=
∣
A
∪
B
∣
∣
A
∩
B
∣
其中，其值范围从 0（完全不相交）到 1（完全相同）。
然而，在大规模数据集中精确计算所有文档对之间的 Jaccard 相似性，当
n
较大时，在时间和内存方面的计算成本都很高-O
(n²)
。这使得它在诸如 LLM 训练语料清理或网络规模文档分析等用例中不可行。
MinHash 签名近似雅卡德相似性
MinHash
是一种概率技术，它提供了一种估算 Jaccard 相似性的有效方法。它的工作原理是将每个集合转化为一个紧凑的
签名向量
，保留足够的信息来有效地近似集合相似性。
其核心思想
是
两个集合越相似，它们的 MinHash 签名就越有可能匹配到相同的位置。这一特性使 MinHash 可以近似地计算集合间的 Jaccard 相似度。
这一特性使 MinHash 可以
近似
地计算集合间的
Jaccard 相似度
，而无需直接比较完整的集合。
MinHash 处理过程包括
分层
：将文档转换为重叠标记序列集（分片）
散列
： 对每个散列应用多个独立的散列函数
最小选择
：对于每个散列函数，记录所有散列的
最小
散列值
整个流程如下图所示：
最小散列工作流程
使用的哈希函数数量决定了 MinHash 签名的维度。维数越高，近似精度越高，但存储和计算量也会随之增加。
用于 MinHash 的 LSH
虽然 MinHash 签名大大降低了计算文档间精确 Jaccard 相似性的成本，但穷举比较每一对签名向量在规模上仍然是低效的。
为了解决这个问题，我们使用了
LSH
。LSH 通过确保相似项目以高概率散列到同一个 "桶 "中，从而实现快速的近似相似性搜索--避免了直接比较每一对的需要。
这一过程包括
签名分割：
一个
n 维
MinHash 签名被分为
b 个
带。每个段包含
r 个
连续的哈希值，因此总签名长度满足：
n = b × r
。
例如，如果有一个 128 维的 MinHash 签名
(n = 128
)，并将其分为 32 个段
(b = 32
)，那么每个段包含 4 个哈希值
(r = 4
)。
带级散列：
分割后，使用标准哈希函数对每个带进行独立处理，将其分配到一个桶中。如果两个签名在一个带内产生了相同的哈希值，即它们属于同一个桶，那么它们就被认为是潜在的匹配对象。
候选选择：
在至少一个频段内发生碰撞的配对会被选为相似性候选。
为什么会成功？
从数学上讲，如果两个签名的 Jaccard 相似度为
s
、
它们在某一行（哈希位置）相同的概率为
ss
s
它们在一个条带的所有
rr
r 行中匹配的概率是
srs^r
s
r
它们在
至少一个带中
匹配的概率是
1-
(
1-sr
)
b1
- (1 - s^r)^b
1
-
(1
-
s
r
)
b
详情请参阅
位置敏感散列
。
考虑三个具有 128 维 MinHash 签名的文档：
Lsh 工作流程 1
首先，LSH 将 128 维签名分为 32 个带，每个带有 4 个连续值：
Lsh 工作流程 2
然后，使用哈希函数将每个带散列到不同的桶中。共享散列的文档对被选为相似性候选文档。在下面的示例中，文档 A 和文档 B 被选为相似性候选对象，因为它们的哈希结果在
带 0
中相撞：
Lsh 工作流程 3
带的数量由
mh_lsh_band
参数控制。更多信息，请参阅
索引构建参数
。
MHJACCARD：比较 MinHash 签名
MinHash 签名使用固定长度的二进制向量近似于集合间的 Jaccard 相似性。但是，由于这些签名不保留原始集合，因此无法直接应用
JACCARD
、
L2
或
COSINE
等标准度量来比较它们。
为了解决这个问题，Milvus 引入了一种专门的度量类型，称为
MHJACCARD
，专为比较 MinHash 签名而设计。
在 Milvus 中使用 MinHash 时：
向量场的类型必须是
BINARY_VECTOR
index_type
必须是
MINHASH_LSH
（或
BIN_FLAT
)
metric_type
必须设置为
MHJACCARD
使用其他度量类型要么无效，要么产生不正确的结果。
有关此度量类型的更多信息，请参阅
MHJACCARD
。
重复数据删除工作流程
由 MinHash LSH 支持的重复数据删除流程允许 Milvus 在将近乎重复的文本或结构化记录插入 Collections 之前，高效地识别并过滤掉它们。
分块和预处理
：将传入的文本数据或结构化数据（如记录、字段）分割成块；对文本进行规范化处理（小写、去除标点符号），并根据需要删除停止词。
构建特征
：构建 MinHash 所用的标记集（例如，从文本中提取小块；对结构化数据进行字段标记串联）。
MinHash 签名生成
：为每个数据块或记录计算 MinHash 签名。
二进制向量转换
：将签名转换为与 Milvus 兼容的二进制向量。
插入前搜索
使用 MinHash LSH 索引在目标 Collections 中搜索输入项的近似重复项。
插入并存储
：只将唯一项目插入 Collections。这些项目在未来的删除检查中将成为可搜索项目。
前提条件
在 Milvus 中使用 MinHash LSH 之前，必须先生成
MinHash 签名
。这些紧凑的二进制签名近似于集合之间的 Jaccard 相似性，是在 Milvus 中进行基于
MHJACCARD
的搜索所必需的。
选择生成 MinHash 签名的方法
根据您的工作量，您可以选择
使用 Python 的
datasketch
以简化（建议用于原型开发）
使用分布式工具（如 Spark、Ray）处理大规模数据集
如果性能调整非常重要，则执行自定义逻辑（NumPy、C++ 等）。
在本指南中，我们使用
datasketch
，以简化并兼容 Milvus 输入格式。
安装所需的库
安装本示例所需的软件包：
pip install pymilvus datasketch numpy
生成 MinHash 签名
我们将生成 256 维 MinHash 签名，每个哈希值表示为 64 位整数。这与
MINHASH_LSH
的预期向量格式一致。
from
datasketch
import
MinHash
import
numpy
as
np

MINHASH_DIM =
256
HASH_BIT_WIDTH =
64
def
generate_minhash_signature
(
text, num_perm=MINHASH_DIM
) ->
bytes
:
    m = MinHash(num_perm=num_perm)
for
token
in
text.lower().split():
        m.update(token.encode(
"utf8"
))
return
m.hashvalues.astype(
'>u8'
).tobytes()
# Returns 2048 bytes
每个签名为 256 × 64 位 = 2048 字节。该字节字符串可直接插入
BINARY_VECTOR
字段。有关 Milvus 中使用的二进制向量的更多信息，请参阅
二进制向量
。
(可选）准备原始标记集（用于精细搜索）
默认情况下，Milvus 只使用 MinHash 签名和 LSH 索引来查找近似邻域。这种方法速度很快，但可能会返回误报或错过近似匹配。
如果您想要
精确的 Jaccard 相似性
，Milvus 支持使用原始标记集的精炼搜索。启用方法如下
将标记集存储为单独的
VARCHAR
字段
在
建立索引参数
时设置
"with_raw_data": True
并在
执行相似性搜索
时启用
"mh_search_with_jaccard": True
令牌集提取示例
：
def
extract_token_set
(
text:
str
) ->
str
:
    tokens =
set
(text.lower().split())
return
" "
.join(tokens)
使用 MinHash LSH
一旦你的 MinHash 向量和原始令牌集准备就绪，你就可以使用
MINHASH_LSH
使用 Milvus 对它们进行存储、索引和搜索。
连接到集群
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
)
# Update if your URI is different
// java
// nodejs
// go
# restful
定义 Collections 模式
用 Schema 定义模式：
主键
用于 MinHash 签名的
BINARY_VECTOR
字段
原始标记集的
VARCHAR
字段（如果启用了精炼搜索）
原始文本的
document
字段（可选
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
DataType

VECTOR_DIM = MINHASH_DIM * HASH_BIT_WIDTH
# 256 × 64 = 8192 bits
schema = client.create_schema(auto_id=
False
, enable_dynamic_field=
False
)
schema.add_field(
"doc_id"
, DataType.INT64, is_primary=
True
)
schema.add_field(
"minhash_signature"
, DataType.BINARY_VECTOR, dim=VECTOR_DIM)
schema.add_field(
"token_set"
, DataType.VARCHAR, max_length=
1000
)
# required for refinement
schema.add_field(
"document"
, DataType.VARCHAR, max_length=
1000
)
// java
// nodejs
// go
# restful
建立索引参数并创建 Collections
构建
MINHASH_LSH
索引并启用 Jaccard 精细化：
Python
Java
NodeJS
Go
cURL
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"minhash_signature"
,
    index_type=
"MINHASH_LSH"
,
    metric_type=
"MHJACCARD"
,
    params={
"mh_element_bit_width"
: HASH_BIT_WIDTH,
# Must match signature bit width
"mh_lsh_band"
:
16
,
# Band count (128/16 = 8 hashes per band)
"with_raw_data"
:
True
# Required for Jaccard refinement
}
)

client.create_collection(
"minhash_demo"
, schema=schema, index_params=index_params)
// java
// nodejs
// go
# restful
有关索引构建参数的更多信息，请参阅
索引构建参数
。
插入数据
为每个文档准备
二进制 MinHash 签名
序列化标记集字符串
(可选）原始文本
Python
Java
NodeJS
Go
cURL
documents = [
"machine learning algorithms process data automatically"
,
"deep learning uses neural networks to model patterns"
]

insert_data = []
for
i, doc
in
enumerate
(documents):
    sig = generate_minhash_signature(doc)
    token_str = extract_token_set(doc)
    insert_data.append({
"doc_id"
: i,
"minhash_signature"
: sig,
"token_set"
: token_str,
"document"
: doc
    })

client.insert(
"minhash_demo"
, insert_data)
client.flush(
"minhash_demo"
)
// java
// nodejs
// go
# restful
执行相似性搜索
Milvus 支持两种使用 MinHash LSH 的相似性搜索模式：
近似搜索
- 仅使用 MinHash 签名和 LSH 来获得快速但概率性的结果。
精细搜索
- 使用原始标记集重新计算 Jaccard 相似性，以提高准确性。
5.1 准备查询
要执行相似性搜索，请为查询文档生成 MinHash 签名。该签名必须与数据插入时使用的维度和编码格式一致。
Python
Java
NodeJS
Go
cURL
query_text =
"neural networks model patterns in data"
query_sig = generate_minhash_signature(query_text)
// java
// nodejs
// go
# restful
5.2 近似搜索（仅限 LSH）
这种方法速度快、可扩展，但可能会错过近似匹配或包含误报：
Python
Java
NodeJS
Go
cURL
search_params={
"metric_type"
:
"MHJACCARD"
,
"params"
: {}
}
approx_results = client.search(
    collection_name=
"minhash_demo"
,
    data=[query_sig],
    anns_field=
"minhash_signature"
,
search_params=search_params,
limit=
3
,
    output_fields=[
"doc_id"
,
"document"
],
    consistency_level=
"Strong"
)
for
i, hit
in
enumerate
(approx_results[
0
]):
    sim =
1
- hit[
'distance'
]
print
(
f"
{i+
1
}
. Similarity:
{sim:
.3
f}
|
{hit[
'entity'
][
'document'
]}
"
)
// java
// nodejs
// go
# restful
5.3 精细搜索（推荐用于提高准确性）：
这可以使用存储在 Milvus 中的原始标记集进行精确的 Jaccard 比较。速度稍慢，但推荐用于质量敏感型任务：
Python
Java
NodeJS
Go
cURL
search_params = {
"metric_type"
:
"MHJACCARD"
,
"params"
: {
"mh_search_with_jaccard"
:
True
,
# Enable real Jaccard computation
"refine_k"
:
5
# Refine top 5 candidates
}
}
refined_results = client.search(
    collection_name=
"minhash_demo"
,
    data=[query_sig],
    anns_field=
"minhash_signature"
,
search_params=search_params,
limit=
3
,
    output_fields=[
"doc_id"
,
"document"
],
    consistency_level=
"Strong"
)
for
i, hit
in
enumerate
(refined_results[
0
]):
    sim =
1
- hit[
'distance'
]
print
(
f"
{i+
1
}
. Similarity:
{sim:
.3
f}
|
{hit[
'entity'
][
'document'
]}
"
)
// java
// nodejs
// go
# restful
索引参数
本节概述了用于建立索引和在索引上执行搜索的参数。
索引构建参数
下表列出了
建立索引
时可在
params
中配置的参数。
参数
说明
值范围
调整建议
mh_element_bit_width
MinHash 签名中每个哈希值的位宽。必须能被 8 整除。
8, 16, 32, 64
使用
32
以平衡性能和精度。使用
64
可在数据集较大时获得更高精度。使用
16
可节省内存，但精度损失可接受。
mh_lsh_band
LSH MinHash 签名的分段数。控制召回率与性能的权衡。
[1，
签名长度］
对于 128 段签名：从 32 段（4 个值/段）开始。增加到 64 段可提高召回率，减少到 16 段可提高性能。必须平均分配签名长度。
mh_lsh_code_in_mem
是否将 LSH 哈希代码存储在匿名内存中 (
true
) 或使用内存映射 (
false
)。
真，假
对于大型数据集（>100 万集），使用
false
，以减少内存使用量。对于需要最大搜索速度的较小数据集，使用
true
。
with_raw_data
是否将原始 MinHash 签名与 LSH 代码一起存储，以便完善。
真, 假
需要高精度且存储成本可接受时，使用
true
。使用
false
可在略微降低精确度的情况下最大限度地减少存储开销。
mh_lsh_bloom_false_positive_prob
用于 LSH 代码桶优化的 Bloom 过滤器的误报概率。
[0.001, 0.1]
使用
0.01
以平衡内存使用和准确性。较低的值 (
0.001
) 会减少误报，但会增加内存。较高值 (
0.05
) 可节省内存，但可能会降低精确度。
特定于索引的搜索参数
下表列出了
在索引上搜索
时可在
search_params.params
中配置的参数。
参数
说明
值范围
调整建议
mh_search_with_jaccard
是否对候选结果执行精确的 Jaccard 相似性计算以进行细化。
true, false
对于精度要求较高的应用（如重复数据删除），请使用
true
。在可以接受轻微精度损失的情况下，使用
false
进行更快的近似搜索。
refine_k
Jaccard 精炼前检索的候选结果数量。仅当
mh_search_with_jaccard
是
true
时有效。
[top_k
,*top_k*10*]。
设置为所需
top_k
的 2-5 倍，以实现召回率与性能之间的良好平衡。数值越大，召回率越高，但计算成本也会增加。
mh_lsh_batch_search
是否为多个同时查询启用批量优化。
真, 假
同时搜索多个查询时使用
true
，以提高吞吐量。单次查询时使用
false
，以减少内存开销。