创建用户和角色
Milvus 通过 RBAC 实现细粒度访问控制。您可以从创建用户和角色开始，然后为角色分配权限或权限组，最后通过向用户授予角色来管理访问控制。这种方法可确保访问管理的效率和安全性。本页将介绍如何在 Milvus 中创建用户和角色。
用户
初始化 Milvus 实例后，会自动生成一个根用户，用于首次连接 Milvus 时进行身份验证。根用户的用户名是
root
，密码是
Milvus
。根用户的默认角色是
admin
，可以访问所有资源。为确保数据安全，请妥善保管根用户的凭据，防止未经授权的访问。
对于日常操作，我们建议创建用户而不是使用根用户。
创建用户
下面的示例显示了如何创建用户名为
user_1
、密码为
P@ssw0rd
的用户。用户名和密码必须遵循以下规则：
用户名：必须以字母开头，只能包含大写或小写字母、数字和下划线。
密码：长度必须为 8-64 个字符，必须包括以下三种字符：大写字母、小写字母、数字和特殊字符。
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

client.create_user(user_name=
"user_1"
, password=
"P@ssw0rd"
)
import
io.milvus.v2.client.ConnectConfig;
import
io.milvus.v2.client.MilvusClientV2;
import
io.milvus.v2.service.rbac.request.CreateUserReq;
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
CreateUserReq
createUserReq
=
CreateUserReq.builder()
        .userName(
"user_1"
)
        .password(
"P@ssw0rd"
)
        .build();
        
client.createUser(createUserReq);
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

err = client.CreateUser(ctx, milvusclient.NewCreateUserOption(
"user_1"
,
"P@ssw0rd"
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
createUser
({
username
:
'user_1'
,
password
:
'P@ssw0rd'
,
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
/v2/vectordb/users/create"
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
    "password": "P@ssw0rd"
}'
更新密码
创建用户后，如果忘记密码，可以更新密码。
新密码也必须遵循以下规则：
长度必须为 8-64 个字符，并包含以下三个字符：大写字母、小写字母、数字和特殊字符。
下面的示例显示了如何将用户
user_1
的密码更新为
NewP@ssw0rd
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

client.update_password(
    user_name=
"user_1"
,
    old_password=
"P@ssw0rd"
,
    new_password=
"NewP@ssw0rd"
)
import
io.milvus.v2.service.rbac.request.UpdatePasswordReq;
UpdatePasswordReq
updatePasswordReq
=
UpdatePasswordReq.builder()
        .userName(
"user_1"
)
        .password(
"P@ssw0rd"
)
        .newPassword(
"NewP@ssw0rd"
)
        .build();
client.updatePassword(updatePasswordReq);
err = client.UpdatePassword(ctx, milvusclient.NewUpdatePasswordOption(
"user_1"
,
"P@ssw0rd"
,
"NewP@ssw0rd"
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
client.
updateUser
({
username
:
'user_1'
,
newPassword
:
'P@ssw0rd'
,
oldPassword
:
'NewP@ssw0rd'
,
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/users/update_password"
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
    "newPassword": "P@ssw0rd!",
    "userName": "user_1",
    "password": "P@ssw0rd"
}'
列出用户
创建多个用户后，您可以列出并查看所有现有用户。
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
List<String> resp = client.listUsers();
users, err := client.ListUsers(ctx, milvusclient.NewListUserOption())
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}
await
client.
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
下面是一个输出示例。
root
是 Milvus 自动生成的默认用户。
user_1
是刚刚创建的新用户。
[
'root'
,
'user_1'
]
角色
Milvus 提供了一个名为
admin
的内置角色，它是一个管理员角色，可以访问所有实例下的资源，并拥有所有操作的权限。为实现更精细的访问管理和增强数据安全性，建议根据需要创建自定义角色。
创建角色
下面的示例演示了如何创建名为
role_a
的角色。
角色名称必须遵循以下规则：
必须以字母开头，且只能包含大写或小写字母、数字和下划线。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client.create_role(role_name=
"role_a"
)
import
io.milvus.v2.service.rbac.request.CreateRoleReq;
CreateRoleReq
createRoleReq
=
CreateRoleReq.builder()
        .roleName(
"role_a"
)
        .build();
err = client.CreateRole(ctx, milvusclient.NewCreateRoleOption(
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
createRole
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
/v2/vectordb/roles/create"
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
列出角色
创建多个角色后，您可以列出并查看所有现有角色。
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
List<String> roles = client.listRoles();
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
下面是一个输出示例。
admin
是 Milvus 中的默认角色。
role_a
是刚刚创建的新角色。
['admin', 'role_a']