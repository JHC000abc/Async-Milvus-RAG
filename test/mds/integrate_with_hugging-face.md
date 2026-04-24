使用 Milvus 和 Hugging Face 进行问题解答
基于语义搜索的问题解答系统的工作原理是从给定查询问题的问答数据集中找出最相似的问题。一旦确定了最相似的问题，数据集中的相应答案就会被视为查询问题的答案。这种方法依靠语义相似性度量来确定问题之间的相似性并检索相关答案。
本教程展示了如何使用
Hugging Face
作为数据加载器和嵌入生成器进行数据处理，并使用
Milvus
作为向量数据库进行语义搜索，从而构建一个问题解答系统。
开始之前
你需要确保安装了所有必需的依赖项：
pymilvus
: python 软件包可与由 Milvus 或 Zilliz Cloud 提供的向量数据库服务配合使用。
datasets
,
transformers
: Hugging Face 软件包管理数据并利用模型。
torch
：一个功能强大的库提供高效的张量计算和深度学习工具。
$ pip install --upgrade pymilvus milvus-lite transformers datasets torch
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
。(点击屏幕上方的 "Runtime（运行时）"菜单，从下拉菜单中选择 "Restart session（重新启动会话）"）。
准备数据
在本节中，我们将从 Hugging Face 数据集中加载示例问答对。作为演示，我们只从
SQuAD
的验证拆分中获取部分数据。
from
datasets
import
load_dataset


DATASET =
"squad"
# Name of dataset from HuggingFace Datasets
INSERT_RATIO =
0.001
# Ratio of example dataset to be inserted
data = load_dataset(DATASET, split=
"validation"
)
# Generates a fixed subset. To generate a random subset, remove the seed.
data = data.train_test_split(test_size=INSERT_RATIO, seed=
42
)[
"test"
]
# Clean up the data structure in the dataset.
data = data.
map
(
lambda
val: {
"answer"
: val[
"answers"
][
"text"
][
0
]},
    remove_columns=[
"id"
,
"answers"
,
"context"
],
)
# View summary of example data
print
(data)
Dataset({
    features: ['title', 'question', 'answer'],
    num_rows: 11
})
要生成问题的嵌入，您可以从 Hugging Face 模型中选择一个文本嵌入模型。在本教程中，我们将以小型句子嵌入模型
all-MiniLM-L6-v2
为例。
from
transformers
import
AutoTokenizer, AutoModel
import
torch

MODEL = (
"sentence-transformers/all-MiniLM-L6-v2"
# Name of model from HuggingFace Models
)
INFERENCE_BATCH_SIZE =
64
# Batch size of model inference
# Load tokenizer & model from HuggingFace Hub
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModel.from_pretrained(MODEL)
def
encode_text
(
batch
):
# Tokenize sentences
encoded_input = tokenizer(
        batch[
"question"
], padding=
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
# Perform pooling
token_embeddings = model_output[
0
]
    attention_mask = encoded_input[
"attention_mask"
]
    input_mask_expanded = (
        attention_mask.unsqueeze(-
1
).expand(token_embeddings.size()).
float
()
    )
    sentence_embeddings = torch.
sum
(
        token_embeddings * input_mask_expanded,
1
) / torch.clamp(input_mask_expanded.
sum
(
1
),
min
=
1e-9
)
# Normalize embeddings
batch[
"question_embedding"
] = torch.nn.functional.normalize(
        sentence_embeddings, p=
2
, dim=
1
)
return
batch


data = data.
map
(encode_text, batched=
True
, batch_size=INFERENCE_BATCH_SIZE)
data_list = data.to_list()
插入数据
现在，我们已经准备好带有问题嵌入的问答对。下一步是将它们插入向量数据库。
我们首先需要连接 Milvus 服务并创建一个 Milvus Collections。
from
pymilvus
import
MilvusClient


MILVUS_URI =
"./huggingface_milvus_test.db"
# Connection URI
COLLECTION_NAME =
"huggingface_test"
# Collection name
DIMENSION =
384
# Embedding dimension depending on model
milvus_client = MilvusClient(MILVUS_URI)
if
milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(
    collection_name=COLLECTION_NAME,
    dimension=DIMENSION,
    auto_id=
True
,
# Enable auto id
enable_dynamic_field=
True
,
# Enable dynamic fields
vector_field_name=
"question_embedding"
,
# Map vector field name and embedding column in dataset
consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
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
将所有数据插入 Collections：
milvus_client.insert(collection_name=COLLECTION_NAME, data=data_list)
{'insert_count': 11,
 'ids': [450072488481390592, 450072488481390593, 450072488481390594, 450072488481390595, 450072488481390596, 450072488481390597, 450072488481390598, 450072488481390599, 450072488481390600, 450072488481390601, 450072488481390602],
 'cost': 0}
提出问题
将所有数据插入 Milvus 后，我们就可以提出问题，看看最接近的答案是什么。
questions = {
"question"
: [
"What is LGM?"
,
"When did Massachusetts first mandate that children be educated in schools?"
,
    ]
}
# Generate question embeddings
question_embeddings = [v.tolist()
for
v
in
encode_text(questions)[
"question_embedding"
]]
# Search across Milvus
search_results = milvus_client.search(
    collection_name=COLLECTION_NAME,
    data=question_embeddings,
    limit=
3
,
# How many search results to output
output_fields=[
"answer"
,
"question"
],
# Include these fields in search results
)
# Print out results
for
q, res
in
zip
(questions[
"question"
], search_results):
print
(
"Question:"
, q)
for
r
in
res:
print
(
            {
"answer"
: r[
"entity"
][
"answer"
],
"score"
: r[
"distance"
],
"original question"
: r[
"entity"
][
"question"
],
            }
        )
print
(
"\n"
)
Question: What is LGM?
{'answer': 'Last Glacial Maximum', 'score': 0.956273078918457, 'original question': 'What does LGM stands for?'}
{'answer': 'coordinate the response to the embargo', 'score': 0.2120140939950943, 'original question': 'Why was this short termed organization created?'}
{'answer': '"Reducibility Among Combinatorial Problems"', 'score': 0.1945795714855194, 'original question': 'What is the paper written by Richard Karp in 1972 that ushered in a new era of understanding between intractability and NP-complete problems?'}


Question: When did Massachusetts first mandate that children be educated in schools?
{'answer': '1852', 'score': 0.9709997177124023, 'original question': 'In what year did Massachusetts first require children to be educated in schools?'}
{'answer': 'several regional colleges and universities', 'score': 0.34164726734161377, 'original question': 'In 1890, who did the university decide to team up with?'}
{'answer': '1962', 'score': 0.1931006908416748, 'original question': 'When were stromules discovered?'}