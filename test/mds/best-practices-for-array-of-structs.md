使用结构数组设计数据模型
Compatible with Milvus 2.6.4+
现代人工智能应用，尤其是在物联网（IoT）和自动驾驶领域，通常会对丰富的结构化事件进行推理：带有时间戳和向量嵌入的传感器读数、带有错误代码和音频片段的诊断日志，或者带有位置、速度和场景上下文的行程片段。这些都要求数据库能够本机支持嵌套数据的摄取和搜索。
Milvus 没有要求用户将原子结构事件转换为平面数据模型，而是引入了结构数组（Array of Structs），数组中的每个结构都可以容纳标量和向量，从而保持了语义的完整性。
为什么要使用结构数组
从自动驾驶到多模态检索，现代人工智能应用越来越依赖于嵌套的异构数据。传统的平面数据模型难以表示复杂的关系，如
"一个文档包含许多注释块
"或
"一个驾驶场景包含多个观察到的操作
"。这正是 Milvus 的结构数组数据类型的优势所在。
数组结构体允许您存储一组有序的结构化元素，其中每个结构体都包含自己的标量字段和向量嵌入的组合。这使得它非常适合于
分层数据
：具有多个子记录的父实体，如具有许多文本块的书籍或具有许多注释帧的视频。
多模态嵌入
：每个 Struct 都可以容纳多个向量，如文本嵌入加图像嵌入，以及元数据。
时间或顺序数据
：数组字段中的结构体可以自然地表示时间序列或逐步发生的事件。
与存储 JSON blob 或在多个 Collections 中分割数据的传统变通方法不同，Structs 数组可在 Milvus 内提供原生 Schema 执行、向量索引和高效存储。
Schema 设计指南
除了在《
面向搜索的数据模型设计
》中讨论的所有准则外，在开始在数据模型设计中使用 Structs 阵列之前，还应考虑以下事项。
定义 Struct 模式 Schema
在将 Array 字段添加到 Collections 之前，请定义内部的 Struct 模式。Struct 中的每个字段都必须明确类型，标量
（VARCHAR
、
INT
、
BOOLEAN
等）或向量
（FLOAT_VECTOR
）。
建议您只包含用于检索或显示的字段，以保持 Schema 结构的精简。避免使用未使用的元数据造成臃肿。
深思熟虑地设置最大容量
每个数组字段都有一个属性，用于指定每个实体的数组字段可容纳的最大元素数。根据用例的上限来设置。例如，每个文档有 1000 个文本块，或每个驾驶场景有 100 个操作。
过高的值会浪费内存，因此需要进行一些计算来确定 Array 字段中 Struct 的最大数量。
在 Structs 中索引向量字段
对于向量场，包括 Collections 中的向量场和 Struct 中定义的向量场，都必须进行索引。对于 Struct 中的向量字段，应使用
AUTOINDEX
或
HNSW
作为索引类型，并使用
MAX_SIM
系列作为度量类型。
有关所有适用限制的详细信息，请参阅
限制
。
真实世界示例为自动驾驶建立 CoVLA 数据集模型
综合视觉-语言-动作（CoVLA）数据集由
图灵汽车公司
推出，并在 2025 年计算机视觉应用冬季会议（WACV）上被接受，它为训练和评估自动驾驶中的视觉-语言-动作（VLA）模型提供了丰富的基础。每个数据点（通常是视频片段）不仅包含原始视觉输入，还包含描述以下内容的结构化字幕：
自我车辆的行为
（例如，"向左并线，同时避让迎面而来的车辆"）、
检测到
的存在
对象
（如前方车辆、行人、交通信号灯），以及
场景的帧级
标题
。
这种分层、多模式的特性使其成为结构阵列功能的理想候选对象。有关 CoVLA 数据集的详细信息，请参阅
CoVLA 数据集网站
。
步骤 1：将数据集映射到 Collections Schema 中
CoVLA 数据集是一个大规模、多模态驾驶数据集，包含 10,000 个视频片段，总时长超过 80 小时。该数据集以 20Hz 的频率对帧进行采样，并为每一帧添加详细的自然语言说明以及车辆状态和检测到的物体坐标信息。
数据集结构如下：
├── video_1                                       (VIDEO)
# video.mp4
│   ├── video_id                                  (INT)
│   ├── video_url                                 (STRING)
│   ├── frames                                    (ARRAY)
│   │   ├── frame_1                               (STRUCT)
│   │   │   ├── caption                           (STRUCT)
# captions.jsonl
│   │   │   │   ├── plain_caption                 (STRING)
│   │   │   │   ├── rich_caption                  (STRING)
│   │   │   │   ├── risk                          (STRING)
│   │   │   │   ├── risk_correct                  (BOOL)
│   │   │   │   ├── risk_yes_rate                 (FLOAT)
│   │   │   │   ├── weather                       (STRING)
│   │   │   │   ├── weather_rate                  (FLOAT)
│   │   │   │   ├── road                          (STRING)
│   │   │   │   ├── road_rate                     (FLOAT)
│   │   │   │   ├── is_tunnel                     (BOOL)
│   │   │   │   ├── is_tunnel_yes_rate            (FLOAT)
│   │   │   │   ├── is_highway                    (BOOL)
│   │   │   │   ├── is_highway_yes_rate           (FLOAT)
│   │   │   │   ├── has_pedestrain                (BOOL)
│   │   │   │   ├── has_pedestrain_yes_rate       (FLOAT)
│   │   │   │   ├── has_carrier_car               (BOOL)
│   │   │   ├── traffic_light                     (STRUCT)
# traffic_lights.jsonl
│   │   │   │   ├── index                         (INT)
│   │   │   │   ├──
class
(STRING)
│   │   │   │   ├── bbox                          (LIST<FLOAT>)
│   │   │   ├── front_car                         (STRUCT)
# front_cars.jsonl
│   │   │   │   ├── has_lead                      (BOOL)
│   │   │   │   ├── lead_prob                     (FLOAT)
│   │   │   │   ├── lead_x                        (FLOAT)
│   │   │   │   ├── lead_y                        (FLOAT)
│   │   │   │   ├── lead_speed_kmh                (FLOAT)
│   │   │   │   ├── lead_a                        (FLOAT)
│   │   ├── frame_2                               (STRUCT)
│   │   ├── ...                                   (STRUCT)
│   │   ├── frame_n                               (STRUCT)
├── video_2
├── ...
├── video_n
您可以发现，CoVLA 数据集的结构具有很强的层次性，将 Collections 数据分为多个
.jsonl
文件，同时还有
.mp4
格式的视频片段。
在 Milvus 中，您可以使用 JSON 字段或 Array-of-Structs 字段在 Collections Schema 中创建嵌套结构。当向量嵌入是嵌套格式的一部分时，只支持结构数组字段。不过，数组内的结构体本身不能包含更多嵌套结构。要在保留基本关系的同时存储 CoVLA 数据集，就需要删除不必要的层次结构并将数据扁平化，使其符合 Milvus Collections Schema。
下图说明了我们如何使用下面的 Schema 模式为这个数据集建模：
数据集模型
上图说明了视频剪辑的结构，其中包括以下字段：
video_id
是主键，接受 INT64 类型的整数。
states
是一个原始 JSON 主体，包含当前视频中每一帧的小我车辆状态。
captions
是一个 Struct 数组，每个 Struct 都有以下字段：
frame_id
标识当前视频中的特定帧。
plain_caption
是对当前帧的描述，不包含周围环境，如天气、路况等，
plain_cap_vector
是其相应的向量嵌入。
rich_caption
是对当前有环境的帧的描述，
rich_cap_vector
是其对应的向量嵌入。
risk
是对当前帧中小我车辆所面临风险的描述，
risk_vector
是其对应的向量嵌入，以及
帧的其他所有属性，如
road
,
weather
,
is_tunnel
,
has_pedestrain
, 等。
traffic_lights
是一个 JSON 主体，包含当前帧中识别出的所有交通信号灯。
front_cars
也是一个结构数组，包含当前帧中识别出的所有前导车。
步骤 2：初始化 Schema
首先，我们需要初始化标题 Struct、front_cars Struct 和 Collections 的模式。
初始化标题结构（Caption Struct）的模式。
client = MilvusClient(
"http://localhost:19530"
)
# create the schema for the caption struct
schema_for_caption = client.create_struct_field_schema()

