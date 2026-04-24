验证用户访问
本指南介绍如何在 Milvus 中管理用户身份验证，包括启用身份验证、以用户身份连接和修改用户凭证。
TLS 和用户身份验证是两种不同的安全方法。如果在 Milvus 系统中同时启用了用户身份验证和 TLS，则必须提供用户名、密码和证书文件路径。有关如何启用 TLS 的信息，请参阅 "
传输中的加密
"。
本页的代码片段使用新的
MilvusClient
(Python) 与 Milvus 进行交互。用于其他语言的新 MilvusClient SDK 将在未来更新中发布。
启用用户身份验证
Docker Compose
Helm
Milvus 操作符
要为您的 Milvus 服务器启用用户身份验证，请在 Milvus 配置文件
milvus.yaml
中将 common.security.authorizationEnabled 设置为 true。有关配置的更多信息，请参阅
使用 Docker Compose 配置 Milvus
。
...
common:
...
security:
authorizationEnabled:
true
...
要启用 Milvus 服务器的用户身份验证，请在 Milvus 配置文件
values.yaml
中将 authorizationEnabled 设为 true。有关配置的更多信息，请参阅
使用 Helm Charts 配置 Milvus
。
...
extraConfigFiles:
user.yaml:
|+
    common:
      security:
        authorizationEnabled: true
...
要启用身份验证，请在
Milvus
CRD 中将
spec.config.common.security.authorizationEnabled
设置为
true
。有关 Milvus CRD 的更多信息，请参阅
使用 Milvus Operator 配置 Milvus
。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
# Omit other fields ...
config:
common:
security:
authorizationEnabled:
true
通过身份验证连接 Milvus
启用身份验证后，需要使用用户名和密码连接到 Milvus。默认情况下，启动 Milvus 时会创建
root
用户，密码为
Milvus
。下面是一个示例，说明如何使用默认
root
用户在启用身份验证后连接 Milvus：
# use default `root` user to connect to Milvus
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
'http://localhost:19530'
,
# replace with your own Milvus server address
token=
"root:Milvus"
)
如果在启用身份验证的情况下连接 Milvus 时未能提供有效令牌，则会收到 gRPC 错误。
创建新用户
以默认
root
用户身份连接后，可以按以下步骤创建和验证新用户：
# create a user
client.create_user(
    user_name=
"user_1"
,
    password=
"P@ssw0rd"
,
)
# verify the user has been created
client.describe_user(
"user_1"
)
# output
# {'user_name': 'user_1', 'roles': ()}
有关创建用户的更多信息，请参阅
create_user()
。
使用新用户连接 Milvus
使用新创建用户的凭据进行连接：
# connect to milvus with the newly created user
client = MilvusClient(
    uri=
"http://localhost:19530"
,
    token=
"user_1:P@ssw0rd"
)
更新用户密码
用以下代码更改现有用户的密码：
# update password
client.update_password(
    user_name=
"user_1"
,
    old_password=
"P@ssw0rd"
,
    new_password=
"P@ssw0rd123"
)
有关更新用户密码的更多信息，请参阅
update_password()
。
如果忘记了旧密码，Milvus 提供了一个配置项，允许将某些用户指定为超级用户。这样，重置密码时就不需要旧密码了。
默认情况下，Milvus 配置文件中的
common.security.superUsers
字段为空，这意味着所有用户在重置密码时都必须提供旧密码。不过，你可以将特定用户指定为超级用户，他们不需要提供旧密码。在下面的代码段中，
root
和
foo
被指定为超级用户。
你应该在管理 Milvus 实例运行的 Milvus 配置文件中添加以下配置项。
common:
security:
superUsers:
root,
foo
删除用户
要删除用户，请使用
drop_user()
方法。
client.drop_user(user_name=
"user_1"
)
要删除用户，你不能是被删除的用户。否则，将引发错误。
列出所有用户
列出所有用户。
# list all users
client.list_users()
限制条件
用户名不得为空，长度不得超过 32 个字符。必须以字母开头，且只能包含下划线、字母或数字。
密码必须至少包含 6 个字符，长度不得超过 256 个字符。
下一步
你可能还想了解如何
扩展 Milvus 集群
如果您已准备好在云上部署集群：
了解如何
使用 Terraform 在亚马逊 EKS 上部署 Milvus
学习如何
使用 Kubernetes 在 GCP 上部署 Milvus 集群
了解如何
使用 Kubernetes 在 Microsoft Azure 上部署 Milvus