Cohere
Milvus 通过
CohereRerankFunction
类支持
Cohere
Reranker 模型
。通过该功能，您可以有效地对查询-文档对的相关性进行评分。
要使用该功能，请安装必要的依赖项：
pip install --upgrade pymilvus
pip install
"pymilvus[model]"
然后，实例化
CohereRerankFunction
：
from
pymilvus.model.reranker
import
CohereRerankFunction
# Define the rerank function
cohere_rf = CohereRerankFunction(
    model_name=
"rerank-english-v3.0"
,
# Specify the model name. Defaults to `rerank-english-v2.0`.
api_key=COHERE_API_KEY
# Replace with your Cohere API key
)
参数
model_name
(字符串）
要使用的模型名称。可以指定任何可用的 Cohere Reranker 模型名称，例如
rerank-english-v3.0
,
rerank-multilingual-v3.0
等。如果不指定此参数，则将使用
rerank-english-v2.0
。有关可用模型的列表，请参阅
Rerankers
。
api_key
（字符串）
访问 Cohere API 的 API 密钥。有关如何创建 API 密钥的信息，请参阅
Cohere dashboard
。
然后，使用以下代码根据查询结果对文档进行 Rerankers：
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

results = cohere_rf(
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
预期输出类似于下图：
Index:
1
Score:
0.99691266
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
3
Score:
0.8578872
Text: The invention of the Logic Theorist by Allen Newell, Herbert A. Simon,
and
Cliff Shaw
in
1955
marked the creation of the first true AI program, which was capable of solving logic problems, akin to proving mathematical theorems.

Index:
0
Score:
0.3589146
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