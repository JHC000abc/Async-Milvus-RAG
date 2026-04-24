为角色授予权限或权限组
创建角色后，就可以向角色授予权限。本指南将介绍如何向角色授予权限或权限组。
向角色授予权限或权限组
Milvus 2.5 引入了新版本的 API，简化了授予操作。向角色授予权限时，不再需要查找对象类型。以下是参数和相应的解释。
role_name：
需要授予权限或权限组的目标角色名称。
资源
：权限的目标资源，可以是特定实例、数据库或 Collections。
下表解释了如何在
client.grantV2()
方法中指定资源。
级别
资源
授予方法
注释
Collections
特定 Collections
client.grant_privilege_v2(
     role_name="roleA", 
     privilege="CollectionAdmin",
     collection_name="col1", 
     db_name="db1"
 )
输入目标 Collections 的名称以及目标 Collections 所属数据库的名称。
特定数据库下的所有集合
client.grant_privilege_v2(
     role_name="roleA", 
     privilege="CollectionAdmin",
     collection_name="*", 
     db_name="db1"
 )
输入目标数据库名称和通配符
*
作为 Collection 名称。
数据库
特定数据库
client.grant_privilege_v2(
     role_name="roleA", 
     privilege="DatabaseAdmin", 
     collection_name="*", 
     db_name="db1"
 )
输入目标数据库的名称和通配符
*
作为 Collections 名称。
当前实例下的所有数据库
client.grant_privilege_v2(
     role_name="roleA", 
     privilege="DatabaseAdmin", 
     collection_name="*", 
     db_name="*"
 )
输入
*
作为数据库名称，输入
*
作为 Collections 名称。
实例
当前实例
client.grant_privilege_v2(
     role_name="roleA", 
     privilege="ClusterAdmin", 
     collection_name="*", 
     db_name="*"
 )
输入
*
作为数据库名称，输入
*
作为 Collections 名称。
权限
：需要授予角色的特定权限或
权限组
。目前，Milvus 提供了 56 种可授予的特权。下表列出了 Milvus 中的特权。
下表中的类型列是用户为方便快速查找特权而设置的，仅用于分类目的。授予权限时，不需要了解类型。只需输入相应的权限即可。
类型
权限
说明
客户端的相关 API 说明
数据库权限
列出数据库
查看当前实例中的所有数据库
列出数据库
描述数据库
查看数据库的详细信息
描述数据库
创建数据库
创建数据库
创建数据库
删除数据库
删除数据库
删除数据库
更改数据库
修改数据库属性
更改数据库
Collections 权限
获取刷新状态
检查 Collections 清除操作符的状态
获取刷新状态
获取加载状态
检查 Collections 的加载状态
获取加载状态
获取加载进度
检查 Collections 的加载进度
获取加载进度
显示收藏集
查看具有收藏权限的所有 Collections
显示收藏集
列出别名
查看某个 Collection 的所有别名
列出别名
描述收藏集
查看 Collections 的详细信息
描述集合
描述别名
查看别名的详细信息
描述别名
获取统计数据
获取 Collections 的统计数据（如 Collections 中实体的数量）
获取集合统计信息
创建集合
创建 Collections
创建收藏集
删除收藏集
删除 Collections
删除收藏集
加载
加载 Collections
加载集合/
获取
加载进度/获取加载状态
释放
释放一个 Collections
释放集合
刷新
将 Collections 中的所有实体持久化到一个密封段中。任何在冲洗操作后插入的实体都将存储在新的段中。
刷新/获取刷新
状态
压缩
手动触发压缩
压缩
重命名集合
重命名 Collections
重命名集合
创建别名
为 Collections 创建别名
创建别名
删除别名
删除 Collections 的别名
删除别名
全部清除
清除数据库中的所有 Collections
全部清除
分区权限
有分区
检查是否存在分区
HasPartition
显示分区
查看 Collections 中的所有分区
显示分区
创建分区
创建分区
创建分区
删除分区
删除分区
删除分区
索引权限
索引详情
查看索引的详细信息
DescribeIndex/GetIndexState/GetIndexBuildProgress
创建索引
创建索引
创建索引
删除索引
删除索引
删除索引
资源管理权限
负载平衡
实现负载平衡
负载平衡
创建资源组
创建资源组
创建资源组
删除资源组
删除资源组
删除资源组
更新资源组
更新资源组
更新资源组
描述资源组
查看资源组的详细信息
描述资源组
列出资源组
查看当前实例的所有资源组
列出资源组
转移节点
在资源组之间转移节点
传输节点
传输副本
在资源组之间传输副本
传输复制
备份 RBAC
为当前实例中所有与 RBAC 相关的操作创建备份
备份 RBAC
还原 RBAC
恢复当前实例中所有 RBAC 相关操作的备份
还原 RBAC
实体权限
查询
进行查询
查询
搜索
进行搜索
搜索
插入
插入实体
插入
删除
删除实体
删除
插入
插入实体
插入
导入
批量插入或导入实体
批量插入/导入
RBAC 权限
创建所有权
创建用户或角色
创建用户/创建角色
更新用户
更新用户密码
更新凭证
删除所有权
删除用户密码或角色
删除凭证/删除角色
选择所有权
查看被授予特定角色的所有用户
选择角色/选择授权
管理所有权
管理用户或角色，或向用户授予角色
操作用户角色/操作权限/操作权限 V2
选择用户
查看授予用户的所有角色
选择用户
创建权限组
创建权限组
创建权限组
删除权限组
删除权限组
删除特权组
列出特权组
查看当前实例中的所有特权组
列出特权组
操作特权组
向特权组添加特权或从特权组移除特权
操作特权组
下面的示例演示了如何在
default
数据库下的
collection_01
上授予
PrivilegeSearch
权限，以及如何将名为
privilege_group_1
的特权组授予角色
role_a
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

