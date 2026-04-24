文本高亮显示
Compatible with Milvus 2.6.8+
Milvus 的高亮显示器通过使用可定制的标签对文本字段中的匹配术语进行注释。高亮有助于解释文档匹配的原因，提高结果的可读性，并支持在搜索和 RAG 应用程序中进行丰富的渲染。
高亮显示是作为最终搜索结果集的后处理步骤执行的。它不会影响候选检索、过滤逻辑、排序或评分。
高亮工具提供三个独立的控制维度：
高亮显示哪些术语
您可以选择高亮显示的术语来自何处。例如，高亮显示
BM25 全文搜索
中使用的搜索词，或
基于文本的过滤表达式
（如
TEXT_MATCH
条件）中指定的查询词。
高亮显示术语的呈现方式
您可以通过配置在每个匹配词前后插入的标记来控制匹配词在高亮输出中的显示方式。例如，使用
{}
等简单标记或
<em></em>
等 HTML 标记进行丰富的呈现。
高亮文本的返回方式
您可以控制高亮结果如何以片段形式返回，包括片段的起始位置、长度以及返回的片段数量。
以下章节将介绍这些情况。
在 BM25 全文搜索中高亮显示搜索词
执行 BM25 全文搜索时，可在返回结果中高亮显示
搜索词
，以帮助解释文档与查询匹配的原因。要了解有关 BM25 全文搜索的更多信息，请参阅全文
搜索
。
在这种情况下，高亮显示的术语直接来自 BM25 全文搜索中使用的搜索术语。高亮显示器使用这些术语在最终结果中注释匹配的文本。
假设文本字段中存储了以下内容：
Milvus supports full text search. Use BM25 for keyword relevance. Filters can narrow results.
高亮显示配置
要在 BM25 全文搜索中突出显示搜索词，请创建
LexicalHighlighter
并启用 BM25 全文搜索的搜索词突出显示功能：
from
pymilvus
import
LexicalHighlighter

highlighter = LexicalHighlighter(
    pre_tags=[
"{"
],
# Tag inserted before each highlighted term
post_tags=[
"}"
],
# Tag inserted after each highlighted term
highlight_search_text=
True
# Enable search term highlighting for BM25 full text search
)
在此示例中：
pre_tags
和
post_tags
控制高亮文本在输出中的显示方式。在本例中，匹配的术语由
{}
包装（例如，
{term}
）。您也可以以列表形式提供多个标记（例如，
["<b>", "<i>"]
）。当多个术语被高亮显示时，标记将按顺序应用，并根据匹配序列旋转。
highlight_search_text=True
告诉 Milvus 使用 BM25 全文搜索中的搜索词作为高亮显示词的来源。
创建高亮对象后，将其配置应用于 BM25 全文搜索请求：
results = client.search(
    ...,
    data=[
"BM25"
],
# Search term used in BM25 full text search
highlighter=highlighter
# Pass highlighter config here
)
高亮输出
启用高亮输出后，Milvus 会在专用的
highlight
字段中返回高亮文本。默认情况下，高亮输出以片段形式返回，从第一个匹配词开始。
在本例中，搜索词是
"BM25"
，因此它在返回结果中被高亮显示：
{
...
,
"highlight"
:
{
"text"
:
[
"{BM25} for keyword relevance. Filters can narrow results."
]
}
}
要控制返回片段的位置、长度和数量，请参阅
以片段形式返回高亮文本
。
在筛选中高亮显示查询词
除了高亮显示搜索条件外，还可以高亮显示基于文本的筛选表达式中使用的条件。
目前，查询术语高亮显示只支持
TEXT_MATCH
过滤条件。要了解更多信息，请参阅
文本匹配
。
在这种情况下，高亮显示的术语来自基于文本的过滤表达式。过滤决定哪些文档匹配，而高亮显示器则注释匹配的文本跨度。
假设以下内容存储在文本字段中：
This document explains how text filtering works
in
Milvus.
高亮显示配置
要高亮显示过滤中使用的查询词，请创建
LexicalHighlighter
并定义与过滤条件相对应的
highlight_query
：
from
pymilvus
import
LexicalHighlighter

