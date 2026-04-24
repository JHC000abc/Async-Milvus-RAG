升级 Pulsar
本文介绍了将 Pulsar 组件从 V2 升级到 V3 的过程，如果您已经部署了使用 Pulsar V2 的 Milvus。
自 Milvus v2.5 起，
milvus-helm
和
milvus-operator
将默认使用 Pulsar V3，以修复一些错误和安全漏洞。 虽然 Milvus 2.5 与 Pulsar 2.x 兼容，但升级到 Pulsar V3 是可选的。为了提高稳定性和性能，我们建议升级到 Pulsar V3。
如果你希望使用 Pulsar V2 与 Milvus v2.5.x，请阅读
Use Pulsar V2 with Milvus v2.5.x
。
升级过程需要短暂的服务中断（通常需要几分钟到十多分钟，视数据量而定）。
操作前，需要停止所有正在运行的客户端向 Milvus 写入数据。否则，写入的数据可能会丢失。
本文假设 Milvus 安装在命名空间
default
并命名为
my-release
。在执行从本页复制的命令时，请将参数更改为自己的命名空间和发布名称。
确保您的工作环境在 Kubernetes 集群的上述命名空间下拥有权限，并安装了以下命令。
a.
kubectl
>= 1.20
b.
helm
>= 3.14.0
c.
cat
,
grep
,
awk
用于字符串操作符操作
d.
curl
或
Attu v2.4+
用于与 Milvus 管理 API 交互
路线图
升级过程包括以下步骤：
保存脉冲星中未消耗的数据。
停止 Milvus 并删除脉冲星 V2。
启动脉冲星 V3 和 Milvus。
步骤
本节提供在 Milvus 中将 Pulsar 从 V2 升级到 V3 的详细步骤。
保留 Pulsar 中未消耗的数据
在这一步中，需要确保 Pulsar 中的现有数据已持久化到对象存储服务中。 有两种方法可供选择，你可以根据自己的需要进行选择。
方法 1：使用 Attu
如果你的工作 Milvus 部署中只有少量的 Collections，且分段不多，你可以使用 Attu 将数据持久化到对象存储服务。
选择所有数据库中的每个 Collections，进入
Segments
面板，点击
Flush
按钮
Collections 的分段面板
然后在弹出窗口中再次点击
Flush
。
Attu 中的数据刷新提示
然后等到所有 Collections 的持久分段状态都是
Flushed
。
在 Attu 中查看数据刷新状态
方法 2：使用管理 API
将 Milvus 代理的 9091 端口代理到本地主机，以便进行后续操作。
kubectl -n default port-forward deploy/my-release-milvus-proxy 9091:9091 &
输出。
[
1
]
8116
Forwarding
from
127.0
.0
.1
:9091
->
9091
保存 Pid 以备日后清理。
pid=8116
触发将所有插入数据从 Pulsar 持久化到 Ojbect 存储的操作。
curl 127.0.0.1:9091/api/v1/collections \
|curl 127.0.0.1:9091/api/v1/persist -d @/dev/stdin\
|jq
'.flush_coll_segIDs'
| jq
'[.[] | .data[]]'
| jq
'{segmentIDs: (.)}'
\
> flushing_segments.json
cat
flushing_segments.json
输出。
{
"segmentIDs":
[
454097953998181000
,
454097953999383600
,
454097953998180800
]
}
检查刷新的所有段。
cat
flushing_segments.json|  curl -X GET 127.0.0.1:9091/api/v1/persist/state -d @/dev/stdin
完成后，你会看到以下输出
{
"status"
:
{
}
,
"flushed"
:
true
}
停止后台
kubectl port-forward
进程
kill
$pid
输出。
[
1
]
+
8116
terminated
kubectl
-n
default
port-forward
deploy/my-release-milvus-proxy
9091
:9091
停止 Milvus 并删除 Pulsar V2
在这一步中，需要停止 Milvus pod 并删除 Pulsar V2 部署。 有两个独立的部分可用：
针对 Milvus Helm 用户
如果使用 Milvus Helm 图表安装了 Milvus，请转到
使用 Helm 删除 Pulsar V2
。
针对 Milvus 操作符用户
如果您使用 Milvus 操作符安装了 Milvus，请转到
使用 Milvus 操作符删除 Pulsar V2
。
使用 Helm 删除 Pulsar V2
如果使用 Milvus Helm 图表安装了 Milvus，请按照以下步骤停止 Milvus pod 并删除 Pulsar V2 部署。
将当前 Milvus 发布值保存到
values.yaml
，以便以后恢复。
helm -n default get values my-release -o yaml > values.yaml
cat
values.yaml
使用命令停止 Milvus 和所有依赖项。不用担心数据卷，它们将被默认保留。
helm -n default uninstall my-release
输出
These resources were kept due to the resource policy:
[PersistentVolumeClaim] my-release-minio

