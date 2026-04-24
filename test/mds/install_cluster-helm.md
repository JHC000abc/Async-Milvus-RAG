使用 Helm 在 Kubernetes 中运行 Milvus
本页说明如何使用
Milvus Helm 图表
在 Kubernetes 中启动 Milvus 实例。
概述
Helm 使用一种称为图表的打包格式。图表是描述一组相关 Kubernetes 资源的文件 Collections。Milvus 提供了一组图表，可帮助您部署 Milvus 依赖项和组件。
前提条件
安装 Helm CLI
。
创建 K8s 集群
。
安装
StorageClass
。您可以按以下步骤检查已安装的 StorageClass。
$ kubectl get sc

NAME                  PROVISIONER                  RECLAIMPOLICY    VOLUMEBIINDINGMODE    ALLOWVOLUMEEXPANSION     AGE
standard (default)    k8s.io/minikube-hostpath     Delete           Immediate
false
安装前检查
硬件和软件要求
。
安装 Milvus 之前，建议使用
Milvus 大小工具
，根据数据大小估算硬件需求。这有助于确保 Milvus 安装的最佳性能和资源分配。
如果您在绘制图像时遇到任何问题，请通过
community@zilliz.com
联系我们，并提供有关问题的详细信息，我们将为您提供必要的支持。
安装 Milvus Helm 图表
在安装 Milvus Helm 图表之前，您需要添加 Milvus Helm 资源库。
helm repo add zilliztech https://zilliztech.github.io/milvus-helm/
位于
https://github.com/milvus-io/milvus-helm
的 Milvus Helm Charts 软件仓库已经归档。我们现在使用
https://github.com/zilliztech/milvus-helm
上的新版本库。存档版本库仍可用于 4.0.31 之前的图表，但以后的版本则使用新版本库。
然后按如下方法从版本库中获取 Milvus 图表：
$
helm repo update
你可以随时运行此命令获取最新的 Milvus Helm 图表。
在线安装
1.部署 Milvus 集群
安装好 Helm 图表后，就可以在 Kubernetes 上启动 Milvus 了。本节将指导你部署一个 Milvus 集群。
需要独立部署？
如果你更喜欢以独立模式（单节点）部署 Milvus 以进行开发或测试，请使用此命令：
helm install my-release zilliztech/milvus \
  --
set
image.all.tag=v2.6.13 \
  --
set
cluster.enabled=
false
\
  --
set
pulsarv3.enabled=
false
\
  --
set
standalone.messageQueue=woodpecker \
  --
set
woodpecker.enabled=
true
\
  --
set
streaming.enabled=
true
注意
：独立模式使用 Woodpecker 作为默认消息队列，并启用流节点组件。有关详情，请参阅
架构概述
和
使用 Woodpecker
。
部署 Milvus 集群：
以下命令使用 Woodpecker 作为推荐的消息队列，以针对 v2.6.13 的优化设置部署 Milvus 群集：
helm install my-release zilliztech/milvus \
  --
set
image.all.tag=v2.6.13 \
  --
set
pulsarv3.enabled=
false
\
  --
set
woodpecker.enabled=
true
\
  --
set
streaming.enabled=
true
\
  --
set
indexNode.enabled=
false
此命令的作用：
使用
Woodpecker
作为消息队列（建议使用，以减少维护工作）
启用新的
流节点
组件以提高性能
禁用传统的
索引节点
（其功能现在由数据节点处理）
禁用 Pulsar，改用 Woodpecker
Milvus 2.6.x 中的架构变更：
消息队列
：现在推荐使用
Woodpecker
（与 Pulsar 相比，减少了基础设施维护工作）
新组件
：引入
流节点
并默认启用
合并组件
：
索引节点
和
数据节点
合并为一个
数据节点
有关完整架构的详细信息，请参阅
架构概述
。
其他消息队列选项：
如果你更喜欢使用
Pulsar
（传统选择）而不是 Woodpecker：
helm install my-release zilliztech/milvus \
  --
set
image.all.tag=v2.6.13 \
  --
set
streaming.enabled=
true
\
  --
set
indexNode.enabled=
false
下一步：
上述命令以推荐配置部署 Milvus。用于生产：
使用
Milvus 大小工具
，根据数据大小优化设置
查看
Milvus 系统配置清单
，了解高级配置选项
重要说明：
版本命名
：仅使用字母、数字和破折号（不允许使用点）
Kubernetes v1.25+
：如果遇到 PodDisruptionBudget 问题，请使用此解决方法：
helm install my-release zilliztech/milvus \
  --
