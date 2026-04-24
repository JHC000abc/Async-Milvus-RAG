使用 Milvus 和 Camel 的检索增强生成 (RAG) 系统
本指南演示了如何使用 Camel 和 Milvus 构建检索-增强生成（RAG）系统。
RAG 系统将检索系统与生成模型相结合，根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
Camel
是一个多 Agents 框架。
Milvus
是世界上最先进的开源向量数据库，专为支持 Embeddings 相似性搜索和人工智能应用而构建。
在本笔记本中，我们将展示 CAMEL 检索模块的定制方式和自动方式的用法。我们还将展示如何将
AutoRetriever
与
ChatAgent
结合起来，并通过使用
Function Calling
进一步将
AutoRetriever
与
RolePlaying
结合起来。
包括 4 个主要部分：
自定义 RAG
自动 RAG
使用自动 RAG 的单个 Agents
使用自动 RAG 进行角色扮演
加载数据
让我们首先从 https://arxiv.org/pdf/2303.17760.pdf 加载 Camel 文件。这将是我们的本地示例数据。
$ pip install -U
"camel-ai[all]"
pymilvus milvus-lite
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重新启动运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重新启动会话"）。
import
os
import
requests

os.makedirs(
"local_data"
, exist_ok=
True
)

url =
"https://arxiv.org/pdf/2303.17760.pdf"
response = requests.get(url)
with
open
(
"local_data/camel paper.pdf"
,
"wb"
)
as
file:
    file.write(response.content)
1.自定义 RAG
在本节中，我们将设置自定义 RAG 管道，以
VectorRetriever
为例。我们将把
OpenAIEmbedding
设置为嵌入模型，把
MilvusStorage
设置为其存储空间。
要设置 OpenAI 嵌入，我们需要设置
OPENAI_API_KEY
。
os.environ[
"OPENAI_API_KEY"
] =
"Your Key"
导入并设置嵌入实例：
from
camel.embeddings
import
OpenAIEmbedding

embedding_instance = OpenAIEmbedding()
导入并设置向量存储实例：
from
camel.storages
import
MilvusStorage

storage_instance = MilvusStorage(
    vector_dim=embedding_instance.get_output_dim(),
    url_and_api_key=(
"./milvus_demo.db"
,
# Your Milvus connection URI
""
,
# Your Milvus token
),
    collection_name=
"camel_paper"
,
)
对于
url_and_api_key
：
使用本地文件，例如
./milvus.db
，作为 Milvus 连接 URI 是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在此文件中。
如果数据规模较大，可以在
docker 或 kubernetes
上设置性能更强的 Milvus 服务器。在这种设置中，请使用服务器 uri（例如
http://localhost:19530
）作为您的 url。
如果你想使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整连接 uri 和令牌，它们与 Zilliz Cloud 中的
公共端点和 Api 密钥
相对应。
导入并设置检索器实例：
默认情况下，
similarity_threshold
设置为 0.75。您可以更改。
from
camel.retrievers
import
VectorRetriever

vector_retriever = VectorRetriever(
    embedding_model=embedding_instance, storage=storage_instance
)
我们使用集成的
Unstructured Module
将内容分割成小块，内容将通过
chunk_by_title
功能自动分割，每个小块的最大字符数为 500 字符，这是
OpenAIEmbedding
的合适长度。分块中的所有文本将被嵌入并存储到向量存储实例中，这需要一些时间，请稍候。
vector_retriever.process(content_input_path=
"local_data/camel paper.pdf"
)
[nltk_data] Downloading package punkt to /root/nltk_data...
[nltk_data]   Unzipping tokenizers/punkt.zip.
[nltk_data] Downloading package averaged_perceptron_tagger to
[nltk_data]     /root/nltk_data...
[nltk_data]   Unzipping taggers/averaged_perceptron_tagger.zip.
现在，我们可以通过查询从向量存储中获取信息。默认情况下，它会返回余弦相似度得分最高的前 1 个块中的文本内容，相似度得分应高于 0.75，以确保检索到的内容与查询相关。您也可以更改
top_k
值。
返回的字符串列表包括
相似度得分
内容路径
元数据
文本
retrieved_info = vector_retriever.query(query=
"What is CAMEL?"
, top_k=
1
)
print
(retrieved_info)
[{'similarity score': '0.8321675658226013', 'content path': 'local_data/camel paper.pdf', 'metadata': {'last_modified': '2024-04-19T14:40:00', 'filetype': 'application/pdf', 'page_number': 45}, 'text': 'CAMEL Data and Code License The intended purpose and licensing of CAMEL is solely for research use. The source code is licensed under Apache 2.0. The datasets are licensed under CC BY NC 4.0, which permits only non-commercial usage. It is advised that any models trained using the dataset should not be utilized for anything other than research purposes.\n\n45'}]
让我们试试不相关的查询：
retrieved_info_irrelevant = vector_retriever.query(
    query=
"Compared with dumpling and rice, which should I take for dinner?"
, top_k=
1
)
print
(retrieved_info_irrelevant)
[{'text': 'No suitable information retrieved from local_data/camel paper.pdf                 with similarity_threshold = 0.75.'}]
2.自动 RAG
在本节中，我们将使用默认设置运行
AutoRetriever
。它使用
OpenAIEmbedding
作为默认嵌入模型，使用
Milvus
作为默认向量存储。
您需要做的是
设置内容输入路径，可以是本地路径或远程网址
为 Milvus 设置远程网址和 api 密钥
提供查询
自动 RAG 管道将为给定的内容输入路径创建 Collections，Collection 名称将根据内容输入路径名称自动设置，如果该 Collections 存在，它将直接进行检索。
from
camel.retrievers
import
AutoRetriever
from
camel.types
import
StorageType

