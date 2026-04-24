Elasticsearch 查询到 Milvus
基于 Apache Lucene 构建的 Elasticsearch 是领先的开源搜索引擎。然而，它在现代人工智能应用中面临着各种挑战，包括更新成本高、实时性差、碎片管理效率低、非云原生设计以及资源需求过高。作为云原生向量数据库，Milvus 通过解耦存储和计算、高效的高维数据索引以及与现代基础设施的无缝集成，克服了这些问题。它为人工智能工作负载提供了卓越的性能和可扩展性。
本文旨在帮助您将代码库从 Elasticsearch 迁移到 Milvus，并提供中间转换查询的各种示例。
概述
在 Elasticsearch 中，查询上下文中的操作会生成相关性分数，而过滤器上下文中的操作不会生成相关性分数。同样，Milvus 的搜索会产生相似性得分，而类似过滤器的查询则不会。将代码库从 Elasticsearch 迁移到 Milvus 时，关键原则是将 Elasticsearch 查询上下文中使用的字段转换为向量字段，以便生成相似性得分。
下表列出了一些 Elasticsearch 查询模式及其在 Milvus 中的对应模式。
Elasticsearch 查询
Milvus 对应模式
备注
全文查询
匹配查询
全文搜索
两者提供类似的功能。
术语级查询
ID
in
操作符
在过滤器上下文中使用这些 Elasticsearch 查询时，两者都能提供相同或类似的功能。
前缀查询
like
操作符
范围查询
比较操作符，如
>
,
<
,
>=
, 和
<=
术语查询
比较操作符，如
==
术语查询
in
操作符
通配符查询
like
操作符
布尔查询
逻辑操作符，如
AND
在过滤器上下文中使用时，这两种操作符都能提供类似的功能。
向量查询
kNN 查询
搜索
Milvus 提供更高级的向量搜索功能。
互易等级融合
混合搜索
Milvus 支持多种 Rerankers 策略。
全文本查询
在 Elasticsearch 中，全文查询使您能够搜索分析过的文本字段，如电子邮件正文。查询字符串将使用索引过程中应用于字段的相同分析器进行处理。
匹配查询
在 Elasticsearch 中，匹配查询会返回与所提供的文本、数字、日期或布尔值相匹配的文档。在匹配之前会对所提供的文本进行分析。
下面是一个使用匹配查询的 Elasticsearch 搜索请求示例。
resp = client.search(
    query={
"match"
: {
"message"
: {
"query"
:
"this is a test"
}
        }
    },
)
Milvus 通过全文搜索功能提供了相同的功能。你可以按如下方式将上述 Elasticsearch 查询转换为 Milvus 查询：
res = client.search(
    collection_name=
"my_collection"
,
    data=[
'How is the weather in Jamaica?'
],
    anns_field=
"message_sparse"
,
    output_fields=[
"id"
,
"message"
]
)
在上面的示例中，
message_sparse
是一个稀疏向量字段，由名为
message
的 VarChar 字段衍生而来。Milvus 使用 BM25 嵌入模型将
message
字段中的值转换为稀疏向量嵌入，并将其存储在
message_sparse
字段中。收到搜索请求后，Milvus 会使用相同的 BM25 模型嵌入纯文本查询有效载荷，并执行稀疏向量搜索，然后返回
output_fields
参数中指定的
id
和
message
字段以及相应的相似性分数。
要使用此功能，必须在
message
字段上启用分析器，并定义一个函数从中导出
message_sparse
字段。有关启用分析器和在 Milvus 中创建派生函数的详细说明，请参阅
全文搜索
。
术语级查询
在 Elasticsearch 中，术语级查询用于根据结构化数据中的精确值查找文档，如日期范围、IP 地址、价格或产品 ID。本节概述了一些 Elasticsearch 术语级查询在 Milvus 中的可能等价形式。为了与 Milvus 的功能保持一致，本节中的所有示例都在过滤器上下文中进行了操作符调整。
ID
在 Elasticsearch 中，你可以在过滤器上下文中根据 ID 查找文件，如下所示：
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"ids"
: {
"values"
: [
"1"
,
"4"
,
"100"
]
                }            
            }
        }
    },
)
在 Milvus 中，你也可以根据 ID 查找实体，如下所示：
# Use the filter parameter
res = client.query(
    collection_name=
"my_collection"
,
filter
=
"id in [1, 4, 100]"
,
    output_fields=[
"id"
,
"title"
]
)
# Use the ids parameter
res = client.query(
    collection_name=
"my_collection"
,
    ids=[
1
,
4
,
100
],
    output_fields=[
"id"
,
"title"
]
)
你可以在
本页
找到 Elasticsearch 示例。有关查询和获取请求以及 Milvus 中过滤器表达式的详细信息，请参阅
查询
和
过滤
。
前缀查询
在 Elasticsearch 中，你可以在过滤器上下文中查找在所提供字段中包含特定前缀的文档，如下所示：
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"prefix"
: {
"user"
: {
"value"
:
"ki"
}
                }           
            }
        }
    },
)
在 Milvus 中，你可以按如下方式查找其值以指定前缀开头的实体：
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'user like "ki%"'
,
    output_fields=[
"id"
,
"user"
]
)
你可以在
本页
找到 Elasticsearch 示例。有关 Milvus 中
like
操作符的详细信息，请参阅
使用
LIKE
进行模式匹配
。
范围查询
在 Elasticsearch 中，您可以查找包含所提供范围内术语的文档，如下所示：
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"range"
: {
"age"
: {
"gte"
:
10
,
"lte"
:
20
}
                }           
            }
        }
    },
)
在 Milvus 中，你可以按如下方式查找特定字段中的值在所提供范围内的实体：
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'10 <= age <= 20'
,
    output_fields=[
"id"
,
"user"
,
"age"
]
)
你可以在
本页
找到 Elasticsearch 示例。有关 Milvus 中比较操作符的详细信息，请参阅
比较操作符
。
术语查询
在 Elasticsearch 中，你可以查找在所提供字段中包含
精确
术语的文档，如下所示：
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"term"
: {
"status"
: {
"value"
:
"retired"
}
                }            
            }
        }
    },
)
在 Milvus 中，您可以按如下方式查找指定字段中的值正好是指定术语的实体：
# use ==
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'status=="retired"'
,
    output_fields=[
"id"
,
"user"
,
"status"
]
)
# use TEXT_MATCH
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'TEXT_MATCH(status, "retired")'
,
    output_fields=[
"id"
,
"user"
,
"status"
]
)
你可以在
本页
找到 Elasticsearch 示例。有关 Milvus 中比较操作符的详细信息，请参阅
比较操作符
。
术语查询
在 Elasticsearch 中，你可以查找在所提供字段中包含一个或多个
精确
术语的文档，如下所示：
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"terms"
: {
"degree"
: [
"graduate"
,
"post-graduate"
]
                }        
            }
        }
    }
)
Milvus 没有与此完全等价的词。不过，您可以按如下方式查找指定字段中的值为指定术语之一的实体：
# use in
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'degree in ["graduate", "post-graduate"]'
,
    output_fields=[
"id"
,
"user"
,
"degree"
]
)
# use TEXT_MATCH
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'TEXT_MATCH(degree, "graduate post-graduate")'
,
    output_fields=[
"id"
,
"user"
,
"degree"
]
)
您可以在
本页
找到 Elasticsearch 示例。有关 Milvus 中范围操作符的详细信息，请参阅
范围操作符
。
通配符查询
在 Elasticsearch 中，你可以查找包含与通配符模式匹配的术语的文档，如下所示：
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"wildcard"
: {
"user"
: {
"value"
:
"ki*y"
}
                }          
            }
        }
    },
)
Milvus 在过滤条件中不支持通配符。不过，你可以使用
like
操作符来实现类似的效果，如下所示：
res = client.query(
    collection_name=
"my_collection"
,
filter
=
'user like "ki%" AND user like "%y"'
,
    output_fields=[
"id"
,
"user"
]
)
您可以在
本页
找到 Elasticsearch 示例。有关 Milvus 中范围操作符的详细信息，请参阅
范围操作符
。
布尔查询
在 Elasticsearch 中，布尔查询是指匹配与其他查询的布尔组合相匹配的文档的查询。
下面的示例改编自
本页
Elasticsearch 文档中的一个示例。该查询将返回名称中包含
kimchy
的用户，并带有
production
标记。
resp = client.search(
    query={
"bool"
: {
"filter"
: {
"term"
: {
"user"
:
"kimchy"
}
            },
"filter"
: {
"term"
: {
"tags"
:
"production"
}
            }
        }
    },
)
在 Milvus 中，你可以做类似的事情，如下所示：
filter
= 

