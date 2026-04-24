数据库
Milvus 在集合之上引入了
数据库
层，为管理和组织数据提供了更有效的方式，同时支持多租户。
什么是数据库
在 Milvus 中，数据库是组织和管理数据的逻辑单元。为了提高数据安全性并实现多租户，你可以创建多个数据库，为不同的应用程序或租户从逻辑上隔离数据。例如，创建一个数据库用于存储用户 A 的数据，另一个数据库用于存储用户 B 的数据。
创建数据库
您可以使用 Milvus RESTful API 或 SDK 以编程方式创建数据。
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

client.create_database(
    db_name=
"my_database_1"
)
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.service.database.request.*;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .token(
"root:Milvus"
)
        .build();
MilvusClientV2
client
=
new
MilvusClientV2
(config);
CreateDatabaseReq
createDatabaseReq
=
CreateDatabaseReq.builder()
        .databaseName(
"my_database_1"
)
        .build();
client.createDatabase(createDatabaseReq);
import
{
MilvusClient
}
from
'@zilliz/milvus2-sdk-node'
;
const
client =
new
MilvusClient
({
address
:
"http://localhost:19530"
,
token
:
'root:Milvus'
});
await
client.
createDatabase
({
db_name
:
"my_database_1"
});
cli, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
    Username:
"Milvus"
,
    Password:
"root"
,
})
if
err !=
nil
{
// handle err
}

err = cli.CreateDatabase(ctx, milvusclient.NewCreateDatabaseOption(
"my_database_1"
))
if
err !=
nil
{
// handle err
}
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
/v2/vectordb/databases/create"
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
    "dbName": "my_database_1"
}'
您还可以在创建数据库时为其设置属性。下面的示例设置了数据库的副本数量。
Python
Java
NodeJS
Go
cURL
client.create_database(
    db_name=
"my_database_2"
,
    properties={
"database.replica.number"
:
3
}
)
Map<String, String> properties =
new
HashMap
<>();
properties.put(
"database.replica.number"
,
"3"
);
CreateDatabaseReq
createDatabaseReq
=
CreateDatabaseReq.builder()
        .databaseName(
"my_database_2"
)
        .properties(properties)
        .build();
client.createDatabase(createDatabaseReq);
await
client.
createDatabase
({
db_name
:
"my_database_2"
,
properties
: {
"database.replica.number"
:
3
}
});
err := cli.CreateDatabase(ctx, milvusclient.NewCreateDatabaseOption(
"my_database_2"
).WithProperty(
"database.replica.number"
,
3
))
if
err !=
nil
{
// handle err
}
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
/v2/vectordb/databases/create"
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
    "dbName": "my_database_2",
    "properties": {
        "database.replica.number": 3
    }
}'
查看数据库
您可以使用 Milvus RESTful API 或 SDK 列出所有现有数据库并查看其详细信息。
Python
Java
NodeJS
Go
cURL
# List all existing databases
client.list_databases()
# Output
# ['default', 'my_database_1', 'my_database_2']
# Check database details
client.describe_database(
    db_name=
"default"
)
# Output
# {"name": "default"}
import
io.milvus.v2.service.database.response.*;
ListDatabasesResp
listDatabasesResp
=
client.listDatabases();
DescribeDatabaseResp
descDBResp
=
client.describeDatabase(DescribeDatabaseReq.builder()
        .databaseName(
"default"
)
        .build());
await
client.
describeDatabase
({
db_name
:
'default'
});
// List all existing databases
databases, err := cli.ListDatabase(ctx, milvusclient.NewListDatabaseOption())
if
err !=
nil
{
// handle err
}
log.Println(databases)

