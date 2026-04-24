使用 Milvus 搜索图像
在本笔记本中，我们将向您展示如何使用 Milvus 在数据集中搜索相似图像。我们将使用
ImageNet
数据集的一个子集，然后搜索阿富汗猎犬的图像来演示这一点。
数据集准备
首先，我们需要加载数据集并解压缩，以便进一步处理。
$
wget https://github.com/milvus-io/pymilvus-assets/releases/download/imagedata/reverse_image_search.zip
$
unzip -q -o reverse_image_search.zip
前提条件
要运行本笔记本，您需要安装以下依赖项：
pymilvus>=2.4.2
timm
火炬
numpy
sklearn
枕头
要运行 Colab，我们提供了安装必要依赖项的便捷命令。
$
pip install pymilvus --upgrade
$
pip install timm
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
。(点击屏幕上方的 "Runtime（运行时）"菜单，从下拉菜单中选择 "Restart session（重新启动会话）"）。
定义特征提取器
然后，我们需要定义一个特征提取器，利用 timm 的 ResNet-34 模型从图像中提取嵌入信息。
import
torch
from
PIL
import
Image
import
timm
from
sklearn.preprocessing
import
normalize
from
timm.data
import
resolve_data_config
from
timm.data.transforms_factory
import
create_transform
class
FeatureExtractor
:
def
__init__
(
self, modelname
):
# Load the pre-trained model
self
.model = timm.create_model(
            modelname, pretrained=
True
, num_classes=
0
, global_pool=
"avg"
)
self
.model.
eval
()
# Get the input size required by the model
self
.input_size =
self
.model.default_cfg[
"input_size"
]

        config = resolve_data_config({}, model=modelname)
# Get the preprocessing function provided by TIMM for the model
self
.preprocess = create_transform(**config)
def
__call__
(
self, imagepath
):
# Preprocess the input image
input_image = Image.
open
(imagepath).convert(
"RGB"
)
# Convert to RGB if needed
input_image =
self
.preprocess(input_image)
# Convert the image to a PyTorch tensor and add a batch dimension
input_tensor = input_image.unsqueeze(
0
)
# Perform inference
with
torch.no_grad():
            output =
self
.model(input_tensor)
# Extract the feature vector
feature_vector = output.squeeze().numpy()
return
normalize(feature_vector.reshape(
1
, -
1
), norm=
"l2"
).flatten()
创建 Milvus Collections
然后，我们需要创建一个 Milvus Collections 来存储图像嵌入信息
from
pymilvus
import
MilvusClient
# Set up a Milvus client
client = MilvusClient(uri=
"example.db"
)
# Create a collection in quick setup mode
if
client.has_collection(collection_name=
"image_embeddings"
):
    client.drop_collection(collection_name=
"image_embeddings"
)
client.create_collection(
    collection_name=
"image_embeddings"
,
    vector_field_name=
"vector"
,
    dimension=
512
,
    auto_id=
True
,
    enable_dynamic_field=
True
,
    metric_type=
"COSINE"
,
)
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
将嵌入数据插入 Milvus
我们将使用 ResNet34 模型提取每张图片的嵌入，并将训练集中的图片插入 Milvus。
import
os

extractor = FeatureExtractor(
"resnet34"
)

root =
"./train"
insert =
True
if
insert
is
True
:
for
dirpath, foldername, filenames
in
os.walk(root):
for
filename
in
filenames:
if
filename.endswith(
".JPEG"
):
                filepath = dirpath +
"/"
+ filename
                image_embedding = extractor(filepath)
                client.insert(
"image_embeddings"
,
                    {
"vector"
: image_embedding,
"filename"
: filepath},
                )
from
IPython.display
import
display

query_image =
"./test/Afghan_hound/n02088094_4261.JPEG"
results = client.search(
"image_embeddings"
,
    data=[extractor(query_image)],
    output_fields=[
"filename"
],
    search_params={
"metric_type"
:
"COSINE"
},
)
images = []
for
result
in
results:
for
hit
in
result[:
10
]:
        filename = hit[
"entity"
][
"filename"
]
        img = Image.
open
(filename)
        img = img.resize((
150
,
150
))
        images.append(img)

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
for
idx, img
in
enumerate
(images):
    x = idx %
5
y = idx //
5
concatenated_image.paste(img, (x *
150
, y *
150
))
display(
"query"
)
display(Image.
open
(query_image).resize((
150
,
150
)))
display(
"results"
)
display(concatenated_image)
'query'
png
'results'
结果
我们可以看到，大部分图片都与搜索图片属于同一类别，即阿富汗猎犬。这说明我们找到了与搜索图片相似的图片。
快速部署
要了解如何使用本教程启动在线演示，请参阅
示例应用程序
。