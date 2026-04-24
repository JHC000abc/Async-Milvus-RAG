删除用户和角色
为确保数据安全，建议你删除不再使用的用户和角色。本指南将介绍如何删除用户和角色。
删除用户
下面的示例演示了如何删除用户
user_1
。
不能删除
root
用户。
Python
Java
纯文本
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
# create a user
client.drop_user(user_name=
"user_1"
)
import
io.milvus.v2.client.ConnectConfig
import
io.milvus.v2.client.MilvusClientV2
import
io.milvus.v2.service.rbac.request.DropUserReq
ConnectConfig
connectConfig
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
(connectConfig);
DropUserReq
dropUserReq
=
DropUserReq.builder()
        .userName(
"user_1"
)
        .build();
client.dropUser(dropUserReq);
import (
    "context"
    "fmt"

    "github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer cancel()

client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address: "localhost:19530",
    APIKey:  "root:Milvus",
})
if err != nil {
    fmt.Println(err.Error())
    // handle error
}
defer client.Close(ctx)

err = client.DropUser(ctx, milvusclient.NewDropUserOption("user_1"))
if err != nil {
    fmt.Println(err.Error())
    // handle error
}
const
{
MilvusClient
,
DataType
} =
require
(
"@zilliz/milvus2-sdk-node"
)
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

milvusClient.
deleteUser
({
username
:
'user_1'
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
/v2/vectordb/users/drop"
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
    "userName": "user_1"
}'
下拉用户后，可以列出所有现有用户，检查下拉操作是否成功。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client.list_users()
import
io.milvus.v2.service.rbac.request.listUsersReq

List<String> resp = client.listUsers();
users, err := client.ListUsers(ctx, milvusclient.NewListUserOption())
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
const
{
MilvusClient
,
DataType
} =
require
(
"@zilliz/milvus2-sdk-node"
)
await
milvusClient.
listUsers
();
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/users/list"
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
'{}'
下面是一个输出示例。列表中没有
user_1
。下拉操作符成功。
[
'root'
]
删除角色
下面的示例演示了如何删除角色
role_a
。
不能删除内置角色
admin
。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client.drop_role(role_name=
"role_a"
)
import
io.milvus.v2.service.rbac.request.DropRoleReq
DropRoleReq
dropRoleReq
=
DropRoleReq.builder()
        .roleName(
"role_a"
)
        .build();
client.dropRole(dropRoleReq);
err = client.DropRole(ctx, milvusclient.NewDropRoleOption(
"role_a"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
const
{
MilvusClient
,
DataType
} =
require
(
"@zilliz/milvus2-sdk-node"
)
await
milvusClient.
dropRole
({
roleName
:
'role_a'
,
 });
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/drop"
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
    "roleName": "role_a"
}'
角色下拉后，您可以列出所有现有角色，以检查下拉操作是否成功。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client.list_roles()
List<String> resp = client.listRoles();
roles, err := client.ListRoles(ctx, milvusclient.NewListRoleOption())
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
await
client.
listRoles
({
includeUserInfo
:
true
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/list"
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
'{}'
下面是一个输出示例。列表中没有
role_a
。下拉操作符成功。
[
'admin'
]