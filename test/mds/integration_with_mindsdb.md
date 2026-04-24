将 Milvus 与 MindsDB 相集成
MindsDB
是一款功能强大的工具，用于将人工智能应用程序与各种企业数据源集成。它作为一个联合查询引擎，在细致回答结构化和非结构化数据查询的同时，还能为无序的数据带来秩序。无论您的数据是分散在 SaaS 应用程序、数据库还是数据仓库中，MindsDB 都能使用标准 SQL 对其进行连接和查询。它通过知识库提供最先进的自主RAG系统，支持数百种数据源，并提供从本地开发到云环境的灵活部署选项。
本教程演示了如何将 Milvus 与 MindsDB 集成，通过类似 SQL 的操作来管理和查询向量嵌入，使您能够利用 MindsDB 的 AI 功能和 Milvus 的向量数据库功能。
本教程主要参考了
MindsDB Milvus处理程序
的官方文档。如果你在本教程中发现任何过时的部分，可以优先参考官方文档，并为我们创建一个问题。
安装MindsDB
开始之前，请通过
Docker
或
Docker Desktop
在本地安装MindsDB。
在继续之前，确保你对MindsDB和Milvus的基本概念和操作符都有扎实的理解。
参数介绍
建立连接所需的参数如下
uri
：Milvus 数据库的 uri，可以设置为本地".db "文件，也可以设置为 docker 或云服务。
token
根据 uri 选项支持 docker 或云服务的令牌
用于建立连接的可选参数有
这些参数用于
SELECT
查询：
search_default_limit
：在选择语句中传递的默认限制（默认值=100）
search_metric_type
：用于搜索的度量类型（默认="L2）
search_ignore_growing
：在进行相似性搜索时是否忽略不断增长的片段（默认值=假）
search_params
特定于
search_metric_type
（默认值={"nprobe"：10}）。
这些用于
CREATE
查询：
create_auto_id
id：插入无 ID 记录时是否自动生成 ID（默认值为 False）
create_id_max_len
创建表格时 id 字段的最大长度（默认值=64）
create_embedding_dim
创建表格时的嵌入维度（默认值=8）
create_dynamic_field
创建的表是否有动态字段（默认为 true）
create_content_max_len
内容列的最大长度（默认值=200）
create_content_default_value
内容列的默认值（默认值=''）
create_schema_description
模式的描述（默认值=''）
create_alias
模式的别名（默认值='默认值）
create_index_params
在 Embeddings 列上创建的索引的参数（default={}）。
create_index_metric_type
：用于创建索引的度量（默认值='L2')
create_index_type
索引类型（默认='AUTOINDEX）
使用方法
在继续之前，请确保
pymilvus
版本与此
固定版本
相同。如果发现版本兼容性问题，可以回滚 pymilvus 版本，或在此
需求文件
中自定义版本。
创建连接
为了使用该处理程序并连接到 MindsDB 中的 Milvus 服务器，可以使用以下语法：
CREATE
DATABASE milvus_datasource
WITH
ENGINE
=
'milvus'
,
  PARAMETERS
=
{
    "uri": "./milvus_local.db",
    "token": "",
    "create_embedding_dim":
3
,
    "create_auto_id":
true
};
如果你只需要一个本地向量数据库，用于小规模数据或原型设计，那么将uri设置为本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在这个文件中。
如果要在生产中使用更大规模的数据和流量，可以在
Docker 或 Kubernetes
上设置 Milvus 服务器。在此设置中，请使用服务器地址和端口作为
uri
，例如
http://localhost:19530
。如果启用了 Milvus 上的身份验证功能，请将
token
设置为
"<your_username>:<your_password>"
，否则无需设置令牌。
您也可以在
Zilliz Cloud
上使用完全托管的 Milvus。只需将
uri
和
token
设置为 Zilliz Cloud 实例的
公共端点和 API 密钥
。
放弃连接
要放弃连接，请使用此命令
DROP
DATABASE milvus_datasource;
创建表格
要从预先存在的表中插入数据，请使用
CREATE
CREATE
TABLE
milvus_datasource.test
(
SELECT
*
FROM
sqlitedb.test);
删除 Collection
不支持删除 Collections
查询和选择
要使用搜索向量查询数据库，可在
WHERE
子句中使用
search_vector
注意事项：
如果省略
LIMIT
，则会使用
search_default_limit
，因为 Milvus 需要它
不支持元数据列，但如果 Collections 启用了动态 Schema，则可以像普通查询一样进行查询，见下面的示例
动态字段无法显示，但可以查询
SELECT
*
from
milvus_datasource.test
WHERE
search_vector
=
'[3.0, 1.0, 2.0, 4.5]'
LIMIT
10
;
如果省略
search_vector
，这将成为基本搜索，并返回
LIMIT
或
search_default_limit
中的 Collections 条目数量
SELECT
*
from
milvus_datasource.test
可以像普通 SQL 一样在动态字段上使用
WHERE
子句
SELECT
*
FROM
milvus_datasource.createtest
WHERE
category
=
"science";
删除记录
可以像使用 SQL 一样使用
DELETE
删除条目。
注意事项
Milvus 只支持删除具有明确指定主键的实体。
只能使用
IN
操作符
DELETE
FROM
milvus_datasource.test
WHERE
id
IN
(
1
,
2
,
3
);
插入记录
您也可以像这样插入单个记录：
INSERT
INTO
milvus_test.testable (id,content,metadata,embeddings)
VALUES
("id3",
'this is a test'
,
'{"test": "test"}'
,
'[1.0, 8.0, 9.0]'
);
更新
Milvus API 不支持更新记录。你可以尝试使用
DELETE
和
INSERT
更多详情和示例，请参阅
MindsDB官方文档
。