使用 Milvus 和 FiftyOne 进行视觉搜索
FiftyOne
是一款用于构建高质量数据集和计算机视觉模型的开源工具。本指南可帮助您将 Milvus 的相似性搜索功能集成到 FiftyOne 中，从而在自己的数据集上进行视觉搜索。
FiftyOne 提供了一个 API，用于创建 Milvus Collections、上传向量和运行相似性查询，既可以在 Python 中
编程
，也可以在应用程序中通过点选进行操作。本页演示的重点是编程集成。
前提条件
开始之前，请确保具备以下条件：
运行中的
Milvus 服务器
。
安装了
pymilvus
和
fiftyone
的 Python 环境。
要搜索的图像
数据集
。
安装要求
在本例中，我们将使用
pymilvus
和
fiftyone
。您可以通过运行以下命令来安装它们：
python3 -m pip install pymilvus fiftyone torch torchvision
基本配方
使用 Milvus 在 FiftyOne 数据集上创建相似性索引并以此查询数据的基本工作流程如下：
将
数据集
载入 FiftyOne
为数据集中的样本或斑块计算向量嵌入，或选择一个模型来使用生成嵌入。
使用
compute_similarity()
方法为数据集中的样本或对象补丁生成 Milvus 相似性指数，方法是设置参数
backend="milvus"
并指定一个您选择的
brain_key
。
使用此 Milvus 相似性索引查询数据时，请使用
sort_by_similarity()
.
如果需要，可以删除该索引。
程序
下面的示例演示了上述工作流程。
1.将数据集加载到 FiftyOne，并计算样本的嵌入度
以下代码使用 FiftyOne 提供的样本图像集来演示集成。您可以参考
这篇文章
准备自己的图像集。
import
fiftyone
as
fo
import
fiftyone.brain
as
fob
import
fiftyone.zoo
as
foz
# Step 1: Load your data into FiftyOne
dataset = foz.load_zoo_dataset(
"quickstart"
)
# Steps 2 and 3: Compute embeddings and create a similarity index
milvus_index = fob.compute_similarity(
    dataset,
    brain_key=
"milvus_index"
,
    backend=
"milvus"
,
)
2.进行视觉相似性搜索
现在，您可以使用 Milvus 相似性索引对数据集进行视觉相似性搜索。
# Step 4: Query your data
query = dataset.first().
id
# query by sample ID
view = dataset.sort_by_similarity(
    query,
    brain_key=
"milvus_index"
,
    k=
10
,
# limit to 10 most similar samples
)
# Step 5 (optional): Cleanup
# Delete the Milvus collection
milvus_index.cleanup()
# Delete run record from FiftyOne
dataset.delete_brain_run(
"milvus_index"
)
3.删除索引
如果您不再需要 Milvus 相似性索引，可以使用以下代码将其删除：
# Step 5: Delete the index
milvus_index.delete()
使用 Milvus 后台
默认情况下，调用
compute_similarity()
或
sort_by_similarity()
将使用 sklearn 后端。
要使用 Milvus 后端，只需将可选的后端参数
compute_similarity()
的可选后台参数设置为
"milvus"
：
import
fiftyone.brain
as
fob

fob.compute_similarity(..., backend=
"milvus"
, ...)
或者，你也可以通过设置以下环境变量，永久配置 FiftyOne 使用 Milvus 后端：
export FIFTYONE_BRAIN_DEFAULT_SIMILARITY_BACKEND=milvus
或通过设置位于
~/.fiftyone/brain_config.json
的
大脑配置
中的
default_similarity_backend
参数，永久
配置 FiftyOne
使用 Milvus 后端：
{
"default_similarity_backend"
:
"milvus"
}
身份验证
如果您使用的是自定义的 Milvus 服务器，您可以通过多种方式提供您的认证。
环境变量（推荐）
配置 Milvus 认证的推荐方式是将其存储在下图所示的环境变量中，每当与 Milvus 建立连接时，FiftyOne 都会自动访问这些变量。
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_URI=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_USER=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_PASSWORD=XXXXXX
# also available if necessary
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_SECURE=true
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_TOKEN=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_DB_NAME=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_CLIENT_KEY_PATH=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_CLIENT_PEM_PATH=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_CA_PEM_PATH=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_SERVER_PEM_PATH=XXXXXX
export FIFTYONE_BRAIN_SIMILARITY_MILVUS_SERVER_NAME=XXXXXX
FiftyOne 大脑配置
您也可以将凭据存储在位于
~/.fiftyone/brain_config.json
的
大脑配置
中：
{
"similarity_backends"
: {
"milvus"
: {
"uri"
:
"XXXXXX"
,
"user"
:
"XXXXXX"
,
"password"
:
"XXXXXX"
,
# also available if necessary
"secure"
: true,
"token"
:
"XXXXXX"
,
"db_name"
:
"XXXXXX"
,
"client_key_path"
:
"XXXXXX"
,
"client_pem_path"
:
"XXXXXX"
,
"ca_pem_path"
:
"XXXXXX"
,
"server_pem_path"
:
"XXXXXX"
,
"server_name"
:
"XXXXXX"
}
    }
}
请注意，这个文件在您创建之前并不存在。
关键字参数
每次调用需要连接到 Milvus 的方法时，您可以手动提供您的 Milvus 认证作为关键字参数。
compute_similarity()
等需要连接 Milvus 的方法时，您都可以手动提供 Milvus 凭据作为关键字参数：
import
fiftyone.brain
as
fob

