为 GCP 上的 Milvus 设置 Layer-7 负载平衡器
与 Layer-4 负载平衡器相比，Layer-7 负载平衡器具有智能负载平衡和缓存功能，是云原生服务的最佳选择。
本指南将指导您为已经在第 4 层负载平衡器后面运行的 Milvus 集群设置第 7 层负载平衡器。
开始之前
您的 GCP 账户中已经存在一个项目。
要创建项目，请参阅
创建和管理项目
。本指南中使用的项目名称是
milvus-testing-nonprod
。
您已在本地安装了
gcloud CLI
、
kubectl
和
Helm
，或者决定使用基于浏览器的
Cloud Shell
。
您已使用 GCP 账户凭据
初始化了 gcloud CLI
。
您已
在 GCP 的第 4 层负载平衡器后面部署了 Milvus 集群
。
调整 Milvus 配置
本指南假定您已
在 GCP 的第 4 层负载平衡器后面部署了 Milvus 群集
。
在为该 Milvus 群集设置 Layer-7 负载平衡器之前，请运行以下命令移除 Layer-4 负载平衡器。
helm upgrade my-release milvus/milvus --
set
service.type=ClusterIP
作为 Layer-7 负载平衡器的后端服务，Milvus 必须满足
一定的加密要求
，这样才能理解来自负载平衡器的 HTTP/2 请求。因此，你需要在 Milvus 集群上启用 TLS，具体操作如下。
helm upgrade my-release milvus/milvus -f tls.yaml
在负载均衡器上启用 TLS：
extraConfigFiles:
user.yaml:
|+
    common:
      security:
        tlsMode: 1
设置健康检查端点
为确保服务可用性，GCP 上的 Layer-7 负载均衡需要探测后端服务的健康状况。因此，我们需要设置一个 BackendConfig 来封装健康检查端点，并通过注解将 BackendConfig 与 Milvus 服务关联起来。
以下代码段就是 BackendConfig 的设置。将其保存为
backendconfig.yaml
，以便以后使用。
apiVersion:
cloud.google.com/v1
kind:
BackendConfig
metadata:
name:
my-release-backendconfig
namespace:
default
spec:
healthCheck:
port:
9091
requestPath:
/healthz
type:
HTTP
然后运行以下命令创建健康检查端点。
kubectl apply -f backendconfig.yaml
最后，更新 Milvus 服务的注解，要求我们稍后创建的 Layer-7 负载平衡器使用刚刚创建的端点执行健康检查。
kubectl annotate service my-release-milvus \
    cloud.google.com/app-protocols=
'{"milvus":"HTTP2"}'
\
    cloud.google.com/backend-config=
'{"default": "my-release-backendconfig"}'
\
    cloud.google.com/neg=
'{"ingress": true}'
--overwrite
关于第一个注释、
Milvus 原生于基于 HTTP/2 的 gRPC。因此，我们可以使用 HTTP/2 作为 Layer-7 负载平衡器和 Milvus 之间的通信协议。
至于第二个注释、
Milvus 只通过 gRPC 和 HTTP/1 提供健康检查端点。我们需要设置一个 BackendConfig 来封装健康检查端点，并将其与 Milvus 服务关联，以便 Layer-7 负载均衡器探查该端点以了解 Milvus 的健康状况。
至于第三个注释、
它要求在创建入口后创建网络端点组（NEG）。当 NEG 与 GKE Ingress 一起使用时，Ingress 控制器会帮助创建负载平衡器的所有方面。这包括创建虚拟 IP 地址、转发规则、健康检查、防火墙规则等。有关详细信息，请参阅
Google Cloud 文档
。
准备 TLS 证书
TLS 需要证书才能工作。
创建证书有两种方法，即自我管理和 Google 管理。
本指南使用
my-release.milvus.io
作为访问我们 Milvus 服务的域名。
创建自我管理证书
运行以下命令创建证书。
# Generates a tls.key.
openssl genrsa -out tls.key 2048
# Creates a certificate and signs it with the preceding key.
openssl req -new -key tls.key -out tls.csr \
    -subj
