在 AWS 上为 Milvus 设置 Layer-7 负载平衡器
与 Layer-4 负载平衡器相比，Layer-7 负载平衡器具有智能负载平衡和缓存功能，是云原生服务的最佳选择。
本指南将指导您为已经在第 4 层负载平衡器后面运行的 Milvus 集群设置第 7 层负载平衡器。
开始之前
您已
在 AWS 上的第 4 层负载平衡器后面部署了一个 Milvus 群集
。
调整 Milvus 配置
本指南假设您已
在 AWS 上的第 4 层负载平衡器后面部署了 Milvus 群集
。
在为该 Milvus 群集设置 Layer-7 负载平衡器之前，请运行以下命令移除 Layer-4 负载平衡器。
helm upgrade milvus-demo milvus/milvus -n milvus --
set
service.type=ClusterIP
准备 TLS 证书
TLS 需要证书才能工作。我们使用
ACM
管理证书，因此需要将现有证书导入 ACM。请参阅
导入证书
。下面是一个示例。
# If the import-certificate command is successful, it returns the arn of the imported certificate.
aws acm import-certificate --certificate fileb://Certificate.pem \
      --certificate-chain fileb://CertificateChain.pem \
      --private-key fileb://PrivateKey.pem
创建入口以生成 Layer-7 负载平衡器
按以下步骤准备输入文件，并将其命名为
ingress.yaml
。
将证书 arn 和 host 替换为您自己的。
apiVersion:
networking.k8s.io/v1
kind:
Ingress
metadata:
namespace:
milvus
name:
milvus-demo
annotations:
alb.ingress.kubernetes.io/scheme:
internet-facing
alb.ingress.kubernetes.io/backend-protocol-version:
GRPC
alb.ingress.kubernetes.io/target-type:
ip
alb.ingress.kubernetes.io/listen-ports:
'[{"HTTPS":443}]'
alb.ingress.kubernetes.io/certificate-arn:
"arn:aws:acm:region:account-id:certificate/certificate-id"
spec:
ingressClassName:
alb
rules:
-
host:
milvus-demo.milvus.io
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
milvus-demo
port:
number:
19530
然后，将该文件应用于 EKS 群集，即可创建 Ingress。
kubectl apply -f ingress.yaml
现在，等待 AWS 设置 Layer-7 负载平衡器。您可以运行
kubectl -f ingress.yaml get -w
输出结果应与下图类似：
NAME          CLASS   HOSTS                   ADDRESS                                                                PORTS   AGE
milvus-demo   alb     milvus-demo.milvus.io   k8s-milvus-milvusde-2f72215c02-778371620.us-east-2.elb.amazonaws.com   80      10m
一旦
ADDRESS
字段中显示地址，Layer-7 负载平衡器就可以使用了。
验证通过 Layer-7 负载平衡器的连接
本指南使用 PyMilvus 来验证与我们刚刚创建的 Layer-7 负载均衡器后面的 Milvus 服务的连接。有关详细步骤，请
阅读此文
。
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

connections.connect(
"default"
, host=
"k8s-milvus-milvusde-2f72215c02-778371620.us-east-2.elb.amazonaws.com"
, port=
"443"
, secure=
True
, server_name=
"milvus-demo.milvus.io"
)
host
和
server_name
应替换为您自己的
名称
。
如果已设置 DNS 记录将域名映射到 alb，请将
host
替换为域名，省略
server_name
。