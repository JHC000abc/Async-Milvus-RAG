使用 Milvus 操作符配置元存储
Milvus 使用 etcd 来存储元数据。本主题介绍如何在使用 Milvus Operator 安装 Milvus 时配置元存储依赖关系。有关详细信息，请参阅 Milvus Operator 存储库中的
配置 Milvus Operator 的元存储
。
本主题假设您已部署 Milvus Operator。
有关详细信息，请参阅
部署 Milvus Operator
。
您需要指定使用 Milvus Operator 启动 Milvus 群集的配置文件。
kubectl
apply
-f
https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml
您只需编辑
milvus_cluster_default.yaml
中的代码模板，即可配置第三方依赖关系。下文将分别介绍如何配置对象存储、etcd 和 Pulsar。
配置 etcd
在
spec.dependencies.etcd
下添加配置 etcd 的必填字段。
etcd
支持 和 。
external
inCluster
用于配置外部 etcd 服务的字段包括
external
:
true
值表示 Milvus 使用外部 etcd 服务。
endpoints
:etcd 的端点。
外部 etcd
示例
下面的示例配置了外部 etcd 服务。
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
dependencies:
# Optional
etcd:
# Optional
# Whether (=true) to use an existed external etcd as specified in the field endpoints or
# (=false) create a new etcd inside the same kubernetes cluster for milvus.
external:
true
# Optional default=false
# The external etcd endpoints if external=true
endpoints:
-
192.168
.1
.1
:2379
components:
{}
config:
{}
内部 etcd
inCluster
表示当 milvus 集群启动时，etcd 服务会在集群中自动启动。
示例
下面的示例配置了内部 etcd 服务。
apiVersion:
milvus.io/v1alpha1
kind:
Milvus
metadata:
name:
my-release
labels:
app:
milvus
spec:
dependencies:
etcd:
inCluster:
values:
replicaCount:
5
resources:
limits:
cpu:
'4'
memory:
8Gi
requests:
cpu:
200m
memory:
512Mi
components:
{}
config:
{}
上例将副本数量指定为
5
，并限制了 etcd 的计算资源。
在
values.yaml
中查找配置内部 etcd 服务的完整配置项。如上例所示，根据需要在
etcd.inCluster.values
下添加配置项。
假设配置文件名为
milvuscluster.yaml
，请运行以下命令应用配置。
kubectl apply -f milvuscluster.yaml
下一步
了解如何使用 Milvus Operator 配置其他 Milvus 依赖项：
使用 Milvus Operator 配置对象存储
使用 Milvus Operator 配置消息存储器