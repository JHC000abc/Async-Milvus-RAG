Agents.md - Milvus
Milvus 是一个开源向量数据库，用于相似性搜索、混合搜索和 RAG。您可以通过 PyMilvus SDK 的
MilvusClient
界面与之交互。将下面的完整提示复制到您的人工智能工具中，即可自动应用这些规则。有关特定任务的详细提示，请参阅
人工智能提示
。
如何使用此提示
从下面的完整提示部分
复制
完整提示
。
将其
保存
到人工智能工具所需的位置 - 有关位置的详细信息，请参阅
环境表
。
在生成或审核 Milvus 代码时，您的人工智能助手将自动应用这些规则。
对于
Cursor
用户：从
完整提示
部分复制提示，并将其保存在项目中的
.cursor/rules/
下。
完整提示
在光标中打开
# AGENTS.md — Milvus

Milvus is an open-source vector database for similarity search, hybrid search, and RAG. You interact with it through the PyMilvus SDK's `MilvusClient` interface.

Use these rules whenever you generate, review, or debug code that connects to Milvus or Zilliz Cloud.

## Client & connection

1. **CRITICAL — Always use `MilvusClient`.** Never use the legacy ORM API (`connections.connect()`, `Collection()`, `utility.list_collections()`). The ORM API is deprecated and will be removed. If the user provides ORM code, rewrite it to `MilvusClient`.

2. **Connection patterns.** Local unauthenticated: `uri` only. Zilliz Cloud or authenticated Milvus: `uri` + `token`.

```python
# Local Milvus
client = MilvusClient(uri="http://localhost:19530")

# Zilliz Cloud / authenticated Milvus
client = MilvusClient(uri="YOUR_MILVUS_URI", token="YOUR_MILVUS_TOKEN")
```

## Schema & data

3. **CRITICAL — Use `DataType` enum, not strings.** Write `DataType.FLOAT_VECTOR`, not `"FLOAT_VECTOR"`.

4. **CRITICAL — Schema is immutable in v2.5.x and earlier.** You cannot add, modify, or delete fields after creation — drop and recreate the collection. In v2.6+, you can add new nullable fields with `add_collection_field()` but still cannot modify or delete existing fields.

5. **Primary keys: `INT64` or `VARCHAR` only.** Composite primary keys are not supported. Primary keys must be unique across the entire collection, including across partitions.

6. **Use `upsert()` to update entities.** There is no `client.update()` method. `upsert()` replaces the entire entity if the primary key exists, or inserts a new one. Use `insert()` only when you are certain there are no primary key conflicts.

7. **BM25 must be defined at collection creation time.** The BM25 function and text analyzer cannot be added to an existing collection.

## Index & loading

8. **CRITICAL — Index before load, load before search.** A vector field must have an index before the collection can be loaded. A collection must be loaded before any search or query. Shortcut: pass both `schema` and `index_params` to `create_collection()` and Milvus handles index creation and loading automatically.

9. **Start with `AUTOINDEX`.** Use `index_type="AUTOINDEX"` unless you have specific requirements. Choose HNSW for high recall, DiskANN for larger-than-RAM datasets, IVF_FLAT for memory-constrained scenarios.

## Search

10. **CRITICAL — One vector per `AnnSearchRequest`.** Each sub-request in a hybrid search accepts exactly one query vector. Do not pass a list of multiple vectors.

11. **One ranker per `hybrid_search()` call.** You cannot chain `WeightedRanker` and `RRFRanker` together. Pick one.

## Quick start

```python
from pymilvus import MilvusClient, DataType

client = MilvusClient(uri="http://localhost:19530")

# 1. Define schema
schema = client.create_schema(auto_id=True)
schema.add_field("id", DataType.INT64, is_primary=True)
schema.add_field("vector", DataType.FLOAT_VECTOR, dim=768)
schema.add_field("text", DataType.VARCHAR, max_length=512)

# 2. Define index
index_params = client.prepare_index_params()
index_params.add_index(field_name="vector", index_type="AUTOINDEX", metric_type="COSINE")

# 3. Create collection (auto-indexes and auto-loads)
client.create_collection(collection_name="docs", schema=schema, index_params=index_params)

# 4. Insert
client.insert(collection_name="docs", data=[
    {"vector": [0.1] * 768, "text": "first doc"},
    {"vector": [0.2] * 768, "text": "second doc"},
])

# 5. Search
results = client.search(
    collection_name="docs",
    data=[[0.15] * 768],
    limit=5,
    output_fields=["text"],
)
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Using `connections.connect()` / `Collection()` | Rewrite with `MilvusClient` |
| Calling `client.search()` before loading | Pass `index_params` to `create_collection()`, or call `create_index()` then `load_collection()` first |
| Multiple vectors in one `AnnSearchRequest` | One vector per sub-request; create multiple `AnnSearchRequest` objects |
| Calling `client.update()` | Use `client.upsert()` |
| Adding BM25 after collection exists | Define BM25 function and analyzer at `create_collection()` time |
| String field types (`"FLOAT_VECTOR"`) | Use `DataType.FLOAT_VECTOR` from the enum |