highlighter = LexicalHighlighter(
    pre_tags=[
"{"
],
# Tag inserted before each highlighted term
post_tags=[
"}"
],
# Tag inserted after each highlighted term
highlight_query=[{
"type"
:
"TextMatch"
,
# Text filtering type
"field"
:
"text"
,
# Target text field
"text"
:
"text filtering"
# Terms to highlight
}]
)
在此配置中：
pre_tags
和
post_tags
控制高亮文本在输出中的显示方式。在这种情况下，匹配的术语由
{}
封装（例如，
{term}
）。您也可以以列表形式提供多个标记（例如，
["<b>", "<i>"]
）。当多个术语被高亮显示时，标记将按顺序应用，并根据匹配序列旋转。
highlight_query
定义应高亮显示哪些过滤词。
创建高亮对象后，将相同的过滤表达式和高亮配置应用到搜索请求中：
results = client.search(
    ...,
filter
=
'TEXT_MATCH(text, "text filtering")'
,
highlighter=highlighter
# Pass highlighter config here
)
高亮输出
当过滤启用查询词高亮时，Milvus 会在专门的
highlight
字段中返回高亮文本。默认情况下，高亮输出以片段形式返回，从第一个匹配词开始。
在本例中，第一个匹配词是
"text"
，因此返回的高亮文本从该位置开始：
{
...
,
"highlight"
:
{
"text"
:
[
"{text} {filtering} works in Milvus."
]
}
}
要控制返回片段的位置、长度和数量，请参阅
以片段形式返回高亮文本
。
基于片段的高亮输出
默认情况下，Milvus 以片段形式返回高亮文本，从第一个匹配词开始。片段相关设置允许你进一步控制片段的返回方式，而不改变高亮显示的术语。
假设以下内容存储在一个文本字段中：
Milvus supports full text search. Use BM25 for keyword relevance. Filters can narrow results.
高亮显示配置
要控制高亮显示片段的形状，请在
LexicalHighlighter
中配置片段相关选项：
from
pymilvus
import
LexicalHighlighter

highlighter = LexicalHighlighter(
    pre_tags=[
"{"
],
    post_tags=[
"}"
],
    highlight_search_text=
True
,
    fragment_offset=
5
,
# Number of characters to reserve before the first matched term
fragment_size=
60
,
# Max. length of each fragment to return
num_of_fragments=
1
# Max. number of fragments to return
)
在此配置中
fragment_offset
在第一个高亮显示术语之前保留前导上下文。
fragment_size
限制每个片段包含多少文本。
num_of_fragments
控制返回片段的数量。
创建高亮对象后，将高亮配置应用于搜索请求：
results = client.search(
    ...,
    data=[
"BM25"
],
highlighter=highlighter
# Pass highlighter config here
)
高亮输出
启用基于片段的高亮后，Milvus 会在
highlight
字段中以片段形式返回高亮文本：
{
...
,
"highlight"
:
{
"text"
:
[
"Use {BM25} for keyword relevance. Filters can narrow results."
]
}
}
在此输出中：
片段并不完全从
{BM25}
开始，因为
fragment_offset
已设置。
只返回一个片段，因为
num_of_fragments
为 1。
片段长度以
fragment_size
为上限。
示例
准备工作
使用荧光笔之前，请确保正确配置了您的 Collections。
下面的示例创建了一个支持 BM25 全文搜索和
TEXT_MATCH
查询的 Collections，然后插入了示例文档。
准备您的 Collections
from
pymilvus
import
(
    MilvusClient,
    DataType,
    Function,
    FunctionType,
    LexicalHighlighter,
)