auto_retriever = AutoRetriever(
    url_and_api_key=(
"./milvus_demo.db"
,
# Your Milvus connection URI
""
,
# Your Milvus token
),
    storage_type=StorageType.MILVUS,
    embedding_model=embedding_instance,
)

retrieved_info = auto_retriever.run_vector_retriever(
    query=
"What is CAMEL-AI"
,
    content_input_paths=[
"local_data/camel paper.pdf"
,
# example local path
"https://www.camel-ai.org/"
,
# example remote url
],
    top_k=
1
,
    return_detailed_info=
True
,
)
print
(retrieved_info)
Original Query:
{What is CAMEL-AI}
Retrieved Context:
{'similarity score': '0.8252888321876526', 'content path': 'local_data/camel paper.pdf', 'metadata': {'last_modified': '2024-04-19T14:40:00', 'filetype': 'application/pdf', 'page_number': 7}, 'text': ' Section 3.2, to simulate assistant-user cooperation. For our analysis, we set our attention on AI Society setting. We also gathered conversational data, named CAMEL AI Society and CAMEL Code datasets and problem-solution pairs data named CAMEL Math and CAMEL Science and analyzed and evaluated their quality. Moreover, we will discuss potential extensions of our framework and highlight both the risks and opportunities that future AI society might present.'}
{'similarity score': '0.8378663659095764', 'content path': 'https://www.camel-ai.org/', 'metadata': {'filetype': 'text/html', 'languages': ['eng'], 'page_number': 1, 'url': 'https://www.camel-ai.org/', 'link_urls': ['#h.3f4tphhd9pn8', 'https://join.slack.com/t/camel-ai/shared_invite/zt-2g7xc41gy-_7rcrNNAArIP6sLQqldkqQ', 'https://discord.gg/CNcNpquyDc'], 'link_texts': [None, None, None], 'emphasized_text_contents': ['Mission', 'CAMEL-AI.org', 'is an open-source community dedicated to the study of autonomous and communicative agents. We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks. To facilitate research in this field, we provide, implement, and support various types of agents, tasks, prompts, models, datasets, and simulated environments.', 'Join us via', 'Slack', 'Discord', 'or'], 'emphasized_text_tags': ['span', 'span', 'span', 'span', 'span', 'span', 'span']}, 'text': 'Mission\n\nCAMEL-AI.org is an open-source community dedicated to the study of autonomous and communicative agents. We believe that studying these agents on a large scale offers valuable insights into their behaviors, capabilities, and potential risks. To facilitate research in this field, we provide, implement, and support various types of agents, tasks, prompts, models, datasets, and simulated environments.\n\nJoin us via\n\nSlack\n\nDiscord\n\nor'}
3.带有自动 RAG 的单一 Agents
在本节中，我们将展示如何将
AutoRetriever
与一个
ChatAgent
结合起来。
让我们设置一个 Agents 函数，在该函数中，我们可以通过向该代理提供查询来获取响应。
from
camel.agents
import
ChatAgent
from
camel.messages
import
BaseMessage
from
camel.types
import
RoleType
from
camel.retrievers
import
AutoRetriever
from
camel.types
import
StorageType
def
single_agent
(
query:
str
) ->
str
:
# Set agent role
assistant_sys_msg = BaseMessage(
        role_name=
"Assistant"
,
        role_type=RoleType.ASSISTANT,
        meta_dict=
None
,
        content=
"""You are a helpful assistant to answer question,
         I will give you the Original Query and Retrieved Context,
        answer the Original Query based on the Retrieved Context,
        if you can't answer the question just say I don't know."""
,
    )
