高级视频搜索：利用 Twelve Labs 和 Milvus 进行语义检索
简介
欢迎阅读本综合教程，了解如何使用
Twelve Labs Embed API
和 Milvus 实现语义视频搜索。在本指南中，我们将探讨如何利用
Twelve Labs先进的多模态嵌入
和
Milvus高效的向量数据库
来创建强大的视频搜索解决方案。通过整合这些技术，开发人员可以开启视频内容分析的新可能性，实现基于内容的视频检索、推荐系统和能够理解视频数据细微差别的复杂搜索引擎等应用。
本教程将指导您完成从设置开发环境到实施功能性语义视频搜索应用程序的整个过程。我们将介绍一些关键概念，例如从视频中生成多模态 Embeddings、在 Milvus 中高效存储这些嵌入以及执行相似性搜索以检索相关内容。无论您是要构建视频分析平台、内容发现工具，还是要利用视频搜索功能增强现有应用程序，本指南都将为您提供相关知识和实用步骤，帮助您在项目中充分利用 Twelve Labs 和 Milvus 的综合优势。
前提条件
在我们开始之前，请确保您具备以下条件：
Twelve Labs API 密钥（如果没有，请登录 https://api.twelvelabs.io） 系统上已安装 Python 3.7 或更高版本
设置开发环境
为您的项目创建一个新目录并导航至该目录：
mkdir video-search-tutorial
cd video-search-tutorial
设置虚拟环境（可选但推荐）：
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
安装所需的 Python 库：
pip install twelvelabs pymilvus
为项目创建一个新的 Python 文件：
touch video_search.py
这个 video_search.py 文件将是我们在教程中使用的主要脚本。接下来，将 Twelve Labs API 密钥设置为环境变量，以确保安全：
export TWELVE_LABS_API_KEY='your_api_key_here'
连接 Milvus
要与 Milvus 建立连接，我们将使用 MilvusClient 类。这种方法简化了连接过程，并允许我们使用基于本地文件的 Milvus 实例，非常适合我们的教程。
from
pymilvus
import
MilvusClient
# Initialize the Milvus client
milvus_client = MilvusClient(
"milvus_twelvelabs_demo.db"
)
print
(
"Successfully connected to Milvus"
)
这段代码创建了一个新的 Milvus 客户端实例，它将把所有数据存储在一个名为 milvus_twelvelabs_demo.db 的文件中。这种基于文件的方法非常适合开发和测试目的。
创建用于视频 Embeddings 的 Milvus Collections
现在我们已经连接到 Milvus，让我们创建一个 Collections 来存储视频 Embeddings 和相关元数据。我们将定义 Collections Schema，如果还不存在，则创建该 Collection。
# Initialize the collection name
collection_name =
"twelvelabs_demo_collection"
# Check if the collection already exists and drop it if it does
if
milvus_client.has_collection(collection_name=collection_name):
    milvus_client.drop_collection(collection_name=collection_name)
# Create the collection
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=
1024
# The dimension of the Twelve Labs embeddings
)
print
(
f"Collection '
{collection_name}
' created successfully"
)
在这段代码中，我们首先检查 Collection 是否已经存在，如果存在，则删除它。这样可以确保我们从一个干净的环境开始。我们创建的 Collections 维度为 1024，与 Twelve Labs 的嵌入输出维度一致。
使用 Twelve Labs 的嵌入式 API 生成嵌入词
为了使用 Twelve Labs Embed API 为视频生成嵌入式内容，我们将使用 Twelve Labs Python SDK。这个过程包括创建一个 Embeddings 任务，等待任务完成，然后检索结果。以下是实现方法：
首先，确保已安装 Twelve Labs SDK，并导入必要的模块：
from
twelvelabs
import
TwelveLabs
from
twelvelabs.models.embed
import
EmbeddingsTask
import
os
# Retrieve the API key from environment variables
TWELVE_LABS_API_KEY = os.getenv(
'TWELVE_LABS_API_KEY'
)
初始化 Twelve Labs 客户端：
twelvelabs_client = TwelveLabs(api_key=TWELVE_LABS_API_KEY)
创建一个函数，为给定的视频 URL 生成 Embeddings：
def
generate_embedding
(
video_url
):
"""
    Generate embeddings for a given video URL using the Twelve Labs API.

    This function creates an embedding task for the specified video URL using
    the Marengo-retrieval-2.6 engine. It monitors the task progress and waits
    for completion. Once done, it retrieves the task result and extracts the
    embeddings along with their associated metadata.

    Args:
        video_url (str): The URL of the video to generate embeddings for.

    Returns:
        tuple: A tuple containing two elements:
            1. list: A list of dictionaries, where each dictionary contains:
                - 'embedding': The embedding vector as a list of floats.
                - 'start_offset_sec': The start time of the segment in seconds.
                - 'end_offset_sec': The end time of the segment in seconds.
                - 'embedding_scope': The scope of the embedding (e.g., 'shot', 'scene').
            2. EmbeddingsTaskResult: The complete task result object from Twelve Labs API.

    Raises:
        Any exceptions raised by the Twelve Labs API during task creation,
        execution, or retrieval.
    """
