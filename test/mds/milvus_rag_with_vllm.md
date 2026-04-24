用 Milvus、vLLM 和 Llama 3.1 构建 RAG
加州大学伯克利分校于 2024 年 7 月向
LF AI & Data 基金会
捐赠了用于 LLM 推理和服务的快速易用库
vLLM
，将其作为一个处于孵化阶段的项目。作为同类成员项目，我们欢迎 vLLM 加入 LF AI & Data 大家庭！🎉
大型语言模型
（LLMs
）和
向量数据库
通常搭配构建检索增强生成
（RAG
），这是一种流行的人工智能应用架构，用于解决
人工智能幻觉问题
。本篇博客将向您展示如何使用 Milvus、vLLM 和 Llama 3.1 构建并运行 RAG。更具体地说，我将向您展示如何在 Milvus 中将文本信息
嵌入
并存储为
向量 embeddings
，并将此向量存储作为知识库来高效检索与用户问题相关的文本块。最后，我们将利用 vLLM 为 Meta 的 Llama 3.1-8B 模型提供服务，生成由检索到的文本增强的答案。让我们深入了解一下！
Milvus、vLLM 和 Meta's Llama 3.1 简介
Milvus 向量数据库
Milvus
是一个开源、
专门构建的
分布式向量数据库，用于为
生成式人工智能
（GenAI）工作负载存储、索引和搜索向量。它能够执行
混合搜索、
元数据过滤
、重排序并高效处理数万亿向量，这使得 Milvus 成为人工智能和机器学习工作负载的首选。
Milvus
可在本地、集群上运行，也可托管在完全托管的
Zilliz Cloud
中。
vLLM
vLLM
是加州大学伯克利分校 SkyLab 启动的一个开源项目，专注于优化 LLM 服务性能。它使用 PagedAttention、连续批处理和优化的 CUDA 内核进行高效内存管理。与传统方法相比，vLLM 将服务性能提高了 24 倍，同时将 GPU 内存使用量减少了一半。
根据论文
"Efficient Memory Management for Large Language Model Serving with PagedAttention
"，KV 缓存使用了大约 30% 的 GPU 内存，导致潜在的内存问题。KV 缓存存储在连续的内存中，但改变大小会导致内存碎片，从而降低计算效率。
图片 1.现有系统中的 KV 缓存内存管理（2023 年分页关注
论文）
通过为 KV 缓存使用虚拟内存，vLLM 只在需要时分配 GPU 物理内存，从而消除了内存碎片，避免了预分配。在测试中，vLLM 的表现优于
HuggingFace Transformers
（HF）和
文本生成推理
（TGI），在英伟达 A10G 和 A100 GPU 上，vLLM 的吞吐量比 HF 高出 24 倍，比 TGI 高出 3.5 倍。
图 2.vLLM 的吞吐量是 HF 的 8.5-15 倍，是 TGI 的 3.3-3.5 倍（2023
vLLM 博客
）。
Meta's Llama 3.1
Meta's Llama 3.1
于 2024 年 7 月 23 日发布。405B 模型在多个公共基准上提供了最先进的性能，其上下文窗口为 128,000 个输入代币，并允许各种商业用途。在发布 4050 亿参数模型的同时，Meta 还发布了 Llama3 70B（700 亿参数）和 8B（80 亿参数）的更新版本。模型权重可
在 Meta 网站上
下载。
一个重要的启示是，对生成的数据进行微调可以提高性能，但劣质示例会降低性能。Llama 团队开展了大量工作，利用模型本身、辅助模型和其他工具识别并移除这些不良示例。
使用 Milvus 构建并执行 RAG-Retrieval
准备数据集。
我使用
Milvus
官方
文档
作为本演示的数据集，并将其下载保存到本地。
from
langchain.document_loaders
import
DirectoryLoader
# Load HTML files already saved in a local directory
path =
"../../RAG/rtdocs_new/"
global_pattern =
'*.html'
loader = DirectoryLoader(path=path, glob=global_pattern)
docs = loader.load()
# Print num documents and a preview.
print
(
f"loaded
{
len
(docs)}
documents"
)
print
(docs[
0
].page_content)
pprint.pprint(docs[
0
].metadata)
loaded 22 documents
Why Milvus Docs Tutorials Tools Blog Community Stars0 Try Managed Milvus FREE Search Home v2.4.x About ...
{'source': 'https://milvus.io/docs/quickstart.md'}
下载一个 Embeddings 模型。
接下来，从 HuggingFace 下载一个免费的开源
嵌入模型
。
import
torch
from
sentence_transformers
import
SentenceTransformer
# Initialize torch settings for device-agnostic code.
N_GPU = torch.cuda.device_count()
DEVICE = torch.device(
'cuda:N_GPU'
if
torch.cuda.is_available()
else
'cpu'
)
# Download the model from huggingface model hub.
model_name =
"BAAI/bge-large-en-v1.5"
encoder = SentenceTransformer(model_name, device=DEVICE)
# Get the model parameters and save for later.
EMBEDDING_DIM = encoder.get_sentence_embedding_dimension()
MAX_SEQ_LENGTH_IN_TOKENS = encoder.get_max_seq_length()
# Inspect model parameters.
print
(
f"model_name:
{model_name}
"
)
print
(
f"EMBEDDING_DIM:
{EMBEDDING_DIM}
"
)
print
(
f"MAX_SEQ_LENGTH:
{MAX_SEQ_LENGTH}
"
)
model_name: BAAI/bge-large-en-v1.5
EMBEDDING_DIM: 1024
MAX_SEQ_LENGTH: 512
将自定义数据分块并编码为向量。
我将使用固定长度的 512 个字符，重叠率为 10%。
from
langchain.text_splitter
import
RecursiveCharacterTextSplitter