schema_for_caption.add_field(
    field_name=
"frame_id"
,
    datatype=DataType.INT64,
    description=
"ID of the frame to which the ego vehicle's behavior belongs"
)

schema_for_caption.add_field(
    field_name=
"plain_caption"
,
    datatype=DataType.VARCHAR,
    max_length=
1024
,
    description=
"plain description of the ego vehicle's behaviors"
)

schema_for_caption.add_field(
    field_name=
"plain_cap_vector"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
768
,
    description=
"vectors for the plain description of the ego vehicle's behaviors"
)

schema_for_caption.add_field(
    field_name=
"rich_caption"
,
    datatype=DataType.VARCHAR,
    max_length=
1024
,
    description=
"rich description of the ego vehicle's behaviors"
)

schema_for_caption.add_field(
    field_name=
"rich_cap_vector"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
768
,
    description=
"vectors for the rich description of the ego vehicle's behaviors"
)

schema_for_caption.add_field(
    field_name=
"risk"
,
    datatype=DataType.VARCHAR,
    max_length=
1024
,
    description=
"description of the ego vehicle's risks"
)

schema_for_caption.add_field(
    field_name=
"risk_vector"
,
    datatype=DataType.FLOAT_VECTOR,
    dim=
768
,
    description=
"vectors for the description of the ego vehicle's risks"
)

