安装支持 GPU 的 Milvus 的要求
本页列出了设置支持 GPU 的 Milvus 的硬件和软件要求。
计算能力
GPU 设备的计算能力必须是下列之一：6.0, 7.0, 7.5, 8.0, 8.6, 9.0.
要检查您的 GPU 设备是否满足要求，请在英伟达™（NVIDIA®）开发人员网站上查看 "
您的 GPU 计算能力
"。
英伟达驱动程序
用于 GPU 设备的英伟达
™
（NVIDIA®）驱动程序必须安装在某个
受支持的 Linux 发行版
上，并已按照
本指南
安装了英伟达™（NVIDIA®）容器工具包。
对于 Ubuntu 22.04 用户，可以使用以下命令安装驱动程序和容器工具包：
$
sudo
apt install --no-install-recommends nvidia-headless-545 nvidia-utils-545
其他操作系统用户请参考
官方安装指南
。
运行以下命令可检查驱动程序是否已正确安装：
$
modinfo nvidia | grep
"^version"
version:        545.29.06
建议使用 545 及以上版本的驱动程序。
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
访问 K8s 群集。如果本地未安装
kubectl
，请参阅在
minikube 内使用 kubectl
。
如何使用 GPU 工作节点启动 K8s 群集？
如果你喜欢使用支持 GPU 的工作节点，可以按照以下步骤创建一个带有 GPU 工作节点的 K8s 集群。我们建议在带有 GPU 工作节点的 K8s 集群上安装 Milvus，并使用默认配置的存储类。
准备 GPU 工作节点
要使用支持 GPU 的工作节点，请按照
准备 GPU 节点
中的步骤操作。
在 K8s 上启用 GPU 支持
按照
以下步骤
使用 Helm 部署
nvidia-device-plugin
。
设置完成后，使用以下命令查看 GPU 资源。将
<gpu-worker-node>
替换为实际节点名称。
$
kubectl describe node <gpu-worker-node>
Capacity:
  ...
  nvidia.com/gpu:     4
  ...
  Allocatable:
  ...
  nvidia.com/gpu:     4
  ...
  ```