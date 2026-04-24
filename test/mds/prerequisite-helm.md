在 Kubernetes 上运行 Milvus 的要求
本页列出了启动和运行 Milvus 所需的硬件和软件要求。
硬件要求
组件
要求
建议
备注
中央处理器
英特尔第二代酷睿处理器或更高版本
苹果硅
独立：4 核或更高
集群：8 核或更多
CPU 指令集
SSE4.2
AVX
AVX2
AVX-512
SSE4.2
AVX
AVX2
AVX-512
Milvus 中的向量相似性搜索和索引建立需要 CPU 支持单指令、多数据（SIMD）扩展集。确保 CPU 至少支持所列 SIMD 扩展之一。更多信息，请参阅
带 AVX 的 CPU
。
内存
单机：8G
集群：32G
单机：16G
集群： 128G128G
内存大小取决于数据量。
硬盘
SATA 3.0 固态硬盘或 CloudStorage
NVMe SSD 或更高版本
硬盘大小取决于数据量。
软件要求
建议在 Linux 平台上运行 Kubernetes 集群。
kubectl 是 Kubernetes 的命令行工具。使用的 kubectl 版本应与群集的版本相差一个小版本。使用最新版本的 kubectl 有助于避免不可预见的问题。
本地运行 Kubernetes 集群时需要 minikube。确保在使用 Helm 安装 Milvus 之前安装 Docker。更多信息，请参阅
获取 Docker
。
操作符
软件
注意
Linux 平台
Kubernetes 1.16 或更高版本
kubectl
Helm 3.0.0 或更高版本
minikube（适用于 Milvus 单机版）
Docker 19.03 或更高版本（适用于 Milvus 单机版）
更多信息，请参阅
Helm 文档
。
软件
版本
备注
etcd
3.5.0
请参阅
其他磁盘要求
。
MinIO
RELEASE.2024-12-18T13-15-44Z
脉冲星
2.8.2
其他磁盘要求
磁盘性能对 etcd 至关重要。强烈建议使用本地 NVMe SSD。较慢的磁盘响应速度可能会导致频繁的群集选举，最终降低 etcd 服务的性能。
要测试磁盘是否合格，请使用
fio
。
mkdir
test-data
fio --rw=write --ioengine=
sync
--fdatasync=1 --directory=test-data --size=2200m --bs=2300 --name=mytest
理想情况下，磁盘应达到 500 IOPS 以上，第 99 百分位数 fsync 延迟应低于 10 毫秒。请阅读 etcd
文档
了解更多详细要求。
常见问题
如何在本地启动 K8s 集群进行测试？
你可以使用
minikube
、
kind
和
Kubeadm
等工具在本地快速建立 Kubernetes 集群。下面的步骤以 minikube 为例。
下载 minikube
转到 "
开始
"页面，检查是否满足 "
你需要什么 "
部分列出的条件，点击描述目标平台的按钮，然后复制命令下载并安装二进制文件。
使用 minikube 启动 K8s 集群
$
minikube start
检查 K8s 群集的状态
您可以使用以下命令检查已安装的 K8s 群集的状态。
$
kubectl cluster-info
确保可以通过
kubectl
访问 K8s 群集。如果您尚未在本地安装
kubectl
，请参阅
在 minikube 内使用 kubectl
。
下一步
如果你的硬件和软件符合要求，你就可以
使用 Milvus Operator 在 Kubernets 中操作 Milvus
使用 Helm 在 Kubernetes 中运行 Milvus
有关安装 Milvus 时可设置的参数，请参阅
系统配置
。