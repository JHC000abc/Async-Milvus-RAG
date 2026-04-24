使用 Milvus + PII 屏蔽器构建 RAG
PII（个人身份信息）是一种可用于识别个人身份的敏感数据。
由
HydroX AI
开发的
PII Masker
是一款先进的开源工具，旨在利用尖端的人工智能模型保护您的敏感数据。无论您是在处理客户数据、执行数据分析，还是在确保遵守隐私法规，PII Masker 都能提供强大、可扩展的解决方案，确保您的信息安全。
在本教程中，我们将展示如何将 PII Masker 与 Milvus 结合使用，以保护 RAG（检索-增强生成）应用中的隐私数据。通过将 PII Masker 的数据屏蔽功能与 Milvus 的高效数据检索功能相结合，您可以创建安全、符合隐私标准的管道，放心地处理敏感信息。这种方法可确保您的应用程序符合隐私标准，并有效保护用户数据。
准备工作
开始使用 PII Masker
按照 PII Masker 的
安装指南
安装所需的依赖项并下载模型。下面是一个简单的指南：
$
git
clone
https://github.com/HydroXai/pii-masker-v1.git
$
cd
pii-masker-v1/pii-masker
从
https://huggingface.co/hydroxai/pii_model_weight
下载模型，并用其中的文件替换：
pii-masker/output_model/deberta3base_1024/
依赖项和环境
$
pip install --upgrade pymilvus openai requests tqdm dataset
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
作为环境变量。
$
export
OPENAI_API_KEY=sk-***********
然后创建一个 python 或 jupyter 笔记本来运行以下代码。
准备数据
让我们生成一些包含 PII 信息的假数据行，用于测试或演示。
text_lines = [
"Alice Johnson, a resident of Dublin, Ireland, attended a flower festival at Hyde Park on May 15, 2023. She entered the park at noon using her digital passport, number 23456789. Alice spent the afternoon admiring various flowers and plants, attending a gardening workshop, and having a light snack at one of the food stalls. While there, she met another visitor, Mr. Thompson, who was visiting from London. They exchanged tips on gardening and shared contact information: Mr. Thompson's address was 492, Pine Lane, and his cell phone number was +018.221.431-4517. Alice gave her contact details: home address, Ranch 16"
,
"Hiroshi Tanaka, a businessman from Tokyo, Japan, went to attend a tech expo at the Berlin Convention Center on November 10, 2023. He registered for the event at 9 AM using his digital passport, number Q-24567680. Hiroshi networked with industry professionals, participated in panel discussions, and had lunch with some potential partners. One of the partners he met was from Munich, and they decided to keep in touch: the partner's office address was given as house No. 12, Road 7, Block E. Hiroshi offered his business card with the address, 654 Sakura Road, Tokyo."
,
"In an online forum discussion about culinary exchanges around the world, several participants shared their experiences. One user, Male, with the email 2022johndoe@example.com, shared his insights. He mentioned his ID code 1A2B3C4D5E and reference number L87654321 while residing in Italy but originally from Australia. He provided his +0-777-123-4567 and described his address at 456, Flavorful Lane, Pasta, IT, 00100."
,
"Another user joined the conversation on the topic of international volunteering opportunities. Identified as Female, she used the email 2023janedoe@example.com to share her story. She noted her 9876543210123 and M1234567890123 while residing in Germany but originally from Brazil. She provided her +0-333-987-6543 and described her address at 789, Sunny Side Street, Berlin, DE, 10178."
,
]
使用 PIIMasker 屏蔽数据
初始化 PIIMasker 对象并加载模型。
from
model
import
PIIMasker

masker = PIIMasker()
然后从文本行列表中屏蔽 PII，并打印屏蔽后的结果。
masked_results = []
for
full_text
in
text_lines:
    masked_text, _ = masker.mask_pii(full_text)
    masked_results.append(masked_text)
for
res
in
masked_results:
print
(res +
"\n"
)
Alice [B-NAME] , a resident of Dublin Ireland attended flower festival at Hyde Park on May 15 2023 [B-PHONE_NUM] She entered the park noon using her digital passport number 23 [B-ID_NUM] [B-NAME] afternoon admiring various flowers and plants attending gardening workshop having light snack one food stalls While there she met another visitor Mr Thompson who was visiting from London They exchanged tips shared contact information : ' s address 492 [I-STREET_ADDRESS] his cell phone + [B-PHONE_NUM] [B-NAME] details home Ranch [B-STREET_ADDRESS]