CHUNK_SIZE =
512
chunk_overlap = np.
round
(CHUNK_SIZE *
0.10
,
0
)
print
(
f"chunk_size:
{CHUNK_SIZE}
, chunk_overlap:
{chunk_overlap}
"
)
# Define the splitter.
child_splitter = RecursiveCharacterTextSplitter(
   chunk_size=CHUNK_SIZE,
   chunk_overlap=chunk_overlap)
# Chunk the docs.
chunks = child_splitter.split_documents(docs)
print
(
f"
{
len
(docs)}
docs split into
{
len
(chunks)}
child documents."
)
# Encoder input is doc.page_content as strings.
list_of_strings = [doc.page_content
for
doc
in
chunks
if
hasattr
(doc,
'page_content'
)]
# Embedding inference using HuggingFace encoder.
embeddings = torch.tensor(encoder.encode(list_of_strings))
# Normalize the embeddings.
embeddings = np.array(embeddings / np.linalg.norm(embeddings))
# Milvus expects a list of `numpy.ndarray` of `numpy.float32` numbers.
converted_values =
list
(
map
(np.float32, embeddings))
# Create dict_list for Milvus insertion.
dict_list = []
for
chunk, vector
in
zip
(chunks, converted_values):
# Assemble embedding vector, original text chunk, metadata.
chunk_dict = {
'chunk'
: chunk.page_content,
'source'
: chunk.metadata.get(
'source'
,
""
),
'vector'
: vector,
   }
   dict_list.append(chunk_dict)
chunk_size: 512, chunk_overlap: 51.0
22 docs split into 355 child documents.
在 Milvus 中保存向量。
将编码后的向量 Embeddings 纳入 Milvus 向量数据库。
# Connect a client to the Milvus Lite server.
from
pymilvus
import
MilvusClient
mc = MilvusClient(
"milvus_demo.db"
)
# Create a collection with flexible schema and AUTOINDEX.
COLLECTION_NAME =
"MilvusDocs"
mc.create_collection(COLLECTION_NAME,
       EMBEDDING_DIM,
       consistency_level=
"Eventually"
,
       auto_id=
True
, 
       overwrite=
True
)
# Insert data into the Milvus collection.
print
(
"Start inserting entities"
)
start_time = time.time()
mc.insert(
   COLLECTION_NAME,
   data=dict_list,
   progress_bar=
True
)


end_time = time.time()
print
(
f"Milvus insert time for
{
len
(dict_list)}
vectors: "
, end=
""
)
print
(
f"
{
round
(end_time - start_time,
2
)}
seconds"
)
Start inserting entities
Milvus insert time for 355 vectors: 0.2 seconds
执行向量搜索。
提出一个问题，然后在 Milvus 中搜索知识库中的最近邻块。
SAMPLE_QUESTION =
"What do the parameters for HNSW mean?"
# Embed the question using the same encoder.
query_embeddings = torch.tensor(encoder.encode(SAMPLE_QUESTION))
# Normalize embeddings to unit length.
query_embeddings = F.normalize(query_embeddings, p=
2
, dim=
1
)
# Convert the embeddings to list of list of np.float32.
query_embeddings =
list
(
map
(np.float32, query_embeddings))
# Define metadata fields you can filter on.
OUTPUT_FIELDS =
list
(dict_list[
0
].keys())
OUTPUT_FIELDS.remove(
'vector'
)
# Define how many top-k results you want to retrieve.
TOP_K =
2
# Run semantic vector search using your query and the vector database.
results = mc.search(
    COLLECTION_NAME,
    data=query_embeddings,
    output_fields=OUTPUT_FIELDS,
    limit=TOP_K,
    consistency_level=
"Eventually"
)
检索结果如下所示。
Retrieved result #1
distance = 0.7001987099647522
('Chunk text: layer, finds the node closest to the target in this layer, and'
...
'outgoing')
source: https://milvus.io/docs/index.md

