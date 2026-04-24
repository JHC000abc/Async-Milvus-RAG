使用 Milvus 和 Cohere 进行问题解答
本页说明了如何使用 Milvus 作为向量数据库和 Cohere 作为嵌入系统，创建基于 SQuAD 数据集的问题解答系统。
开始之前
本页中的代码片段需要安装
pymilvus
、
cohere
、
pandas
、
numpy
和
tqdm
。在这些软件包中，
PYMILVUS
是 Milvus 的客户端。如果系统中没有这些软件包，请运行以下命令进行安装：
pip install pymilvus cohere pandas numpy tqdm
然后需要加载本指南中使用的模块。
import
cohere
import
pandas
import
numpy
as
np
from
tqdm
import
tqdm
from
pymilvus
import
connections, FieldSchema, CollectionSchema, DataType, Collection, utility
参数
在这里，我们可以找到以下代码段中使用的参数。其中有些参数需要更改，以适应你的环境。每个参数旁边都有说明。
FILE =
'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json'
# The SQuAD dataset url
COLLECTION_NAME =
'question_answering_db'
# Collection name
DIMENSION =
1024
# Embeddings size, cohere embeddings default to 4096 with the large model
COUNT =
5000
# How many questions to embed and insert into Milvus
BATCH_SIZE =
96
# How large of batches to use for embedding and insertion
MILVUS_HOST =
'localhost'
# Milvus server URI
MILVUS_PORT =
'19530'
COHERE_API_KEY =
'replace-this-with-the-cohere-api-key'
# API key obtained from Cohere
要进一步了解本页使用的模型和数据集，请参阅
co:here
和
SQuAD
。
准备数据集
在本例中，我们将使用斯坦福问题解答数据集（SQuAD）作为回答问题的真实来源。该数据集以 JSON 文件的形式提供，我们将使用
pandas
加载它。
# Download the dataset
dataset = pandas.read_json(FILE)
# Clean up the dataset by grabbing all the question answer pairs
simplified_records = []
for
x
in
dataset[
'data'
]:
for
y
in
x[
'paragraphs'
]:
for
z
in
y[
'qas'
]:
if
len
(z[
'answers'
]) !=
0
:
                simplified_records.append({
'question'
: z[
'question'
],
'answer'
: z[
'answers'
][
0
][
'text'
]})
# Grab the amount of records based on COUNT
simplified_records = pandas.DataFrame.from_records(simplified_records)
simplified_records = simplified_records.sample(n=
min
(COUNT,
len
(simplified_records)), random_state =
42
)
# Check the length of the cleaned dataset matches count
print
(
len
(simplified_records))
输出结果应该是数据集中的记录数
5000
创建 Collections
本节涉及 Milvus 和为本用例设置数据库。在 Milvus 中，我们需要设置一个 Collections 并为其建立索引。
# Connect to Milvus Database
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
# Remove collection if it already exists
if
utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)
# Create collection which includes the id, title, and embedding.
fields = [
    FieldSchema(name=
'id'
, dtype=DataType.INT64, is_primary=
True
, auto_id=
True
),
    FieldSchema(name=
'original_question'
, dtype=DataType.VARCHAR, max_length=
1000
),
    FieldSchema(name=
'answer'
, dtype=DataType.VARCHAR, max_length=
1000
),
    FieldSchema(name=
'original_question_embedding'
, dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
]
schema = CollectionSchema(fields=fields)
collection = Collection(name=COLLECTION_NAME, schema=schema)
# Create an IVF_FLAT index for collection.
index_params = {
'metric_type'
:
'IP'
,
'index_type'
:
"IVF_FLAT"
,
'params'
:{
"nlist"
:
1024
}
}
collection.create_index(field_name=
"original_question_embedding"
, index_params=index_params)
collection.load()
插入数据
设置好 Collections 后，我们需要开始插入数据。这分为三个步骤
读取数据、
嵌入原始问题，以及
将数据插入我们刚刚在 Milvus 上创建的 Collections。
在本例中，数据包括原始问题、原始问题的 Embeddings 和原始问题的答案。
# Set up a co:here client.
cohere_client = cohere.Client(COHERE_API_KEY)
# Extract embeddings from questions using Cohere
def
embed
(
texts, input_type
):
    res = cohere_client.embed(texts, model=
'embed-multilingual-v3.0'
, input_type=input_type)
return
res.embeddings
# Insert each question, answer, and qustion embedding
total = pandas.DataFrame()
for
batch
in
tqdm(np.array_split(simplified_records, (COUNT/BATCH_SIZE) +
1
)):
    questions = batch[
'question'
].tolist()
    embeddings = embed(questions,
"search_document"
)
    
    data = [
        {
'original_question'
: x,
'answer'
: batch[
'answer'
].tolist()[i],
'original_question_embedding'
: embeddings[i]
        }
for
i, x
in
enumerate
(questions)
    ]

    collection.insert(data=data)

time.sleep(
10
)
提问
将所有数据插入 Milvus Collections 后，我们就可以向系统提问了，方法是将我们的问题短语用 Cohere 嵌入，然后用 Collections 进行搜索。
刚插入数据时的搜索速度可能会稍慢一些，因为搜索未编入索引的数据是以暴力方式进行的。一旦新数据被自动编入索引，搜索速度就会加快。
# Search the cluster for an answer to a question text
def
search
(
text, top_k =
5
):
# AUTOINDEX does not require any search params
search_params = {}

    results = collection.search(
        data = embed([text],
"search_query"
),
# Embeded the question
anns_field=
'original_question_embedding'
,
        param=search_params,
        limit = top_k,
# Limit to top_k results per search
output_fields=[
'original_question'
,
'answer'
]
# Include the original question and answer in the result
)

    distances = results[
0
].distances
    entities = [ x.entity.to_dict()[
'entity'
]
for
x
in
results[
0
] ]

    ret = [ {
"answer"
: x[
1
][
"answer"
],
"distance"
: x[
0
],
"original_question"
: x[
1
][
'original_question'
]
    }
for
x
in
zip
(distances, entities)]
return
ret
# Ask these questions
search_questions = [
'What kills bacteria?'
,
'What\'s the biggest dog?'
]
# Print out the results in order of [answer, similarity score, original question]
ret = [ {
"question"
: x,
"candidates"
: search(x) }
for
x
in
search_questions ]
输出结果应类似于下图：
#
Output
#
# [
#
{
#
"question"
:
"What kills bacteria?"
,
#
"candidates"
: [
#
{
#
"answer"
:
"farming"
,
#
"distance"
: 0.6261022090911865,
#
"original_question"
:
"What makes bacteria resistant to antibiotic treatment?"
#
},
#
{
#
"answer"
:
"Phage therapy"
,
#
"distance"
: 0.6093736886978149,
#
"original_question"
:
"What has been talked about to treat resistant bacteria?"
#
},
#
{
#
"answer"
:
"oral contraceptives"
,
#
"distance"
: 0.5902313590049744,
#
"original_question"
:
"In therapy, what does the antibacterial interact with?"
#
},
#
{
#
"answer"
:
"slowing down the multiplication of bacteria or killing the bacteria"
,
#
"distance"
: 0.5874154567718506,
#
"original_question"
:
"How do antibiotics work?"
#
},
#
{
#
"answer"
:
"in intensive farming to promote animal growth"
,
#
"distance"
: 0.5667208433151245,
#
"original_question"
:
"Besides in treating human disease where else are antibiotics used?"
#
}
#
]
#
},
#
{
#
"question"
:
"What's the biggest dog?"
,
#
"candidates"
: [
#
{
#
"answer"
:
"English Mastiff"
,
#
"distance"
: 0.7875324487686157,
#
"original_question"
:
"What breed was the largest dog known to have lived?"
#
},
#
{
#
"answer"
:
"forest elephants"
,
#
"distance"
: 0.5886962413787842,
#
"original_question"
:
"What large animals reside in the national park?"
#
},
#
{
#
"answer"
:
"Rico"
,
#
"distance"
: 0.5634892582893372,
#
"original_question"
:
"What is the name of the dog that could ID over 200 things?"
#
},
#
{
#
"answer"
:
"Iditarod Trail Sled Dog Race"
,
#
"distance"
: 0.546872615814209,
#
"original_question"
:
"Which dog-sled race in Alaska is the most famous?"
#
},
#
{
#
"answer"
:
"part of the family"
,
#
"distance"
: 0.5387814044952393,
#
"original_question"
:
"Most people today describe their dogs as what?"
#
}
#
]
#
}
#
]