"/CN=my-release.milvus.io"
openssl x509 -req -days 99999 -
in
tls.csr -signkey tls.key \
    -out tls.crt
然后在 GKE 集群中用这些文件创建一个秘密，以供日后使用。
kubectl create secret tls my-release-milvus-tls --cert=./tls.crt --key=./tls.key
创建谷歌管理证书
以下代码段是 ManagedCertificate 设置。将其保存为
managed-crt.yaml
，以便日后使用。
apiVersion:
networking.gke.io/v1
kind:
ManagedCertificate
metadata:
name:
my-release-milvus-tls
spec:
domains:
-
my-release.milvus.io
在 GKE 集群中应用以下设置，创建受管证书：
kubectl apply -f ./managed-crt.yaml
这可能会持续一段时间。您可以运行
kubectl get -f ./managed-crt.yaml -o yaml -w
输出结果应与下图类似：
status:
  certificateName: mcrt-34446a53-d639-4764-8438-346d7871a76e
  certificateStatus: Provisioning
  domainStatus:
  - domain: my-release.milvus.io
    status: Provisioning
一旦
certificateStatus
变为
Active
，您就可以设置负载平衡器了。
创建入口以生成 Layer-7 负载平衡器
用以下代码段之一创建一个 YAML 文件。
使用自我管理证书
apiVersion:
networking.k8s.io/v1
kind:
Ingress
metadata:
name:
my-release-milvus
namespace:
default
spec:
tls:
-
hosts:
-
my-release.milvus.io
secretName:
my-release-milvus-tls
rules:
-
host:
my-release.milvus.io
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
使用 Google 管理的证书
apiVersion:
networking.k8s.io/v1
kind:
Ingress
metadata:
name:
my-release-milvus
namespace:
default
annotations:
networking.gke.io/managed-certificates:
"my-release-milvus-tls"
spec:
rules:
-
host:
my-release.milvus.io
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
然后，将该文件应用到 GKE 集群，即可创建 Ingress。
kubectl apply -f ingress.yaml
现在，等待 Google 设置 Layer-7 负载均衡器。您可以运行
kubectl  -f ./config/samples/ingress.yaml get -w
输出结果应与下图类似：
NAME                CLASS    HOSTS                  ADDRESS   PORTS   AGE
my-release-milvus   <none>   my-release.milvus.io             80      4s
my-release-milvus   <none>   my-release.milvus.io   34.111.144.65   80, 443   41m
一旦
ADDRESS
字段中显示了 IP 地址，Layer-7 负载平衡器就可以使用了。端口 80 和端口 443 都显示在上述输出中。请记住，为了您的利益，应始终使用端口 443。
验证通过 Layer-7 负载均衡器的连接
本指南使用 PyMilvus 来验证与我们刚刚创建的 Layer-7 负载均衡器后面的 Milvus 服务的连接。有关详细步骤，请
阅读此文
。
请注意，连接参数会因
准备 TLS 证书
中管理证书的方式而不同。
from
pymilvus
import
(
    connections,
    utility,
    FieldSchema,
    CollectionSchema,
    DataType,
    Collection,
)
# For self-managed certificates, you need to include the certificate in the parameters used to set up the connection.
connections.connect(
"default"
, host=
"34.111.144.65"
, port=
"443"
, server_pem_path=
"tls.crt"
, secure=
True
, server_name=
"my-release.milvus.io"
)
# For Google-managed certificates, there is not need to do so.
connections.connect(
"default"
, host=
"34.111.144.65"
, port=
"443"
, secure=
True
, server_name=
"my-release.milvus.io"
)
host
和
port
中的 IP 地址和
端口号
应与
Create an Ingress to generate a Layer-7 Load Balancer
末尾列出的一致。
如果已设置 DNS 记录将域名映射到主机 IP 地址，请将
host
中的 IP 地址替换为域名，省略
server_name
。