Hiroshi [B-NAME] [I-STREET_ADDRESS] a businessman from Tokyo Japan went to attend tech expo at the Berlin Convention Center on November 10 2023 . He registered for event 9 AM using his digital passport number Q [B-ID_NUM] [B-NAME] with industry professionals participated in panel discussions and had lunch some potential partners One of he met was Munich they decided keep touch : partner ' s office address given as house No [I-STREET_ADDRESS] [B-NAME] business card 654 [B-STREET_ADDRESS]

In an online forum discussion about culinary exchanges around the world [I-STREET_ADDRESS] several participants shared their experiences [I-STREET_ADDRESS] One user Male with email 2022 [B-EMAIL] his insights He mentioned ID code 1 [B-ID_NUM] [I-PHONE_NUM] reference number L [B-ID_NUM] residing in Italy but originally from Australia provided + [B-PHONE_NUM] [I-PHONE_NUM] described address at 456 [I-STREET_ADDRESS]

Another user joined the conversation on topic of international volunteering opportunities . Identified as Female , she used email 2023 [B-EMAIL] share her story She noted 98 [B-ID_NUM] [I-PHONE_NUM] M [B-ID_NUM] residing in Germany but originally from Brazil provided + [B-PHONE_NUM] [I-PHONE_NUM] described address at 789 [I-STREET_ADDRESS] DE 10 178
准备 Embeddings 模型
我们初始化 OpenAI 客户端，准备嵌入模型。
from
openai
import
OpenAI

openai_client = OpenAI()
定义一个函数，使用 OpenAI 客户端生成文本嵌入。我们以
text-embedding-3-small
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
"text-embedding-3-small"
)
        .data[
0
]
        .embedding
    )
生成一个测试嵌入，并打印其维度和前几个元素。
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
1536
[0.009889289736747742, -0.005578675772994757, 0.00683477520942688, -0.03805781528353691, -0.01824733428657055, -0.04121600463986397, -0.007636285852640867, 0.03225184231996536, 0.018949154764413834, 9.352207416668534e-05]
将数据载入 Milvus
创建 Collections
from
pymilvus
import
MilvusClient

milvus_client = MilvusClient(uri=
"./milvus_demo.db"
)
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
如果你有大规模数据，比如超过一百万个向量，你可以在
Docker 或 Kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器地址和端口作为 uri，例如
http://localhost:19530
。如果在 Milvus 上启用了身份验证功能，请使用 "
:
" 作为令牌，否则不要设置令牌。
如果您想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
检查 Collections 是否已存在，如果已存在，则删除它。
collection_name =
"my_rag_collection"
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
遍历屏蔽文本行，创建 Embeddings，然后将数据插入 Milvus。
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
(tqdm(masked_results, desc=
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
Creating embeddings: 100%|██████████| 4/4 [00:01<00:00,  2.60it/s]





{'insert_count': 4, 'ids': [0, 1, 2, 3], 'cost': 0}
构建 RAG
为查询检索数据
让我们指定一个关于文档的问题。
question =
"What was the office address of Hiroshi's partner from Munich?"
在 Collections 中搜索该问题并检索语义 top-1 匹配。
search_res = milvus_client.search(
    collection_name=collection_name,
    data=[
        emb_text(question)
    ],
# Use the `emb_text` function to convert the question to an embedding vector
limit=
1
,
# Return top 1 results
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
        "Hiroshi [B-NAME] [I-STREET_ADDRESS] a businessman from Tokyo Japan went to attend tech expo at the Berlin Convention Center on November 10 2023 . He registered for event 9 AM using his digital passport number Q [B-ID_NUM] [B-NAME] with industry professionals participated in panel discussions and had lunch some potential partners One of he met was Munich they decided keep touch : partner ' s office address given as house No [I-STREET_ADDRESS] [B-NAME] business card 654 [B-STREET_ADDRESS]",
        0.6544462442398071
    ]
]
使用 LLM 获取 RAG 响应
将检索到的文档转换为字符串格式。
context =
"\n"
.join(
    [line_with_distance[
0
]
for
line_with_distance
in
retrieved_lines_with_distances]
)
为 Lanage 模型定义系统和用户提示。
注：我们告诉 LLM，如果片段中没有有用的信息，就说 "我不知道"。
SYSTEM_PROMPT =
"""
Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided. If there are no useful information in the snippets, just say "I don't know".
AI:
"""
USER_PROMPT =
f"""
Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
<context>
{context}
</context>
<question>
{question}
</question>
"""
使用 OpenAI ChatGPT 根据提示生成回复。
response = openai_client.chat.completions.create(
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
: SYSTEM_PROMPT},
        {
"role"
:
"user"
,
"content"
: USER_PROMPT},
    ],
)
print
(response.choices[
0
].message.content)
I don't know.
在这里我们可以看到，由于我们用掩码替换了 PII，LLM 无法根据上下文获取 PII 信息。所以它的回答是"通过这种方式，我们可以有效保护用户的隐私。