# Add auto retriever
auto_retriever = AutoRetriever(
        url_and_api_key=(
"./milvus_demo.db"
,
# Your Milvus connection URI
""
,
# Your Milvus token
),
        storage_type=StorageType.MILVUS,
        embedding_model=embedding_instance,
    )

    retrieved_info = auto_retriever.run_vector_retriever(
        query=query,
        content_input_paths=[
"local_data/camel paper.pdf"
,
# example local path
"https://www.camel-ai.org/"
,
# example remote url
],
# vector_storage_local_path="storage_default_run",
top_k=
1
,
        return_detailed_info=
True
,
    )
# Pass the retrieved infomation to agent
user_msg = BaseMessage.make_user_message(role_name=
"User"
, content=retrieved_info)
    agent = ChatAgent(assistant_sys_msg)
# Get response
assistant_response = agent.step(user_msg)
return
assistant_response.msg.content
print
(single_agent(
"What is CAMEL-AI"
))
CAMEL-AI is an open-source community dedicated to the study of autonomous and communicative agents. It provides, implements, and supports various types of agents, tasks, prompts, models, datasets, and simulated environments to facilitate research in this field.
4.使用自动 RAG 进行角色扮演
在本节中，我们将展示如何通过应用
Function Calling
将
RETRIEVAL_FUNCS
与
RolePlaying
结合起来。
from
typing
import
List
from
colorama
import
Fore
from
camel.agents.chat_agent
import
FunctionCallingRecord
from
camel.configs
import
ChatGPTConfig
from
camel.functions
import
(
    MATH_FUNCS,
    RETRIEVAL_FUNCS,
)
from
camel.societies
import
RolePlaying
from
camel.types
import
ModelType
from
camel.utils
import
print_text_animated
def
role_playing_with_rag
(
task_prompt, model_type=ModelType.GPT_4O, chat_turn_limit=
10
) ->
None
:
    task_prompt = task_prompt

    user_model_config = ChatGPTConfig(temperature=
0.0
)

    function_list = [
        *MATH_FUNCS,
        *RETRIEVAL_FUNCS,
    ]
    assistant_model_config = ChatGPTConfig(
        tools=function_list,
        temperature=
0.0
,
    )

    role_play_session = RolePlaying(
        assistant_role_name=
"Searcher"
,
        user_role_name=
"Professor"
,
        assistant_agent_kwargs=
dict
(
            model_type=model_type,
            model_config=assistant_model_config,
            tools=function_list,
        ),
        user_agent_kwargs=
dict
(
            model_type=model_type,
            model_config=user_model_config,
        ),
        task_prompt=task_prompt,
        with_task_specify=
False
,
    )
print
(
        Fore.GREEN
        +
f"AI Assistant sys message:\n
{role_play_session.assistant_sys_msg}
\n"
)
print
(Fore.BLUE +
f"AI User sys message:\n
{role_play_session.user_sys_msg}
\n"
)
print
(Fore.YELLOW +
f"Original task prompt:\n
{task_prompt}
\n"
)
print
(
        Fore.CYAN
        +
f"Specified task prompt:\n
{role_play_session.specified_task_prompt}
\n"
)
print
(Fore.RED +
f"Final task prompt:\n
{role_play_session.task_prompt}
\n"
)

    n =
0
input_msg = role_play_session.init_chat()
while
n < chat_turn_limit:
        n +=
1
assistant_response, user_response = role_play_session.step(input_msg)
if
assistant_response.terminated:
print
(
                Fore.GREEN
                + (
"AI Assistant terminated. Reason: "
f"
{assistant_response.info[
'termination_reasons'
]}
."
)
            )
break
if
user_response.terminated:
print
(
                Fore.GREEN
                + (
"AI User terminated. "
f"Reason:
{user_response.info[
'termination_reasons'
]}
."
)
            )
break
# Print output from the user
print_text_animated(Fore.BLUE +
f"AI User:\n\n
{user_response.msg.content}
\n"
)
# Print output from the assistant, including any function
# execution information
print_text_animated(Fore.GREEN +
"AI Assistant:"
)
        tool_calls:
