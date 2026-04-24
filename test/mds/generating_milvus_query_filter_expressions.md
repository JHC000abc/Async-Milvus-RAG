使用大型语言模型生成 Milvus 查询过滤表达式
在本教程中，我们将演示如何使用大型语言模型（LLMs）从自然语言查询自动生成 Milvus 过滤表达式。这种方法允许用户用普通英语表达复杂的过滤条件，然后将这些条件转换为适当的 Milvus 语法，从而使向量数据库查询更容易访问。
Milvus 支持复杂的过滤功能，包括
基本操作符
：比较操作符，如
==
,
!=
,
>
,
<
,
>=
、
<=
布尔操作符
：逻辑操作符，如
and
,
or
,
not
用于复杂条件的逻辑操作符
字符串操作符
：使用
like
和其他字符串函数进行模式匹配
数组操作符
：使用
array_contains
,
array_length
等处理数组字段。
JSON 操作符
：使用专用操作符查询 JSON 字段
通过将 LLMs 与 Milvus 文档集成，我们可以创建一个智能系统，它能理解自然语言查询并生成语法正确的过滤表达式。本教程将介绍建立该系统的过程，并重点介绍其在各种过滤场景中的有效性。
依赖关系和环境
$
pip install --upgrade pymilvus openai requests docling beautifulsoup4
print("Environment setup complete!")
设置环境变量
配置您的 OpenAI API 凭据，以启用嵌入生成和基于 LLM 的过滤表达式创建。将
'your_openai_api_key'
替换为您实际的 OpenAI API 密钥。
import
os
import
openai

os.environ[
"OPENAI_API_KEY"
] =
"your_openai_api_key"
api_key = os.getenv(
"OPENAI_API_KEY"
)
if
not
api_key:
raise
ValueError(
"Please set the OPENAI_API_KEY environment variable!"
)

openai.api_key = api_key
print
(
"API key loaded."
)
创建样本 Collections
现在，让我们创建一个包含用户数据的样本 Collections。该 Collections 将包含标量字段（用于过滤）和向量嵌入（用于语义搜索）。我们将使用 OpenAI 的文本嵌入模型来生成用户信息的向量表示。
from
pymilvus
import
MilvusClient, FieldSchema, CollectionSchema, DataType
import
os
from
openai
import
OpenAI
import
uuid

client = MilvusClient(uri=
"http://localhost:19530"
)
openai_client = OpenAI(api_key=os.environ.get(
"OPENAI_API_KEY"
))
embedding_model =
"text-embedding-3-small"
embedding_dim =
1536
fields = [
    FieldSchema(
        name=
"pk"
,
        dtype=DataType.VARCHAR,
        is_primary=
True
,
        auto_id=
False
,
        max_length=
100
,
    ),
    FieldSchema(name=
"name"
, dtype=DataType.VARCHAR, max_length=
128
),
    FieldSchema(name=
"age"
, dtype=DataType.INT64),
    FieldSchema(name=
"city"
, dtype=DataType.VARCHAR, max_length=
128
),
    FieldSchema(name=
"hobby"
, dtype=DataType.VARCHAR, max_length=
128
),
    FieldSchema(name=
"embedding"
, dtype=DataType.FLOAT_VECTOR, dim=embedding_dim),
]
schema = CollectionSchema(fields=fields, description=
"User data embedding example"
)
collection_name =
"user_data_collection"
if
client.has_collection(collection_name):
    client.drop_collection(collection_name)
# Strong consistency waits for all loads to complete, adding latency with large datasets
# client.create_collection(
#     collection_name=collection_name, schema=schema, consistency_level="Strong"
# )
client.create_collection(collection_name=collection_name, schema=schema)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"embedding"
,
    index_type=
"IVF_FLAT"
,
    metric_type=
"COSINE"
,
    params={
"nlist"
:
128
},
)
client.create_index(collection_name=collection_name, index_params=index_params)

