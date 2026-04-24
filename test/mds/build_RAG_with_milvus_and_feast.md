使用 Milvus 和 Feast 构建 RAG
在本教程中，我们将使用
Feast
和
Milvus
构建一个检索增强生成（RAG）管道。Feast 是一个开源特征存储库，可简化机器学习的特征管理，为训练和实时推理提供高效的结构化数据存储和检索。Milvus 是一个高性能向量数据库，专为快速相似性搜索而设计，非常适合在 RAG 工作流中检索相关文档。
从本质上讲，我们将使用 Feast 将文档和结构化数据（即特征）注入到 LLM（大型语言模型）的上下文中，以 Milvus 作为在线向量数据库，为 RAG 应用程序（检索增强生成）提供动力。
为什么选择 Feast？
Feast 解决了这一流程中的几个常见问题：
在线检索：
在推理时，LLMs 经常需要访问并非现成可用的数据，需要从其他数据源进行预计算。
Feast 可以管理部署到各种在线存储（如 Milvus、DynamoDB、Redis、Google 云数据存储）的数据，并确保必要的特征在推理时始终
可用
，而且是
全新计算的
。
向量搜索：
Feast 已构建了对向量相似性搜索的支持，可通过声明方式轻松配置，因此用户可以专注于自己的应用。Milvus 提供强大而高效的向量相似性搜索功能。
更丰富的结构化数据：
在进行向量搜索的同时，用户还可以查询标准结构化字段，以注入 LLM 上下文，从而获得更好的用户体验。
特征/上下文和版本管理：
企业内的不同团队往往无法跨项目和服务重复使用数据，导致应用逻辑重复。模型具有数据依赖性，需要进行版本控制，例如在模型/提示版本上运行 A/B 测试时。
Feast 可以发现以前使用过的文档、功能并进行协作，还可以对数据集进行版本控制。
我们将
使用
Parquet 文件离线存储
和
Milvus 在线存储
部署本地功能存储。
将离线存储（Parquet 文件）中的数据（即特征值）写入/实体化到在线存储（Milvus）中。
使用带有 Milvus 向量搜索功能的 Feast SDK 服务于特征值
将文档注入到 LLM 的上下文中以回答问题
本教程基于
Feast Repository
中的官方 Milvus 集成指南。虽然我们努力保持本教程的更新，但如果您遇到任何差异，请参阅官方指南，并随时在我们的资源库中打开一个问题，以进行任何必要的更新。
准备工作
依赖关系
$
pip install
'feast[milvus]'
openai -U -q
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
我们将使用 OpenAI 作为 LLM 提供商。您可以登录其官方网站，并将
OPENAI_API_KEY
设置为环境变量。
import
os
from
openai
import
OpenAI

os.environ[
"OPENAI_API_KEY"
] =
"sk-**************"
llm_client = OpenAI(
    api_key=os.environ.get(
"OPENAI_API_KEY"
),
)
准备数据
我们将使用以下文件夹中的数据作为示例：
Feast RAG 功能库
下载数据后，您会发现以下文件：
feature_repo/
│── data/
# Contains pre-processed Wikipedia city data in Parquet format
│── example_repo.py
# Defines feature views and entities for the city data
│── feature_store.yaml
# Configures Milvus and feature store settings
│── test_workflow.py
# Example workflow for Feast operations
密钥配置文件
1. feature_store.yaml
该文件用于配置功能存储基础架构：
project:
rag
provider:
local
registry:
data/registry.db
online_store:
type:
milvus
# Uses Milvus for vector storage
path:
data/online_store.db
vector_enabled:
true
# Enables vector similarity search
embedding_dim:
384
# Dimension of our embeddings
index_type:
"FLAT"
# Vector index type
metric_type:
"COSINE"
# Similarity metric
offline_store:
type:
file
# Uses file-based offline storage
该配置建立了
Milvus 作为在线存储，用于快速向量检索
基于文件的离线存储，用于历史数据处理
利用 COSINE 相似性的向量搜索功能
2. example_repo.py
包含城市数据的特征定义，包括
城市实体定义
城市信息和 Embeddings 的特征视图
向量数据库的 Schema 规范
3.数据目录
包含经过预处理的维基百科城市数据，包括
城市描述和摘要
预先计算的 Embeddings（384 维向量）
城市名称和州等相关元数据
这些文件共同创建了一个特征库，将 Milvus 的向量搜索功能与 Feast 的特征管理相结合，从而为我们的 RAG 应用程序高效检索相关城市信息。
检查数据
本演示中的原始特征数据存储在本地 parquet 文件中。该数据集是不同城市的维基百科摘要。让我们先检查数据。
import
pandas
as
pd

