Attu 桌面快速入门
1.简介
Attu
是 Milvus 的一体化开源管理工具。它具有直观的图形用户界面（GUI），可让您轻松与数据库交互。只需点击几下，您就可以直观地查看集群状态、管理元数据、执行数据查询等。
2.安装桌面应用程序
访问 Attu
GitHub Releases 页面
下载桌面版 Attu。选择适合您操作系统的版本，然后按照安装步骤进行操作。
注意 macOS（M 系列芯片）：
如果遇到错误：
attu.app
is
damaged
and
cannot be opened.
在终端中运行以下命令以绕过此问题：
sudo
xattr -rd com.apple.quarantine /Applications/attu.app
3.连接 Milvus
Attu 支持连接
Milvus Standalone
和
Zilliz Cloud
，可灵活使用本地或云托管数据库。
要在本地使用 Milvus Standalone：
按照
Milvus 安装指南
启动 Milvus Standalone。
打开 Attu 并输入连接信息：
Milvus 地址：你的 Milvus Standalone 服务器 URI，例如 http://localhost:19530
其他可选设置：你可以根据你的 Milvus 配置进行设置，也可以保留为默认设置。
单击 "连接 "访问数据库。
您也可以在
Zilliz Cloud
上连接完全托管的 Milvus。只需将
Milvus Address
和
token
设置为 Zilliz Cloud 实例的
公共端点和 API 密钥
。
点击访问数据库。
4.准备数据、创建 Collections 和插入数据
4.1 准备数据
我们使用
Milvus 文档 2.4.x
中的常见问题页面作为本示例的数据集。
下载并提取数据：
wget https://github.com/milvus-io/milvus-docs/releases/download/v2.4.6-preview/milvus_docs_2.4.x_en.zip
unzip -q milvus_docs_2.4.x_en.zip -d milvus_docs
处理 Markdown 文件：
from
glob
import
glob

text_lines = []
for
file_path
in
glob(
"milvus_docs/en/faq/*.md"
, recursive=
True
):
with
open
(file_path,
"r"
)
as
file:
        file_text = file.read()
    text_lines += file_text.split(
"# "
)
4.2 生成嵌入模型
定义一个嵌入模型，使用
milvus_model
生成文本嵌入。我们以
DefaultEmbeddingFunction
模型为例，它是一个经过预训练的轻量级嵌入模型。
from
pymilvus
import
model
as
milvus_model

embedding_model = milvus_model.DefaultEmbeddingFunction()
# Generate test embedding
test_embedding = embedding_model.encode_queries([
"This is a test"
])[
0
]
embedding_dim =
len
(test_embedding)
print
(embedding_dim)
print
(test_embedding[:
10
])
输出：
768
[-0.04836066  0.07163023 -0.01130064 -0.03789345 -0.03320649 -0.01318448
 -0.03041712 -0.02269499 -0.02317863 -0.00426028]
4.3 创建 Collections
连接到 Milvus 并创建一个 Collection：
from
pymilvus
import
MilvusClient
# Connect to Milvus Standalone
client = MilvusClient(uri=
"http://localhost:19530"
)

collection_name =
"attu_tutorial"
# Drop collection if it exists
if
client.has_collection(collection_name):
    client.drop_collection(collection_name)
# Create a new collection
client.create_collection(
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
4.4 插入数据
遍历文本行，创建嵌入，并将数据插入 Milvus：
from
tqdm
import
tqdm

data = []
doc_embeddings = embedding_model.encode_documents(text_lines)
for
i, line
in
enumerate
(tqdm(text_lines, desc=
"Creating embeddings"
)):
    data.append({
"id"
: i,
"vector"
: doc_embeddings[i],
"text"
: line})

client.insert(collection_name=collection_name, data=data)
4.5 可视化数据和 Schema
现在，我们可以使用 Attu 的界面可视化数据 Schema 和插入的实体。Schema 显示已定义的字段，包括
id
类型的字段
Int64
和
vector
类型的字段
FloatVector(768)
以及
Inner Product (IP)
度量。Collections 中加载了
72 个实体
。
此外，我们还可以查看插入的数据，包括 ID、向量 Embeddings 和存储文本内容等元数据的 Dynamic Field。界面支持根据指定条件或动态字段进行过滤和查询。
5.可视化搜索结果和关系
Attu 提供了可视化和探索数据关系的强大界面。要检查插入的数据点及其相似性关系，请按照以下步骤操作：
5.1
执行搜索
导航至 Attu 中的 "
向量搜索
"选项卡。
单击 "
生成随机数据
"按钮创建测试查询。
单击 "
搜索"
，根据生成的数据检索结果。
结果显示在表格中，显示每个匹配实体的 ID、相似度得分和 Dynamic Field。
5.2
探索数据关系
单击结果面板中的 "
探索 "
按钮，可将查询向量与搜索结果之间的关系可视化为
类似知识图谱的结构
。
中心节点
代表搜索向量。
连接的节点
代表搜索结果，点击它们将显示相应节点的详细信息。
5.3
展开图
双击任何结果节点可展开其连接。此操作可显示所选节点与 Collections 中其他数据点之间的其他关系，从而创建一个
更大的、相互连接的知识图谱
。
通过这种扩展视图，可以根据向量相似性更深入地探索数据点之间的关系。
6.结论
Attu 简化了存储在 Milvus 中的向量数据的管理和可视化。从数据插入到查询执行和交互式探索，它为处理复杂的向量搜索任务提供了一个直观的界面。凭借动态 Schema 支持、图形搜索可视化和灵活的查询过滤器等功能，Attu 使用户能够有效地分析大规模数据集。
通过利用 Attu 的可视化探索工具，用户可以更好地理解他们的数据，识别隐藏的关系，并做出数据驱动的决策。今天就开始使用 Attu 和 Milvus 探索您自己的数据集吧！