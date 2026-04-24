范围搜索
范围搜索可将返回实体的距离或得分限制在特定范围内，从而提高搜索结果的相关性。本页将帮助您了解什么是范围搜索以及进行范围搜索的步骤。
概述
执行范围搜索请求时，Milvus 以 ANN 搜索结果中与查询向量最相似的向量为圆心，以搜索请求中指定的
半径
为外圈半径，以
range_filter
为内圈半径，画出两个同心圆。所有相似度得分在这两个同心圆形成的环形区域内的向量都将被返回。这里，
range_filter
可以设置为
0
，表示将返回指定相似度得分（半径）范围内的所有实体。
范围搜索
上图显示，范围搜索请求包含两个参数：
半径
和
range_filter
。收到范围搜索请求后，Milvus 会执行以下操作：
使用指定的度量类型
（COSINE
）查找与查询向量最相似的所有向量嵌入。
过滤与查询向量的
距离
或
得分
在
半径
和
range_filter
参数指定范围内的向量嵌入。
从筛选出的实体中返回
前 K
个实体。
设置
radius
和
range_filter
的方法因搜索的度量类型而异。下表列出了在不同度量类型下设置这两个参数的要求。
度量类型
名称
设置半径和范围筛选器的要求
L2
L2 距离越小，表示相似度越高。
要忽略最相似的向量 Embeddings，请确保
range_filter
<= 距离 <
radius
IP
IP 距离越大，表示相似度越高。
要忽略最相似的向量嵌入，请确保
radius
< 距离 <=
range_filter
COSINE
COSINE 距离越大，表示相似度越高。
要忽略最相似的向量嵌入，请确保
radius
< 距离 <=
range_filter
JACCARD
Jaccard 距离越小，表示相似度越高。
要忽略最相似的向量嵌入，请确保
range_filter
<= 距离 <
radius
HAMMING
汉明距离越小，表示相似度越高。
要忽略最相似的向量嵌入，请确保
range_filter
<= 距离 <
radius
示例
本节演示如何进行范围搜索。以下代码片段中的搜索请求不带度量类型，表示默认度量类型为
COSINE
。在这种情况下，请确保
半径
值小于
range_filter
值。
在以下代码片段中，将
radius
设为
0.4
，将
range_filter
设为
0.6
，这样 Milvus 就会返回与查询向量的距离或分数在
0.4
至
0.6
范围内的所有实体。
Python
Java
Go
NodeJS
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

query_vector = [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]

res = client.search(
    collection_name=
"my_collection"
,
    data=[query_vector],
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
for
hits
in
res:
print
(
"TopK results:"
)
for
hit
in
hits:
print
(hit)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
 io.milvus.v2.service.vector.request.SearchReq
import
io.milvus.v2.service.vector.request.data.FloatVec;
import
io.milvus.v2.service.vector.response.SearchResp
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
Map<String,Object> extraParams =
new
HashMap
<>();
extraParams.put(
"radius"
,
0.4
);
extraParams.put(
"range_filter"
,
0.6
);
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(queryVector))
        .topK(
5
)
        .searchParams(extraParams)
        .build();
SearchResp
searchResp
=
client.search(searchReq);

List<List<SearchResp.SearchResult>> searchResults = searchResp.getSearchResults();
for
(List<SearchResp.SearchResult> results : searchResults) {
    System.out.println(
"TopK results:"
);
for
(SearchResp.SearchResult result : results) {
        System.out.println(result);
    }
}
// Output
// TopK results:
// SearchResp.SearchResult(entity={}, score=0.5975797, id=4)
// SearchResp.SearchResult(entity={}, score=0.46704385, id=5)
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/index"
"github.com/milvus-io/milvus/client/v2/entity"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

milvusAddr :=
"localhost:19530"
client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address: milvusAddr,
})
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
defer
client.Close(ctx)

queryVector := []
float32
{
0.3580376395471989
,
-0.6023495712049978
,
0.18414012509913835
,
-0.26286205330961354
,
0.9029438446296592
}

annParam := index.NewCustomAnnParam()
annParam.WithRadius(
0.4
)
annParam.WithRangeFilter(
0.6
)
resultSets, err := client.Search(ctx, milvusclient.NewSearchOption(
"my_collection"
,
// collectionName
5
,
// limit
[]entity.Vector{entity.FloatVector(queryVector)},
).WithConsistencyLevel(entity.ClStrong).
    WithANNSField(
"vector"
).
    WithAnnParam(annParam))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
for
_, resultSet :=
range
resultSets {
    fmt.Println(
"IDs: "
, resultSet.IDs.FieldData().GetScalars())
    fmt.Println(
"Scores: "
, resultSet.Scores)
}
import
{
MilvusClient
,
DataType
}
from
"@zilliz/milvus2-sdk-node"
;
const
address =
"http://localhost:19530"
;
const
token =
"root:Milvus"
;
const
client =
new
MilvusClient
({address, token});
var
query_vector = [
0.3580376395471989
, -
0.6023495712049978
,
0.18414012509913835
, -
0.26286205330961354
,
0.9029438446296592
]

res =
await
client.
search
({
collection_name
:
"my_collection"
,
data
: [query_vector],
limit
:
5
,
params
: {
"radius"
:
0.4
,
"range_filter"
:
0.6
}
})
export
CLUSTER_ENDPOINT=
"http://localhost:19530"
export
TOKEN=
"root:Milvus"
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/entities/search"
\
--header
"Authorization: Bearer
${TOKEN}
"
\
--header
"Content-Type: application/json"
\
-d
'{
    "collectionName": "my_collection",
    "data": [
        [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]
    ],
    "annsField": "vector",
    "limit": 5,
    "searchParams": {
        "params": {
            "radius": 0.4,
            "range_filter": 0.6
        }
    }
}'
# {"code":0,"cost":0,"data":[]}
如果查询向量已经存在于目标 Collections 中，请考虑使用
ids
代替在搜索前检索它们。有关详情，请参阅
主键搜索
。