client = MilvusClient(uri=
"http://localhost:19530"
)
COLLECTION_NAME =
"highlighter_demo"
# Clean up existing collection
if
client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)
# Define schema
schema = client.create_schema(enable_dynamic_field=
False
)
schema.add_field(field_name=
"id"
, datatype=DataType.INT64, is_primary=
True
, auto_id=
True
)
schema.add_field(
    field_name=
"text"
,
    datatype=DataType.VARCHAR,
    max_length=
2000
,
    enable_analyzer=
True
,
# Required for BM25
enable_match=
True
,
# Required for TEXT_MATCH
)
schema.add_field(field_name=
"sparse_vector"
, datatype=DataType.SPARSE_FLOAT_VECTOR)
# Add BM25 function
schema.add_function(Function(
    name=
"text_bm25"
,
    function_type=FunctionType.BM25,
    input_field_names=[
"text"
],
    output_field_names=[
"sparse_vector"
],
))
# Create index
index_params = client.prepare_index_params()
index_params.add_index(
    field_name=
"sparse_vector"
,
    index_type=
"SPARSE_INVERTED_INDEX"
,
    metric_type=
"BM25"
,
    params={
"inverted_index_algo"
:
"DAAT_MAXSCORE"
,
"bm25_k1"
:
1.2
,
"bm25_b"
:
0.75
},
)