db, err := cli.DescribeDatabase(ctx, milvusclient.NewDescribeDatabaseOption(
"default"
))
if
err !=
nil
{
// handle err
}
log.Println(db)
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
/v2/vectordb/databases/describe"
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
    "dbName": "default"
}'
管理数据库属性
每个数据库都有自己的属性，您可以在
创建数据库
时设置数据库属性（如
创建数据库
中所述），也可以更改和删除任何现有数据库的属性。
下表列出了可能的数据库属性。
属性名称
类型
属性描述
database.replica.number
整数
指定数据库的副本数量。
database.resource_groups
字符串
以逗号分隔的列表形式列出的与指定数据库相关的资源组名称。
database.diskQuota.mb
整数
指定数据库的最大磁盘空间大小（MB）。
database.max.collections
整数
指定数据库中允许的最大 Collections 数量。
database.force.deny.writing
布尔
是否强制指定的数据库拒绝写操作。
database.force.deny.reading
布尔
是否强制指定的数据库拒绝读取操作。
timezone
字符串
指定应用于数据库内时间敏感操作的默认时区，尤其是
TIMESTAMPTZ
字段。除非设置了集合级时区，否则集合将继承数据库时区。查询级时区参数可暂时覆盖数据库和 Collections 的默认时区。其值必须是有效的
IANA 时区标识符
（例如，
亚洲/上海
、
美国/芝加哥
或
UTC
）。有关如何使用
TIMESTAMPTZ
字段的详细信息，请参阅
TIMESTAMPTZ 字段
。
更改数据库属性
您可以按以下方式更改现有数据库的属性。下面的示例限制了您可以在数据库中创建的 Collections 数量。
Python
Java
NodeJS
Go
cURL
client.alter_database_properties(
    db_name=
"my_database_1"
,
    properties={
"database.max.collections"
:
10
}
)
client.alterDatabaseProperties(AlterDatabasePropertiesReq.builder()
        .databaseName(
"my_database_1"
)
        .property(
"database.max.collections"
,
"10"
)
        .build());
await
milvusClient.
alterDatabaseProperties
({
db_name
:
"my_database_1"
,
properties
: {
"database.max.collections"
,
"10"
},
})
err := cli.AlterDatabaseProperties(ctx, milvusclient.NewAlterDatabasePropertiesOption(
"my_database_1"
).
    WithProperty(
"database.max.collections"
,
1
))
if
err !=
nil
{
// handle err
}
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
/v2/vectordb/databases/alter"
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
    "dbName": "my_database",
    "properties": {
        "database.max.collections": 10
    }
}'
删除数据库属性
您还可以通过如下方式删除数据库属性来重置该属性。下面的示例删除了可以在数据库中创建的 Collection 数量限制。
Python
Java
NodeJS
Go
cURL
client.drop_database_properties(
    db_name=
"my_database_1"
,
    property_keys=[
"database.max.collections"
]
)
client.dropDatabaseProperties(DropDatabasePropertiesReq.builder()
        .databaseName(
"my_database_1"
)
        .propertyKeys(Collections.singletonList(
"database.max.collections"
))
        .build());
await
milvusClient.
dropDatabaseProperties
({
db_name
: my_database_1,
properties
: [
"database.max.collections"
],
});
err := cli.DropDatabaseProperties(ctx, milvusclient.NewDropDatabasePropertiesOption(
"my_database_1"
,
"database.max.collections"
))
if
err !=
nil
{
// handle err
}
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
/v2/vectordb/databases/alter"
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
    "dbName": "my_database",
    "propertyKeys": [
        "database.max.collections"
    ]
}'
使用数据库
你可以在不断开与 Milvus 连接的情况下从一个数据库切换到另一个数据库。
RESTful API 不支持此操作符。
Python
Java
NodeJS
Go
cURL
client.use_database(
    db_name=
"my_database_2"
)
client.useDatabase(
"my_database_2"
);
await
milvusClient.
useDatabase
({
db_name
:
"my_database_2"
,
});
err = cli.UseDatabase(ctx, milvusclient.NewUseDatabaseOption(
"my_database_2"
))
if
err !=
nil
{
// handle err
}
# This operation is unsupported because RESTful does not provide a persistent connection.
# As a workaround, initiate the required request again with the target database.
删除数据库
一旦不再需要数据库，就可以删除数据库。请注意
不能丢弃默认数据库。
在删除数据库之前，需要先删除数据库中的所有 Collections。
你可以使用 Milvus RESTful API 或 SDK 以编程方式创建数据。
Python
Java
NodeJS
Go
cURL
client.drop_database(
    db_name=
"my_database_2"
)
client.dropDatabase(DropDatabaseReq.builder()
        .databaseName(
"my_database_2"
)
        .build());
await
milvusClient.
dropDatabase
({
db_name
:
"my_database_2"
,
});
err = cli.DropDatabase(ctx, milvusclient.NewDropDatabaseOption(
"my_database_2"
))
if
err !=
nil
{
// handle err
}
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
/v2/vectordb/databases/drop"
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
    "dbName": "my_database"
}'
常见问题
如何管理数据库的权限？
Milvus 使用基于角色的访问控制（RBAC）来管理权限。您可以创建具有特定权限的角色，并将其分配给用户，从而控制他们对不同数据库的访问。有关详细信息，请参阅
RBAC 文档
。
数据库有配额限制吗？
是的，Milvus 允许您为数据库设置配额限制，如收藏的最大数量。有关限制的全面列表，请参阅
Milvus 限制文档
。