List
[FunctionCallingRecord] = assistant_response.info[
"tool_calls"
]
for
func_record
in
tool_calls:
            print_text_animated(
f"
{func_record}
"
)
        print_text_animated(
f"
{assistant_response.msg.content}
\n"
)
if
"CAMEL_TASK_DONE"
in
user_response.msg.content:
break
input_msg = assistant_response.msg
使用定义的检索器函数运行角色扮演：
role_playing_with_rag(
    task_prompt=
"""What is the main termination reasons for AI Society
                   dataset, how many number of messages did camel decided to
                   limit, what's the value plus 100? You should refer to the
                   content in path camel/local_data/camel paper.pdf"""
)
AI Assistant sys message:
BaseMessage(role_name='Searcher', role_type=<RoleType.ASSISTANT: 'assistant'>, meta_dict={'task': "What is the main termination reasons for AI Society dataset, how many number of messages did camel decided to limit, what's the value plus 100?", 'assistant_role': 'Searcher', 'user_role': 'Professor'}, content="===== RULES OF ASSISTANT =====\nNever forget you are a Searcher and I am a Professor. Never flip roles! Never instruct me!\nWe share a common interest in collaborating to successfully complete a task.\nYou must help me to complete the task.\nHere is the task: What is the main termination reasons for AI Society dataset, how many number of messages did camel decided to limit, what's the value plus 100?. Never forget our task!\nI must instruct you based on your expertise and my needs to complete the task.\n\nI must give you one instruction at a time.\nYou must write a specific solution that appropriately solves the requested instruction and explain your solutions.\nYou must decline my instruction honestly if you cannot perform the instruction due to physical, moral, legal reasons or your capability and explain the reasons.\nUnless I say the task is completed, you should always start with:\n\nSolution: <YOUR_SOLUTION>\n\n<YOUR_SOLUTION> should be very specific, include detailed explanations and provide preferable detailed implementations and examples and lists for task-solving.\nAlways end <YOUR_SOLUTION> with: Next request.")

AI User sys message:
BaseMessage(role_name='Professor', role_type=<RoleType.USER: 'user'>, meta_dict={'task': "What is the main termination reasons for AI Society dataset, how many number of messages did camel decided to limit, what's the value plus 100?", 'assistant_role': 'Searcher', 'user_role': 'Professor'}, content='===== RULES OF USER =====\nNever forget you are a Professor and I am a Searcher. Never flip roles! You will always instruct me.\nWe share a common interest in collaborating to successfully complete a task.\nI must help you to complete the task.\nHere is the task: What is the main termination reasons for AI Society dataset, how many number of messages did camel decided to limit, what\'s the value plus 100?. Never forget our task!\nYou must instruct me based on my expertise and your needs to solve the task ONLY in the following two ways:\n\n1. Instruct with a necessary input:\nInstruction: <YOUR_INSTRUCTION>\nInput: <YOUR_INPUT>\n\n2. Instruct without any input:\nInstruction: <YOUR_INSTRUCTION>\nInput: None\n\nThe "Instruction" describes a task or question. The paired "Input" provides further context or information for the requested "Instruction".\n\nYou must give me one instruction at a time.\nI must write a response that appropriately solves the requested instruction.\nI must decline your instruction honestly if I cannot perform the instruction due to physical, moral, legal reasons or my capability and explain the reasons.\nYou should instruct me not ask me questions.\nNow you must start to instruct me using the two ways described above.\nDo not add anything else other than your instruction and the optional corresponding input!\nKeep giving me instructions and necessary inputs until you think the task is completed.\nWhen the task is completed, you must only reply with a single word <CAMEL_TASK_DONE>.\nNever say <CAMEL_TASK_DONE> unless my responses have solved your task.')

Original task prompt:
What is the main termination reasons for AI Society dataset, how many number of messages did camel decided to limit, what's the value plus 100?

Specified task prompt:
None

Final task prompt:
What is the main termination reasons for AI Society dataset, how many number of messages did camel decided to limit, what's the value plus 100?



AI User:

Instruction: Provide a summary of the main termination reasons in the AI Society dataset.
Input: None


AI Assistant:

Function Execution: local_retriever
    Args: {'query': 'main termination reasons for AI Society dataset'}
    Result: Original Query:
{main termination reasons for AI Society dataset}
Retrieved Context:
Next we examine the conversation termination reasons for both AI Society and Code datasets. As can be seen in Figure 8, the main termination reasons for AI Society dataset is Assistant Instruct whereas for Code it is Token Limit. The latter is expected as the since responses that contain code tend to be long. It is also interesting to note that in both datasets, the termination due to Maximum Number of Messages is low indicating that the limit of 40 maximum messages is reasonable. Our decision t

Solution: The main termination reason for the AI Society dataset is "Assistant Instruct." This indicates that conversations in the AI Society dataset typically end when the assistant is instructed to terminate the conversation.

Next request.


AI User:

Instruction: Identify the number of messages that the camel decided to limit in the context provided.
Input: None


AI Assistant:

Solution: The context provided from the local retriever indicates that the camel decided to limit the number of messages to a maximum of 40 messages. This is mentioned in the retrieved context where it states that the termination due to Maximum Number of Messages is low, indicating that the limit of 40 maximum messages is reasonable.

Next request.


AI User:

Instruction: Calculate the value of the message limit plus 100.
Input: None


AI Assistant:

Function Execution: add
    Args: {'a': 40, 'b': 100}
    Result: 140

Solution: The value of the message limit plus 100 is 140.

Next request.


AI User:

CAMEL_TASK_DONE


AI Assistant:

Solution: Understood, the task is completed.

Next request.