res = client.query(
    collection_name=
"my_collection"
,
filter
=
'user like "%kimchy%" AND ARRAY_CONTAINS(tags, "production")'
,
    output_fields=[
"id"
,
"user"
,
"age"
,
"tags"
]
)
上面的示例假定在目标 Collections 中有一个
VarChar
类型的
user
字段和一个
Array
类型的
tags
字段。查询将返回名称中包含
kimchy
的用户，并带有
production
标记。
向量查询
在 Elasticsearch 中，向量查询是对向量字段进行处理以有效执行语义搜索的专门查询。
Knn 查询
Elasticsearch 支持近似 kNN 查询和精确、强制 kNN 查询。你可以用这两种方式找到与查询向量最近的
k 个
向量，以相似度指标来衡量，具体如下：
resp = client.search(
    index=
"my-image-index"
,
    size=
3
,
    query={
"knn"
: {
"field"
:
"image-vector"
,
"query_vector"
: [
                -
5
,
9
,
                -
12
],
"k"
:
10
}
    },
)
作为专门的向量数据库，Milvus 使用索引类型来优化向量搜索。通常，它优先考虑对高维向量数据进行近似近邻（ANN）搜索。虽然使用 FLAT 索引类型的暴力 kNN 搜索能得到精确的结果，但它既耗时又耗资源。相比之下，使用 AUTOINDEX 或其他索引类型的 ANN 搜索能在速度和精确度之间取得平衡，其性能明显比 kNN 更快、更节省资源。
在 Mlivus 中，与上述向量查询类似的等价关系是这样的：
res = client.search(
    collection_name=
"my_collection"
,
    anns_field=
"image-vector"
data=[[-
5
,
9
, -
12
]],
    limit=
10
)
您可以在
本页
找到 Elasticsearch 示例。有关 Milvus 中 ANN 搜索的详细信息，请阅读
基本 ANN 搜索
。
互惠排名融合
Elasticsearch 提供互惠排名融合 (RRF)，可将具有不同相关性指标的多个结果集合并为一个排名结果集。
下面的示例演示了如何将传统的基于术语的搜索与 k-nearest neighbors (kNN) 向量搜索相结合，以提高搜索相关性：
client.search(
    index=
"my_index"
,
    size=
10
,
    query={
"retriever"
: {
"rrf"
: {
"retrievers"
: [
                    {
"standard"
: {
"query"
: {
"term"
: {
"text"
:
"shoes"
}
                            }
                        }
                    },
                    {
"knn"
: {
"field"
:
"vector"
,
"query_vector"
: [
1.25
,
2
,
3.5
],
# Example vector; replace with your actual query vector
"k"
:
50
,
"num_candidates"
:
100
}
                    }
                ],
"rank_window_size"
:
50
,
"rank_constant"
:
20
}
        }
    }
)
在这个例子中，RRF 将两个检索器的结果结合在一起：
对
text
字段中包含术语
"shoes"
的文档进行标准的基于术语的搜索。
使用提供的查询向量对
vector
字段进行 kNN 检索。
每个检索器最多可贡献 50 个最匹配结果，RRF 会对这些结果进行重新排序，并返回最终的前 10 个结果。
在 Milvus 中，您可以通过组合多个向量字段的搜索、应用重新排序策略并从组合列表中检索前 K 结果来实现类似的混合搜索。Milvus 支持 RRF 和加权重排序策略。更多详情，请参阅
Rerankers
。
下面是上述 Elasticsearch 示例在 Milvus 中的非严格等价。
search_params_dense = {
"data"
: [[
1.25
,
2
,
3.5
]],
"anns_field"
:
"vector"
,
"param"
: {
"metric_type"
:
"IP"
,
"params"
: {
"nprobe"
:
10
},
    },
"limit"
:
100
}