data_to_insert = [
    {
"name"
:
"John"
,
"age"
:
23
,
"city"
:
"Shanghai"
,
"hobby"
:
"Drinking coffee"
},
    {
"name"
:
"Alice"
,
"age"
:
29
,
"city"
:
"New York"
,
"hobby"
:
"Reading books"
},
    {
"name"
:
"Bob"
,
"age"
:
31
,
"city"
:
"London"
,
"hobby"
:
"Playing chess"
},
    {
"name"
:
"Eve"
,
"age"
:
27
,
"city"
:
"Paris"
,
"hobby"
:
"Painting"
},
    {
"name"
:
"Charlie"
,
"age"
:
35
,
"city"
:
"Tokyo"
,
"hobby"
:
"Cycling"
},
    {
"name"
:
"Grace"
,
"age"
:
22
,
"city"
:
"Berlin"
,
"hobby"
:
"Photography"
},
    {
"name"
:
"David"
,
"age"
:
40
,
"city"
:
"Toronto"
,
"hobby"
:
"Watching movies"
},
    {
"name"
:
"Helen"
,
"age"
:
30
,
"city"
:
"Sydney"
,
"hobby"
:
"Cooking"
},
    {
"name"
:
"Frank"
,
"age"
:
28
,
"city"
:
"Beijing"
,
"hobby"
:
"Hiking"
},
    {
"name"
:
"Ivy"
,
"age"
:
26
,
"city"
:
"Seoul"
,
"hobby"
:
"Dancing"
},
    {
"name"
:
"Tom"
,
"age"
:
33
,
"city"
:
"Madrid"
,
"hobby"
:
"Writing"
},
]
def
get_embeddings
(
texts
):
return
[
        rec.embedding
for
rec
in
openai_client.embeddings.create(
input
=texts, model=embedding_model, dimensions=embedding_dim
        ).data
    ]


texts = [
f"
{item[
'name'
]}
from
{item[
'city'
]}
is
{item[
'age'
]}
years old and likes
{item[
'hobby'
]}
."
for
item
in
data_to_insert
]
embeddings = get_embeddings(texts)

insert_data = []
for
item, embedding
in
zip
(data_to_insert, embeddings):
    item_with_embedding = {
"pk"
:
str
(uuid.uuid4()),
"name"
: item[
"name"
],
"age"
: item[
"age"
],
"city"
: item[
"city"
],
"hobby"
: item[
"hobby"
],
"embedding"
: embedding,
    }
    insert_data.append(item_with_embedding)

client.insert(collection_name=collection_name, data=insert_data)
print
(
f"Collection '
{collection_name}
' has been created and data has been inserted."
)
打印 3 个样本数据
上面的代码创建了一个具有以下结构的 Milvus Collections：
pk
：主键字段（VARCHAR）
name
：用户名（VARCHAR）
年龄
：用户年龄（INT64）
city：城市
用户城市（VARCHAR）
hobby
：用户爱好（VARCHAR）
embedding
：向量嵌入（FLOAT_VECTOR，1536 维度）
我们插入了 11 个样本用户的个人信息，并生成了用于语义搜索功能的 embeddings。在嵌入之前，每个用户的信息都会被转换成一个描述性文本，其中包含他们的姓名、所在地、年龄和兴趣爱好。让我们通过查询一些样本记录来验证我们的 Collection 是否创建成功并包含预期的数据。
from
pymilvus
import
MilvusClient
import
os
from
openai
import
OpenAI

client = MilvusClient(uri=
"http://localhost:19530"
)
collection_name =
"user_data_collection"
client.load_collection(collection_name=collection_name)

result = client.query(
    collection_name=collection_name,
filter
=
""
,
    output_fields=[
"name"
,
"age"
,
"city"
,
"hobby"
],
    limit=
3
,
)
for
record
in
result:
print
(record)
Collections 过滤表达式文档
为了帮助大型语言模型更好地理解 Milvus 的过滤表达式语法，我们需要为它提供相关的官方文档。我们将使用
docling
库从 Milvus 官方网站上抓取几个关键页面。
这些页面包含以下详细信息
布尔操作符
：
and
,
or
,
not
用于复杂的逻辑条件
基本操作符
：比较操作符，如
==
,
!=
,
>
,
<
,
>=
、
<=
过滤模板
：高级过滤模式和语法
字符串匹配
：使用
like
和其他字符串操作进行模式匹配
这些文档将作为我们的 LLM 生成准确过滤表达式的知识库。
import
docling
from
docling.document_converter
import
DocumentConverter

