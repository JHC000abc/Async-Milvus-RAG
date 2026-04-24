搜索迭代器
ANN Search 对单次查询可调用的实体数量有最大限制，因此仅使用基本 ANN Search 可能无法满足大规模检索的需求。对于 topK 超过 16,384 的 ANN Search 请求，建议考虑使用 SearchIterator。本节将介绍如何使用 SearchIterator 以及相关注意事项。
概述
Search 请求返回搜索结果，而 SearchIterator 返回迭代器。您可以调用该迭代器的
next()
方法来获取搜索结果。
具体来说，您可以如下使用 SearchIterator：
创建一个 SearchIterator，并设置
每次搜索请求返回的实体数
和
返回的实体总数
。
在循环中调用 SearchIterator 的
next()
方法，以分页方式获取搜索结果。
如果
next()
方法返回的结果为空，则调用迭代器的
close()
方法结束循环。
创建搜索迭代器
以下代码片段演示了如何创建一个 SearchIterator。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
connections, Collection

connections.connect(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)
# create iterator
query_vectors = [
    [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]]

collection = Collection(
"iterator_collection"
)

iterator = collection.search_iterator(
    data=query_vectors,
    anns_field=
"vector"
,
    param={
"metric_type"
:
"L2"
,
"params"
: {
"nprobe"
:
16
}},
batch_size=
50
,
output_fields=[
"color"
],
limit=
20000
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.orm.iterator.SearchIterator;
import
io.milvus.v2.common.IndexParam.MetricType;
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
java.util.*;
MilvusClientV2
client
=
new
MilvusClientV2
(ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build());
FloatVec
queryVector
=
new
FloatVec
(
new
float
[]{
0.3580376395471989f
, -
0.6023495712049978f
,
0.18414012509913835f
, -
0.26286205330961354f
,
0.9029438446296592f
});
SearchIterator
searchIterator
=
client.searchIterator(SearchIteratorReq.builder()
        .collectionName(
"iterator_collection"
)
        .vectors(Collections.singletonList(queryVector))
        .vectorFieldName(
"vector"
)
        .batchSize(
500L
)
        .outputFields(Lists.newArrayList(
"color"
))
        .topK(
20000
)
        .metricType(IndexParam.MetricType.COSINE)
        .build());
// go
import
{
MilvusClient
}
from
'@zilliz/milvus2-sdk-node'
;
const
milvusClient =
new
MilvusClient
({
address
:
'http://localhost:19530'
,
token
:
'root:Milvus'
,
});
const
queryVectors = [
[
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
],
];
const
collectionName =
'iterator_collection'
;
const
iterator = milvusClient.
searchIterator
({
collection_name
: collectionName,
vectors
: queryVectors,
anns_field
:
'vector'
,
params
: {
metric_type
:
'L2'
,
params
: {
nprobe
:
16
} },
batch_size
:
50
,
output_fields
: [
'color'
],
limit
:
20000
,
});
# restful
在上述示例中，您将每次搜索返回的实体数
（batch_
size
/batchSize
）设置为 50，将返回的实体总数
（topK
）设置为 20,000。
使用 SearchIterator
SearchIterator 就绪后，您可以调用它的 next() 方法，以分页方式获取搜索结果。
Python
Java
Go
NodeJS
cURL
results = []
while
True
:
result = iterator.
next
()
if
not
result:
iterator.close()
break
for
hit
in
result:
        results.append(hit.to_dict())
import
io.milvus.response.QueryResultsWrapper;
while
(
true
) {
    List<QueryResultsWrapper.RowRecord> res = searchIterator.next();
if
(res.isEmpty()) {
        searchIterator.close();
break
;
    }
for
(QueryResultsWrapper.RowRecord record : res) {
        System.out.println(record);
    }
}
// go
for
await
(
const
result
of
iterator) {
console
.
log
(result);
}
# restful
在上述代码示例中，您创建了一个无限循环，并在循环中调用
next()
方法将搜索结果存储到一个变量中，然后在
next()
没有返回任何结果时关闭迭代器。