Retrieved result #2
distance = 0.6953287124633789
('Chunk text: this value can improve recall rate at the cost of increased'
...
'to the target')
source: https://milvus.io/docs/index.md
使用 vLLM 和 Llama 3.1-8B 构建并执行 RAG 生成
从 HuggingFace 安装 vLLM 和模型
vLLM 默认从 HuggingFace 下载大型语言模型。一般来说，无论何时想在 HuggingFace 上使用全新的模型，都应该进行 pip install --upgrade 或 -U。此外，您还需要 GPU 才能使用 vLLM 对 Meta 的 Llama 3.1 模型进行推理。
有关所有 vLLM 支持模型的完整列表，请参阅此
文档页面
。
#
(Recommended) Create a new conda environment.
conda create -n myenv python=3.11 -y
conda activate myenv
#
Install vLLM with CUDA 12.1.
pip install -U vllm transformers torch


import vllm, torch
from vllm import LLM, SamplingParams
#
Clear the GPU memory cache.
torch.cuda.empty_cache()
#
Check the GPU.
!nvidia-smi
要了解有关如何安装 vLLM 的更多信息，请参阅其
安装
页面。
获取 HuggingFace 令牌。
HuggingFace 上的某些模型（如 Meta Llama 3.1）要求用户接受其许可证后才能下载权重。因此，您必须创建一个 HuggingFace 账户，接受模型的许可证，并生成一个令牌。
访问 HuggingFace 上的这个
Llama3.1 页面
时，您会收到一条信息，要求您同意相关条款。在下载模型权重之前，请单击 "
接受许可
"以接受 Meta 条款。批准时间通常不超过一天。
收到批准后，您必须生成一个新的 HuggingFace 令牌。您的旧令牌将无法使用新权限。
在安装 vLLM 之前，请使用新令牌登录 HuggingFace。下面，我使用 Colab secrets 来存储令牌。
#
Login to HuggingFace using your new token.
from huggingface_hub import login
from google.colab import userdata
hf_token = userdata.get('HF_TOKEN')
login(token = hf_token, add_to_git_credential=True)
运行 RAG 生成
在演示中，我们运行
Llama-3.1-8B
模型，这需要 GPU 和相当大的内存来启动。下面的示例是在配备 A100 GPU 的 Google Colab Pro（10 美元/月）上运行的。要进一步了解如何运行 vLLM，可以查看
快速入门文档
。
# 1. Choose a model
MODELTORUN =
"meta-llama/Meta-Llama-3.1-8B-Instruct"
# 2. Clear the GPU memory cache, you're going to need it all!
torch.cuda.empty_cache()
# 3. Instantiate a vLLM model instance.
llm = LLM(model=MODELTORUN,
         enforce_eager=
True
,
         dtype=torch.bfloat16,
         gpu_memory_utilization=
0.5
,
         max_model_len=
1000
,
         seed=
415
,
         max_num_batched_tokens=
3000
)
使用从 Milvus 检索到的上下文和来源编写提示。
# Separate all the context together by space.
contexts_combined =
' '
.join(contexts)
# Lance Martin, LangChain, says put the best contexts at the end.
contexts_combined =
' '
.join(
reversed
(contexts))
# Separate all the unique sources together by comma.
source_combined =
' '
.join(
reversed
(
list
(
dict
.fromkeys(sources))))


SYSTEM_PROMPT =
f"""First, check if the provided Context is relevant to
the user's question.  Second, only if the provided Context is strongly relevant, answer the question using the Context.  Otherwise, if the Context is not strongly relevant, answer the question without using the Context. 
Be clear, concise, relevant.  Answer clearly, in fewer than 2 sentences.
Grounding sources:
{source_combined}
Context:
{contexts_combined}
User's question:
{SAMPLE_QUESTION}
"""
prompts = [SYSTEM_PROMPT]
现在，使用检索到的内容块和塞进提示中的原始问题生成一个答案。
# Sampling parameters
sampling_params = SamplingParams(temperature=
0.2
, top_p=
0.95
)
# Invoke the vLLM model.
outputs = llm.generate(prompts, sampling_params)
# Print the outputs.
for
output
in
outputs:
   prompt = output.prompt
   generated_text = output.outputs[
0
].text
# !r calls repr(), which prints a string inside quotes.
print
()
print
(
f"Question:
{SAMPLE_QUESTION!r}
"
)
   pprint.pprint(
f"Generated text:
{generated_text!r}
"
)
Question: 'What do the parameters for HNSW MEAN!?'
Generated text: 'Answer: The parameters for HNSW (Hiera(rchical Navigable Small World Graph) are: '
'* M: The maximum degree of nodes on each layer oof the graph, which can improve '
'recall rate at the cost of increased search time. * efConstruction and ef: ' 
'These parameters specify a search range when building or searching an index.'
我觉得上面的答案非常完美！
如果您对这个演示感兴趣，可以亲自尝试一下，并告诉我们您的想法。也欢迎您加入我们
在 Discord 上的 Milvus 社区
，直接与 GenAI 的所有开发人员交流。
参考资料
vLLM
官方文档
和
模型页面
。
2023 vLLM 关于分页注意力的论文
2023 vLLM
在 Ray 峰会上的
演讲
vLLM 博客：
vLLM：使用 PagedAttention 提供简单、快速、廉价的 LLM 服务
关于运行 vLLM 服务器的实用博客：
部署 vLLM：分步指南
喇嘛 3 群模型 | 研究 - Meta 的人工智能