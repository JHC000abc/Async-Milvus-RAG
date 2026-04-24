在 OpenShift 上部署 Milvus 群集
本主题将逐步介绍如何在 OpenShift 上部署 Milvus。
先决条件
在开始部署过程之前，请确保您拥有
运行中的 OpenShift 群集。
具有足够权限的 OpenShift 群集访问权限（
cluster-admin
角色或同等权限）。
访问 OpenShift 容器平台 Web 控制台。
第 1 步：安装 Cert Manager
管理 Milvus Operator 的 TLS 证书需要 Cert Manager。
为您的 OpenShift 版本查找合适的 Cert 管理器版本：
Cert Manager Releases
。
按照官方指南安装 Cert Manager：
安装证书管理器
。
验证证书管理器是否正常工作：
在 openshift 控制台中，导航至
Workloads
>
Pods
。选择项目
cert-manager
。
cert-manager-1
确保所有 pod 已准备就绪。例如，下图显示 pod 仍在启动中。请等待所有 pod 准备就绪。
证书管理器-2
步骤 2：为 Milvus Operator 签发自签名证书
确保以
kubeadmin
或同等权限登录。
创建以下名为
milvus-operator-certificate.yaml
的清单文件：
# milvus-operator-certificate.yaml
apiVersion:
cert-manager.io/v1
kind:
Certificate
metadata:
name:
milvus-operator-serving-cert
namespace:
milvus-operator
spec:
dnsNames:
-
milvus-operator-webhook-service.milvus-operator.svc
-
milvus-operator-webhook-service.milvus-operator.svc.cluster.local
issuerRef:
kind:
Issuer
name:
milvus-operator-selfsigned-issuer
secretName:
milvus-operator-webhook-cert
---
apiVersion:
cert-manager.io/v1
kind:
Issuer
metadata:
name:
milvus-operator-selfsigned-issuer
namespace:
milvus-operator
spec:
selfSigned:
{}
应用该文件：
kubectl apply -f milvus-operator-certificate.yaml
第 3 步：安装 Milvus 操作符
现在可以开始安装 Milvus Operator。建议使用 Helm 安装 Milvus Operator，以简化配置过程。
添加 Milvus Operator Helm 资源库：
helm repo add milvus-operator https://zilliztech.github.io/milvus-operator/
helm repo update milvus-operator
安装 Milvus Operator：
helm -n milvus-operator upgrade --install --create-namespace milvus-operator milvus-operator/milvus-operator
第 4 步：部署 Milvus
按照 Milvus 文档网站上的其余指南进行操作：
部署 Milvus
。
下一步
如果你想了解如何在其他云上部署 Milvus：
使用 Kubernetes 在 AWS 上部署 Milvus 群集
使用 Kubernetes 在 Azure 上部署 Milvus 群集
使用 Kubernetes 在 GCP 上部署 Milvus 群集