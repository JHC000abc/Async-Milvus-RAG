用 Vanna 和 Milvus 编写 SQL
Vanna
是一个开源 Python RAG（检索增强生成）框架，用于生成 SQL 和相关功能。
Milvus
是世界上最先进的开源向量数据库，用于支持 Embeddings 相似性搜索和人工智能应用。
Vanna 的工作分为两个简单的步骤--在你的数据上训练一个 RAG "模型"，然后提出问题，这些问题将返回 SQL 查询，这些查询可以设置为在你的数据库上运行。本指南演示了如何使用 Vanna 根据存储在数据库中的数据生成并执行 SQL 查询。
前提条件
在运行本笔记本之前，请确保已安装以下依赖项：
$ pip install
"vanna[milvus,openai]"
milvus-lite
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
你还需要在环境变量中设置
OPENAI_API_KEY
。您可以从
OpenAI
获取 API 密钥。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
数据准备
首先，我们需要继承 Vanna 的
Milvus_VectorStore
和
OpenAI_Chat
类，并定义一个新类
VannaMilvus
，将两者的功能结合起来。
from
pymilvus
import
MilvusClient, model
from
vanna.milvus
import
Milvus_VectorStore
from
vanna.openai
import
OpenAI_Chat
class
VannaMilvus
(Milvus_VectorStore, OpenAI_Chat):
def
__init__
(
self, config=
None
):
        Milvus_VectorStore.__init__(
self
, config=config)
        OpenAI_Chat.__init__(
self
, config=config)
我们使用必要的配置参数初始化
VannaMilvus
类。我们使用
milvus_client
实例来存储嵌入式数据，并使用从
milvus_model
初始化的
model.DefaultEmbeddingFunction()
来生成嵌入式数据。C
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
，它们对应于 Zilliz Cloud 中的
公共端点和 Api 密钥
。
milvus_uri =
"./milvus_vanna.db"
milvus_client = MilvusClient(uri=milvus_uri)

vn_milvus = VannaMilvus(
    config={
"api_key"
: os.getenv(
"OPENAI_API_KEY"
),
"model"
:
"gpt-3.5-turbo"
,
"milvus_client"
: milvus_client,
"embedding_function"
: model.DefaultEmbeddingFunction(),
"n_results"
:
2
,
# The number of results to return from Milvus semantic search.
}
)
这是一个只有少量数据样本的简单示例，因此我们将
n_results
设置为 2，以确保搜索到最相似的前 2 个结果。实际上，在处理较大的训练数据集时，应将
n_results
设置为更高的值。
我们将使用一个样本 SQLite 数据库，其中包含一些样本数据表。
import
sqlite3

sqlite_path =
"./my-database.sqlite"
sql_connect = sqlite3.connect(sqlite_path)
c = sql_connect.cursor()

init_sqls =
"""
CREATE TABLE IF NOT EXISTS Customer (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Company TEXT NOT NULL,
    City TEXT NOT NULL,
    Phone TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Company (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Industry TEXT NOT NULL,
    Location TEXT NOT NULL,
    EmployeeCount INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS User (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Email TEXT NOT NULL UNIQUE
);

INSERT INTO Customer (Name, Company, City, Phone) 
VALUES ('John Doe', 'ABC Corp', 'New York', '123-456-7890');

INSERT INTO Customer (Name, Company, City, Phone) 
VALUES ('Jane Smith', 'XYZ Inc', 'Los Angeles', '098-765-4321');

INSERT INTO Company (Name, Industry, Location, EmployeeCount)
VALUES ('ABC Corp', 'cutting-edge technology', 'New York', 100);

INSERT INTO User (Username, Email)
VALUES ('johndoe123', 'johndoe123@example.com');
"""
for
sql
in
init_sqls.split(
";"
):
    c.execute(sql)

sql_connect.commit()
# Connect to the SQLite database
vn_milvus.connect_to_sqlite(sqlite_path)
使用数据进行训练
我们可以在 SQLite 数据库的 DDL 数据上训练模型。我们获取 DDL 数据并将其输入
train
函数。
# If there exists training data, we should remove it before training.
existing_training_data = vn_milvus.get_training_data()
if
len
(existing_training_data) >
0
:
for
_, training_data
in
existing_training_data.iterrows():
        vn_milvus.remove_training_data(training_data[
"id"
])
# Get the DDL of the SQLite database
df_ddl = vn_milvus.run_sql(
"SELECT type, sql FROM sqlite_master WHERE sql is not null"
)
# Train the model on the DDL data
for
ddl
in
df_ddl[
"sql"
].to_list():
    vn_milvus.train(ddl=ddl)
Adding ddl: CREATE TABLE Customer (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Company TEXT NOT NULL,
    City TEXT NOT NULL,
    Phone TEXT NOT NULL
)
Adding ddl: CREATE TABLE sqlite_sequence(name,seq)
Adding ddl: CREATE TABLE Company (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Industry TEXT NOT NULL,
    Location TEXT NOT NULL,
    EmployeeCount INTEGER NOT NULL
)
Adding ddl: CREATE TABLE User (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Email TEXT NOT NULL UNIQUE
)
除了对 DDL 数据进行训练，我们还可以对数据库的文档和 SQL 查询进行训练。
# Add documentation about your business terminology or definitions.
vn_milvus.train(
    documentation=
"ABC Corp specializes in cutting-edge technology solutions and innovation."
)
vn_milvus.train(
    documentation=
"XYZ Inc is a global leader in manufacturing and supply chain management."
)
# You can also add SQL queries to your training data.
vn_milvus.train(sql=
"SELECT * FROM Customer WHERE Name = 'John Doe'"
)
Adding documentation....
Adding documentation....
Using model gpt-3.5-turbo for 65.0 tokens (approx)
Question generated with sql: What are the details of the customer named John Doe? 
Adding SQL...