schema_for_caption.add_field(
    field_name=
"risk_correct"
,
    datatype=DataType.BOOL,
    description=
"whether the risk assessment is correct"
)

schema_for_caption.add_field(
    field_name=
"risk_yes_rate"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of risk being present"
)

schema_for_caption.add_field(
    field_name=
"weather"
,
    datatype=DataType.VARCHAR,
    max_length=
50
,
    description=
"weather condition"
)

schema_for_caption.add_field(
    field_name=
"weather_rate"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of the weather condition"
)

schema_for_caption.add_field(
    field_name=
"road"
,
    datatype=DataType.VARCHAR,
    max_length=
50
,
    description=
"road type"
)

schema_for_caption.add_field(
    field_name=
"road_rate"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of the road type"
)

schema_for_caption.add_field(
    field_name=
"is_tunnel"
,
    datatype=DataType.BOOL,
    description=
"whether the road is a tunnel"
)

schema_for_caption.add_field(
    field_name=
"is_tunnel_yes_rate"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of the road being a tunnel"
)

schema_for_caption.add_field(
    field_name=
"is_highway"
,
    datatype=DataType.BOOL,
    description=
"whether the road is a highway"
)

schema_for_caption.add_field(
    field_name=
"is_highway_yes_rate"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of the road being a highway"
)

schema_for_caption.add_field(
    field_name=
"has_pedestrian"
,
    datatype=DataType.BOOL,
    description=
"whether there is a pedestrian present"
)

schema_for_caption.add_field(
    field_name=
"has_pedestrian_yes_rate"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of pedestrian presence"
)

schema_for_caption.add_field(
    field_name=
"has_carrier_car"
,
    datatype=DataType.BOOL,
    description=
"whether there is a carrier car present"
)
初始化前车结构的 Schema 模式
虽然前车不涉及向量嵌入，但由于数据大小超过了 JSON 字段的最大值，因此仍需将其作为 Struct 数组包含在内。
schema_for_front_car = client.create_struct_field_schema()

schema_for_front_car.add_field(
    field_name=
"frame_id"
,
    datatype=DataType.INT64,
    description=
"ID of the frame to which the ego vehicle's behavior belongs"
)

schema_for_front_car.add_field(
    field_name=
"has_lead"
,
    datatype=DataType.BOOL,
    description=
"whether there is a leading vehicle"
)

schema_for_front_car.add_field(
    field_name=
"lead_prob"
,
    datatype=DataType.FLOAT,
    description=
"probability/confidence of the leading vehicle's presence"
)

schema_for_front_car.add_field(
    field_name=
"lead_x"
,
    datatype=DataType.FLOAT,
    description=
"x position of the leading vehicle relative to the ego vehicle"
)

schema_for_front_car.add_field(
    field_name=
"lead_y"
,
    datatype=DataType.FLOAT,
    description=
"y position of the leading vehicle relative to the ego vehicle"
)

schema_for_front_car.add_field(
    field_name=
"lead_speed_kmh"
,
    datatype=DataType.FLOAT,
    description=
"speed of the leading vehicle in km/h"
)

schema_for_front_car.add_field(
    field_name=
"lead_a"
,
    datatype=DataType.FLOAT,
    description=
"acceleration of the leading vehicle"
)
为 Collections 初始化 Schema
schema = client.create_schema()

schema.add_field(
    field_name=
"video_id"
,
    datatype=DataType.VARCHAR,
    description=
"primary key"
,
    max_length=
16
,
    is_primary=
True
,
    auto_id=
False
)

schema.add_field(
    field_name=
"video_url"
,
    datatype=DataType.VARCHAR,
    max_length=
512
,
    description=
"URL of the video"
)

schema.add_field(
    field_name=
"captions"
,
    datatype=DataType.ARRAY,
    element_type=DataType.STRUCT,
    struct_schema=schema_for_caption,
    max_capacity=
600
,
    description=
"captions for the current video"
)

schema.add_field(
    field_name=
"traffic_lights"
,
    datatype=DataType.JSON,
    description=
"frame-specific traffic lights identified in the current video"
)

schema.add_field(
    field_name=
"front_cars"
,
    datatype=DataType.ARRAY,
    element_type=DataType.STRUCT,
    struct_schema=schema_for_front_car,
    max_capacity=
600
,
    description=
"frame-specific leading cars identified in the current video"
)
第 3 步：设置索引参数
所有向量字段都必须有索引。要索引元素 Struct 中的向量字段，需要使用
AUTOINDEX
或
HNSW
作为索引类型，并使用
MAX_SIM
系列度量类型来衡量嵌入列表之间的相似性。
index_params = client.prepare_index_params()

