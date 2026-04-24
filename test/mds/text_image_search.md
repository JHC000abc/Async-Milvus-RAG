使用 Milvus 进行文本到图像搜索
文本到图像搜索是一种先进的技术，允许用户使用自然语言文本描述搜索图像。它利用预训练的多模态模型将文本和图像转换为共享语义空间中的 Embeddings，从而实现基于相似性的比较。
在本教程中，我们将探讨如何使用 OpenAI 的 CLIP（对比语言-图像预训练）模型和 Milvus 实现基于文本的图像检索。我们将使用 CLIP 生成图像嵌入，将其存储在 Milvus 中，并执行高效的相似性搜索。
前提条件
开始之前，请确保已准备好所有必需的软件包和示例数据。
安装依赖项
pymilvus>=2.4.2
用于与 Milvus 数据库交互
clip
用于使用 CLIP 模型
pillow
用于图像处理和可视化
$
pip install --upgrade pymilvus pillow
$
pip install git+https://github.com/openai/CLIP.git
如果使用的是 Google Colab，可能需要
重启运行时
（导航至界面顶部的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
下载示例数据
我们将使用
ImageNet
数据集的一个子集（100 个类别，每个类别 10 幅图像）作为示例图像。以下命令将下载示例数据，并将其解压缩到本地文件夹
./images_folder
中：
$
wget https://github.com/towhee-io/examples/releases/download/data/reverse_image_search.zip
$
unzip -q reverse_image_search.zip -d images_folder
设置 Milvus
在继续之前，请设置您的 Milvus 服务器，并使用您的 URI（以及可选的令牌）进行连接：
Milvus Lite（为方便起见推荐使用）
：将 URI 设置为本地文件，如 ./milvus.db。这会自动利用
Milvus Lite
将所有数据存储在一个文件中。
Docker 或 Kubernetes（用于大规模数据）
：要处理更大的数据集，可使用
Docker 或 Kubernetes
部署性能更强的 Milvus 服务器。在这种情况下，请使用服务器 URI（如 http://localhost:19530）进行连接。
Zilliz Cloud（托管服务）
：如果使用
Zilliz Cloud
（Milvus 的完全托管云服务），请将公共端点设为 URI，将 API Key 设为令牌。
from
pymilvus
import
MilvusClient

milvus_client = MilvusClient(uri=
"milvus.db"
)
开始使用
现在您已经有了必要的依赖项和数据，是时候设置功能提取器并开始使用 Milvus 了。本节将引导你完成构建文本到图片搜索系统的关键步骤。最后，我们将演示如何根据文本查询检索图像并将其可视化。
定义特征提取器
我们将使用预训练的 CLIP 模型来生成图像和文本嵌入。在本节中，我们将加载经过预训练的 CLIP
ViT-B/32
变体，并定义用于图像和文本编码的辅助函数：
encode_image(image_path)
:将图像处理和编码为特征向量
encode_text(text)
:将文本查询编码为特征向量
这两个函数都对输出特征进行归一化处理，通过将向量转换为单位长度来确保一致的比较，这对于精确的余弦相似性计算至关重要。
import
clip
from
PIL
import
Image
# Load CLIP model
model_name =
"ViT-B/32"
model, preprocess = clip.load(model_name)
model.
eval
()
# Define a function to encode images
def
encode_image
(
image_path
):
    image = preprocess(Image.
open
(image_path)).unsqueeze(
0
)
    image_features = model.encode_image(image)
    image_features /= image_features.norm(
        dim=-
1
, keepdim=
True
)
# Normalize the image features
return
image_features.squeeze().tolist()
# Define a function to encode text
def
encode_text
(
text
):
    text_tokens = clip.tokenize(text)
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(
        dim=-
1
, keepdim=
True
)
# Normalize the text features
return
text_features.squeeze().tolist()
数据输入
要实现语义图像搜索，我们首先需要为所有图像生成 Embeddings，并将其存储到向量数据库中，以便进行高效索引和检索。本节将逐步介绍如何将图像数据导入 Milvus。
1.创建 Milvus Collections
在存储图像 Embeddings 之前，需要创建一个 Milvus Collections。下面的代码演示了如何以默认的 COSINE 度量类型在快速设置模式下创建一个 Collection。Collections 包括以下字段：
id
:启用自动 ID 的主字段。
vector
:用于存储浮点向量 Embeddings 的字段。
如果需要自定义 Schema，详细说明请参阅
Milvus 文档
。
collection_name =
"image_collection"
# Drop the collection if it already exists
if
milvus_client.has_collection(collection_name):
    milvus_client.drop_collection(collection_name)
# Create a new collection in quickstart mode
milvus_client.create_collection(
    collection_name=collection_name,
    dimension=
512
,
# this should match the dimension of the image embedding
auto_id=
True
,
# auto generate id and store in the id field
enable_dynamic_field=
True
,
# enable dynamic field for scalar fields
)
2.向 Milvus 插入数据
在这一步中，我们使用预定义的图像编码器为示例数据目录中的所有 JPEG 图像生成嵌入。然后将这些嵌入信息连同相应的文件路径一起插入到 Milvus Collections 中。Collections 中的每个条目都由以下内容组成：
嵌入向量
：图像的数字表示。存储在字段
vector
中。
文件路径
：供参考的图像文件位置。作为动态字段存储在
filepath
字段中。
import
os
from
glob
import
glob


image_dir =
"./images_folder/train"
raw_data = []
for
image_path
in
glob(os.path.join(image_dir,
"**/*.JPEG"
)):
    image_embedding = encode_image(image_path)
    image_dict = {
"vector"
: image_embedding,
"filepath"
: image_path}
    raw_data.append(image_dict)
insert_result = milvus_client.insert(collection_name=collection_name, data=raw_data)
print
(
"Inserted"
, insert_result[
"insert_count"
],
"images into Milvus."
)
Inserted 1000 images into Milvus.
执行搜索
现在，让我们使用示例文本查询执行一次搜索。这将根据图像与给定文本描述的语义相似性检索出最相关的图像。
query_text =
"a white dog"
query_embedding = encode_text(query_text)

search_results = milvus_client.search(
    collection_name=collection_name,
    data=[query_embedding],
    limit=
10
,
# return top 10 results
output_fields=[
"filepath"
],
# return the filepath field
)
可视化结果：
from
IPython.display
import
display


width =
150
*
5
height =
150
*
2
concatenated_image = Image.new(
"RGB"
, (width, height))

result_images = []
for
result
in
search_results:
for
hit
in
result:
        filename = hit[
"entity"
][
"filepath"
]
        img = Image.
open
(filename)
        img = img.resize((
150
,
150
))
        result_images.append(img)
for
idx, img
in
enumerate
(result_images):
    x = idx %
5
y = idx //
5
concatenated_image.paste(img, (x *
150
, y *
150
))
print
(
f"Query text:
{query_text}
"
)
print
(
"\nSearch results:"
)
display(concatenated_image)
Query text: a white dog

Search results:
png