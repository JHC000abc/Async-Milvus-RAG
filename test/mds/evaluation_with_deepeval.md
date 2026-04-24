使用 DeepEval 进行评估
本指南演示了如何使用
DeepEval
评估基于
Milvus
的检索增强生成 (RAG) 管道。
RAG 系统将检索系统与生成模型相结合，根据给定提示生成新文本。该系统首先使用 Milvus 从语料库中检索相关文档，然后使用生成模型根据检索到的文档生成新文本。
DeepEval 是一个帮助您评估 RAG 管道的框架。现有的工具和框架可以帮助您构建这些管道，但评估和量化管道性能可能很难。这就是 DeepEval 的用武之地。
前提条件
运行本笔记本之前，请确保已安装以下依赖项：
$ pip install --upgrade pymilvus milvus-lite openai requests tqdm pandas deepeval
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕顶部的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 OpenAI 作为 LLM。您应将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-*****************"
定义 RAG 管道
我们将定义使用 Milvus 作为向量存储、OpenAI 作为 LLM 的 RAG 类。该类包含
load
方法（将文本数据加载到 Milvus）、
retrieve
方法（检索与给定问题最相似的文本数据）和
answer
方法（使用检索到的知识回答给定问题）。
from
typing
import
List
from
tqdm
import
tqdm
from
openai
import
OpenAI
from
pymilvus
import
MilvusClient
class
RAG
:
"""
    RAG(Retrieval-Augmented Generation) class built upon OpenAI and Milvus.
    """
def
__init__
(
self, openai_client: OpenAI, milvus_client: MilvusClient
):
self
._prepare_openai(openai_client)
self
._prepare_milvus(milvus_client)
def
_emb_text
(
self, text:
str
) ->
List
[
float
]:
return
(
self
.openai_client.embeddings.create(
input
=text, model=
self
.embedding_model)
            .data[
0
]
            .embedding
        )
def
_prepare_openai
(
self,
        openai_client: OpenAI,
        embedding_model:
str
=
"text-embedding-3-small"
,
        llm_model:
str
=
"gpt-4o-mini"
,
):
self
.openai_client = openai_client
self
.embedding_model = embedding_model
self
.llm_model = llm_model
self
.SYSTEM_PROMPT =
"""
            Human: You are an AI assistant. You are able to find answers to the questions from the contextual passage snippets provided.
        """
self
.USER_PROMPT =
"""
            Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags.
            <context>
            {context}
            </context>
            <question>
            {question}
            </question>
        """
def
_prepare_milvus
(
self, milvus_client: MilvusClient, collection_name:
str
=
"rag_collection"
):
self
.milvus_client = milvus_client
self
.collection_name = collection_name
if
self
.milvus_client.has_collection(
self
.collection_name):
self
.milvus_client.drop_collection(
self
.collection_name)
        embedding_dim =
len
(
self
._emb_text(
"demo"
))
self
.milvus_client.create_collection(
            collection_name=
self
.collection_name,
            dimension=embedding_dim,
            metric_type=
"IP"
,
            consistency_level=
"Bounded"
,
# Supported values are (`"Strong"`, `"Session"`, `"Bounded"`, `"Eventually"`). See https://milvus.io/docs/consistency.md#Consistency-Level for more details.
)
def
load
(
self, texts:
List
[
str
]
):
"""
        Load the text data into Milvus.
        """
data = []
for
i, line
in
enumerate
(tqdm(texts, desc=
"Creating embeddings"
)):
            data.append({
"id"
: i,
"vector"
:
self
._emb_text(line),
"text"
: line})
self
.milvus_client.insert(collection_name=
self
.collection_name, data=data)
def
retrieve
(
self, question:
str
, top_k:
int
=
3
) ->
List
[
str
]:
"""
        Retrieve the most similar text data to the given question.
        """
search_res =
self
.milvus_client.search(
            collection_name=
self
.collection_name,
            data=[
self
._emb_text(question)],
            limit=top_k,
            search_params={
"metric_type"
:
"IP"
,
"params"
: {}},
# inner product distance
output_fields=[
"text"
],
# Return the text field
)
        retrieved_texts = [res[
"entity"
][
"text"
]
for
res
in
search_res[
0
]]
return
retrieved_texts[:top_k]
def
answer
(
self,
        question:
str
,
        retrieval_top_k:
int
=
3
,
        return_retrieved_text:
bool
=
False
,
):
"""
        Answer the given question with the retrieved knowledge.
        """
retrieved_texts =
self
.retrieve(question, top_k=retrieval_top_k)
        user_prompt =
self
.USER_PROMPT.
format
(
            context=
"\n"
.join(retrieved_texts), question=question
        )
        response =
