LangExtract + Milvus 集成
本指南演示了如何使用
LangExtract
与
Milvus
来构建智能文档处理和检索系统。
LangExtract 是一个 Python 库，它使用大型语言模型 (LLMs) 从非结构化文本文档中提取结构化信息，并提供精确的源基础。该系统将 LangExtract 的提取能力与 Milvus 的向量存储相结合，既能进行语义相似性搜索，又能进行精确的元数据过滤。
这种整合对于内容管理、语义搜索、知识发现以及基于提取的文档属性构建推荐系统尤为重要。
先决条件
在运行本笔记本之前，请确保已安装以下依赖项：
$
pip install --upgrade pymilvus milvus-lite langextract google-genai requests tqdm pandas
如果使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 Gemini 作为 LLM。您应将
api key
GEMINI_API_KEY
作为环境变量。
import
os

os.environ[
"GEMINI_API_KEY"
] =
"AIza*****************"
定义 LangExtract + Milvus 管道
我们将定义使用 LangExtract 进行结构化信息提取、使用 Milvus 作为向量存储的管道。
import
langextract
as
lx
import
textwrap
from
google
import
genai
from
google.genai.types
import
EmbedContentConfig
from
pymilvus
import
MilvusClient, DataType
import
uuid
配置和设置
让我们为集成配置全局参数。我们将使用 Gemini 的 Embeddings 模型为文档生成向量表示。
genai_client = genai.Client()

