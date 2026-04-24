开始使用 Mem0 和 Milvus
Mem0
是人工智能应用的智能记忆层，旨在通过保留用户偏好和随时间不断调整来提供个性化和高效的交互。作为聊天机器人和人工智能驱动工具的理想选择，Mem0 可创建无缝、上下文感知的体验。
在本教程中，我们将介绍基本的 Mem0 内存管理操作--添加、检索、更新、搜索、删除和跟踪内存历史记录--使用高性能开源向量数据库
Milvus
，它为高效存储和检索提供了动力。本实践介绍将指导您完成基础内存操作，帮助您利用 Mem0 和 Milvus 构建个性化的人工智能交互。
准备工作
下载所需程序库
$
pip install mem0ai pymilvus milvus-lite
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
（点击屏幕顶部的 "运行时 "菜单，从下拉菜单中选择 "重新启动会话"）。
用 Milvus 配置 Mem0
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api 密钥
OPENAI_API_KEY
设置为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-***********"
现在，我们可以将 Mem0 配置为使用 Milvus 作为向量存储库
# Define Config
from
mem0
import
Memory

config = {
"vector_store"
: {
"provider"
:
"milvus"
,
"config"
: {
"collection_name"
:
"quickstart_mem0_with_milvus"
,
"embedding_model_dims"
:
"1536"
,
"url"
:
"./milvus.db"
,
# Use local vector database for demo purpose
},
    },
"version"
:
"v1.1"
,
}

m = Memory.from_config(config)
如果你只需要一个本地向量数据库，用于小规模数据或原型设计，那么将 uri 设置为本地文件，例如
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
如果您使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 API 密钥
相对应。
使用 Mem0 和 Milvus 管理用户记忆库
添加记忆库
add
函数将非结构化文本作为内存存储在 Milvus 中，并将其与特定用户和可选元数据关联。
在这里，我们将爱丽丝的记忆 "努力提高我的网球技术 "连同相关元数据一起添加到 Milvus 中。
# Add a memory to user: Working on improving tennis skills
res = m.add(
    messages=
"I am working on improving my tennis skills."
,
    user_id=
"alice"
,
    metadata={
"category"
:
"hobbies"
},
)

res
{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',
   'memory': 'Working on improving tennis skills',
   'event': 'ADD'}],
 'relations': []}
更新记忆
我们可以使用
add
函数的返回值检索内存 ID，这样就可以通过
update
用新信息更新内存。
# Get memory_id
memory_id = res[
"results"
][
0
][
"id"
]
# Update this memory with new information: Likes to play tennis on weekends
m.update(memory_id=memory_id, data=
"Likes to play tennis on weekends"
)
{'message': 'Memory updated successfully!'}
获取用户的所有内存
我们可以使用
get_all
函数查看所有插入的内存，或通过 Milvus 中的
user_id
进行筛选。
请注意，我们可以看到该记忆已从 "努力提高网球技能 "更改为 "喜欢在周末打网球"。
# Get all memory for the user Alice
m.get_all(user_id=
"alice"
)
{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',
   'memory': 'Likes to play tennis on weekends',
   'hash': '4c3bc9f87b78418f19df6407bc86e006',
   'metadata': None,
   'created_at': '2024-11-01T19:33:44.116920-07:00',
   'updated_at': '2024-11-01T19:33:47.619857-07:00',
   'user_id': 'alice'}]}
查看记忆更新历史
我们还可以通过
history
函数指定我们感兴趣的内存_id，查看内存更新历史。
m.history(memory_id=memory_id)
[{'id': '71ed3cec-5d9a-4fa6-a009-59802450c0b9',
  'memory_id': '77162018-663b-4dfa-88b1-4f029d6136ab',
  'old_memory': None,
  'new_memory': 'Working on improving tennis skills',
  'event': 'ADD',
  'created_at': '2024-11-01T19:33:44.116920-07:00',
  'updated_at': None},
 {'id': 'db2b003c-ffb7-42e4-bd8a-b9cf56a02bb9',
  'memory_id': '77162018-663b-4dfa-88b1-4f029d6136ab',
  'old_memory': 'Working on improving tennis skills',
  'new_memory': 'Likes to play tennis on weekends',
  'event': 'UPDATE',
  'created_at': '2024-11-01T19:33:44.116920-07:00',
  'updated_at': '2024-11-01T19:33:47.619857-07:00'}]
搜索内存
我们可以使用
search
函数查找与用户最相关的内存。
让我们从为 Alice 添加另一个内存开始。
new_mem = m.add(
"I have a linear algebra midterm exam on November 20"
,
    user_id=
"alice"
,
    metadata={
"category"
:
"task"
},
)
现在，我们调用
get_all
，指定 user_id，以验证我们确实有 2 个用户 Alice 的内存条目。
m.get_all(user_id=
"alice"
)
{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',
   'memory': 'Likes to play tennis on weekends',
   'hash': '4c3bc9f87b78418f19df6407bc86e006',
   'metadata': None,
   'created_at': '2024-11-01T19:33:44.116920-07:00',
   'updated_at': '2024-11-01T19:33:47.619857-07:00',
   'user_id': 'alice'},
  {'id': 'aa8eaa38-74d6-4b58-8207-b881d6d93d02',
   'memory': 'Has a linear algebra midterm exam on November 20',
   'hash': '575182f46965111ca0a8279c44920ea2',
   'metadata': {'category': 'task'},
   'created_at': '2024-11-01T19:33:57.271657-07:00',
   'updated_at': None,
   'user_id': 'alice'}]}
现在我们可以通过提供
query
和
user_id
来执行
search
。请注意，我们默认使用
L2
指标进行相似性搜索，因此
score
越小表示相似性越高。
m.search(query=
"What are Alice's hobbies"
, user_id=
"alice"
)
{'results': [{'id': '77162018-663b-4dfa-88b1-4f029d6136ab',
   'memory': 'Likes to play tennis on weekends',
   'hash': '4c3bc9f87b78418f19df6407bc86e006',
   'metadata': None,
   'score': 1.2807445526123047,
   'created_at': '2024-11-01T19:33:44.116920-07:00',
   'updated_at': '2024-11-01T19:33:47.619857-07:00',
   'user_id': 'alice'},
  {'id': 'aa8eaa38-74d6-4b58-8207-b881d6d93d02',
   'memory': 'Has a linear algebra midterm exam on November 20',
   'hash': '575182f46965111ca0a8279c44920ea2',
   'metadata': {'category': 'task'},
   'score': 1.728922724723816,
   'created_at': '2024-11-01T19:33:57.271657-07:00',
   'updated_at': None,
   'user_id': 'alice'}]}
删除内存
我们还可以通过提供相应的
memory_id
来
delete
内存。
我们将删除内存 "喜欢在周末打网球"，因为它的
memory_id
已被检索，并调用
get_all
验证删除是否成功。
m.delete(memory_id=memory_id)

m.get_all(
"alice"
)
{'results': [{'id': 'aa8eaa38-74d6-4b58-8207-b881d6d93d02',
   'memory': 'Has a linear algebra midterm exam on November 20',
   'hash': '575182f46965111ca0a8279c44920ea2',
   'metadata': {'category': 'task'},
   'created_at': '2024-11-01T19:33:57.271657-07:00',
   'updated_at': None,
   'user_id': 'alice'}]}