# Create an embedding task
task = twelvelabs_client.embed.task.create(
        engine_name=
"Marengo-retrieval-2.6"
,
        video_url=video_url
    )
print
(
f"Created task: id=
{task.
id
}
engine_name=
{task.engine_name}
status=
{task.status}
"
)
# Define a callback function to monitor task progress
def
on_task_update
(
task: EmbeddingsTask
):
print
(
f"  Status=
{task.status}
"
)
# Wait for the task to complete
status = task.wait_for_done(
        sleep_interval=
2
,
        callback=on_task_update
    )
print
(
f"Embedding done:
{status}
"
)
# Retrieve the task result
task_result = twelvelabs_client.embed.task.retrieve(task.
id
)
# Extract and return the embeddings
embeddings = []
for
v
in
task_result.video_embeddings:
        embeddings.append({
'embedding'
: v.embedding.
float
,
'start_offset_sec'
: v.start_offset_sec,
'end_offset_sec'
: v.end_offset_sec,
'embedding_scope'
: v.embedding_scope
        })
return
embeddings, task_result
使用该函数为视频生成 Embeddings：
# Example usage
video_url =
"https://example.com/your-video.mp4"
# Generate embeddings for the video
embeddings, task_result = generate_embedding(video_url)
print
(
f"Generated
{
len
(embeddings)}
embeddings for the video"
)
for
i, emb
in
enumerate
(embeddings):
print
(
f"Embedding
{i+
1
}
:"
)
print
(
f"  Scope:
{emb[
'embedding_scope'
]}
"
)
print
(
f"  Time range:
{emb[
'start_offset_sec'
]}
-
{emb[
'end_offset_sec'
]}
seconds"
)
print
(
f"  Embedding vector (first 5 values):
{emb[
'embedding'
][:
5
]}
"
)
print
()
该实现允许您使用 Twelve Labs Embed API 为任何视频 URL 生成嵌入式内容。generate_embedding 函数负责处理从创建任务到获取结果的整个过程。它会返回一个字典列表，每个字典都包含一个嵌入向量及其元数据（时间范围和范围）。在生产环境中，切记要处理潜在的错误，如网络问题或 API 限制。根据具体的使用情况，您可能还需要执行重试或更强大的错误处理。
将嵌入式数据插入 Milvus
使用 Twelve Labs Embed API 生成嵌入式数据后，下一步就是将这些嵌入式数据及其元数据插入 Milvus Collections。通过这一过程，我们可以存储和索引我们的视频 embeddings，以便日后进行高效的相似性搜索。
下面介绍如何将嵌入式数据插入 Milvus：
def
insert_embeddings
(
milvus_client, collection_name, task_result, video_url
):
"""
    Insert embeddings into the Milvus collection.

    Args:
        milvus_client: The Milvus client instance.
        collection_name (str): The name of the Milvus collection to insert into.
        task_result (EmbeddingsTaskResult): The task result containing video embeddings.
        video_url (str): The URL of the video associated with the embeddings.

    Returns:
        MutationResult: The result of the insert operation.

    This function takes the video embeddings from the task result and inserts them
    into the specified Milvus collection. Each embedding is stored with additional
    metadata including its scope, start and end times, and the associated video URL.
    """
data = []
for
i, v
in
enumerate
(task_result.video_embeddings):
        data.append({
"id"
: i,
"vector"
: v.embedding.
float
,
"embedding_scope"
: v.embedding_scope,
"start_offset_sec"
: v.start_offset_sec,
"end_offset_sec"
: v.end_offset_sec,
"video_url"
: video_url
        })

    insert_result = milvus_client.insert(collection_name=collection_name, data=data)
print
(
f"Inserted
{
len
(data)}
embeddings into Milvus"
)
return
insert_result
# Usage example
video_url =
"https://example.com/your-video.mp4"
# Assuming this function exists from previous step
embeddings, task_result = generate_embedding(video_url)
# Insert embeddings into the Milvus collection
insert_result = insert_embeddings(milvus_client, collection_name, task_result, video_url)
print
(insert_result)
该函数准备插入数据，包括嵌入向量、时间范围和源视频 URL 等所有相关元数据。然后，它使用 Milvus 客户端将这些数据插入指定的 Collections。
执行相似性搜索
将嵌入向量存储到 Milvus 后，我们就可以执行相似性搜索，根据查询向量找到最相关的视频片段。下面是实现这一功能的方法：
def
perform_similarity_search
(
milvus_client, collection_name, query_vector, limit=
5
):
"""
    Perform a similarity search on the Milvus collection.

    Args:
        milvus_client: The Milvus client instance.
        collection_name (str): The name of the Milvus collection to search in.
        query_vector (list): The query vector to search for similar embeddings.
        limit (int, optional): The maximum number of results to return. Defaults to 5.

    Returns:
        list: A list of search results, where each result is a dictionary containing
              the matched entity's metadata and similarity score.

    This function searches the specified Milvus collection for embeddings similar to
    the given query vector. It returns the top matching results, including metadata
    such as the embedding scope, time range, and associated video URL for each match.
    """