COLLECTION_NAME =
"document_extractions"
EMBEDDING_MODEL =
"gemini-embedding-001"
EMBEDDING_DIM =
3072
# Default dimension for gemini-embedding-001
初始化 Milvus 客户端
现在让我们初始化 Milvus 客户端。为简单起见，我们将使用本地数据库文件，但这可以很容易地扩展到完整的 Milvus 服务器部署。
client = MilvusClient(uri=
"./milvus_demo.db"
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
样本数据准备
在本演示中，我们将使用电影描述作为样本文档。这展示了 LangExtract 从非结构化文本中提取流派、角色和主题等结构化信息的能力。
sample_documents = [
"John McClane fights terrorists in a Los Angeles skyscraper during Christmas Eve. The action-packed thriller features intense gunfights and explosive scenes."
,
"A young wizard named Harry Potter discovers his magical abilities at Hogwarts School. The fantasy adventure includes magical creatures and epic battles."
,
"Tony Stark builds an advanced suit of armor to become Iron Man. The superhero movie showcases cutting-edge technology and spectacular action sequences."
,
"A group of friends get lost in a haunted forest where supernatural creatures lurk. The horror film creates a terrifying atmosphere with jump scares."
,
"Two detectives investigate a series of mysterious murders in New York City. The crime thriller features suspenseful plot twists and dramatic confrontations."
,
"A brilliant scientist creates artificial intelligence that becomes self-aware. The sci-fi thriller explores the dangers of advanced technology and human survival."
,
"A romantic comedy about two friends who fall in love during a cross-country road trip. The drama explores personal growth and relationship dynamics."
,
"An evil sorcerer threatens to destroy the magical kingdom. A brave hero must gather allies and master ancient magic to save the fantasy world."
,
"Space marines battle alien invaders on a distant planet. The action sci-fi movie features futuristic weapons and intense combat in space."
,
"A detective investigates supernatural crimes in Victorian London. The horror thriller combines period drama with paranormal investigation themes."
,
]
print
(
"=== LangExtract + Milvus Integration Demo ==="
)
print
(
f"Preparing to process
{
len
(sample_documents)}
documents"
)
=== LangExtract + Milvus Integration Demo ===
Preparing to process 10 documents
设置 Milvus Collections
在存储提取的数据之前，我们需要创建一个具有相应 Schema 的 Milvus Collections。该 Collections 将存储原始文档文本、向量嵌入和提取的元数据字段。
print
(
"\n1. Setting up Milvus collection..."
)
# Drop existing collection if it exists
if
client.has_collection(collection_name=COLLECTION_NAME):
    client.drop_collection(collection_name=COLLECTION_NAME)
print
(
f"Dropped existing collection:
{COLLECTION_NAME}
"
)
# Create collection schema
schema = client.create_schema(
    auto_id=
False
,
    enable_dynamic_field=
True
,
    description=
"Document extraction results and vector storage"
,
)
# Add fields - simplified to 3 main metadata fields
schema.add_field(
    field_name=
"id"
, datatype=DataType.VARCHAR, max_length=
100
, is_primary=
True
)
schema.add_field(
    field_name=
"document_text"
, datatype=DataType.VARCHAR, max_length=
10000
)
schema.add_field(
    field_name=
"embedding"
, datatype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM
)
# Create collection
client.create_collection(collection_name=COLLECTION_NAME, schema=schema)
print
(
f"Collection '
{COLLECTION_NAME}
' created successfully"
)
# Create vector index
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"embedding"
,
    index_type=
"AUTOINDEX"
,
    metric_type=
"COSINE"
,
)
client.create_index(collection_name=COLLECTION_NAME, index_params=index_params)
print
(
"Vector index created successfully"
)
1. Setting up Milvus collection...
Dropped existing collection: document_extractions
Collection 'document_extractions' created successfully
Vector index created successfully
定义提取模式 Schema
LangExtract 使用提示和示例来引导 LLM 提取结构化信息。让我们来定义电影描述的提取 Schema，指定要提取哪些信息以及如何对其进行分类。
print
(
"\n2. Extracting tags from documents..."
)
# Define extraction prompt - for movie descriptions, specify attribute value ranges
prompt = textwrap.dedent(
"""\
    Extract movie genre, main characters, and key themes from movie descriptions.
    Use exact text for extractions. Do not paraphrase or overlap entities.
    
    For each extraction, provide attributes with values from these predefined sets:
    
    Genre attributes:
    - primary_genre: ["action", "comedy", "drama", "horror", "sci-fi", "fantasy", "thriller", "crime", "superhero"]
    - secondary_genre: ["action", "comedy", "drama", "horror", "sci-fi", "fantasy", "thriller", "crime", "superhero"]
    
    Character attributes:
    - role: ["protagonist", "antagonist", "supporting"]
    - type: ["hero", "villain", "detective", "military", "wizard", "scientist", "friends", "investigator"]
    
    Theme attributes:
    - theme_type: ["conflict", "investigation", "personal_growth", "technology", "magic", "survival", "romance"]
    - setting: ["urban", "space", "fantasy_world", "school", "forest", "victorian", "america", "future"]
    
    Focus on identifying key elements that would be useful for movie search and filtering."""
)
2. Extracting tags from documents...
提供示例，更好地提取信息
为了提高提取的质量和一致性，我们将为 LangExtract 提供一些示例。这些示例展示了预期的格式，有助于模型理解我们的提取要求。
# Provide examples to guide the model - n-shot examples for movie descriptions
# Unify attribute keys to ensure consistency in extraction results
examples = [
    lx.data.ExampleData(
        text=
"A space marine battles alien creatures on a distant planet. The sci-fi action movie features futuristic weapons and intense combat scenes."
,
        extractions=[
            lx.data.Extraction(
                extraction_class=
"genre"
,
                extraction_text=
"sci-fi action"
,
                attributes={
"primary_genre"
:
"sci-fi"
,
"secondary_genre"
:
"action"
},
            ),
            lx.data.Extraction(
                extraction_class=
"character"
,
                extraction_text=
"space marine"
,
                attributes={
"role"
:
"protagonist"
,
"type"
:
"military"
},
            ),
            lx.data.Extraction(
                extraction_class=
"theme"
,
                extraction_text=
"battles alien creatures"
,
                attributes={
"theme_type"
:
"conflict"
,
"setting"
:
"space"
},
            ),
        ],
    ),
    lx.data.ExampleData(
        text=
"A detective investigates supernatural murders in Victorian London. The horror thriller film combines period drama with paranormal elements."
,
        extractions=[
            lx.data.Extraction(
                extraction_class=
"genre"
,
                extraction_text=
"horror thriller"
,
                attributes={
"primary_genre"
:
"horror"
,
"secondary_genre"
:
"thriller"
},
            ),
            lx.data.Extraction(
                extraction_class=
"character"
,
                extraction_text=
"detective"
,
                attributes={
"role"
:
"protagonist"
,
"type"
:
"detective"
},
            ),
            lx.data.Extraction(
                extraction_class=
"theme"
,
                extraction_text=
"supernatural murders"
,
                attributes={
"theme_type"
:
"investigation"
,
"setting"
:
"victorian"
},
            ),
        ],
    ),
    lx.data.ExampleData(
        text=
"Two friends embark on a road trip adventure across America. The comedy drama explores friendship and self-discovery through humorous situations."
,
        extractions=[
            lx.data.Extraction(
                extraction_class=
"genre"
,
                extraction_text=
"comedy drama"
,
                attributes={
"primary_genre"
:
"comedy"
,
"secondary_genre"
:
"drama"
},
            ),
            lx.data.Extraction(
                extraction_class=
"character"
,
                extraction_text=
"two friends"
,
                attributes={
"role"
:
"protagonist"
,
"type"
:
"friends"
},
            ),
            lx.data.Extraction(
                extraction_class=
"theme"
,
                extraction_text=
"friendship and self-discovery"
,
                attributes={
"theme_type"
:
"personal_growth"
,
"setting"
:
"america"
},
            ),
        ],
    ),
]
# Extract from each document
extraction_results = []
for
doc
in
sample_documents:
    result = lx.extract(
        text_or_documents=doc,
        prompt_description=prompt,
        examples=examples,
        model_id=
"gemini-2.0-flash"
,
    )
    extraction_results.append(result)