milvus_index = fob.compute_similarity(
    ...
    backend=
"milvus"
,
    brain_key=
"milvus_index"
,
    uri=
"XXXXXX"
,
    user=
"XXXXXX"
,
    password=
"XXXXXX"
,
# also available if necessary
secure=
True
,
    token=
"XXXXXX"
,
    db_name=
"XXXXXX"
,
    client_key_path=
"XXXXXX"
,
    client_pem_path=
"XXXXXX"
,
    ca_pem_path=
"XXXXXX"
,
    server_pem_path=
"XXXXXX"
,
    server_name=
"XXXXXX"
,
)
请注意，使用此策略时，您必须在以后通过
load_brain_results()
:
milvus_index = dataset.load_brain_results(
"milvus_index"
,
    uri=
"XXXXXX"
,
    user=
"XXXXXX"
,
    password=
"XXXXXX"
,
# also available if necessary
secure=
True
,
    token=
"XXXXXX"
,
    db_name=
"XXXXXX"
,
    client_key_path=
"XXXXXX"
,
    client_pem_path=
"XXXXXX"
,
    ca_pem_path=
"XXXXXX"
,
    server_pem_path=
"XXXXXX"
,
    server_name=
"XXXXXX"
,
)
Milvus 配置参数
Milvus 后端支持多种查询参数，可用于自定义相似性查询。这些参数包括
collection_
name（无
）：要使用或创建的 Milvus Collection 的名称。如果没有提供，将创建一个新的 Collections
metric
（
"dotproduct"）
：创建新索引时使用的嵌入距离度量。支持的值是 (
"dotproduct"
,
"euclidean"
)
consistency_level
（
"会话"）
：要使用的一致性级别。支持的值有 (
"Strong"
,
"Session"
,
"Bounded"
,
"Eventually"
)
有关这些参数的详细信息，请参阅
Milvus 身份验证文档
和
Milvus 一致性级别文档
。
你可以通过上一节描述的任何策略来指定这些参数。下面是一个包含所有可用参数的
大脑配置
示例：
{
"similarity_backends"
:
{
"milvus"
:
{
"collection_name"
:
"your_collection"
,
"metric"
:
"dotproduct"
,
"consistency_level"
:
"Strong"
}
}
}
不过，通常这些参数会直接传递给
compute_similarity()
来配置特定的新索引：
milvus_index = fob.compute_similarity(
    ...
    backend=
"milvus"
,
    brain_key=
"milvus_index"
,
    collection_name=
"your_collection"
,
    metric=
"dotproduct"
,
    consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
)
管理大脑运行
FiftyOne 提供了多种方法，你可以用来管理大脑运行。
例如，你可以调用
list_brain_runs()
来查看数据集上可用的脑键：
import
fiftyone.brain
as
fob
# List all brain runs
dataset.list_brain_runs()
# Only list similarity runs
dataset.list_brain_runs(
type
=fob.Similarity)
# Only list specific similarity runs
dataset.list_brain_runs(
type
=fob.Similarity,
    patches_field=
"ground_truth"
,
    supports_prompts=
True
,
)
或使用
get_brain_info()
检索大脑运行的配置信息：
info = dataset.get_brain_info(brain_key)
print
(info)
使用
load_brain_results()
加载
SimilarityIndex
实例。
您可以使用
rename_brain_run()
重命名与现有相似性结果运行相关的大脑密钥：
dataset.rename_brain_run(brain_key, new_brain_key)
最后，可以使用
delete_brain_run()
删除大脑运行：
dataset.delete_brain_run(brain_key)
调用
delete_brain_run()
只会删除 FiftyOne 数据集中的大脑运行记录，而不会删除任何相关的 Milvus Collections：
# Delete the Milvus collection
milvus_index = dataset.load_brain_results(brain_key)
milvus_index.cleanup()
有关使用 Milvus 后端在 FiftyOne 数据集上进行常见向量搜索的工作流程，请参阅
此处的示例
。