self
.openai_client.chat.completions.create(
            model=
self
.llm_model,
            messages=[
                {
"role"
:
"system"
,
"content"
:
self
.SYSTEM_PROMPT},
                {
"role"
:
"user"
,
"content"
: user_prompt},
            ],
        )
if
not
return_retrieved_text:
return
response.choices[
0
].message.content
else
:
return
response.choices[
0
].message.content, retrieved_texts
让我们用 OpenAI 和 Milvus 客户端初始化 RAG 类。
openai_client = OpenAI()
milvus_client = MilvusClient(uri=
"./milvus_demo.db"
)

my_rag = RAG(openai_client=openai_client, milvus_client=milvus_client)
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
运行 RAG 管道并获取结果
我们使用
Milvus 开发指南
作为 RAG 中的私有知识，它是简单 RAG 管道的良好数据源。
下载并将其加载到 RAG 管道中。
import
urllib.request
import
os

url =
"https://raw.githubusercontent.com/milvus-io/milvus/master/DEVELOPMENT.md"
file_path =
"./Milvus_DEVELOPMENT.md"
if
not
os.path.exists(file_path):
    urllib.request.urlretrieve(url, file_path)
with
open
(file_path,
"r"
)
as
file:
    file_text = file.read()

text_lines = file_text.split(
"# "
)
my_rag.load(text_lines)
Creating embeddings: 100%|██████████| 47/47 [00:20<00:00,  2.26it/s]
让我们定义一个关于开发指南文档内容的查询问题。然后使用
answer
方法获取答案和检索到的上下文文本。
question =
"what is the hardware requirements specification if I want to build Milvus and run from source code?"
my_rag.answer(question, return_retrieved_text=
True
)
('The hardware requirements specification to build and run Milvus from source code is as follows:\n\n- 8GB of RAM\n- 50GB of free disk space',
 ['Hardware Requirements\n\nThe following specification (either physical or virtual machine resources) is recommended for Milvus to build and run from source code.\n\n```\n- 8GB of RAM\n- 50GB of free disk space\n```\n\n##',
  'Building Milvus on a local OS/shell environment\n\nThe details below outline the hardware and software requirements for building on Linux and MacOS.\n\n##',
  "Software Requirements\n\nAll Linux distributions are available for Milvus development. However a majority of our contributor worked with Ubuntu or CentOS systems, with a small portion of Mac (both x86_64 and Apple Silicon) contributors. If you would like Milvus to build and run on other distributions, you are more than welcome to file an issue and contribute!\n\nHere's a list of verified OS types where Milvus can successfully build and run:\n\n- Debian/Ubuntu\n- Amazon Linux\n- MacOS (x86_64)\n- MacOS (Apple Silicon)\n\n##"])
现在，让我们准备一些问题及其相应的地面实况答案。我们从 RAG 管道中获取答案和上下文。
from
datasets
import
Dataset
import
pandas
as
pd

question_list = [
"what is the hardware requirements specification if I want to build Milvus and run from source code?"
,
"What is the programming language used to write Knowhere?"
,
"What should be ensured before running code coverage?"
,
]
ground_truth_list = [
"If you want to build Milvus and run from source code, the recommended hardware requirements specification is:\n\n- 8GB of RAM\n- 50GB of free disk space."
,
"The programming language used to write Knowhere is C++."
,
"Before running code coverage, you should make sure that your code changes are covered by unit tests."
,
]
contexts_list = []
answer_list = []
for
question
in
tqdm(question_list, desc=
"Answering questions"
):
    answer, contexts = my_rag.answer(question, return_retrieved_text=
True
)
    contexts_list.append(contexts)
    answer_list.append(answer)

df = pd.DataFrame(
    {
"question"
: question_list,
"contexts"
: contexts_list,
"answer"
: answer_list,
"ground_truth"
: ground_truth_list,
    }
)
rag_results = Dataset.from_pandas(df)
df
/Users/eureka/miniconda3/envs/zilliz/lib/python3.9/site-packages/tqdm/auto.py:21: TqdmWarning: IProgress not found. Please update jupyter and ipywidgets. See https://ipywidgets.readthedocs.io/en/stable/user_install.html
  from .autonotebook import tqdm as notebook_tqdm
Answering questions: 100%|██████████| 3/3 [00:03<00:00,  1.06s/it]
.dataframe tbody tr th:only-of-type { vertical-align: middle; }<pre><code translate="no">.dataframe tbody tr th {
    vertical-align: top;
}