print
(
f"Successfully extracted from document:
{doc[:
50
]}
..."
)
print
(
f"Completed tag extraction, processed
{
len
(extraction_results)}
documents"
)
处理结果并将其向量化
现在，我们需要处理提取结果，并为每个文档生成向量嵌入。我们还将把提取的属性扁平化为单独的字段，以便在 Milvus 中轻松搜索。
print
(
"\n3. Processing extraction results and generating vectors..."
)

processed_data = []
for
result
in
extraction_results:
# Generate vectors for documents
embedding_response = genai_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[result.text],
        config=EmbedContentConfig(
            task_type=
"RETRIEVAL_DOCUMENT"
,
            output_dimensionality=EMBEDDING_DIM,
        ),
    )
    embedding = embedding_response.embeddings[
0
].values
print
(
f"Successfully generated vector:
{result.text[:
30
]}
..."
)
# Initialize data structure, flatten attributes into separate fields
data_entry = {
"id"
: result.document_id
or
str
(uuid.uuid4()),
"document_text"
: result.text,
"embedding"
: embedding,
# Initialize all possible fields with default values
"genre"
:
"unknown"
,
"primary_genre"
:
"unknown"
,
"secondary_genre"
:
"unknown"
,
"character_role"
:
"unknown"
,
"character_type"
:
"unknown"
,
"theme_type"
:
"unknown"
,
"theme_setting"
:
"unknown"
,
    }
# Process extraction results, flatten attributes
for
extraction
in
result.extractions:
if
extraction.extraction_class ==
"genre"
:
# Flatten genre attributes
data_entry[
"genre"
] = extraction.extraction_text
            attrs = extraction.attributes
or
{}
            data_entry[
"primary_genre"
] = attrs.get(
"primary_genre"
,
"unknown"
)
            data_entry[
"secondary_genre"
] = attrs.get(
"secondary_genre"
,
"unknown"
)
elif
extraction.extraction_class ==
"character"
:
# Flatten character attributes (take first main character's attributes)
attrs = extraction.attributes
or
{}
if
(
                data_entry[
"character_role"
] ==
"unknown"
):
# Only take first character's attributes
data_entry[
"character_role"
] = attrs.get(
"role"
,
"unknown"
)
                data_entry[
"character_type"
] = attrs.get(
"type"
,
"unknown"
)
elif
extraction.extraction_class ==
"theme"
:
# Flatten theme attributes (take first main theme's attributes)
attrs = extraction.attributes
or
{}
if
(
                data_entry[
"theme_type"
] ==
"unknown"
):
# Only take first theme's attributes
data_entry[
"theme_type"
] = attrs.get(
"theme_type"
,
"unknown"
)
                data_entry[
"theme_setting"
] = attrs.get(
"setting"
,
"unknown"
)

    processed_data.append(data_entry)
