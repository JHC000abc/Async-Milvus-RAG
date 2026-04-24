使用 PyTorch 和 Milvus 进行图像搜索
本指南介绍一个集成 PyTorch 和 Milvus 以使用 Embeddings 执行图像搜索的示例。PyTorch 是一个强大的开源深度学习框架，广泛用于构建和部署机器学习模型。在本例中，我们将利用其 Torchvision 库和预先训练好的 ResNet50 模型来生成表示图像内容的特征向量（嵌入）。这些嵌入向量将存储在高性能向量数据库 Milvus 中，以实现高效的相似性搜索。使用的数据集是来自
Kaggle
的印象派分类器数据集。通过将 PyTorch 的深度学习功能与 Milvus 的可扩展搜索功能相结合，本示例演示了如何构建一个强大而高效的图像检索系统。
让我们开始吧
安装需求
在本例中，我们将使用
pymilvus
连接使用 Milvus，使用
torch
运行嵌入模型，使用
torchvision
进行实际模型和预处理，使用
gdown
下载示例数据集，使用
tqdm
加载条形图。
pip install pymilvus torch gdown torchvision tqdm
抓取数据
我们将使用
gdown
从 Google Drive 抓取压缩包，然后使用内置的
zipfile
库解压。
import
gdown
import
zipfile

