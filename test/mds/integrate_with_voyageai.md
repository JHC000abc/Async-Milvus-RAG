使用Milvus和VoyageAI进行语义搜索
本指南展示了如何将
VoyageAI的Embedding API
与Milvus向量数据库结合使用，对文本进行语义搜索。
开始
开始之前，请确保您已准备好 Voyage API 密钥，或从
VoyageAI 网站
获取一个。
本示例中使用的数据是书名。你可以
在这里
下载数据集，并将其放在运行以下代码的同一目录下。
首先，安装 Milvus 和 Voyage AI 的软件包：
$ pip install --upgrade voyageai pymilvus milvus-lite
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
。(点击屏幕上方的 "Runtime（运行时）"菜单，从下拉菜单中选择 "Restart session（重新启动会话）"）。
这样，我们就可以生成 Embeddings 并使用向量数据库进行语义搜索了。
使用 VoyageAI 和 Milvus 搜索书名
在下面的示例中，我们从下载的 CSV 文件中加载书名数据，使用 Voyage AI 嵌入模型生成向量表示，并将其存储到 Milvus 向量数据库中进行语义搜索。
import
voyageai
from
pymilvus
import
MilvusClient

MODEL_NAME =
"voyage-law-2"
# Which model to use, please check https://docs.voyageai.com/docs/embeddings for available models
DIMENSION =
1024
# Dimension of vector embedding
# Connect to VoyageAI with API Key.
voyage_client = voyageai.Client(api_key=
"<YOUR_VOYAGEAI_API_KEY>"
)

docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]

vectors = voyage_client.embed(texts=docs, model=MODEL_NAME, truncation=
False
).embeddings
# Prepare data to be stored in Milvus vector database.
# We can store the id, vector representation, raw text and labels such as "subject" in this case in Milvus.
data = [
    {
"id"
: i,
"vector"
: vectors[i],
"text"
: docs[i],
"subject"
:
"history"
}
for
i
in
range
(
len
(docs))
]
# Connect to Milvus, all data is stored in a local file named "milvus_voyage_demo.db"
# in current directory. You can also connect to a remote Milvus server following this
# instruction: https://milvus.io/docs/install_standalone-docker.md.
milvus_client = MilvusClient(uri=
"milvus_voyage_demo.db"
)
COLLECTION_NAME =
"demo_collection"
# Milvus collection name
# Create a collection to store the vectors and text.
if
milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(collection_name=COLLECTION_NAME, dimension=DIMENSION)
# Insert all data into Milvus vector database.
res = milvus_client.insert(collection_name=
"demo_collection"
, data=data)
print
(res[
"insert_count"
])
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
有了 Milvus 向量数据库中的所有数据，我们现在就可以通过为查询生成向量 Embeddings 来执行语义搜索，并进行向量搜索。
queries = [
"When was artificial intelligence founded?"
]

query_vectors = voyage_client.embed(
    texts=queries, model=MODEL_NAME, truncation=
False
).embeddings

res = milvus_client.search(
    collection_name=COLLECTION_NAME,
# target collection
data=query_vectors,
# query vectors
limit=
2
,
# number of returned entities
output_fields=[
"text"
,
"subject"
],
# specifies fields to be returned
)
for
q
in
queries:
print
(
"Query:"
, q)
for
result
in
res:
print
(result)
print
(
"\n"
)
Query: When was artificial intelligence founded?
[{'id': 0, 'distance': 0.7196218371391296, 'entity': {'text': 'Artificial intelligence was founded as an academic discipline in 1956.', 'subject': 'history'}}, {'id': 1, 'distance': 0.6297335028648376, 'entity': {'text': 'Alan Turing was the first person to conduct substantial research in AI.', 'subject': 'history'}}]
使用 VoyageAI 和 Milvus 搜索图像
import
base64
import
voyageai
from
pymilvus
import
MilvusClient
import
urllib.request
import
matplotlib.pyplot
as
plt
from
io
import
BytesIO
import
urllib.request
import
fitz
# PyMuPDF
from
PIL
import
Image
def
pdf_url_to_screenshots
(
url:
str
, zoom:
float
=
1.0
) ->
list
[Image]:
# Ensure that the URL is valid
if
not
url.startswith(
"http"
)
and
url.endswith(
".pdf"
):
raise
ValueError(
"Invalid URL"
)
# Read the PDF from the specified URL
with
urllib.request.urlopen(url)
as
response:
        pdf_data = response.read()
    pdf_stream = BytesIO(pdf_data)
    pdf = fitz.
