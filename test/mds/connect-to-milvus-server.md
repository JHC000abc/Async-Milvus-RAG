连接 Milvus 服务器
本主题介绍如何建立与 Milvus 服务器的客户端连接并配置常用连接选项。
前提条件
已安装所使用语言的 SDK。有关详情，请参阅
Python SDK
、
Java SDK
、
Go SDK
或
Nodejs SDK
。
Milvus 服务器地址（本地默认地址：
http://localhost:19530
，代理端口
19530
）。
如果
启用了身份验证
，请提供
令牌
或
用户名 + 密码
。令牌可以是
username:password
（如
root:Milvus
）。有关详情，请参阅 "
验证用户访问
"和 "
创建用户和角色
"。
通过 URI 连接（禁用身份验证）
使用 Milvus 服务器地址（如
http://localhost:19530
）建立连接。
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
"http://localhost:19530"
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .build();
client =
new
MilvusClientV2
(config);
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
'http://localhost:19530'
});
import
"github.com/milvus-io/milvus/client/v2/milvusclient"
c, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
})
# restful
使用凭证连接（启用身份验证）
提供
"username:password"
或
user
和
password
形式的
令牌
。默认内置管理员为
root:Milvus
（生产时可更改）。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient
# Token form
client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
,
)
# Or explicit user/password
client = MilvusClient(
    uri=
"http://localhost:19530"
,
    user=
"root"
,
    password=
"Milvus"
,
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .username(
"root"
)
        .password(
"Milvus"
)
        .build();
client =
new
MilvusClientV2
(config);
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
'http://localhost:19530'
,
username
:
'root'
,
password
:
'Milvus'
});
import
"github.com/milvus-io/milvus/client/v2/milvusclient"
c, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
    Username:
"root"
,
    Password:
"Milvus"
,
})
# restful
令牌格式为
"<username>:<password>"
。文档明确指出
root:Milvus
为默认凭证，《
创建用户和角色
》指南涵盖了用户管理。
配置超时
设置客户端连接的默认超时时间：
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient

client = MilvusClient(uri=
"http://localhost:19530"
, timeout=
1000
)
# If not set, the timeout defaults to 10s
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .rpcDeadlineMs(
1000
)
        .build();
client =
new
MilvusClientV2
(config);
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
'http://localhost:19530'
,
username
:
'root'
,
password
:
'Milvus'
,
timeout
:
1000
// ms
});
// await client.listCollections({ timeout: 2000})
import
"github.com/milvus-io/milvus/client/v2/milvusclient"
ctx, cancel := context.WithTimeout(context.Background(), time.Second)
defer
cancel()
c, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
})
# restful
此超时仅在建立连接时使用。它不作为其他 API 操作的默认超时。
连接到特定数据库
在构建过程中，使用
db_name
选择目标数据库。也可以稍后使用
using_database()
进行切换。
Python
Java
NodeJS
Go
cURL
from
pymilvus
import
MilvusClient
# Set the database when creating the client
client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
,
    db_name=
"analytics"
,
)
# (Optional) Switch the active database later
# client.using_database("reports")
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
ConnectConfig
config
=
ConnectConfig.builder()
        .uri(
"http://localhost:19530"
)
        .username(
"root"
)
        .password(
"Milvus"
)
        .dbName(
"analytics"
)
        .build();
client =
new
MilvusClientV2
(config);
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
'http://localhost:19530'
,
username
:
'root'
,
password
:
'Milvus'
,
database
:
'analytics'
});
// (Optional) Switch the active database later
// await milvusClient.useDatabase({
//   db_name: 'reports',
//});
import
"github.com/milvus-io/milvus/client/v2/milvusclient"
c, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
    DBName:
"analytics"
,
    APIKey:
"root:Milvus"
,
})
// (Optional) switch the active database later with:
err = c.UseDatabase(ctx, milvusclient.NewUseDatabaseOption(
"reports"
))
# restful
有关创建、列出和描述数据库以及更广泛的数据库管理任务，请参阅
数据库
指南。
下一步
创建 Collections
插入实体
基本向量搜索