url =
'https://drive.google.com/uc?id=1OYDHLEy992qu5C4C8HV5uDIkOWRTAR1_'
output =
'./paintings.zip'
gdown.download(url, output)
with
zipfile.ZipFile(
"./paintings.zip"
,
"r"
)
as
zip_ref:
    zip_ref.extractall(
"./paintings"
)
数据集的大小为 2.35 GB，下载时间取决于网络状况。
全局参数
这些是我们将使用的一些主要全局参数，以便于跟踪和更新。
# Milvus Setup Arguments
COLLECTION_NAME =
'image_search'
# Collection name
DIMENSION =
2048
# Embedding vector size in this example
MILVUS_HOST =
"localhost"
MILVUS_PORT =
"19530"
# Inference Arguments
BATCH_SIZE =
128
TOP_K =
3
设置 Milvus
此时，我们要开始设置 Milvus。具体步骤如下
使用提供的 URI 连接到 Milvus 实例。
from
pymilvus
import
connections
# Connect to the instance
connections.connect(host=MILVUS_HOST, port=MILVUS_PORT)
如果 Collection 已经存在，则删除它。
from
pymilvus
import
utility
# Remove any previous collections with the same name
if
utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME)
创建保存 ID、图片文件路径及其 Embeddings 的 Collection。
from
pymilvus
import
FieldSchema, CollectionSchema, DataType, Collection
# Create collection which includes the id, filepath of the image, and image embedding
fields = [
    FieldSchema(name=
'id'
, dtype=DataType.INT64, is_primary=
True
, auto_id=
True
),
    FieldSchema(name=
'filepath'
, dtype=DataType.VARCHAR, max_length=
200
),
# VARCHARS need a maximum length, so for this example they are set to 200 characters
FieldSchema(name=
'image_embedding'
, dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
]
schema = CollectionSchema(fields=fields)
collection = Collection(name=COLLECTION_NAME, schema=schema)
在新创建的 Collections 上创建索引，并将其加载到内存中。
# Create an AutoIndex index for collection
index_params = {
'metric_type'
:
'L2'
,
'index_type'
:
"IVF_FLAT"
,
'params'
:{
'nlist'
:
16384
}
}
collection.create_index(field_name=
"image_embedding"
, index_params=index_params)
collection.load()
完成这些步骤后，就可以插入并搜索 Collections 了。任何添加的数据都会自动编入索引，并立即可供搜索。如果数据非常新，搜索速度可能会慢一些，因为将对仍在编制索引过程中的数据使用暴力搜索。
插入数据
在本例中，我们将使用
torch
及其模型中心提供的 ResNet50 模型。为了获得 Embeddings，我们要去掉最后的分类层，这样模型就能为我们提供 2048 维的 embeddings。在
torch
上找到的所有视觉模型都使用了与我们这里相同的预处理。
在接下来的几个步骤中，我们将
加载数据。
import
glob
# Get the filepaths of the images
paths = glob.glob(
'./paintings/paintings/**/*.jpg'
, recursive=
True
)
len
(paths)
分批预处理数据。
import
torch
# Load the embedding model with the last layer removed
model = torch.hub.load(
'pytorch/vision:v0.10.0'
,
'resnet50'
, pretrained=
True
)
model = torch.nn.Sequential(*(
list
(model.children())[:-
1
]))
model.
eval
()
嵌入数据。
from
torchvision
import
transforms
# Preprocessing for images
preprocess = transforms.Compose([
    transforms.Resize(
256
),
    transforms.CenterCrop(
224
),
    transforms.ToTensor(),
    transforms.Normalize(mean=[
0.485
,
0.456
,
0.406
], std=[
0.229
,
0.224
,
0.225
]),
])
插入数据。
from
PIL
import
Image
from
tqdm
import
tqdm
# Embed function that embeds the batch and inserts it
def
embed
(
data
):
with
torch.no_grad():
        output = model(torch.stack(data[
0
])).squeeze()
        collection.insert([data[
1
], output.tolist()])

data_batch = [[],[]]
# Read the images into batches for embedding and insertion
for
path
in
tqdm(paths):
    im = Image.
open
(path).convert(
'RGB'
)
    data_batch[
0
].append(preprocess(im))
    data_batch[
1
].append(path)
if
len
(data_batch[
0
]) % BATCH_SIZE ==
0
:
        embed(data_batch)
        data_batch = [[],[]]
# Embed and insert the remainder
if
len
(data_batch[
0
]) !=
0
:
    embed(data_batch)
# Call a flush to index any unsealed segments.
collection.flush()
这一步相对耗时，因为 Embeddings 需要时间。喝一口咖啡，放松一下。
PyTorch 可能无法在 Python 3.9 及更早版本中很好地运行。请考虑使用 Python 3.10 及更高版本。
执行搜索
将所有数据插入 Milvus 后，我们就可以开始执行搜索了。在本例中，我们将搜索两张示例图片。由于我们进行的是批量搜索，因此搜索时间由批量中的图像共享。
import
glob
# Get the filepaths of the search images
search_paths = glob.glob(
'./paintings/test_paintings/**/*.jpg'
, recursive=
True
)
len
(search_paths)
import
time
from
matplotlib
import
pyplot
as
plt
# Embed the search images
def
embed
(
data
):
with
torch.no_grad():
        ret = model(torch.stack(data))
# If more than one image, use squeeze
if
len
(ret) >
1
:
return
ret.squeeze().tolist()
# Squeeze would remove batch for single image, so using flatten
else
:
return
torch.flatten(ret, start_dim=
1
).tolist()

data_batch = [[],[]]
for
path
in
search_paths:
    im = Image.
open
(path).convert(
'RGB'
)
    data_batch[
0
].append(preprocess(im))
    data_batch[
1
].append(path)

embeds = embed(data_batch[
0
])
start = time.time()
res = collection.search(embeds, anns_field=
'image_embedding'
, param={
'nprobe'
:
128
}, limit=TOP_K, output_fields=[
'filepath'
])
finish = time.time()
# Show the image results
f, axarr = plt.subplots(
len
(data_batch[
1
]), TOP_K +
1
, figsize=(
20
,
10
), squeeze=
False
)
for
hits_i, hits
in
enumerate
(res):
    axarr[hits_i][
0
].imshow(Image.
open
(data_batch[
1
][hits_i]))
    axarr[hits_i][
0
].set_axis_off()
    axarr[hits_i][
0
].set_title(
'Search Time: '
+
str
(finish - start))
for
hit_i, hit
in
enumerate
(hits):
        axarr[hits_i][hit_i +
1
].imshow(Image.
open
(hit.entity.get(
'filepath'
)))
        axarr[hits_i][hit_i +
1
].set_axis_off()
        axarr[hits_i][hit_i +
1
].set_title(
'Distance: '
+
str
(hit.distance))
# Save the search result in a separate image file alongside your script.
plt.savefig(
'search_result.png'
)
搜索结果图像应与下图类似：
图像搜索输出