release
"my-release"
uninstalled
需要清除脉冲星 PVC 和 PV 列表（持久卷索赔和持久卷
kubectl -n default get pvc -lapp=pulsar,release=my-release |grep -v NAME |awk
'{print $1}'
> pulsar-pvcs.txt
kubectl -n default get pvc -lapp=pulsar,release=my-release -o custom-columns=VOL:.spec.volumeName|grep -v VOL > pulsar-pvs.txt
echo
"Volume Claims:"
cat
pulsar-pvcs.txt
echo
"Volumes:"
cat
pulsar-pvs.txt
输出
Volume
Claims:
my-release-pulsar-bookie-journal-my-release-pulsar-bookie-0
my-release-pulsar-bookie-journal-my-release-pulsar-bookie-1
my-release-pulsar-bookie-ledgers-my-release-pulsar-bookie-0
my-release-pulsar-bookie-ledgers-my-release-pulsar-bookie-1
my-release-pulsar-zookeeper-data-my-release-pulsar-zookeeper-0
Volumes:
pvc-f590a4de-df31-4ca8-a424-007eac3c619a
pvc-17b0e215-3e14-4d14-901e-1a1dda9ff5a3
pvc-72f83c25-6ea1-45ee-9559-0b783f2c530b
pvc-60dcb6e4-760d-46c7-af1a-d1fc153b0caf
pvc-2da33f64-c053-42b9-bb72-c5d50779aa0a
检查
pulsar-pvcs.txt
的 PVC 列表是否都是 Pulsar 的。确认无误后，删除 PVC。
cat
pulsar-pvcs.txt |xargs -I {} kubectl -n default delete pvc {} --
wait
=
false
输出。
persistentvolumeclaim
"my-release-pulsar-bookie-journal-my-release-pulsar-bookie-0"
deleted
persistentvolumeclaim
"my-release-pulsar-bookie-journal-my-release-pulsar-bookie-1"
deleted
persistentvolumeclaim
"my-release-pulsar-bookie-ledgers-my-release-pulsar-bookie-0"
deleted
persistentvolumeclaim
"my-release-pulsar-bookie-ledgers-my-release-pulsar-bookie-1"
deleted
persistentvolumeclaim
"my-release-pulsar-zookeeper-data-my-release-pulsar-zookeeper-0"
deleted
(可选）根据提供 PVC 的存储类别，您可能还需要手动删除 PV。
cat
pulsar-pvs.txt
|xargs
-I
{}
kubectl
-n
default
delete
pvc
{}
--wait=false
如果输出 NotFound 错误也没关系。它已被 kubernetes 控制器删除。
Error from server (NotFound):
persistentvolumeclaims
"pvc-f590a4de-df31-4ca8-a424-007eac3c619a"
not
found
Error from server (NotFound):
persistentvolumeclaims
"pvc-17b0e215-3e14-4d14-901e-1a1dda9ff5a3"
not
found
Error from server (NotFound):
persistentvolumeclaims
"pvc-72f83c25-6ea1-45ee-9559-0b783f2c530b"
not
found
Error from server (NotFound):
persistentvolumeclaims
"pvc-60dcb6e4-760d-46c7-af1a-d1fc153b0caf"
not
found
Error from server (NotFound):
persistentvolumeclaims
"pvc-2da33f64-c053-42b9-bb72-c5d50779aa0a"
not
found
使用 Milvus 操作符删除 Pulsar V2
如果使用 Milvus 操作符安装了 Milvus，请按照以下步骤停止 Milvus pod 并删除 Pulsar V2 部署。
将当前 Milvus Manifest 保存到
milvus.yaml
以备后用。
kubectl -n default get milvus my-release -o yaml > milvus.yaml
head
milvus.yaml -n 20
输出。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
annotations:
milvus.io/dependency-values-merged:
"true"
milvus.io/pod-service-label-added:
"true"
milvus.io/querynode-current-group-id:
"0"
creationTimestamp:
"2024-11-22T08:06:59Z"
finalizers:
-
milvus.milvus.io/finalizer
generation:
3
labels:
app:
milvus
milvus.io/operator-version:
1.1
.2
name:
my-release
namespace:
default
resourceVersion:
"692217324"
uid:
7a469ed0-9df1-494e-bd9a-340fac4305b5
spec:
components:
创建包含以下内容的
patch.yaml
文件。
# a patch to retain etcd & storage data and delete pulsar data while delete milvus
spec:
dependencies:
etcd:
inCluster:
deletionPolicy:
Retain
pvcDeletion:
false
storage:
inCluster:
deletionPolicy:
Retain
pvcDeletion:
false
pulsar:
inCluster:
deletionPolicy:
Delete
pvcDeletion:
true
使用
kubectl patch
保留 etcd 和存储数据，并在删除 milvus 的同时删除脉冲星数据。
kubectl
-n
default
patch
milvus
my-release
--patch-file
patch.yaml
--type=merge
输出： 停止 Milvus 并删除脉冲星数据。
milvus.milvus.io/my-release patched
停止 Milvus 并删除脉冲星 V2。不用担心 etcd 和对象存储数据卷，它们将被默认保留。
kubectl -n default delete milvus my-release --
wait
=
false
kubectl -n default get milvus my-release
kubectl -n default delete milvus my-release --
wait
=
true
输出结果注意，milvus 优雅停止和操作符删除 pulsar 卷可能需要几分钟时间。
milvus.milvus.io
"my-release"
deleted
NAME         MODE      STATUS     UPDATED   AGE
my-release   cluster   Deleting   True      41m
milvus.milvus.io
"my-release"
deleted
等待命令完成。
再次检查 Milvus 资源是否已消失
kubectl
-n
default
get
milvus
my-release
输出应该如下
No
resources
found
in
default
namespace.
启动 Pulsar V3 和 Milvus
在这一步中，你需要启动 Pulsar V3 和 Milvus pod。 这里有两个独立的部分：
针对 Helm 用户
如果您使用 Milvus Helm 图表安装了 Milvus，请转至
For Helm User
。
针对 Milvus 操作符用户
如果您已经使用 Milvus 操作符安装了 Milvus，请进入
For Milvus Operator 用户
。
启动 Pulsar V3 并使用 Helm
编辑上一步保存的
values.yaml
。
# change the following:
pulsar:
enabled:
false
# set to false
# you may also clean up rest fields under pulsar field
# it's ok to keep them though.
pulsarv3:
enabled:
true
# append other values for pulsar v3 chart if needs
更新本地 Helm repo
helm repo add zilliztech https://zilliztech.github.io/milvus-helm
helm repo update zilliztech
输出
"zilliztech"
already exists with the same configuration, skipping
Hang tight
while
we grab the latest from your chart repositories...
...Successfully got an update from the
"zilliztech"
chart repository
Update Complete. ⎈Happy Helming!⎈
使用编辑后的
values.yaml
，用最新的 Helm 图表版本安装你的 milvus 版本。
helm -n default install my-release zilliztech/milvus --reset-values -f values.yaml
输出
NAME: my-release
LAST DEPLOYED: Fri Nov 22 15:31:27 2024
NAMESPACE: default
STATUS: deployed
REVISION: 1
TEST SUITE: None
通过
kubectl -n default get pods
检查 pod 是否都已调度和运行。
所有 pod 启动可能需要几分钟时间。
输出如下。
NAME                                          READY   STATUS      RESTARTS   AGE
my-release-etcd-0                             1/1     Running     0          4m3s
my-release-milvus-datanode-56487bc4bc-s6mbd   1/1     Running     0          4m5s
my-release-milvus-indexnode-6476894d6-rv85d   1/1     Running     0          4m5s
my-release-milvus-mixcoord-6d8875cb9c-67fcq   1/1     Running     0          4m4s
my-release-milvus-proxy-7bc45d57c5-2qf8m      1/1     Running     0          4m4s
my-release-milvus-querynode-77465747b-kt7f4   1/1     Running     0          4m4s
my-release-minio-684ff4f5df-pnc97             1/1     Running     0          4m5s
my-release-pulsarv3-bookie-0                  1/1     Running     0          4m3s
my-release-pulsarv3-bookie-1                  1/1     Running     0          4m3s
my-release-pulsarv3-bookie-2                  1/1     Running     0          4m3s
my-release-pulsarv3-bookie-init-6z4tk         0/1     Completed   0          4m1s
my-release-pulsarv3-broker-0                  1/1     Running     0          4m2s
my-release-pulsarv3-broker-1                  1/1     Running     0          4m2s
my-release-pulsarv3-proxy-0                   1/1     Running     0          4m2s
my-release-pulsarv3-proxy-1                   1/1     Running     0          4m2s
my-release-pulsarv3-pulsar-init-wvqpc         0/1     Completed   0          4m1s
my-release-pulsarv3-recovery-0                1/1     Running     0          4m3s
my-release-pulsarv3-zookeeper-0               1/1     Running     0          4m2s
my-release-pulsarv3-zookeeper-1               1/1     Running     0          4m2s
my-release-pulsarv3-zookeeper-2               1/1     Running     0          4m2s
启动 Pulsar V3 并使用 Milvus 操作符
编辑上一步保存的
milvus.yaml
。
# change the followings fields:
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
annotations:
null
# this field should be removed or set to null
resourceVersion:
null
# this field should be removed or set to null
uid:
null
# this field should be removed or set to null
spec:
dependencies:
pulsar:
inCluster:
chartVersion:
pulsar-v3
# delete all previous values for pulsar v2 and set it to null.
# you may add additional values here for pulsar v3 if you're sure about it.
values:
null
确保您的 Milvus 操作符已升级到 v1.1.2 或更高版本。
helm
repo
add
milvus-operator
https://zilliztech.github.io/milvus-operator
helm
repo
update
milvus-operator
helm
-n
milvus-operator
upgrade
milvus-operator
milvus-operator/milvus-operator
使用命令用脉冲星 V3 启动 Milvus
kubectl
create
-f
milvus.yaml
输出
milvus.milvus.io/my-release
created
检查 pod，查看是否所有 pod 都已调度并运行
kubectl -n default get pods
。
所有 pod 启动可能需要几分钟时间。
输出如下
NAME
READY
STATUS
RESTARTS
AGE
my-release-etcd-0
1
/1
Running
0
65m
my-release-milvus-datanode-57fd59ff58-5mdrk
1
/1
Running
0
93s
my-release-milvus-indexnode-67867c6b9b-4wsbw
1
/1
Running
0
93s
my-release-milvus-mixcoord-797849f9bb-sf8z5
1
/1
Running
0
93s
my-release-milvus-proxy-5d5bf98445-c55m6
1
/1
Running
0
93s
my-release-milvus-querynode-0-64797f5c9-lw4rh
1
/1
Running
0
92s
my-release-minio-79476ccb49-zvt2h
1
/1
Running
0
65m
my-release-pulsar-bookie-0
1
/1
Running
0
5m10s
my-release-pulsar-bookie-1
1
/1
Running
0
5m10s
my-release-pulsar-bookie-2
1
/1
Running
0
5m10s
my-release-pulsar-bookie-init-v8fdj
0
/1
Completed
0
5m11s
my-release-pulsar-broker-0
1
/1
Running
0
5m11s
my-release-pulsar-broker-1
1
/1
Running
0
5m10s
my-release-pulsar-proxy-0
1
/1
Running
0
5m11s
my-release-pulsar-proxy-1
1
/1
Running
0
5m10s
my-release-pulsar-pulsar-init-5lhx7
0
/1
Completed
0
5m11s
my-release-pulsar-recovery-0
1
/1
Running
0
5m11s
my-release-pulsar-zookeeper-0
1
/1
Running
0
5m11s
my-release-pulsar-zookeeper-1
1
/1
Running
0
5m10s
my-release-pulsar-zookeeper-2
1
/1
Running
0
5m10s