主键搜索
Compatible with Milvus 2.6.9+
在进行相似性搜索时，总是会要求您提供一个或多个查询向量，即使目标 Collections 中已经存在查询向量。为了避免在搜索前检索向量，可以使用主键来代替。
概述
在电子商务平台上，用户可以输入关键字来检索与之匹配的产品。用户查看产品详情页后，平台还会在页面底部显示类似产品列表，供用户比较。
这些推荐会根据与关键词或当前产品的相似度进行排序。为了实现这一目标，平台开发人员需要在实际的相似性搜索之前从 Milvus 获取关键字或当前产品的向量表示，这就增加了平台与 Milvus 之间的往返次数，导致大量高维浮点在网络上传输。
为了简化应用程序与 Milvus 之间的交互逻辑，减少往返次数，避免在网络上传输大量高维浮点数值，可以考虑使用主键搜索。
在主键搜索中，你不需要提供任何查询向量。相反，您需要提供包含查询向量的实体的主键 (
ids
)。
限制和约束
使用主键搜索适用于所有向量数据类型，但从 VarChar 字段派生的稀疏向量字段（如 BM25 函数）除外。
在筛选、范围和分组搜索中，可以使用主键代替查询向量，也可以选择启用分页。不过，该功能不适用于混合搜索和搜索迭代器。
对于涉及嵌入列表的相似性搜索，仍需要检索查询向量，将其排列到嵌入列表中，然后运行搜索。
在 RESTful API 中不能使用主键代替查询向量。
对于不存在的主键或格式不正确的主键，Milvus 会提示错误。
主键和查询向量是相互排斥的。同时提供两者也会导致错误。
示例
以下示例假定目标 Collections 中包含所有提供的 Int64 ID。
主键不用于筛选，仅用于向量检索。
示例 1：基本主键搜索
要进行基本的主键搜索，只需用主键替换查询向量即可。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

res = client.search(
    collection_name=
"quick_setup"
,
    anns_field=
"vector"
,
ids=[
551
,
296
,
43
],
# a list of primary keys
limit=
3
,
    search_params={
"metric_type"
:
"IP"
}
)
for
hits
in
res:
for
hit
in
hits:
print
(hit)
// java
// node.js
// go
# restful
例 2：使用主键进行过滤搜索
下面的示例假设 color 和 likes 是目标 Collection 中 Schema 定义的两个字段。
Python
Java
NodeJS
Go
cURL
res = client.search(
    collection_name=
"my_collection"
,
ids=[
551
,
296
,
43
],
#
filter
=
'color like "red%" and likes > 50'
,
output_fields=[
"color"
,
"likes"
],
limit=
3
,
)
// java
// node.js
// go
# restful
示例 3：使用主键进行范围搜索
Python
Java
NodeJS
Go
cURL
res = client.search(
    collection_name=
"my_collection"
,
ids=[
551
,
296
,
43
],
limit=
3
,
    search_params={
"params"
: {
"radius"
:
0.4
,
"range_filter"
:
0.6
}
}
)
// java
// node.js
// go
# restful
例 4：使用主键进行分组搜索
下面的示例假定
docId
是目标 Collections 中 Schema 定义的字段。
Python
Java
NodeJS
Go
cURL
res = client.search(
    collection_name=
"my_collection"
,
ids=[
551
,
296
,
43
],
limit=
3
,
    group_by_field=
"docId"
,
    output_fields=[
"docId"
]
)
// java
// node.js
// go
# restful