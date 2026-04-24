使用 Milvus 配置 ingress nginx
本主题介绍如何使用 Milvus 配置 ingress nginx。 更多详情，请参阅
ingress-nginx
。
配置 ingress nginx
设置环境
export
DNS_LABEL=
"milvustest"
# Your DNS label must be unique within its Azure location.
export
NAMESPACE=
"ingress-basic"
安装 ingress nginx
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx \
    --create-namespace \
    --namespace
$NAMESPACE
\
    --
set
controller.service.annotations.
"service\.beta\.kubernetes\.io/azure-dns-label-name"
=
$DNS_LABEL
\  
    --
set
controller.service.annotations.
"service\.beta\.kubernetes\.io/azure-load-balancer-health-probe-request-path"
=/healthz
获取外部IP地址
kubectl --namespace
$NAMESPACE
get services -o wide -w ingress-nginx-controller
为入口控制器配置 FQDN。
# Public IP address of your ingress controller
IP=
"MY_EXTERNAL_IP"
# Get the resource-id of the public IP
PUBLICIPID=$(az network public-ip list --query
"[?ipAddress!=null]|[?contains(ipAddress, '
$IP
')].[id]"
--output tsv)
# Update public IP address with DNS name
az network public-ip update --ids
$PUBLICIPID
--dns-name
$DNS_LABEL
# Display the FQDN
az network public-ip show --ids
$PUBLICIPID
--query
"[dnsSettings.fqdn]"
--output tsv
# sample output: milvustest.eastus2.cloudapp.azure.com
安装证书管理器
helm repo add jetstack https://charts.jetstack.io
helm repo update
helm install cert-manager jetstack/cert-manager \
    --namespace
$NAMESPACE
\
    --
set
installCRDs=
true
创建 CA 群集签发器
使用以下清单示例创建群集签发器，如 cluster-issuer.yaml。将 MY_EMAIL_ADDRESS 替换为贵组织的有效地址。
apiVersion:
cert-manager.io/v1
kind:
ClusterIssuer
metadata:
name:
letsencrypt
spec:
acme:
server:
https://acme-v02.api.letsencrypt.org/directory
email:
MY_EMAIL_ADDRESS
privateKeySecretRef:
name:
letsencrypt
solvers:
-
http01:
ingress:
class:
nginx
使用 kubectl apply 命令应用签发器。
kubectl apply -f cluster-issuer.yaml
部署 Milvus
请参阅
Azure
，注意配置
service.type
值，您需要将其更改为
ClusterIP
。
创建 Milvus 入口路由
kubectl apply -f ingress.yaml
请参阅 ingress.yaml 内容：
apiVersion:
networking.k8s.io/v1
kind:
Ingress
metadata:
name:
my-release-milvus
annotations:
cert-manager.io/cluster-issuer:
letsencrypt
nginx.ingress.kubernetes.io/backend-protocol:
GRPC
nginx.ingress.kubernetes.io/force-ssl-redirect:
"true"
nginx.ingress.kubernetes.io/proxy-body-size:
2048m
spec:
ingressClassName:
nginx
tls:
-
hosts:
-
milvustest.eastus2.cloudapp.azure.com
# the FQDN
secretName:
tls-secret
rules:
-
host:
milvustest.eastus2.cloudapp.azure.com
http:
paths:
-
path:
/
pathType:
Prefix
backend:
service:
name:
my-release-milvus
port:
number:
19530
验证
kubectl get certificate 
NAME         READY   SECRET       AGE
tls-secret   True    tls-secret   8m7s
kubectl get ingress
NAME                CLASS   HOSTS                                   ADDRESS        PORTS     AGE
my-release-milvus   nginx   milvustest.eastus2.cloudapp.azure.com   EXTERNAL-IP   80, 443   8m15s
你好 Milvus
请参考
Hello Milvus
，更改 uri args，然后运行代码。
connections.connect(
"default"
,uri=
"https://milvustest.eastus2.cloudapp.azure.com:443"
)