向用户授予角色
创建角色并授予角色权限后，就可以将角色授予用户，这样用户就可以访问资源并执行角色所定义的操作。可以向一个用户授予多个角色，也可以向多个用户授予一个角色。本指南将介绍如何向用户授予角色。
milvus 中的内置用户
root
已被授予
admin
角色，该角色拥有所有权限。您不需要为其分配任何其他角色。
向用户授予角色
下面的示例演示了如何向用户
user_1
授予
role_a
角色。
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

client.grant_role(user_name=
"user_1"
, role_name=
"role_a"
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.rbac.request.GrantRoleReq;
String
CLUSTER_ENDPOINT
=
"http://localhost:19530"
;
String
TOKEN
=
"root:Milvus"
;
ConnectConfig
connectConfig
=
ConnectConfig.builder()
    .uri(CLUSTER_ENDPOINT)
    .token(TOKEN)
    .build();
MilvusClientV2
client
=
new
MilvusClientV2
(connectConfig);
GrantRoleReq
grantRoleReq
=
GrantRoleReq.builder()
        .roleName(
"role_a"
)
        .userName(
"user_1"
)
        .build();
client.grantRole(grantRoleReq);
import
(
"context"
"fmt"
"github.com/milvus-io/milvus/client/v2/milvusclient"
)

ctx, cancel := context.WithCancel(context.Background())
defer
cancel()

client, err := milvusclient.New(ctx, &milvusclient.ClientConfig{
    Address:
"localhost:19530"
,
    APIKey:
"root:Milvus"
,
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

err = client.GrantRole(ctx, milvusclient.NewGrantRoleOption(
"user_1"
,
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
await
client.
grantRole
({
username
:
'user_1'
,
roleName
:
'role_a'
});
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
/v2/vectordb/users/grant_role"
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
    "roleName": "role_a",
    "userName": "user_1"
}'
描述用户
向用户授予角色后，可以通过
describe_user()
方法检查授予操作是否成功。
下面的示例演示了如何检查用户
user_1
的角色。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client.describe_user(user_name=
"user_1"
)
import
io.milvus.v2.service.rbac.request.DescribeUserReq;
import
io.milvus.v2.service.rbac.response.DescribeUserResp;
DescribeUserReq
describeUserReq
=
DescribeUserReq.builder()
        .userName(
"user_1"
)
        .build();
DescribeUserResp
describeUserResp
=
client.describeUser(describeUserReq);
user, err := client.DescribeUser(ctx, milvusclient.NewDescribeUserOption(
"user_1"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
await
client.
describeUser
({
username
:
'user_1'
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/users/describe"
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
下面是一个输出示例。
{
'user_name'
:
'user_1'
,
'roles'
:
'role_a'
}
撤销角色
您还可以撤销已分配给用户的角色。
下面的示例演示了如何撤销分配给用户
role_a
的角色
user_1
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

client.revoke_role(
    user_name=
'user_1'
,
    role_name=
'role_a'
)
import
io.milvus.v2.service.rbac.request.RevokeRoleReq;

client.revokeRole(RevokeRoleReq.builder()
        .userName(
"user_1"
)
        .roleName(
"role_a"
)
        .build());
err = client.RevokeRole(ctx, milvusclient.NewRevokeRoleOption(
"user_1"
,
"role_a"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
await
client.
revokeRole
({
username
:
'user_1'
,
roleName
:
'role_a'
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/users/revoke_role"
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
    "userName": "user_1",
    "roleName": "role_a"
}'