'595b185c-e6ad-47b0-98fd-0e93ef9b6a0a-sql'
让我们来看看训练数据。
training_data = vn_milvus.get_training_data()
training_data
#
id
问题
内容
0
595b185c-e6ad-47b0-98fd-0e93ef9b6a0a-sql
名为 Joh... 的客户的详细信息是什么？
SELECT * FROM Customer WHERE Name = "John Doe
0
25f4956c-e370-4097-994f-996f22d145fa-ddl
无
CREATE TABLE Company（ID INTEGER PRIMARY...
1
b95ecc66-f65b-49dc-a9f1-c1842ad230ff-ddl
无
CREATE TABLE Customer（客户 ID INTEGER PRIMAR...
2
fcc73d15-30a5-4421-9d73-b8c3b0ed5305-ddl
无
CREATE TABLE sqlite_sequence(name,seq)
3
feae618c-5910-4f6f-8b4b-6cc3e03aec06-ddl
无
CREATE TABLE User（ID INTEGER PRIMARY KE...
0
79a48db1-ba1f-4fd5-be99-74f2ca2eaeeb-doc
无
XYZ Inc 是一家全球领先的制造和销售公司。
1
9f9df1b8-ae62-4823-ad28-d7e0f2d1f4c0-doc
无
ABC Corp 专门从事尖端技术的研发和生产。
生成并执行 SQL
由于我们已经对 DDL 数据进行了训练，因此现在可以使用表结构来生成 SQL 查询。
让我们尝试一个简单的问题。
sql = vn_milvus.generate_sql(
"what is the phone number of John Doe?"
)
vn_milvus.run_sql(sql)
SQL Prompt: [{'role': 'system', 'content': "You are a SQLite expert. Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. \n===Tables \nCREATE TABLE Customer (\n    ID INTEGER PRIMARY KEY AUTOINCREMENT,\n    Name TEXT NOT NULL,\n    Company TEXT NOT NULL,\n    City TEXT NOT NULL,\n    Phone TEXT NOT NULL\n)\n\nCREATE TABLE User (\n    ID INTEGER PRIMARY KEY AUTOINCREMENT,\n    Username TEXT NOT NULL UNIQUE,\n    Email TEXT NOT NULL UNIQUE\n)\n\n\n===Additional Context \n\nABC Corp specializes in cutting-edge technology solutions and innovation.\n\nXYZ Inc is a global leader in manufacturing and supply chain management.\n\n===Response Guidelines \n1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. \n2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n3. If the provided context is insufficient, please explain why it can't be generated. \n4. Please use the most relevant table(s). \n5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n"}, {'role': 'user', 'content': 'What are the details of the customer named John Doe?'}, {'role': 'assistant', 'content': "SELECT * FROM Customer WHERE Name = 'John Doe'"}, {'role': 'user', 'content': 'what is the phone number of John Doe?'}]
Using model gpt-3.5-turbo for 367.25 tokens (approx)
LLM Response: SELECT Phone FROM Customer WHERE Name = 'John Doe'
#
电话
0
123-456-7890
下面是一个更复杂的问题。制造公司名称信息在文档数据中，属于背景信息。生成的 SQL 查询将根据特定的制造公司名称检索客户信息。
sql = vn_milvus.generate_sql(
"which customer works for a manufacturing corporation?"
)
vn_milvus.run_sql(sql)
SQL Prompt: [{'role': 'system', 'content': "You are a SQLite expert. Please help to generate a SQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions. \n===Tables \nCREATE TABLE Company (\n    ID INTEGER PRIMARY KEY AUTOINCREMENT,\n    Name TEXT NOT NULL,\n    Industry TEXT NOT NULL,\n    Location TEXT NOT NULL,\n    EmployeeCount INTEGER NOT NULL\n)\n\nCREATE TABLE Customer (\n    ID INTEGER PRIMARY KEY AUTOINCREMENT,\n    Name TEXT NOT NULL,\n    Company TEXT NOT NULL,\n    City TEXT NOT NULL,\n    Phone TEXT NOT NULL\n)\n\n\n===Additional Context \n\nXYZ Inc is a global leader in manufacturing and supply chain management.\n\nABC Corp specializes in cutting-edge technology solutions and innovation.\n\n===Response Guidelines \n1. If the provided context is sufficient, please generate a valid SQL query without any explanations for the question. \n2. If the provided context is almost sufficient but requires knowledge of a specific string in a particular column, please generate an intermediate SQL query to find the distinct strings in that column. Prepend the query with a comment saying intermediate_sql \n3. If the provided context is insufficient, please explain why it can't be generated. \n4. Please use the most relevant table(s). \n5. If the question has been asked and answered before, please repeat the answer exactly as it was given before. \n"}, {'role': 'user', 'content': 'What are the details of the customer named John Doe?'}, {'role': 'assistant', 'content': "SELECT * FROM Customer WHERE Name = 'John Doe'"}, {'role': 'user', 'content': 'which customer works for a manufacturing corporation?'}]
Using model gpt-3.5-turbo for 384.25 tokens (approx)
LLM Response: SELECT * 
FROM Customer 
WHERE Company = 'XYZ Inc'
#
ID
名称
公司名称
城市
电话
0
2
简-史密斯
XYZ Inc
洛杉矶
098-765-4321
断开 SQLite 和 Milvus 的连接并将其删除，以释放资源。
sql_connect.close()
milvus_client.close()

os.remove(sqlite_path)
if
os.path.exists(milvus_uri):
    os.remove(milvus_uri)