index_params.add_index(
    field_name=
"captions[plain_cap_vector]"
, 
    index_type=
"AUTOINDEX"
, 
    metric_type=
"MAX_SIM_COSINE"
, 
    index_name=
"captions_plain_cap_vector_idx"
,
# mandatory for now
index_params={
"M"
:
16
,
"efConstruction"
:
200
}
)

index_params.add_index(
    field_name=
"captions[rich_cap_vector]"
, 
    index_type=
"AUTOINDEX"
, 
    metric_type=
"MAX_SIM_COSINE"
, 
    index_name=
"captions_rich_cap_vector_idx"
,
# mandatory for now
index_params={
"M"
:
16
,
"efConstruction"
:
200
}
)

index_params.add_index(
    field_name=
"captions[risk_vector]"
, 
    index_type=
"AUTOINDEX"
, 
    metric_type=
"MAX_SIM_COSINE"
, 
    index_name=
"captions_risk_vector_idx"
,
# mandatory for now
index_params={
"M"
:
16
,
"efConstruction"
:
200
}
)
建议启用 JSON 字段的 JSON 切碎功能，以加快这些字段的过滤速度。
第 4 步：创建 Collections
Schema 和索引准备就绪后，您就可以按如下步骤创建目标 Collections：
client.create_collection(
    collection_name=
"covla_dataset"
,
    schema=schema,
    index_params=index_params
)
第 5 步：插入数据
Turing Motos 将 CoVLA 数据集整理为多个文件，包括原始视频片段 (
.mp4
)、状态 (
states.jsonl
)、字幕 (
captions.jsonl
)、交通灯 (
traffic_lights.jsonl
)和前车 (
front_cars.jsonl
)。
您需要合并这些文件中每个视频片段的数据块并插入数据。以下是为特定视频片段合并数据块的脚本。
import
json
from
openai
import
OpenAI

openai_client = OpenAI(
    api_key=
'YOUR_OPENAI_API_KEY'
,
)

video_id =
"0a0fc7a5db365174"
# represent a single video with 600 frames
# get all front car records in the specified video clip
entries = []
front_cars = []
with
open
(
'data/front_car/{}.jsonl'
.
format
(video_id),
'r'
)
as
f:
for
line
in
f:
        entries.append(json.loads(line))
for
entry
in
entries:
for
key, value
in
entry.items():
        value[
'frame_id'
] =
int
(key)
        front_cars.append(value)
# get all traffic lights identified in the specified video clip
entries = []
traffic_lights = []
frame_id =
0
with
open
(
'data/traffic_lights/{}.jsonl'
.
format
(video_id),
'r'
)
as
f:
for
line
in
f:
        entries.append(json.loads(line))
for
entry
in
entries:
for
key, value
in
entry.items():
if
not
value
or
(value[
'index'
] ==
1
and
key !=
'0'
):
            frame_id+=
1
if
value:
            value[
'frame_id'
] = frame_id
            traffic_lights.append(value)
else
:
            value_dict = {}
            value_dict[
'frame_id'
] = frame_id
            traffic_lights.append(value_dict)
# get all captions generated in the video clip and convert them into vector embeddings
entries = []
captions = []
with
open
(
'data/captions/{}.jsonl'
.
format
(video_id),
'r'
)
as
f:
for
line
in
f:
        entries.append(json.loads(line))
def
get_embedding
(
text, model=
"embeddinggemma:latest"
):
    response = openai_client.embeddings.create(
input
=text, model=model)
return
response.data[
0
].embedding
# Add embeddings to each entry
for
entry
in
entries:
# Each entry is a dict with a single key (e.g., '0', '1', ...)
for
key, value
in
entry.items():
        value[
'frame_id'
] =
int
(key)
# Convert key to integer and assign to frame_id
if
"plain_caption"
in
value
and
value[
"plain_caption"
]:
            value[
"plain_cap_vector"
] = get_embedding(value[
"plain_caption"
])
if
"rich_caption"
in
value
and
value[
"rich_caption"
]:
            value[
"rich_cap_vector"
] = get_embedding(value[
"rich_caption"
])
if
"risk"
in
value
and
value[
"risk"
]:
            value[
"risk_vector"
] = get_embedding(value[
"risk"
])

        captions.append(value)

data = {
"video_id"
: video_id,
"video_url"
:
"https://your-storage.com/{}"
.
format
(video_id),
"captions"
: captions,
"traffic_lights"
: traffic_lights,
"front_cars"
: front_cars
}
对数据进行相应处理后，您就可以按如下方式插入数据：
client.insert(
    collection_name=
"covla_dataset"
,
    data=[data]
)
# {'insert_count': 1, 'ids': ['0a0fc7a5db365174'], 'cost': 0}