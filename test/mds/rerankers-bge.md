BGE
Milvus 通过
BGERerankFunction
类支持
BGE Reranker 模型
。通过该功能，您可以有效地对查询-文档对的相关性进行评分。
要使用此功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
BGERerankFunction
：
from
pymilvus.model.reranker
import
BGERerankFunction
# Define the rerank function
bge_rf = BGERerankFunction(
    model_name=
"BAAI/bge-reranker-v2-m3"
,
# Specify the model name. Defaults to `BAAI/bge-reranker-v2-m3`.
device=
"cpu"
# Specify the device to use, e.g., 'cpu' or 'cuda:0'
)
参数
model_name
(字符串）
要使用的模型名称。您可以指定任何可用的 BGE Reranker 模型名称，例如
BAAI/bge-reranker-base
,
BAAI/bge-reranker-large
等。如果不指定此参数，则将使用
BAAI/bge-reranker-v2-m3
。有关可用模型的列表，请参阅
模型列表
。
device
（字符串）
可选。用于运行模型的设备。如果不指定，模型将在 CPU 上运行。可以为 CPU 指定
cpu
，为第 n 个 GPU 设备指定
cuda:n
。
然后，使用以下代码根据查询结果对文档进行 Rerankers 排序：
query =
"What event in 1956 marked the official birth of artificial intelligence as a discipline?"
documents = [
"In 1950, Alan Turing published his seminal paper, 'Computing Machinery and Intelligence,' proposing the Turing Test as a criterion of intelligence, a foundational concept in the philosophy and development of artificial intelligence."
,
"The Dartmouth Conference in 1956 is considered the birthplace of artificial intelligence as a field; here, John McCarthy and others coined the term 'artificial intelligence' and laid out its basic goals."
,
"In 1951, British mathematician and computer scientist Alan Turing also developed the first program designed to play chess, demonstrating an early example of AI in game strategy."
,
"The invention of the Logic Theorist by Allen Newell, Herbert A. Simon, and Cliff Shaw in 1955 marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems."
]

results = bge_rf(
    query=query,
    documents=documents,
    top_k=
3
,
)
for
result
in
results:
print
(
f"Index:
{result.index}
"
)
print
(
f"Score:
{result.score:
.6
f}
"
)
print
(
f"Text:
{result.text}
\n"
)
预期的输出结果类似于下图：
Index:
1
Score:
0.991162
Text: The Dartmouth Conference
in
1956
is
considered the birthplace of artificial intelligence
as
a field; here, John McCarthy
and
others coined the term
'artificial intelligence'
and
laid out its basic goals.

Index:
0
Score:
0.032697
Text: In
1950
, Alan Turing published his seminal paper,
'Computing Machinery and Intelligence,'
proposing the Turing Test
as
a criterion of intelligence, a foundational concept
in
the philosophy
and
development of artificial intelligence.

Index:
3
Score:
0.006515
Text: The invention of the Logic Theorist by Allen Newell, Herbert A. Simon,
and
Cliff Shaw
in
1955
marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.