.dataframe thead th {
    text-align: right;
}
</code></pre>
问题
上下文
答案
地面真相
0
硬件要求是什么？
[硬件要求（Hardware Requirements/n）：以下是硬件要求规格。
构建Milvus的硬件要求规范...
如果您想构建 Milvus 并从源代码中运行...
1
用什么编程语言来编写Milvus...
[CMake & Conan\n\nMilvus 的算法库...
编写 Knowherus 的编程语言是什么？
用来编写知乎的编程语言...
2
运行代码覆盖前应确保什么？
[代码覆盖（Code coverage）：在提交您的pull...
在运行代码覆盖之前，应该确保...
运行代码覆盖之前，应确保 ...
评估检索器
在评估大型语言模型（LLM）系统中的 Retriever 时，评估以下几点至关重要：
排名相关性
：检索器如何有效地优先处理相关信息而非无关数据。
上下文检索
：根据输入捕捉和检索上下文相关信息的能力。
平衡性
：检索器如何很好地管理文本块大小和检索范围，以尽量减少无关信息。
这些因素结合在一起，可以让人全面了解检索器如何确定优先级、捕捉和呈现最有用的信息。
from
deepeval.metrics
import
(
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    ContextualRelevancyMetric,
)
from
deepeval.test_case
import
LLMTestCase
from
deepeval
import
evaluate

contextual_precision = ContextualPrecisionMetric()
contextual_recall = ContextualRecallMetric()
contextual_relevancy = ContextualRelevancyMetric()

test_cases = []
for
index, row
in
df.iterrows():
    test_case = LLMTestCase(
input
=row[
"question"
],
        actual_output=row[
"answer"
],
        expected_output=row[
"ground_truth"
],
        retrieval_context=row[
"contexts"
],
    )
    test_cases.append(test_case)
# test_cases
result = evaluate(
    test_cases=test_cases,
    metrics=[contextual_precision, contextual_recall, contextual_relevancy],
    print_results=
False
,
# Change to True to see detailed metric results
)
/Users/eureka/miniconda3/envs/zilliz/lib/python3.9/site-packages/deepeval/__init__.py:49: UserWarning: You are using deepeval version 1.1.6, however version 1.2.2 is available. You should consider upgrading via the "pip install --upgrade deepeval" command.
  warnings.warn(
您正在运行 DeepEval 最新的
上下文精度指标
！
(使用 gpt-4o，
strict=
False
，
async_mode=
True
）
..
.
✨ 您正在运行 DeepEval 最新的
上下文召回指标
！
(使用 gpt-4o，
strict
=False
，
async
_
mode=True
）
..
.
✨ 您正在运行 DeepEval 最新的
上下文相关性指标
！
(使用 gpt-4o，
strict
=False
，
async
_
mode=True
）
..
.
Event loop is already running. Applying nest_asyncio patch to allow async execution...


Evaluating 3 test case(s) in parallel: |██████████|100% (3/3) [Time Taken: 00:11,  3.91s/test case]
测试已完成
🎉！
运行
"deepeval login "
查看 Confident AI 的评估结果。 
‼️ 注意：您也可以直接在 Confident AI 上对 deepeval 的所有指标进行评估。
评估生成
要评估大型语言模型 (LLM) 生成输出的质量，必须关注两个关键方面：
相关性
：评估提示是否有效地引导 LLM 生成有帮助且与上下文相符的回答。
忠实性
：衡量输出的准确性，确保模型生成的信息与事实相符，没有幻觉或矛盾。生成的内容应与检索上下文中提供的事实信息一致。
这些因素共同确保了输出结果的相关性和可靠性。
from
deepeval.metrics
import
AnswerRelevancyMetric, FaithfulnessMetric
from
deepeval.test_case
import
LLMTestCase
from
deepeval
import
evaluate

answer_relevancy = AnswerRelevancyMetric()
faithfulness = FaithfulnessMetric()

test_cases = []
for
index, row
in
df.iterrows():
    test_case = LLMTestCase(
input
=row[
"question"
],
        actual_output=row[
"answer"
],
        expected_output=row[
"ground_truth"
],
        retrieval_context=row[
"contexts"
],
    )
    test_cases.append(test_case)
# test_cases
result = evaluate(
    test_cases=test_cases,
    metrics=[answer_relevancy, faithfulness],
    print_results=
False
,
# Change to True to see detailed metric results
)
✨ 您正在运行 DeepEval 最新的
答案相关性度量标准
！
(使用 gpt-4o，
strict=
False
，
async
_mode=True
）
..
.
✨ 您正在运行 DeepEval 最新的
忠实度指标
！
(使用 gpt-4o，
strict=
False
，
async_mode=
True
）
..
.
Event loop is already running. Applying nest_asyncio patch to allow async execution...


Evaluating 3 test case(s) in parallel: |██████████|100% (3/3) [Time Taken: 00:11,  3.97s/test case]
测试已完成
🎉！
运行
"deepeval login "
查看 Confident AI 的评估结果。 
‼️ 注意：您也可以直接在 Confident AI 上运行对 deepeval 所有指标的评估。