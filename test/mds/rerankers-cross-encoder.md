交叉编码器
Milvus 通过
CrossEncoderRerankFunction
类支持
交叉编码器
。该功能可让您有效地对查询-文档对的相关性进行评分。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
CrossEncoderRerankFunction
：
from
pymilvus.model.reranker
import
CrossEncoderRerankFunction
# Define the rerank function
ce_rf = CrossEncoderRerankFunction(
    model_name=
"cross-encoder/ms-marco-MiniLM-L-6-v2"
,
# Specify the model name.
device=
"cpu"
# Specify the device to use, e.g., 'cpu' or 'cuda:0'
)
参数
：
model_name
(字符串）
要使用的模型名称。可以指定任何可用的跨编码器模型名称，例如
cross-encoder/ms-marco-TinyBERT-L-2-v2
,
cross-encoder/ms-marco-MiniLM-L-2-v2
等。如果不指定该参数，将使用空字符串。有关可用模型的列表，请参阅
预训练交叉编码器
。
device
（字符串）
用于运行模型的设备。可以为 CPU 指定
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

results = ce_rf(
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
预期输出类似于下面的内容：
Index:
1
Score:
6.250533
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
Score: -
2.954602
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
Score: -
4.771512
Text: The invention of the Logic Theorist by Allen Newell, Herbert A. Simon,
and
Cliff Shaw
in
1955
marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.