search_results = milvus_client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=limit,
        output_fields=[
"embedding_scope"
,
"start_offset_sec"
,
"end_offset_sec"
,
"video_url"
]
    )
return
search_results
# define the query vector
# We use the embedding inserted previously as an example. In practice, you can replace it with any video embedding you want to query.
query_vector = task_result.video_embeddings[
0
].embedding.
float
# Perform a similarity search on the Milvus collection
search_results = perform_similarity_search(milvus_client, collection_name, query_vector)
print
(
"Search Results:"
)
for
i, result
in
enumerate
(search_results[
0
]):
print
(
f"Result
{i+
1
}
:"
)
print
(
f"  Video URL:
{result[
'entity'
][
'video_url'
]}
"
)
print
(
f"  Time Range:
{result[
'entity'
][
'start_offset_sec'
]}
-
{result[
'entity'
][
'end_offset_sec'
]}
seconds"
)
print
(
f"  Similarity Score:
{result[
'distance'
]}
"
)
print
()
该实现方法如下
定义一个 perform_similarity_search 函数，该函数接收一个查询向量，并在 Milvus Collections 中搜索相似的嵌入。
使用 Milvus 客户端的搜索方法来查找最相似的向量。
指定我们要检索的输出字段，包括匹配视频片段的元数据。
举例说明如何在查询视频中使用此函数，首先生成其 Embeddings，然后使用它进行搜索。
打印搜索结果，包括相关元数据和相似度得分。
通过执行这些函数，您就创建了一个完整的工作流程，用于在 Milvus 中存储视频嵌入并执行相似性搜索。这种设置可根据 Twelve Labs 的 Embeddings API 生成的多模态嵌入信息，高效检索相似的视频内容。
优化性能
好了，让我们将这款应用提升到一个新的水平！在处理大规模视频 Collections 时，
性能是关键
。为了优化性能，我们应该对
嵌入生成和插入 Milvus 进行批处理
。这样，我们就可以同时处理多个视频，大大减少整体处理时间。此外，我们还可以利用
Milvus 的分区功能
来更有效地组织数据，也许可以按照视频类别或时间段来组织数据。这样，我们就可以只搜索相关的分区，从而加快查询速度。
另一个优化技巧是
对经常访问的 Embeddings 或搜索结果使用缓存机制
。这可以显著改善常用查询的响应时间。不要忘记根据你的特定数据集和查询模式
对 Milvus 的索引参数
进行微调--这里的微调可以大大提高搜索性能。
高级功能
现在，让我们添加一些很酷的功能，让我们的应用程序脱颖而出！我们可以实现
混合搜索，将文本和视频查询结合起来
。事实上，
Twelve Labs Embeddings API 还能为您的文本查询生成文本嵌入
。想象一下，允许用户输入文字描述和视频片段示例，我们就能为两者生成 Embeddings，并在 Milvus 中执行加权搜索。这将为我们提供超级精确的结果。
另一个很棒的功能是
在视频中进行时间搜索
。
我们可以将长视频分解成更小的片段，每个片段都有自己的 Embeddings
。这样，用户就可以找到视频中的特定时刻，而不仅仅是整个片段。还有，为什么不加入一些基本的视频分析功能呢？我们可以使用 Embeddings 对相似的视频片段进行聚类，检测趋势，甚至识别大型视频 Collections 中的异常值。
错误处理和日志记录
面对现实吧，事情可能会出错，一旦出错，我们需要做好准备。
实施强大的错误处理至关重要
。我们应该
在 try-except 块中封装 API 调用和数据库操作
，并在出现故障时向用户提供翔实的错误信息。对于与网络相关的问题，
使用指数级延迟重试
有助于从容应对临时故障。
至于日志，它是我们调试和监控的好朋友
。我们应该使用
Python 的日志模块
来跟踪整个应用程序中的重要事件、错误和性能指标。让我们设置不同的日志级别 - DEBUG 用于开发，INFO 用于一般操作，ERROR 用于关键问题。此外，别忘了实施日志轮换以管理文件大小。有了适当的日志记录，我们就能快速识别和解决问题，确保我们的视频搜索应用程序在扩展时也能顺利运行。
总结
恭喜您！您现在已经使用 Twelve Labs 的嵌入式 API 和 Milvus 构建了一个功能强大的语义视频搜索应用程序。这种集成使您能够以前所未有的准确性和效率处理、存储和检索视频内容。通过利用多模态 Embeddings，您创建了一个能够理解视频数据细微差别的系统，为内容发现、推荐系统和高级视频分析开辟了令人兴奋的可能性。
当您继续开发和完善您的应用时，请记住，Twelve Labs 先进的嵌入生成和 Milvus 可扩展的向量存储相结合，为应对更复杂的视频理解挑战奠定了坚实的基础。我们鼓励您尝试使用所讨论的高级功能，不断突破视频搜索和分析的极限。