print
(
f"Completed data processing, ready to insert
{
len
(processed_data)}
records"
)
3. Processing extraction results and generating vectors...
Successfully generated vector: John McClane fights terrorists...
Successfully generated vector: A young wizard named Harry Pot...
Successfully generated vector: Tony Stark builds an advanced ...
Successfully generated vector: A group of friends get lost in...
Successfully generated vector: Two detectives investigate a s...
Successfully generated vector: A brilliant scientist creates ...
Successfully generated vector: A romantic comedy about two fr...
Successfully generated vector: An evil sorcerer threatens to ...
Successfully generated vector: Space marines battle alien inv...
Successfully generated vector: A detective investigates super...
Completed data processing, ready to insert 10 records
将数据插入 Milvus
处理好数据后，让我们将其插入 Milvus Collections。这将使我们能够执行语义搜索和精确的元数据过滤。
print
(
"\n4. Inserting data into Milvus..."
)
if
processed_data:
    res = client.insert(collection_name=COLLECTION_NAME, data=processed_data)
print
(
f"Successfully inserted
{
len
(processed_data)}
documents into Milvus"
)
print
(
f"Insert result:
{res}
"
)
else
:
print
(
"No data to insert"
)
4. Inserting data into Milvus...
Successfully inserted 10 documents into Milvus
Insert result: {'insert_count': 10, 'ids': ['doc_f8797155', 'doc_78c7e586', 'doc_fa3a3ab5', 'doc_64981815', 'doc_3ab18cb2', 'doc_1ea42b18', 'doc_f0779243', 'doc_386590b7', 'doc_3b3ae1ab', 'doc_851089d6']}
元数据过滤演示
将 LangExtract 与 Milvus 相结合的主要优势之一是能够根据提取的元数据执行精确过滤。让我们用一些过滤表达式搜索来演示一下。
print
(
"\n=== Filter Expression Search Examples ==="
)
# Load collection into memory for querying
print
(
"Loading collection into memory..."
)
client.load_collection(collection_name=COLLECTION_NAME)
print
(
"Collection loaded successfully"
)
# Search for thriller movies
print
(
"\n1. Searching for thriller movies:"
)
results = client.query(
    collection_name=COLLECTION_NAME,
filter
=
'secondary_genre == "thriller"'
,
    output_fields=[
"document_text"
,
"genre"
,
"primary_genre"
,
"secondary_genre"
],
    limit=
5
,
)
for
result
in
results:
print
(
f"-
{result[
'document_text'
][:
100
]}
..."
)
print
(
f"  Genre:
{result[
'genre'
]}
(
{result.get(
'primary_genre'
)}
-
{result.get(
'secondary_genre'
)}
)"
)
# Search for movies with military characters
print
(
"\n2. Searching for movies with military characters:"
)
results = client.query(
    collection_name=COLLECTION_NAME,
filter
=
'character_type == "military"'
,
    output_fields=[
"document_text"
,
"genre"
,
"character_role"
,
"character_type"
],
    limit=
5
,
)
for
result
in
results:
print
(
f"-
{result[
'document_text'
][:
100
]}
..."
)
print
(
f"  Genre:
{result[
'genre'
]}
"
)
print
(
f"  Character:
{result.get(
'character_role'
)}
(
{result.get(
'character_type'
)}
)"
)
=== Filter Expression Search Examples ===
Loading collection into memory...
Collection loaded successfully

1. Searching for thriller movies:
- A brilliant scientist creates artificial intelligence that becomes self-aware. The sci-fi thriller e...
  Genre: sci-fi thriller (sci-fi-thriller)
- Two detectives investigate a series of mysterious murders in New York City. The crime thriller featu...
  Genre: crime thriller (crime-thriller)
- A detective investigates supernatural crimes in Victorian London. The horror thriller combines perio...
  Genre: horror thriller (horror-thriller)
- John McClane fights terrorists in a Los Angeles skyscraper during Christmas Eve. The action-packed t...
  Genre: action-packed thriller (action-thriller)