set
pulsar.bookkeeper.pdb.usePolicy=
false
\
  --
set
pulsar.broker.pdb.usePolicy=
false
\
  --
set
pulsar.proxy.pdb.usePolicy=
false
\
  --
set
pulsar.zookeeper.pdb.usePolicy=
false
有关详细信息，请参阅
Milvus Helm Chart
和
Helm 文档
。
2.检查 Milvus 群集状态
通过检查 pod 状态验证部署是否成功：
kubectl get pods
等待所有 pod 显示 "正在运行 "状态。
在 v2.6.13 配置下，您应该能看到类似以下的 pod：
NAME                                             READY  STATUS   RESTARTS  AGE
my
-
release
-
etcd
-0
1
/
1
Running
0
3
m23s
my
-
release
-
etcd
-1
1
/
1
Running
0
3
m23s
my
-
release
-
etcd
-2
1
/
1
Running
0
3
m23s
my
-
release
-
milvus
-
datanode
-68
cb87dcbd
-4
khpm
1
/
1
Running
0
3
m23s
my
-
release
-
milvus
-
mixcoord
-7
fb9488465
-
dmbbj
1
/
1
Running
0
3
m23s
my
-
release
-
milvus
-
proxy
-6
bd7f5587
-
ds2xv
1
/
1
Running
0
3
m24s
my
-
release
-
milvus
-
querynode
-5
cd8fff495
-
k6gtg
1
/
1
Running
0
3
m24s
my
-
release
-
milvus
-
streaming
-
node
-
xxxxxxxxx
1
/
1
Running
0
3
m24s
my
-
release
-
minio
-0
1
/
1
Running
0
3
m23s
my
-
release
-
minio
-1
1
/
1
Running
0
3
m23s
my
-
release
-
minio
-2
1
/
1
Running
0
3
m23s
my
-
release
-
minio
-3
1
/
1
Running
0
3
m23s
my
-
release
-
pulsar
-
autorecovery
-86
f5dbdf77
-
lchpc
1
/
1
Running
0
3
m24s
my
-
release
-
pulsar
-
bookkeeper
-0
1
/
1
Running
0
3
m23s
my
-
release
-
pulsar
-
bookkeeper
-1
1
/
1
Running
0
98
s
my
-
release
-
pulsar
-
broker
-556
ff89d4c
-2
m29m
1
/
1
Running
0
3
m23s
my
-
release
-
pulsar
-
proxy
-6
fbd75db75
-
nhg4v
1
/
1
Running
0
3
m23s
my
-
release
-
pulsar
-
zookeeper
-0
1
/
1
Running
0
3
m23s
my
-
release
-
pulsar
-
zookeeper
-
metadata
-98
zbr
0
/
1
Completed
0
3
m24s
需要验证的关键组件：
Milvus 组件
：
mixcoord
,
datanode
,
querynode
,
proxy
、
streaming-node
依赖关系
：
etcd
（元数据）、
minio
（对象存储）、
pulsar
（消息队列）
端口转发设置完成后，还可以通过
http://127.0.0.1:9091/webui/
访问
Milvus WebUI
（见下一步）。详情请参阅
Milvus WebUI
。
3.连接到 Milvus
要从 Kubernetes 外部连接到 Milvus 集群，需要设置端口转发。
设置端口转发：
kubectl port-forward service/my-release-milvus 27017:19530
此命令会将本地端口
27017
转发到 Milvus 端口
19530
。你应该看到
Forwarding
from
127.0.0.1:27017
->
19530
连接详情：
本地连接
：
localhost:27017
Milvus 默认端口
：
19530
端口转发选项：
自动分配本地端口
：使用
:19530
而不是
27017:19530
让 kubectl 选择可用端口
监听所有接口
：添加
--address 0.0.0.0
以允许来自其他机器的连接：
kubectl port-forward --address 0.0.0.0 service/my-release-milvus 27017:19530
独立部署
：如果使用独立模式，服务名称保持不变
使用 Milvus 时
保持打开此终端
。现在可以使用任何 Milvus SDK 连接到 Milvus，网址是
localhost:27017
。
(可选）更新 Milvus 配置
您可以通过编辑
values.yaml
文件并再次应用来更新 Milvus 集群的配置。
创建一个包含所需配置的
values.yaml
文件。
以下假设您要启用
proxy.http
。
extraConfigFiles:
user.yaml:
|+
    proxy:
      http:
        enabled: true
有关适用的配置项，请参阅
系统配置
。
应用
values.yaml
文件。
helm upgrade my-release zilliztech/milvus --namespace my-namespace -f values.yaml
检查更新的配置。
helm get values my-release
输出应显示更新的配置。
访问 Milvus WebUI
Milvus 随附一个名为 Milvus WebUI 的内置图形用户界面工具，可通过浏览器访问。Milvus Web UI 采用简单直观的界面，增强了系统的可观察性。你可以使用 Milvus Web UI 观察 Milvus 组件和依赖关系的统计和指标，检查数据库和 Collections 的详细信息，并列出详细的 Milvus 配置。有关 Milvus Web UI 的详细信息，请参阅
Milvus WebUI
。
要启用对 Milvus Web UI 的访问，需要将代理 pod 的端口转发到本地端口。
$
kubectl port-forward --address 0.0.0.0 service/my-release-milvus 27018:9091
Forwarding from 0.0.0.0:27018 -> 9091
现在，你可以通过
http://localhost:27018
访问 Milvus Web UI。
离线安装
如果您处于网络受限的环境，请按照本节的步骤启动 Milvus 集群。
1.获取 Milvus 清单
运行以下命令获取 Milvus 清单。
$
helm template my-release zilliztech/milvus > milvus_manifest.yaml
上述命令会渲染 Milvus 群集的图表模板，并将输出保存到名为
milvus_manifest.yaml
的清单文件中。使用此清单，你可以在单独的 pod 中安装 Milvus 群集及其组件和依赖项。
要在独立模式下安装 Milvus 实例（所有 Milvus 组件都包含在一个 pod 中），应改成运行
helm template my-release --set cluster.enabled=false --set etcd.replicaCount=1 --set minio.mode=standalone --set pulsarv3.enabled=false zilliztech/milvus > milvus_manifest.yaml
，为独立模式下的 Milvus 实例渲染图表模板。
要更改 Milvus 配置，请下载
value.yaml
模板，将所需设置放入其中，然后使用
helm template -f values.yaml my-release zilliztech/milvus > milvus_manifest.yaml
渲染相应的清单。
2.下载图像拉取脚本
图像提取脚本是用 Python 开发的。您应在
requirement.txt
文件中下载脚本及其依赖项。
$
wget https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/offline/requirements.txt
$
wget https://raw.githubusercontent.com/milvus-io/milvus/master/deployments/offline/save_image.py
3.提取并保存图像
运行以下命令提取并保存所需的图像。
$
pip3 install -r requirements.txt
$
python3 save_image.py --manifest milvus_manifest.yaml
图像会被提取到当前目录下名为
images
的子文件夹中。
4.加载图像
现在，您可以在网络受限环境中将图像加载到主机上，具体操作如下：
$
for
image
in
$(find . -
type
f -name
"*.tar.gz"
) ;
do
gunzip -c
$image
| docker load;
done
5.部署 Milvus
$
kubectl apply -f milvus_manifest.yaml
到此为止，你可以按照在线安装的步骤
2
和
3
检查群集状态，并将本地端口转发给 Milvus。
升级运行中的 Milvus 群集
运行以下命令将正在运行的 Milvus 群集升级到最新版本：
$
helm repo update
$
helm upgrade my-release zilliztech/milvus --reset-then-reuse-values
卸载 Milvus
运行以下命令卸载 Milvus。
$ helm uninstall my-release
下一步
在 Docker 中安装 Milvus 后，你可以
查看
Hello Milvus
，了解 Milvus 的功能。
了解 Milvus 的基本操作：
管理数据库
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
使用 Helm 图表升级 Milvus
。
扩展你的 Milvus 集群
。
在云上部署你的 Milvus 集群：
亚马逊 EKS
谷歌云
微软 Azure
探索
Milvus WebUI
，一个用于 Milvus 可观察性和管理的直观 Web 界面。
探索
Milvus 备份
，一个用于 Milvus 数据备份的开源工具。
探索
Birdwatcher
，用于调试 Milvus 和动态配置更新的开源工具。
探索
Attu
，一个用于直观管理 Milvus 的开源图形用户界面工具。
使用 Prometheus 监控 Milvus
。