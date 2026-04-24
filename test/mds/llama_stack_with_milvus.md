与 Milvus 一起使用 Llama Stack 构建 RAG
Llama Stack
是一种面向服务、API 优先的方法，用于构建生产型人工智能应用程序。它提供了一个通用堆栈，允许开发人员随时随地进行开发、部署，并利用生产就绪的构建模块，实现真正的提供商独立性。Llama Stack 重点关注 Meta 的 Llama 模型、可组合性、生产就绪性和合作生态系统。
在本教程中，我们将介绍如何构建一个配置有 Milvus 的 Llama Stack 服务器，使您能够导入您的私有数据作为您的知识库。然后，我们将在服务器上执行查询，创建一个完整的 RAG 应用程序。
准备环境
启动 Llama Stack 服务器有多种方式，例如
作为库
、
构建发行版
等。对于 Llama Stack 中的每个组件，还可以选择不同的提供程序。因此，启动 Llama Stack 服务器的方法有很多种。
本教程使用以下配置作为启动服务的示例。如果希望以其他方式启动，请参阅《
启动 Llama Stack 服务器
》。
我们使用 Conda 构建一个带有 Milvus 配置的自定义 Distributed。
我们使用
Together AI
作为 LLM 提供商。
我们使用默认的
all-MiniLM-L6-v2
作为 Embeddings 模型。
本教程主要参考了
Llama Stack 文档
的官方安装指南。如果你在本教程中发现任何过时的部分，可以优先参考官方指南，并为我们创建一个问题。
启动 Llama Stack 服务器
准备环境
由于我们需要使用 Together AI 作为 LLM 服务，因此必须先登录官方网站申请
API 密钥
，并将 API 密钥
TOGETHER_API_KEY
设置为环境变量。
克隆 Llama Stack 源代码
$ git
clone
https://github.com/meta-llama/llama-stack.git
$
cd
llama-stack
创建 conda 环境并安装依赖项
$ conda create -n stack python=3.10
$ conda activate stack

$ pip install -e .
修改
llama_stack/llama_stack/template/together/run.yaml
中的内容，将 vector_io 部分改为相关的 Milvus 配置。例如，添加
vector_io:
-
provider_id:
milvus
provider_type:
inline::milvus
config:
db_path:
~/.llama/distributions/together/milvus_store.db
#  - provider_id: milvus
#    provider_type: remote::milvus
#    config:
#      uri: http://localhost:19530
#      token: root:Milvus
在 Llama Stack 中，Milvus 有两种配置方式：本地配置，即
inline::milvus
；远程配置，即
remote::milvus
。
最简单的方法是本地配置，需要设置
db_path
，这是本地存储
Milvus-Lite
文件的路径。
远程配置适用于大量数据存储。
如果数据量较大，可以在
Docker 或 Kubernetes
上设置性能良好的 Milvus 服务器。在此设置中，请使用服务器 URI，如
http://localhost:19530
，作为您的
uri
。默认的
token
是
root:Milvus
。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们对应于 Zilliz Cloud 中的
公共端点和 API 密钥
。
从模板构建分发版
运行以下命令构建分发版：
$ llama stack build --template together --image-type conda
将在
~/.llama/distributions/together/together-run.yaml
生成一个文件。然后，运行此命令启动服务器：
$ llama stack run --image-type conda ~/.llama/distributions/together/together-run.yaml
如果一切顺利，您将看到 Llama Stack 服务器在 8321 端口成功运行。
从客户端执行 RAG
启动服务器后，就可以编写客户端代码来访问服务器了。下面是一段示例代码：
import
uuid
from
llama_stack_client.types
import
Document
from
llama_stack_client.lib.agents.agent
import
Agent
from
llama_stack_client.types.agent_create_params
import
AgentConfig
# See https://www.together.ai/models for all available models
INFERENCE_MODEL =
"meta-llama/Llama-3.3-70B-Instruct-Turbo"
LLAMA_STACK_PORT =
8321
def
create_http_client
():
from
llama_stack_client
import
LlamaStackClient
return
LlamaStackClient(
        base_url=
f"http://localhost:
{LLAMA_STACK_PORT}
"
# Your Llama Stack Server URL
)


client = create_http_client()
# Documents to be used for RAG
urls = [
"chat.rst"
,
"llama3.rst"
,
"memory_optimizations.rst"
,
"lora_finetune.rst"
]
documents = [
    Document(
        document_id=
f"num-
{i}
"
,
        content=
f"https://raw.githubusercontent.com/pytorch/torchtune/main/docs/source/tutorials/
{url}
"
,
        mime_type=
"text/plain"
,
        metadata={},
    )
for
i, url
in
enumerate
(urls)
]
# Register a vector database
vector_db_id =
f"test-vector-db-
{uuid.uuid4().
hex
}
"
client.vector_dbs.register(
    vector_db_id=vector_db_id,
    embedding_model=
"all-MiniLM-L6-v2"
,
    embedding_dimension=
384
,
    provider_id=
"milvus"
,
)
print
(
"inserting..."
)
# Insert the documents into the vector database
client.tool_runtime.rag_tool.insert(
    documents=documents, vector_db_id=vector_db_id, chunk_size_in_tokens=
1024
,
)

agent_config = AgentConfig(
    model=INFERENCE_MODEL,
# Define instructions for the agent ( aka system prompt)
instructions=
"You are a helpful assistant"
,
    enable_session_persistence=
False
,
# Define tools available to the agent
toolgroups=[{
"name"
:
"builtin::rag"
,
"args"
: {
"vector_db_ids"
: [vector_db_id]}}],
)

rag_agent = Agent(client, agent_config)
session_id = rag_agent.create_session(
"test-session"
)
print
(
"finish init agent..."
)
user_prompt = (
"What are the top 5 topics that were explained? Only list succinct bullet points."
)
# Get the final answer from the agent
response = rag_agent.create_turn(
    messages=[{
"role"
:
"user"
,
"content"
: user_prompt}],
    session_id=session_id,
    stream=
False
,
)
print
(
f"Response: "
)
print
(response.output_message.content)
运行此代码执行 RAG 查询。 如果一切正常，输出结果应该如下所示：
inserting...
finish init agent...
Response: 
* Fine-Tuning Llama3 with Chat Data
* Evaluating fine-tuned Llama3-8B models with EleutherAI's Eval Harness
* Generating text with our fine-tuned Llama3 model
* Faster generation via quantization
* Fine-tuning on a custom chat dataset