converter = DocumentConverter()
docs = [
    converter.convert(url)
for
url
in
[
"https://milvus.io/docs/boolean.md"
,
"https://milvus.io/docs/basic-operators.md"
,
"https://milvus.io/docs/filtering-templating.md"
,
    ]
]
for
doc
in
docs[:
3
]:
print
(doc.document.export_to_markdown())
文档搜刮提供了 Milvus 过滤器语法的全面覆盖。这个知识库将使我们的 LLM 能够理解构建过滤器表达式的细微差别，包括操作符的正确使用、字段引用和复杂的条件组合。
LLM 驱动的过滤器生成
现在我们有了文档上下文，让我们来设置 LLM 系统以生成过滤器表达式。我们将创建一个结构化的提示，将获取的文档与用户查询结合起来，生成语法正确的 Milvus 过滤表达式。
我们的过滤器生成系统使用精心制作的提示语，它可以
提供上下文
：包括完整的 Milvus 文档作为参考资料
设置限制
：确保 LLM 只使用文档中的语法和功能
确保准确性
：要求语法表达正确
保持重点
：只返回过滤表达式，不做解释
让我们用自然语言查询来测试一下，看看 LLM 的表现如何。
from
openai
import
OpenAI
import
json
from
IPython.display
import
display, Markdown

context =
"\n"
.join([doc.document.export_to_markdown()
for
doc
in
docs])

prompt =
f"""
You are an expert Milvus vector database engineer. Your task is to convert a user's natural language query into a valid Milvus filter expression, using the provided Milvus documentation as your knowledge base.

Follow these rules strictly:
1. Only use the provided documents as your source of knowledge.
2. Ensure the generated filter expression is syntactically correct.
3. If there isn't enough information in the documents to create an expression, state that directly.
4. Only return the final filter expression. Do not include any explanations or extra text.

---
**Milvus Documentation Context:**
{context}
---
**User Query:**
{user_query}
---
**Filter Expression:**
"""
client = OpenAI()
def
generate_filter_expr
(
user_query
):
"""
    Generates a Milvus filter expression from a user query using GPT-4o-mini.
    """
completion = client.chat.completions.create(
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
: prompt},
            {
"role"
:
"user"
,
"content"
: user_query},
        ],
        temperature=
0.0
,
    )
return
completion.choices[
0
].message.content


user_query =
"Find people older than 30 who live in London, Tokyo, or Toronto"
filter_expr = generate_filter_expr(user_query)
print
(
f"Generated filter expression:
{filter_expr}
"
)
LLM 成功生成了一个结合多个条件的过滤表达式：
使用以下运算符进行年龄比较
>
使用
in
操作符进行多个城市匹配
正确的字段引用和语法
这证明了提供全面文档上下文来指导 LLM 过滤器生成的强大功能。
测试生成的过滤器
现在，让我们在实际的 Milvus 搜索操作中使用生成的过滤器表达式来测试一下。我们将结合语义搜索和精确过滤，找到符合查询意图和特定条件的用户。
from
pymilvus
import
MilvusClient
from
openai
import
OpenAI
import
os

client = MilvusClient(uri=
"http://localhost:19530"
)
openai_client = OpenAI(api_key=os.environ.get(
"OPENAI_API_KEY"
))

clean_filter = (
    filter_expr.replace(
"```"
,
""
).replace(
'filter="'
,
""
).replace(
'"'
,
""
).strip()
)
print
(
f"Using filter:
{clean_filter}
"
)

query_embedding = (
    openai_client.embeddings.create(
input
=[user_query], model=
"text-embedding-3-small"
, dimensions=
1536
)
    .data[
0
]
    .embedding
)

search_results = client.search(
    collection_name=
"user_data_collection"
,
    data=[query_embedding],
    limit=
10
,
filter
=clean_filter,
    output_fields=[
"pk"
,
"name"
,
"age"
,
"city"
,
"hobby"
],
    search_params={
"metric_type"
:
"COSINE"
,
"params"
: {
"nprobe"
:
10
},
    },
)
print
(
"Search results:"
)
for
i, hits
in
enumerate
(search_results):
print
(
f"Query
{i}
:"
)
for
hit
in
hits:
print
(
f"  -
{hit}
"
)
print
()
结果分析
搜索结果证明了 LLM 生成的过滤器与 Milvus 向量搜索的成功整合。过滤器正确识别了以下用户
年龄超过 30 岁
居住在伦敦、东京或多伦多
符合查询的语义上下文
这种方法将结构化过滤的精确性与自然语言输入的灵活性结合在一起，使那些可能不熟悉特定查询语法的用户更容易访问向量数据库。