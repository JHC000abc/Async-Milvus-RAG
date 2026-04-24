时间戳
本主题解释时间戳的概念，并介绍 Milvus 向量数据库中与时间戳相关的四个主要参数。
概述
Milvus 是一个向量数据库，可以搜索和查询从非结构化数据转换而来的向量。在进行数据操作语言（DML）操作（包括
数据插入和删除）
时，Milvus 会为参与操作的实体分配时间戳。因此，Milvus 中的所有实体都有一个时间戳属性。而同一 DML 操作符中的实体批次共享相同的时间戳值。
时间戳参数
在 Milvus 中进行向量相似性搜索或查询时，会涉及几个与时间戳相关的参数。
Guarantee_timestamp
Service_timestamp
Graceful_time
Travel_timestamp
Guarantee_timestamp
Guarantee_timestamp
是一种时间戳类型，用于确保在进行向量相似性搜索或查询时， 之前的 DML 操作更新的所有数据都是可见的。例如，如果在下午 3 点插入一批数据，下午 5 点插入另一批数据，而在向量相似性搜索过程中， 的值设置为下午 6 点。这意味着分别在下午 3 点和 5 点插入的两批数据都应参与搜索。
Guarantee_timestamp
Guarantee_timestamp
如果没有配置
Guarantee_timestamp
，Milvus 会自动取搜索请求时的时间点。因此，搜索是在搜索前通过 DML 操作更新了所有数据的数据视图上进行的。
为了省去了解 Milvus 内部
TSO
的麻烦，作为用户，不必直接配置
Guarantee_timestamp
参数。您只需选择
一致性级别
，Milvus 就会自动为您处理
Guarantee_timestamp
参数。每个一致性级别对应一定的
Guarantee_timestamp
值。
Guarantee_Timestamp
.
示例
如上图所示，
Guarantee_timestamp
的值设置为
2021-08-26T18:15:00
（为简单起见，本例中的时间戳用物理时间表示）。在进行搜索或查询时，将搜索或查询 2021-08-26T18:15:00 之前的所有数据。
Service_timestamp
Service_timestamp
是由 Milvus 中的查询节点自动生成和管理的一种时间戳类型。它用于指示哪些 DML 操作由查询节点执行。
查询节点管理的数据可分为两类：
历史数据（或称批量数据）
增量数据（或称为流数据）。
在 Milvus 中，进行搜索或查询前需要加载数据。因此，在进行搜索或查询请求之前，会通过查询节点加载 Collections 中的批量数据。然而，流数据是动态配置插入 Milvus 或从 Milvus 中删除的，这就要求查询节点保持 DML 操作和搜索或查询请求的时间轴。因此，查询节点使用
Service_timestamp
来保留这样一个时间轴。
Service_timestamp
可以看作是某些数据可见的时间点，因为查询节点可以确保
Service_timestamp
之前的所有 DML 操作都已完成。
当有搜索或查询请求传入时，查询节点会比较
Service_timestamp
和
Guarantee_timestamp
的值。主要有两种情况。
服务时间戳
。
情况 1：
Service_timestamp
>=
Guarantee_timestamp
如图 1 所示，
Guarantee_timestamp
的值设置为
2021-08-26T18:15:00
。当
Service_timestamp
的值增长为
2021-08-26T18:15:01
时，这意味着在此时间点之前的所有 DML 操作均由查询节点执行并完成，包括
Guarantee_timestamp
所指示时间之前的 DML 操作。因此，搜索或查询请求可以立即执行。
方案 2：
Service_timestamp
<
Guarantee_timestamp
如图 2 所示，
Guarantee_timestamp
的值设置为
2021-08-26T18:15:00
，而
Service_timestamp
的当前值仅为
2021-08-26T18:14:55
。这意味着只有
2021-08-26T18:14:55
之前的 DML 操作才会被执行并完成，剩下的部分在此时间点之后但在
Guarantee_timestamp
之前的 DML 操作未完成。如果在此时执行搜索或查询，所需的部分数据将不可见且不可用，严重影响搜索或查询结果的准确性。因此，查询节点需要将搜索或查询请求推迟到
guarantee_timestamp
之前的 DML 操作完成后再执行（即当
Service_timestamp
>=
Guarantee_timestamp
）。
Graceful_time
从技术上讲，
Graceful_time
并不是一个时间戳，而是一个时间段（如 100 毫秒）。不过，
Graceful_time
值得一提，因为它与
Guarantee_timestamp
和
Service_timestamp
密切相关。
Graceful_time
是 Milvus 配置文件中的一个可配置参数。它用于指示在某些数据变为可见之前可容忍的时间段。简而言之，可以容忍
Graceful_time
期间未完成的 DML 操作。
当有搜索或查询请求传入时，可能会出现两种情况。
Graceful_Time
.
情况 1：
Service_timestamp
+
Graceful_time
>=
Guarantee_timestamp
如图 1 所示，
Guarantee_timestamp
的值设置为
2021-08-26T18:15:01
，
Graceful_time
设置为
2s
。
Service_timestamp
的值增长为
2021-08-26T18:15:00
。虽然
Service_timestamp
的值仍然小于
Guarantee_timestamp
的值，而且
2021-08-26T18:15:01
之前的所有 DML 操作也没有完成，但如
Graceful_time
的值所示，可以容忍 2 秒钟的数据不可见期。因此，传入的搜索或查询请求可以立即执行。
方案 2：
Service_timestamp
+
Graceful_time
<
Guarantee_timestamp
如图 2 所示，
Guarantee_timestamp
的值设置为
2021-08-26T18:15:01
，
Graceful_time
设置为
2s
。
Service_timestamp
的当前值仅为
2021-08-26T18:14:54
。这意味着预期的 DML 操作尚未完成，即使考虑到 2 秒钟的宽限时间，数据隐形仍是无法容忍的。因此，查询节点需要推迟搜索或查询请求，直到某些 DML 请求完成（即
Service_timestamp
+
Graceful_time
>=
Guarantee_timestamp
）。
下一步
了解
保证时间戳
如何
在 Milvus 中实现可调整的一致性