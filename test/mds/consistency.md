一致性级别
作为一个分布式向量数据库，Milvus 提供了多种一致性级别，以确保每个节点或副本在读写操作期间都能访问相同的数据。目前，支持的一致性级别包括
强
、
有界
、
最终
和
会话
，其中
有界
是默认使用的一致性级别。
概述
Milvus 是一个存储和计算分离的系统。在这个系统中，
数据节点
负责数据的持久性，并最终将其存储在 MinIO/S3 等分布式对象存储中。
查询节点
负责处理搜索等计算任务。这些任务涉及
批量数据
和
流数据的
处理。简单地说，批量数据可以理解为已经存储在对象存储中的数据，而流式数据指的是尚未存储在对象存储中的数据。由于网络延迟，查询节点通常无法保存最新的流数据。如果没有额外的保障措施，直接在流数据上执行搜索可能会导致丢失许多未提交的数据点，从而影响搜索结果的准确性。
批数据和流数据
如上图所示，在收到搜索请求后，查询节点可以同时接收流数据和批量数据。但是，由于网络延迟，查询节点获得的流数据可能不完整。
为了解决这个问题，Milvus 对数据队列中的每条记录都打上时间戳，并不断向数据队列中插入同步时间戳。每当收到同步时间戳（syncTs），QueryNodes 就会将其设置为服务时间，这意味着 QueryNodes 可以查看该服务时间之前的所有数据。基于 ServiceTime，Milvus 可以提供保证时间戳（GuaranteeTs），以满足用户对一致性和可用性的不同要求。用户可以通过在搜索请求中指定 GuaranteeTs，告知查询节点需要在搜索范围中包含指定时间点之前的数据。
服务时间和保证时间
如上图所示，如果 GuaranteeTs 小于 ServiceTime，则表示指定时间点之前的所有数据已全部写入磁盘，允许查询节点立即执行搜索操作。当 GuaranteeTs 大于 ServiceTime 时，查询节点必须等到 ServiceTime 超过 GuaranteeTs 后才能执行搜索操作。
用户需要在查询准确性和查询延迟之间做出权衡。如果用户对一致性要求较高，对查询延迟不敏感，可以将 GuaranteeTs 设置为尽可能大的值；如果用户希望快速获得搜索结果，对查询准确性的容忍度较高，则可以将 GuaranteeTs 设置为较小的值。
一致性级别图解
Milvus 提供四种不同 GuaranteeTs 的一致性级别。
强
使用最新的时间戳作为 GuaranteeTs，查询节点必须等到服务时间满足 GuaranteeTs 后才能执行搜索请求。
最终
GuaranteeTs 设置为极小值（如 1），以避免一致性检查，这样查询节点就可以立即对所有批次数据执行搜索请求。
有限制
（默认）
GuranteeTs 设置为比最新时间戳更早的时间点，以使查询节点在执行搜索时能够容忍一定的数据丢失。
会话
客户端插入数据的最新时间点被用作 GuaranteeTs，以便查询节点能对客户端插入的所有数据执行搜索。
Milvus 使用 "有界滞后 "作为默认的一致性级别。如果未指定保证时间，则使用最新的服务时间作为保证时间。
设置一致性级别
创建 Collections 以及执行搜索和查询时，可以设置不同的一致性级别。
创建 Collections 时设置一致性级别
创建 Collections 时，可以为集合内的搜索和查询设置一致性级别。以下代码示例将一致性级别设置为
"有界
"。
python
java
cURL
client.create_collection(
    collection_name=
"my_collection"
,
    schema=schema,
    consistency_level=
"Bounded"
,
# Defaults to Bounded if not specified
)
CreateCollectionReq
createCollectionReq
=
CreateCollectionReq.builder()
        .collectionName(
"my_collection"
)
        .collectionSchema(schema)
        .consistencyLevel(ConsistencyLevel.BOUNDED)
        .build();
client.createCollection(createCollectionReq);
export
schema=
'{
        "autoId": true,
        "enabledDynamicField": false,
        "fields": [
            {
                "fieldName": "my_id",
                "dataType": "Int64",
                "isPrimary": true
            },
            {
                "fieldName": "my_vector",
                "dataType": "FloatVector",
                "elementTypeParams": {
                    "dim": "5"
                }
            },
            {
                "fieldName": "my_varchar",
                "dataType": "VarChar",
                "isClusteringKey": true,
                "elementTypeParams": {
                    "max_length": 512
                }
            }
        ]
    }'
export
params=
'{
    "consistencyLevel": "Bounded"
}'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/collections/create"
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
"{
    \"collectionName\": \"my_collection\",
    \"schema\":
$schema
,
    \"params\":
$params
}"
consistency_level
参数的可能值是
Strong
,
Bounded
,
Eventually
, 和
Session
。
在搜索中设置一致性级别
您可以随时更改特定搜索的一致性级别。下面的代码示例将一致性级别设置为 "有界"。此更改仅适用于当前搜索请求。
python
java
cURL
res = client.search(
    collection_name=
"my_collection"
,
    data=[query_vector],
    limit=
3
,
    search_params={
"metric_type"
:
"IP"
}，
consistency_level=
"Bounded"
,
)
SearchReq
searchReq
=
SearchReq.builder()
        .collectionName(
"my_collection"
)
        .data(Collections.singletonList(queryVector))
        .topK(
3
)
        .searchParams(params)
        .consistencyLevel(ConsistencyLevel.BOUNDED)
        .build();
SearchResp
searchResp
=
client.search(searchReq);
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
    "limit": 3,
    "consistencyLevel": "Bounded"
}'
该参数也可用于混合搜索和搜索迭代器。
consistency_level
参数的可能值是
Strong
,
Bounded
,
Eventually
, 和
Session
。
在查询中设置一致性级别
您可以随时更改特定搜索的一致性级别。以下代码示例将一致性级别设置为
最终
。该设置仅适用于当前查询请求。
python
java
res = client.query(
    collection_name=
"my_collection"
,
filter
=
"color like \"red%\""
,
    output_fields=[
"vector"
,
"color"
],
    limit=
3
，
consistency_level=
"Eventually"
,
)
QueryReq
queryReq
=
QueryReq.builder()
        .collectionName(
"my_collection"
)
        .filter(
"color like \"red%\""
)
        .outputFields(Arrays.asList(
"vector"
,
"color"
))
        .limit(
3
)
        .consistencyLevel(ConsistencyLevel.EVENTUALLY)
        .build();
QueryResp
getResp
=
client.query(queryReq);
该参数在查询迭代器中也可用。
consistency_level
参数的可能值是
Strong
,
Bounded
,
Eventually
, 和
Session
。