df = pd.read_parquet(
"/path/to/feature_repo/data/city_wikipedia_summaries_with_embeddings.parquet"
)
df[
"vector"
] = df[
"vector"
].apply(
lambda
x: x.tolist())
embedding_length =
len
(df[
"vector"
][
0
])
print
(
f"embedding length =
{embedding_length}
"
)
embedding length = 384
from
IPython.display
import
display

display(df.head())
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
id
item_id
事件时间戳
状态
维基摘要
句子块
向量
0
0
0
2025-01-09 13:36:59.280589
纽约，纽约
纽约，通常被称为纽约市或简称...
纽约，通常被称为纽约市或简称...
[0.1465730518102646, -0.07317650318145752, 0.0...
1
1
1
2025-01-09 13:36:59.280589
纽约，纽约州
纽约，通常称为纽约市或简称 "纽约"。
这座城市由五个行政区组成，每个行政区都有自己的...
[0.05218901485204697, -0.08449874818325043, 0....
2
2
2
2025-01-09 13:36:59.280589
纽约，纽约州
纽约，通常被称为 "纽约市 "或 "纽约"。
纽约是全球金融和商业中心，也是世界上最大的金融中心。
[0.06769222766160965, -0.07371102273464203, -0...
3
3
3
2025-01-09 13:36:59.280589
纽约，纽约州
纽约，通常被称为纽约市或简称...
纽约市是世界上最繁华的城市之一。
[0.12095861881971359, -0.04279915615916252, 0....
4
4
4
2025-01-09 13:36:59.280589
纽约，纽约州
纽约，通常被称为纽约市或简称...
2022 年的人口估计为 8,335...
[0.17943550646305084, -0.09458263963460922, 0....
注册功能定义并部署功能商店
下载
feature_repo
后，我们需要运行
feast apply
来注册
example_repo.py
中定义的功能视图和实体，并将
Milvus
设置为在线商店表。
在运行该命令前，请确保已 nagivated 到
feature_repo
目录。
feast apply
将特征载入 Milvus
现在，我们将特征载入 Milvus。这一步涉及将离线存储中的特征值序列化并写入 Milvus。
from
datetime
import
datetime
from
feast
import
FeatureStore
import
warnings

warnings.filterwarnings(
"ignore"
)

store = FeatureStore(repo_path=
"/path/to/feature_repo"
)
store.write_to_online_store(feature_view_name=
"city_embeddings"
, df=df)
Connecting to Milvus in local mode using /Users/jinhonglin/Desktop/feature_repo/data/online_store.db
请注意，现在有
online_store.db
和
registry.db
，分别存储物化特征和 Schema 信息。我们可以看看
online_store.db
文件。
pymilvus_client = store._provider._online_store._connect(store.config)
COLLECTION_NAME = pymilvus_client.list_collections()[
0
]

milvus_query_result = pymilvus_client.query(
    collection_name=COLLECTION_NAME,
filter
=
"item_id == '0'"
,
)
pd.DataFrame(milvus_query_result[
0
]).head()
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
item_id_pk
created_ts
event_ts
item_id
句子块
状态
向量
维基摘要
0
0100000002000000070000006974656d5f696404000000...
0
1736447819280589
0
纽约，通常被称为纽约市或简称...
纽约州纽约市
0.146573
纽约，常被称为纽约市或简称...
1
0100000002000000070000006974656d5f696404000000...
0
1736447819280589
0
纽约，通常被称为纽约市或简称...
纽约州纽约市
-0.073177
纽约，通常被称为纽约市或简称...
2
0100000002000000070000006974656d5f696404000000...
0
1736447819280589
0
纽约，通常被称为纽约市或简称...
纽约州纽约市
0.052114
纽约，通常被称为纽约市或简称...
3
0100000002000000070000006974656d5f696404000000...
0
1736447819280589
0
纽约，通常称为纽约市或简称...
纽约州纽约市
0.033187
纽约，通常被称为纽约市或简称...
4
0100000002000000070000006974656d5f696404000000...
0
1736447819280589
0
纽约，通常称为纽约市或简称...
纽约, 纽约州
0.012013
纽约，通常被称为纽约市或简称...
构建 RAG
1.使用 PyTorch 和句子变换器嵌入查询
在推理过程中（例如，在用户提交聊天信息时），我们需要嵌入输入文本。这可以看作是输入数据的特征变换。在本例中，我们将使用来自 Hugging Face 的小型 Sentence Transformer 来实现这一功能。
import
torch
import
torch.nn.functional
as
F
from
feast
import
FeatureStore
from
pymilvus
import
MilvusClient, DataType, FieldSchema
from
transformers
import
AutoTokenizer, AutoModel
from
example_repo
import
city_embeddings_feature_view, item

TOKENIZER =
"sentence-transformers/all-MiniLM-L6-v2"
MODEL =
"sentence-transformers/all-MiniLM-L6-v2"
def
mean_pooling
(
model_output, attention_mask
):
    token_embeddings = model_output[
0
]
# First element of model_output contains all token embeddings
input_mask_expanded = (
        attention_mask.unsqueeze(-
1
).expand(token_embeddings.size()).
float
()
    )
return
torch.
sum
(token_embeddings * input_mask_expanded,
1
) / torch.clamp(
        input_mask_expanded.
sum
(
1
),
min
=
1e-9
)
def
run_model
(
sentences, tokenizer, model
):
    encoded_input = tokenizer(
        sentences, padding=
True
, truncation=
True
, return_tensors=
"pt"
)
# Compute token embeddings
with
torch.no_grad():
        model_output = model(**encoded_input)

    sentence_embeddings = mean_pooling(model_output, encoded_input[
"attention_mask"
])
    sentence_embeddings = F.normalize(sentence_embeddings, p=
2
, dim=
1
)
return
sentence_embeddings
2.获取实时向量和数据进行在线推理
将查询转化为 Embeddings 后，下一步就是从向量存储中检索相关文档。在推理时，我们利用向量相似性搜索，找到在线特征存储中存储的最相关的文档嵌入，使用
retrieve_online_documents_v2()
。然后，这些特征向量就可以输入到 LLM 的上下文中。
question =
"Which city has the largest population in New York?"
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER)
model = AutoModel.from_pretrained(MODEL)
query_embedding = run_model(question, tokenizer, model)
query = query_embedding.detach().cpu().numpy().tolist()[
0
]
from
IPython.display
import
display
# Retrieve top k documents
context_data = store.retrieve_online_documents_v2(
    features=[
"city_embeddings:vector"
,
"city_embeddings:item_id"
,
"city_embeddings:state"
,
"city_embeddings:sentence_chunks"
,
"city_embeddings:wiki_summary"
,
    ],
    query=query,
    top_k=
3
,
    distance_metric=
"COSINE"
,
).to_df()
display(context_data)
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
向量
item_id
状态
句子块
维基摘要
距离
0
[0.15548758208751678, -0.08017724752426147, -0...
0
纽约州纽约市
纽约，通常被称为纽约市或简称...
纽约，通常被称为纽约市或简称...
0.743023
1
[0.15548758208751678, -0.08017724752426147, -0...
6
纽约州纽约市
纽约是美国的地理和人口中心。
纽约，通常被称为纽约市或简称 "纽约"。
0.739733
2
[0.15548758208751678, -0.08017724752426147, -0...
7
纽约州纽约市
纽约市拥有超过 2,010 万人口。
纽约，通常被称为 "纽约市 "或简称 "纽约"。
0.728218
3.根据 RAG 上下文对检索到的文档进行格式化
检索相关文档后，我们需要将数据格式化为结构化上下文，以便在下游应用程序中有效使用。这一步骤可确保提取的信息干净、有序，并可随时整合到 RAG 管道中。
def
format_documents
(
context_df
):
    output_context =
""
unique_documents = context_df.drop_duplicates().apply(
lambda
x:
"City & State = {"
+ x[
"state"
]
        +
"}\nSummary = {"
+ x[
"wiki_summary"
].strip()
        +
"}"
,
        axis=
1
,
    )
for
i, document_text
in
enumerate
(unique_documents):
        output_context +=
f"****START DOCUMENT
{i}
****\n
{document_text.strip()}
\n****END DOCUMENT
{i}
****"
return
output_context


RAG_CONTEXT = format_documents(context_data[[
"state"
,
"wiki_summary"
]])
print
(RAG_CONTEXT)
****START DOCUMENT 0****
City & State = {New York, New York}
Summary = {New York, often called New York City or simply NYC, is the most populous city in the United States, located at the southern tip of New York State on one of the world's largest natural harbors. The city comprises five boroughs, each of which is coextensive with a respective county. New York is a global center of finance and commerce, culture and technology, entertainment and media, academics and scientific output, and the arts and fashion, and, as home to the headquarters of the United Nations, is an important center for international diplomacy. New York City is the epicenter of the world's principal metropolitan economy.
With an estimated population in 2022 of 8,335,897 distributed over 300.46 square miles (778.2 km2), the city is the most densely populated major city in the United States. New York has more than double the population of Los Angeles, the nation's second-most populous city. New York is the geographical and demographic center of both the Northeast megalopolis and the New York metropolitan area, the largest metropolitan area in the U.S. by both population and urban area. With more than 20.1 million people in its metropolitan statistical area and 23.5 million in its combined statistical area as of 2020, New York City is one of the world's most populous megacities. The city and its metropolitan area are the premier gateway for legal immigration to the United States. As many as 800 languages are spoken in New York, making it the most linguistically diverse city in the world. In 2021, the city was home to nearly 3.1 million residents born outside the U.S., the largest foreign-born population of any city in the world.
New York City traces its origins to Fort Amsterdam and a trading post founded on the southern tip of Manhattan Island by Dutch colonists in approximately 1624. The settlement was named New Amsterdam (Dutch: Nieuw Amsterdam) in 1626 and was chartered as a city in 1653. The city came under English control in 1664 and was temporarily renamed New York after King Charles II granted the lands to his brother, the Duke of York. before being permanently renamed New York in November 1674. New York City was the capital of the United States from 1785 until 1790. The modern city was formed by the 1898 consolidation of its five boroughs: Manhattan, Brooklyn, Queens, The Bronx, and Staten Island, and has been the largest U.S. city ever since.
Anchored by Wall Street in the Financial District of Lower Manhattan, New York City has been called both the world's premier financial and fintech center and the most economically powerful city in the world. As of 2022, the New York metropolitan area is the largest metropolitan economy in the world with a gross metropolitan product of over US$2.16 trillion. If the New York metropolitan area were its own country, it would have the tenth-largest economy in the world. The city is home to the world's two largest stock exchanges by market capitalization of their listed companies: the New York Stock Exchange and Nasdaq. New York City is an established safe haven for global investors. As of 2023, New York City is the most expensive city in the world for expatriates to live. New York City is home to the highest number of billionaires, individuals of ultra-high net worth (greater than US$30 million), and millionaires of any city in the world.}
****END DOCUMENT 0****
4.使用提取的上下文生成响应
现在，我们已经对检索到的文档进行了格式化，可以将它们整合到一个结构化的提示中，以便生成回复。这一步可以确保助手只依赖检索到的信息，避免产生幻觉。
FULL_PROMPT =
f"""
You are an assistant for answering questions about states. You will be provided documentation from Wikipedia. Provide a conversational answer.
If you don't know the answer, just say "I do not know." Don't make up an answer.

Here are document(s) you should use when answer the users question:
{RAG_CONTEXT}
"""
response = llm_client.chat.completions.create(
    model=
"gpt-4o-mini"
,
    messages=[
        {
"role"
:
"system"
,
"content"
: FULL_PROMPT},
        {
"role"
:
"user"
,
"content"
: question},
    ],
)
print
(
"\n"
.join([c.message.content
for
c
in
response.choices]))
The city with the largest population in New York is New York City itself, often referred to as NYC. It is the most populous city in the United States, with an estimated population of about 8.3 million in 2022.