client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"root:Milvus"
)

client.grant_privilege_v2(
    role_name=
"role_a"
,
    privilege=
"Search"
,
    collection_name=
'collection_01'
,
    db_name=
'default'
,
)
    
client.grant_privilege_v2(
    role_name=
"role_a"
,
    privilege=
"privilege_group_1"
,
    collection_name=
'collection_01'
,
    db_name=
'default'
,
)

client.grant_privilege_v2(
    role_name=
"role_a"
,
    privilege=
"ClusterReadOnly"
,
    collection_name=
'*'
,
    db_name=
'*'
,
)
import
io.milvus.v2.service.rbac.request.GrantPrivilegeReqV2

client.grantPrivilegeV2(GrantPrivilegeReqV2.builder()
        .roleName(
"role_a"
)
        .privilege(
"Search"
)
        .collectionName(
"collection_01"
)
        .dbName(
"default"
)
        .build());

client.grantPrivilegeV2(GrantPrivilegeReqV2.builder()
        .roleName(
"role_a"
)
        .privilege(
"privilege_group_1"
)
        .collectionName(
"collection_01"
)
        .dbName(
"default"
)
        .build());

client.grantPrivilegeV2(GrantPrivilegeReqV2.builder()
        .roleName(
"role_a"
)
        .privilege(
"ClusterReadOnly"
)
        .collectionName(
"*"
)
        .dbName(
"*"
)
        .build());
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