req_dense = ANNSearchRequest(**search_params_dense)

search_params_sparse = {
"data"
: [
"shoes"
],
"anns_field"
:
"text_sparse"
,
"param"
: {
"metric_type"
:
"BM25"
,
    }
}

req_sparse = ANNSearchRequest(**search_params_sparse)

res = client.hybrid_search(
    collection_name=
"my_collection"
,
    reqs=[req_dense, req_sparse],
    reranker=RRFRanker(),
    limit=
10
)
该示例演示了 Milvus 中的混合搜索，它结合了以下内容：
密集向量搜索
：使用内积（IP）度量，将
nprobe
设置为 10，在
vector
字段上进行近似近邻（ANN）搜索。
稀疏向量搜索
：在
text_sparse
字段上使用 BM25 相似度指标。
这些搜索的结果分别执行、合并，并使用 Riprocal Rank Fusion (RRF) 排序器重新排序。混合搜索会从重新排序的列表中返回前 10 个实体。
与 Elasticsearch 的 RRF 排序器（它将标准文本查询和 kNN 搜索的结果合并在一起）不同，Milvus 将稀疏向量搜索和密集向量搜索的结果合并在一起，提供了一种针对多模态数据优化的独特混合搜索能力。
回顾
在本文中，我们介绍了将典型 Elasticsearch 查询转换为 Milvus 对应查询的方法，包括术语级查询、布尔查询、全文查询和向量查询。如果您对其他 Elasticsearch 查询的转换有进一步的问题，请随时联系我们。