open
(stream=pdf_stream, filetype=
"pdf"
)

    images = []
# Loop through each page, render as pixmap, and convert to PIL Image
mat = fitz.Matrix(zoom, zoom)
for
n
in
range
(pdf.page_count):
        pix = pdf[n].get_pixmap(matrix=mat)
# Convert pixmap to PIL Image
img = Image.frombytes(
"RGB"
, [pix.width, pix.height], pix.samples)
        images.append(img)
# Close the document
pdf.close()
return
images
def
image_to_base64
(
image
):
    buffered = BytesIO()
    image.save(buffered,
format
=
"JPEG"
)
    img_str = base64.b64encode(buffered.getvalue())
return
img_str.decode(
"utf-8"
)

DIMENSION =
1024
# Dimension of vector embedding
然后，我们需要为 Milvus 准备输入数据。让我们重用上一章创建的 VoyageAI 客户端。有关可用的 VoyageAI 多模态嵌入模型，请查看此
页面
。
pages = pdf_url_to_screenshots(
"https://www.fdrlibrary.org/documents/356632/390886/readingcopy.pdf"
, zoom=
3.0
)
inputs = [[img]
for
img
in
pages]

vectors = client.multimodal_embed(inputs, model=
"voyage-multimodal-3"
)

inputs = [i[
0
]
if
isinstance
(i[
0
],
str
)
else
image_to_base64(i[
0
])
for
i
in
inputs]
# Prepare data to be stored in Milvus vector database.
# We can store the id, vector representation, raw text and labels such as "subject" in this case in Milvus.
data = [
    {
"id"
: i,
"vector"
: vectors.embeddings[i],
"data"
: inputs[i],
"subject"
:
"fruits"
}
for
i
in
range
(
len
(inputs))
]
接下来，我们创建一个 Milvus 数据库连接，并将嵌入数据插入 Milvus 数据库。
milvus_client = MilvusClient(uri=
"milvus_voyage_multi_demo.db"
)
COLLECTION_NAME =
"demo_collection"
# Milvus collection name
# Create a collection to store the vectors and text.
if
milvus_client.has_collection(collection_name=COLLECTION_NAME):
    milvus_client.drop_collection(collection_name=COLLECTION_NAME)
milvus_client.create_collection(collection_name=COLLECTION_NAME, dimension=DIMENSION)
# Insert all data into Milvus vector database.
res = milvus_client.insert(collection_name=
"demo_collection"
, data=data)
print
(res[
"insert_count"
])
现在，我们可以搜索图像了。这里的查询是一个字符串，但我们也可以用图像进行查询。(我们使用 matplotlib
来
显示结果图像。
queries = [[
"The consequences of a dictator's peace"
]]

query_vectors = client.multimodal_embed(
    inputs=queries, model=
"voyage-multimodal-3"
, truncation=
False
).embeddings

res = milvus_client.search(
    collection_name=COLLECTION_NAME,
# target collection
data=query_vectors,
# query vectors
limit=
4
,
# number of returned entities
output_fields=[
"data"
,
"subject"
],
# specifies fields to be returned
)
for
q
in
queries:
print
(
"Query:"
, q)
for
result
in
res:
        fig, axes = plt.subplots(
1
,
len
(result), figsize=(
66
,
6
))
for
n, page
in
enumerate
(result):
            page_num = page[
'id'
]
            axes[n].imshow(pages[page_num])
            axes[n].axis(
"off"
)

    plt.tight_layout()
    plt.show()