2. Searching for movies with military characters:
- Space marines battle alien invaders on a distant planet. The action sci-fi movie features futuristic...
  Genre: action sci-fi
  Character: protagonist (military)
将语义搜索与元数据过滤相结合
将语义向量搜索与精确的元数据过滤相结合，才是这种集成的真正威力所在。这使我们能够找到语义相似的内容，同时根据提取的属性应用特定的限制条件。
print
(
"\n=== Semantic Search Examples ==="
)
# 1. Search for action-related content + only thriller genre
print
(
"\n1. Searching for action-related content + only thriller genre:"
)
query_text =
"action fight combat battle explosion"
query_embedding_response = genai_client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=[query_text],
    config=EmbedContentConfig(
        task_type=
"RETRIEVAL_QUERY"
,
        output_dimensionality=EMBEDDING_DIM,
    ),
)
query_embedding = query_embedding_response.embeddings[
0
].values

results = client.search(
    collection_name=COLLECTION_NAME,
    data=[query_embedding],
    anns_field=
"embedding"
,
    limit=
3
,
filter
=
'secondary_genre == "thriller"'
,
    output_fields=[
"document_text"
,
"genre"
,
"primary_genre"
,
"secondary_genre"
],
    search_params={
"metric_type"
:
"COSINE"
},
)
if
results:
for
result
in
results[
0
]:
print
(
f"- Similarity:
{result[
'distance'
]:
.4
f}
"
)
print
(
f"  Text:
{result[
'document_text'
][:
100
]}
..."
)
print
(
f"  Genre:
{result.get(
'genre'
)}
(
{result.get(
'primary_genre'
)}
-
{result.get(
'secondary_genre'
)}
)"
)
# 2. Search for magic-related content + fantasy genre + conflict theme
print
(
"\n2. Searching for magic-related content + fantasy genre + conflict theme:"
)
query_text =
"magic wizard spell fantasy magical"
query_embedding_response = genai_client.models.embed_content(
    model=EMBEDDING_MODEL,
    contents=[query_text],
    config=EmbedContentConfig(
        task_type=
"RETRIEVAL_QUERY"
,
        output_dimensionality=EMBEDDING_DIM,
    ),
)
query_embedding = query_embedding_response.embeddings[
0
].values

results = client.search(
    collection_name=COLLECTION_NAME,
    data=[query_embedding],
    anns_field=
"embedding"
,
    limit=
3
,
filter
=
'primary_genre == "fantasy" and theme_type == "conflict"'
,
    output_fields=[
"document_text"
,
"genre"
,
"primary_genre"
,
"theme_type"
,
"theme_setting"
,
    ],
    search_params={
"metric_type"
:
"COSINE"
},
)
if
results:
for
result
in
results[
0
]:
print
(
f"- Similarity:
{result[
'distance'
]:
.4
f}
"
)
print
(
f"  Text:
{result[
'document_text'
][:
100
]}
..."
)
print
(
f"  Genre:
{result.get(
'genre'
)}
(
{result.get(
'primary_genre'
)}
)"
)
print
(
f"  Theme:
{result.get(
'theme_type'
)}
(
{result.get(
'theme_setting'
)}
)"
)
print
(
"\n=== Demo Complete ==="
)
=== Semantic Search Examples ===

1. Searching for action-related content + only thriller genre:
- Similarity: 0.6947
  Text: John McClane fights terrorists in a Los Angeles skyscraper during Christmas Eve. The action-packed t...
  Genre: action-packed thriller (action-thriller)
- Similarity: 0.6128
  Text: Two detectives investigate a series of mysterious murders in New York City. The crime thriller featu...
  Genre: crime thriller (crime-thriller)
- Similarity: 0.5889
  Text: A brilliant scientist creates artificial intelligence that becomes self-aware. The sci-fi thriller e...
  Genre: sci-fi thriller (sci-fi-thriller)

2. Searching for magic-related content + fantasy genre + conflict theme:
- Similarity: 0.6986
  Text: An evil sorcerer threatens to destroy the magical kingdom. A brave hero must gather allies and maste...
  Genre: fantasy (fantasy)
  Theme: conflict (fantasy_world)

=== Demo Complete ===