err = client.GrantV2(ctx, milvusclient.NewGrantV2Option(
"role_a"
,
"Search"
,
"default"
,
"collection_01"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.GrantV2(ctx, milvusclient.NewGrantV2Option(
"role_a"
,
"privilege_group_1"
,
"default"
,
"collection_01"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.GrantV2(ctx, milvusclient.NewGrantV2Option(
"role_a"
,
"ClusterReadOnly"
,
"*"
,
"*"
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
grantPrivilegeV2
({
role
:
"role_a"
,
privilege
:
"Search"
collection_name
:
'collection_01'
db_name
:
'default'
,
});
await
client.
grantPrivilegeV2
({
role
:
"role_a"
,
privilege
:
"privilege_group_1"
collection_name
:
'collection_01'
db_name
:
'default'
,
});
await
client.
grantPrivilegeV2
({
role
:
"role_a"
,
privilege
:
"ClusterReadOnly"
collection_name
:
'*'
db_name
:
'*'
,
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/grant_privilege_v2"
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
    "privilege": "Search",
    "collectionName": "collection_01",
    "dbName":"default"
}'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/grant_privilege_v2"
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
    "privilege": "privilege_group_1",
    "collectionName": "collection_01",
    "dbName":"default"
}'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/grant_privilege_v2"
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
    "privilege": "ClusterReadOnly",
    "collectionName": "*",
    "dbName":"*"
}'
描述角色
下面的示例演示了如何使用
describe_role
方法查看授予角色
role_a
的权限。
Python
Java
Go
NodeJS
cURL
from
pymilvus
import
MilvusClient

client.describe_role(role_name=
"role_a"
)
import
io.milvus.v2.service.rbac.response.DescribeRoleResp;
import
io.milvus.v2.service.rbac.request.DescribeRoleReq
DescribeRoleReq
describeRoleReq
=
DescribeRoleReq.builder()
        .roleName(
"role_a"
)
        .build();
DescribeRoleResp
resp
=
client.describeRole(describeRoleReq);
List<DescribeRoleResp.GrantInfo> infos = resp.getGrantInfos();
import
"github.com/milvus-io/milvus/client/v2/milvusclient"
role, err := client.DescribeRole(ctx, milvusclient.NewDescribeRoleOption(
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
describeRole
({
roleName
:
'role_a'
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/describe"
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
下面是一个输出示例。
{
"role"
:
"role_a"
,
"privileges"
: [
         {
"collection_name"
:
"collection_01"
,
"db_name"
:
"default"
,
"role_name"
:
"role_a"
,
"privilege"
:
"Search"
,
"grantor_name"
:
"root"
},
"privilege_group_1"
]
}
撤销角色的权限或权限组
下面的示例演示了如何撤销
default
数据库下
collection_01
的特权
PrivilegeSearch
以及授予角色
role_a
的特权组
privilege_group_1
。
Python
Java
Go
NodeJS
cURL
client.revoke_privilege_v2(
    role_name=
"role_a"
,
    privilege=
"Search"
,
    collection_name=
'collection_01'
,
    db_name=
'default'
,
)
    
client.revoke_privilege_v2(
    role_name=
"role_a"
,
    privilege=
"privilege_group_1"
,
    collection_name=
'collection_01'
,
    db_name=
'default'
,
)

client.revoke_privilege_v2(
    role_name=
"role_a"
,
    privilege=
"ClusterReadOnly"
,
    collection_name=
'*'
,
    db_name=
'*'
,
)
import
io.milvus.v2.service.rbac.request.RevokePrivilegeReqV2

client.revokePrivilegeV2(RevokePrivilegeReqV2.builder()
        .roleName(
"role_a"
)
        .privilege(
"Search"
)
        .collectionName(
"collection_01"
)
        .dbName(
"default"
)
        .build());

client.revokePrivilegeV2(RevokePrivilegeReqV2.builder()
        .roleName(
"role_a"
)
        .privilege(
"privilege_group_1"
)
        .collectionName(
"collection_01"
)
        .dbName(
"default"
)
        .build());

client.revokePrivilegeV2(RevokePrivilegeReqV2.builder()
        .roleName(
"role_a"
)
        .privilege(
"ClusterReadOnly"
)
        .collectionName(
"*"
)
        .dbName(
"*"
)
        .build());
err = client.RevokePrivilegeV2(ctx, milvusclient.NewRevokePrivilegeV2Option(
"role_a"
,
"Search"
,
"collection_01"
).
        WithDbName(
"default"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.RevokePrivilegeV2(ctx, milvusclient.NewRevokePrivilegeV2Option(
"role_a"
,
"privilege_group_1"
,
"collection_01"
).
    WithDbName(
"default"
))
if
err !=
nil
{
    fmt.Println(err.Error())
// handle error
}

err = client.RevokePrivilegeV2(ctx, milvusclient.NewRevokePrivilegeV2Option(
"role_a"
,
"ClusterReadOnly"
,
"*"
).
    WithDbName(
"*"
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
revokePrivilegeV2
({
role
:
'role_a'
,
privilege
:
'Search'
,
collection_name
:
'collection_01'
,
db_name
:
'default'
});
await
client.
revokePrivilegeV2
({
role
:
'role_a'
,
collection_name
:
'collection_01'
,
privilege
:
'Search'
,
db_name
:
'default'
});
await
client.
revokePrivilegeV2
({
role
:
'role_a'
,
collection_name
:
'*'
,
privilege
:
'ClusterReadOnly'
,
db_name
:
'*'
});
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/revoke_privilege_v2"
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
    "privilege": "Search",
    "collectionName": "collection_01",
    "dbName":"default"
}'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/revoke_privilege_v2"
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
    "privilege": "Search",
    "collectionName": "collection_01",
    "dbName":"default"
}'
curl --request POST \
--url
"
${CLUSTER_ENDPOINT}
/v2/vectordb/roles/revoke_privilege_v2"
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
    "privilege": "ClusterReadOnly",
    "collectionName": "*",
    "dbName":"*"
}'