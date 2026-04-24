使用 AKS 在 Azure 上部署 Milvus
本主题介绍如何使用
Azure Kubernetes 服务
（AKS）和
Azure 门户
调配和创建集群。
前提条件
确保已正确设置 Azure 项目，并且可以访问要使用的资源。如果不确定访问权限，请联系管理员。
软件要求
Azure CLI
kubectl
Helm
或者，也可以使用预装了 Azure CLI、kubectl 和 Helm 的
Cloud Shell
。
安装 Azure CLI 后，确保已正确验证。
配置 Kubernetes 集群
登录 Azure 门户。
在 Azure 门户菜单或
主页上
，选择
创建资源
。
选择
容器
>
Kubernetes 服务
。
在 "
基础知识 "
页面上，配置以下选项：
项目详细信息
：
订阅
：请联系您组织的 Azure 管理员，以确定应该使用哪个订阅。
资源组
：请联系企业的 Azure 管理员，以确定应使用哪个资源组。
群集详细信息
：
Kubernetes 群集名称
：输入群集名称。
区域
：选择一个区域。
可用性区域
：根据需要选择
可用性区域
。对于生产集群，我们建议您选择多个可用性区域。
主节点池
：
节点大小
：建议选择内存至少为 16 GB 的虚拟机，但也可根据需要选择虚拟机大小。
扩展方法
：选择扩展方式。
节点数范围
：选择节点数范围。
节点池
：
启用虚拟节点
：选择复选框以启用虚拟节点。
启用虚拟机规模集
：建议选择
enabled
。
网络连接
：
网络配置
：建议选择
Kubenet
。
DNS 名称前缀
：输入 DNS 名称前缀。
流量路由
：
负载平衡器
：
Standard
。
HTTP 应用程序路由
：不需要。
配置选项后，单击
审查 + 创建
，验证完成后再单击
创建
。创建群集需要几分钟时间。
连接到群集
导航到在 Kubernetes 服务中创建的群集并单击它。
在左侧导航窗格中，单击
Overview
。
在出现的 "
概览 "
页面上，单击 "
连接 "
查看资源组和订阅。
设置订阅和凭据
您可以使用 Azure Cloud Shell 执行以下步骤。
运行以下命令设置订阅。
az account set --subscription EXAMPLE-SUBSCRIPTION-ID
运行以下命令下载凭据并配置 Kubernetes CLI 以使用它们。
az aks get-credentials --resource-group YOUR-RESOURCE-GROUP --name YOUR-CLUSTER-NAME
使用相同的 shell 执行以下步骤。如果切换到另一个 shell，请重新运行前面的命令。
将 Azure Blob Storage 用作外部对象存储
Azure Blob Storage 是 AWS Simple Storage Service (S3) 的 Azure 版本。
创建存储账户和容器
az storage account create -n milvustesting1 -g MyResourceGroup -l eastus --sku Standard_LRS --min-tls-version TLS1_2
az storage container create -n testmilvus --account-name milvustesting1
获取秘钥，使用第一个值
az storage account keys list --account-name milvustesting2
添加 values.yaml
cluster:
enabled:
true
service:
type:
LoadBalancer
extraConfigFiles:
user.yaml:
|+
    common:
      storageType: remote
minio:
enabled:
false
externalS3:
enabled:
true
host:
core.windows.net
port:
443
rootPath:
my-release
bucketName:
testmilvus
# the storage account container name
cloudProvider:
azure
useSSL:
true
accessKey:
"milvustesting1"
# the storage account name
secretKey:
"<secret-key>"
部署 Milvus
现在 Kubernetes 集群已经准备就绪。让我们马上部署 Milvus。
helm repo add milvus https://zilliztech.github.io/milvus-helm/
helm repo update
helm install -f values.yaml my-release milvus/milvus
在前面的命令中，我们在本地添加 Milvus Helm 图表的 repo，并更新 repo 以获取最新图表。然后，我们安装一个 Milvus 实例，并将其命名为
my-release
。
注意配置
service.type
的值，它表明我们希望通过第 4 层负载平衡器暴露 Milvus 实例。
验证部署
所有 pod 运行后，运行以下命令获取外部 IP 地址。
kubectl get services|grep my-release-milvus|grep LoadBalancer|awk
'{print $4}'
你好 Milvus
请参考
Hello Milvus
，将 host 值更改为外部 IP 地址，然后运行代码。
下一步
如果你想了解如何在其他云上部署 Milvus：
使用 Kubernetes 在 AWS 上部署 Milvus 群集
使用 Kubernetes 在 GCP 上部署 Milvus 群集