client.create_collection(collection_name=COLLECTION_NAME, schema=schema, index_params=index_params)
# Insert sample documents
docs = [
"my first test doc"
,
"my second test doc"
,
"my first test doc. Milvus is an open-source vector database built for GenAI applications."
,
"my second test doc. Milvus is an open-source vector database that suits AI applications "
"of every size from running a demo chatbot to building web-scale search."
,
]
client.insert(collection_name=COLLECTION_NAME, data=[{
"text"
: t}
for
t
in
docs])
print
(
f"✓ Collection created with
{
len
(docs)}
documents\n"
)
# Helper for search params
SEARCH_PARAMS = {
"metric_type"
:
"BM25"
,
"params"
: {
"drop_ratio_search"
:
0.0
}}
# Expected output:
# ✓ Collection created with 4 documents
示例 1：在 BM25 全文搜索中突出显示搜索词
本例演示如何在 BM25 全文搜索中突出显示搜索条件。
BM25 全文搜索使用
"test"
作为搜索词
高亮显示器用
{
和
}
标记包裹所有出现的 "test"。
highlighter = LexicalHighlighter(
pre_tags=[
"{"
],
post_tags=[
"}"
],
highlight_search_text=
True
,
# Highlight BM25 query terms
)
results = client.search(
    collection_name=COLLECTION_NAME,
    data=[
"test"
],
    anns_field=
"sparse_vector"
,
    limit=
10
,
    search_params=SEARCH_PARAMS,
    output_fields=[
"text"
],
highlighter=highlighter,
)
for
hit
in
results[
0
]:
print
(
f"
{hit.get(
'highlight'
, {}
).get('text', [])}"
)
print
()
预期输出
['{test} doc']
['{test} doc']
['{test} doc. Milvus is an open-source vector database built for GenAI applications.']
['{test} doc. Milvus is an open-source vector database that suits AI applications of every size from run']
示例 2：在筛选中高亮显示查询词
本例展示了如何高亮显示
TEXT_MATCH
过滤器匹配的术语。
BM25 全文搜索使用
"test"
作为查询词
queries
参数将
"my doc"
添加到高亮列表中
高亮显示器将所有匹配词（
"my"
,
"test"
,
"doc"
）与
{
和 包在一起。
}
highlighter = LexicalHighlighter(
pre_tags=[
"{"
],
post_tags=[
"}"
],
highlight_search_text=
True
,
# Also highlight BM25 term
highlight_query=[
# Additional TEXT_MATCH terms to highlight
{
"type"
:
"TextMatch"
,
"field"
:
"text"
,
"text"
:
"my doc"
},
],
)
results = client.search(
    collection_name=COLLECTION_NAME,
    data=[
"test"
],
    anns_field=
"sparse_vector"
,
    limit=
10
,
    search_params=SEARCH_PARAMS,
    output_fields=[
"text"
],
highlighter=highlighter,
)
for
hit
in
results[
0
]:
print
(
f"
{hit.get(
'highlight'
, {}
).get('text', [])}"
)
print
()
预期输出
['{my} first {test} {doc}']
['{my} second {test} {doc}']
['{my} first {test} {doc}. Milvus is an open-source vector database built for GenAI applications.']
['{my} second {test} {doc}. Milvus is an open-source vector database that suits AI applications of every siz']
例 3：以片段形式返回高亮显示
在此示例中，查询搜索
"Milvus"
并按以下设置返回高亮片段：
fragment_offset
保留第一个高亮跨度前最多 20 个字符作为前导上下文（默认为 0）。
fragment_size
将每个片段限制为大约 60 个字符（默认值为 100）。
num_of_fragments
限制每个文本值返回的片段数量（默认为 5）。
highlighter = LexicalHighlighter(
pre_tags=[
"{"
],
post_tags=[
"}"
],
highlight_search_text=
True
,
fragment_offset=
20
,
# Keep 20 chars before match
fragment_size=
60
,
# Max ~60 chars per fragment
)
results = client.search(
    collection_name=COLLECTION_NAME,
    data=[
"Milvus"
],
    anns_field=
"sparse_vector"
,
    limit=
10
,
    search_params=SEARCH_PARAMS,
    output_fields=[
"text"
],
highlighter=highlighter,
)
for
i, hit
in
enumerate
(results[
0
]):
    frags = hit.get(
'highlight'
, {}).get(
'text'
, [])
print
(
f"  Doc
{i+
1
}
:
{frags}
"
)
print
()
预期输出
Doc 1: ['my first test doc. {Milvus} is an open-source vector database ']
Doc 2: ['my second test doc. {Milvus} is an open-source vector database']
例 4：多查询高亮显示
在 BM25 全文搜索中使用多个查询进行搜索时，每个查询的结果都会单独高亮显示。第一个查询结果包含其搜索词的高亮显示，第二个查询结果包含其搜索词的高亮显示，以此类推。每个查询都使用相同的
highlighter
配置，但各自独立应用。
在下面的示例中
第一个查询在其结果集中高亮显示
"test"
第二个查询在其结果集中高亮显示
"Milvus"
highlighter = LexicalHighlighter(
pre_tags=[
"{"
],
post_tags=[
"}"
],
highlight_search_text=
True
,
)
results = client.search(
    collection_name=COLLECTION_NAME,
    data=[
"test"
,
"Milvus"
],
# Two queries
anns_field=
"sparse_vector"
,
    limit=
2
,
    search_params=SEARCH_PARAMS,
    output_fields=[
"text"
],
highlighter=highlighter,
)
for
nq_idx, hits
in
enumerate
(results):
    query_term = [
"test"
,
"Milvus"
][nq_idx]
print
(
f"  Query '
{query_term}
':"
)
for
hit
in
hits:
print
(
f"
{hit.get(
'highlight'
, {}
).get('text', [])}"
)
print
()
预期输出
Query 'test':
  ['{test} doc']
  ['{test} doc']
Query 'Milvus':
  ['{Milvus} is an open-source vector database built for GenAI applications.']
  ['{Milvus} is an open-source vector database that suits AI applications of every size from running a dem']
例 5：自定义 HTML 标记
您可以使用任何标记进行高亮显示，例如用于网络用户界面的 HTML 安全标记。这在浏览器中呈现搜索结果时非常有用。
highlighter = LexicalHighlighter(
pre_tags=[
"<mark>"
],
post_tags=[
"</mark>"
],
highlight_search_text=
True
,
)
results = client.search(
    collection_name=COLLECTION_NAME,
    data=[
"test"
],
    anns_field=
"sparse_vector"
,
    limit=
2
,
    search_params=SEARCH_PARAMS,
    output_fields=[
"text"
],
highlighter=highlighter,
)
for
hit
in
results[
0
]:
print
(
f"
{hit.get(
'highlight'
, {}
).get('text', [])}"
)
print
()
预期输出
['<mark>test</mark> doc']
['<mark>test</mark> doc']