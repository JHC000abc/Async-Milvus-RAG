传输中的加密
TLS（传输层安全）是确保通信安全的加密协议。Milvus 代理使用 TLS 单向和双向验证。
本主题将介绍如何在 Milvus 代理中启用 TLS，用于 gRPC 和 RESTful 流量。
TLS 和用户身份验证是两种不同的安全方法。如果在 Milvus 系统中同时启用了用户身份验证和 TLS，则需要提供用户名、密码和证书文件路径。有关如何启用用户身份验证的信息，请参阅
验证用户访问
。
创建自己的证书
前提条件
确保已安装 OpenSSL。如果尚未安装，请先
构建并安装
OpenSSL。
openssl version
如果未安装 OpenSSL。可在 Ubuntu 中使用以下命令安装。
sudo apt install openssl
创建文件
创建
gen.sh
文件。
mkdir
cert &&
cd
cert
touch
gen.sh
将以下脚本复制到
gen.sh
。
有必要在
gen.sh
文件中配置
CommonName
。
CommonName
指的是客户端在连接时应指定的服务器名称。
gen.sh
#
!/usr/bin/env sh
#
your variables
Country="US"
State="CA"
Location="Redwood City"
Organization="zilliz"
OrganizationUnit="devops"
CommonName="localhost"
ExpireDays=3650 # 10 years
#
generate private key
for
ca, server and client
openssl genpkey -quiet -algorithm rsa:2048 -out ca.key
openssl genpkey -quiet -algorithm rsa:2048 -out server.key
openssl genpkey -quiet -algorithm rsa:2048 -out client.key
#
create a new ca certificate
openssl req -x509 -new -nodes -key ca.key -sha256 -days 36500 -out ca.pem \
  -subj "/C=$Country/ST=$State/L=$Location/O=$Organization/OU=$OrganizationUnit/CN=$CommonName"
#
prepare extension config
for
signing certificates
echo '[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS = '$CommonName > openssl.cnf
#
sign server certificate with ca
openssl req -new -key server.key\
  -subj "/C=$Country/ST=$State/L=$Location/O=$Organization/OU=$OrganizationUnit/CN=$CommonName"\
  | openssl x509 -req -days $ExpireDays -out server.pem -CA ca.pem -CAkey ca.key -CAcreateserial \
    -extfile ./openssl.cnf -extensions v3_req
#
sign client certificate with ca
openssl req -new -key client.key\
  -subj "/C=$Country/ST=$State/L=$Location/O=$Organization/OU=$OrganizationUnit/CN=$CommonName"\
  | openssl x509 -req -days $ExpireDays -out client.pem -CA ca.pem -CAkey ca.key -CAcreateserial \
    -extfile ./openssl.cnf -extensions v3_req
gen.sh
文件中的变量对创建证书签名请求文件的过程至关重要。前五个变量是基本的签名信息，包括国家、州、地点、组织、组织单位。在配置
CommonName
时需要谨慎，因为它将在客户端与服务器通信时进行验证。
运行
gen.sh
生成证书
运行
gen.sh
文件创建证书。
chmod
+x gen.sh
./gen.sh
将创建以下七个文件：
ca.key
,
ca.pem
,
ca.srl
,
server.key
,
server.pem
,
client.key
,
client.pem
。
请确保
ca.key
,
ca.pem
,
ca.srl
安全，以便以后更新证书。
server.key
和
server.pem
文件由服务器使用，而
client.key
和
client.pem
文件由客户端使用。
更新证书（可选）
如果您想在某些情况下更新证书，例如证书即将过期，可以使用以下脚本。
您的工作目录中需要
ca.key
,
ca.pem
,
ca.srl
。
renew.sh
#
!/usr/bin/env sh
#
your variables
Country="US"
State="CA"
Location="Redwood City"
Organization="zilliz"
OrganizationUnit="devops"
CommonName="localhost"
ExpireDays=3650 # 10 years
#
generate private key
for
ca, server and client
openssl genpkey -quiet -algorithm rsa:2048 -out server.key
openssl genpkey -quiet -algorithm rsa:2048 -out client.key
#
prepare extension config
for
signing certificates
echo '[v3_req]
basicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names
[alt_names]
DNS = '$CommonName > openssl.cnf
#
sign server certificate with ca
openssl req -new -key server.key\
  -subj "/C=$Country/ST=$State/L=$Location/O=$Organization/OU=$OrganizationUnit/CN=$CommonName"\
  | openssl x509 -req -days $ExpireDays -out server.pem -CA ca.pem -CAkey ca.key -CAcreateserial \
    -extfile ./openssl.cnf -extensions v3_req
#
sign client certificate with ca
openssl req -new -key client.key\
  -subj "/C=$Country/ST=$State/L=$Location/O=$Organization/OU=$OrganizationUnit/CN=$CommonName"\
  | openssl x509 -req -days $ExpireDays -out client.pem -CA ca.pem -CAkey ca.key -CAcreateserial \
    -extfile ./openssl.cnf -extensions v3_req
运行
renew.sh
文件创建证书。
chmod
+x renew.sh
./renew.sh
使用 TLS 设置 Milvus 服务器
本节概述了使用 TLS 加密配置 Milvus 服务器的步骤。
为 Docker Compose 设置
1.修改 Milvus 服务器配置
要启用外部 TLS，请在
milvus.yaml
文件中添加以下配置：
proxy:
http:
# for now milvus do not support config restful on same port with grpc
# so we set to 8080, grpc will still use 19530
port:
8080
tls:
serverPemPath:
/milvus/tls/server.pem
serverKeyPath:
/milvus/tls/server.key
caPemPath:
/milvus/tls/ca.pem
common:
security:
tlsMode:
1
参数：
serverPemPath
:服务器证书文件的路径。
serverKeyPath
:服务器密钥文件的路径。
caPemPath
:CA 证书文件的路径。
tlsMode
:外部服务的 TLS 模式。有效值：
1
:单向验证，即只有服务器需要证书，客户端验证证书。该模式要求服务器端提供
server.pem
和
server.key
，客户端提供
server.pem
。
2
:双向验证：服务器和客户端都需要证书才能建立安全连接。这种模式要求服务器端使用
server.pem
、
server.key
和
ca.pem
，客户端使用
client.pem
、
client.key
和
ca.pem
。
要启用内部 TLS，请在
milvus.yaml
文件中添加以下配置：
internaltls:
serverPemPath:
/milvus/tls/server.pem
serverKeyPath:
/milvus/tls/server.key
caPemPath:
/milvus/tls/ca.pem
common:
security:
internaltlsEnabled:
true
参数：
serverPemPath
:服务器证书文件的路径。
serverKeyPath
:服务器密钥文件的路径。
caPemPath
:CA 证书文件的路径。
internaltlsEnabled
:是否启用内部 TLS。目前只支持单向 TLS。
2.将证书文件映射到容器
准备证书文件
在与
docker-compose.yaml
相同的目录下新建一个名为
tls
的文件夹。将
server.pem
、
server.key
和
ca.pem
复制到
tls
文件夹。将它们放在如下目录结构中：
├── docker-compose.yml
├── milvus.yaml
└── tls
├── server.pem
     ├── server.key
     └── ca.pem
更新 Docker Compose 配置
编辑
docker-compose.yaml
文件，在容器内映射证书文件路径，如下所示：
standalone:
container_name:
milvus-standalone
image:
milvusdb/milvus:latest
command:
[
"milvus"
,
"run"
,
"standalone"
]
security_opt:
-
seccomp:unconfined
environment:
ETCD_ENDPOINTS:
etcd:2379
MINIO_ADDRESS:
minio:9000
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
-
${DOCKER_VOLUME_DIRECTORY:-.}/tls:/milvus/tls
-
${DOCKER_VOLUME_DIRECTORY:-.}/milvus.yaml:/milvus/configs/milvus.yaml
使用 Docker Compose 部署 Milvus
执行以下命令部署 Milvus：
sudo
docker compose up -d
为 Milvus 操作符进行设置
将证书文件放到工作目录中。目录结构应如下所示：
├── milvus.yaml (
to
be created later)
├── server.pem
├── server.
key
└── ca.pem
创建一个包含证书文件的密文：
kubectl create secret generic certs --from-file=server.pem --from-file=server.key --from-file=ca.pem
要启用外部 TLS，请在
milvus.yaml
文件中添加以下配置：
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
spec:
config:
proxy:
http:
# for now not support config restful on same port with grpc
# so we set to 8080, grpc will still use 19530
port:
8080
common:
security:
tlsMode:
1
# tlsMode for external service 1 for one-way TLS, 2 for Mutual TLS, 0 for disable
tls:
serverPemPath:
/certs/server.pem
serverKeyPath:
/certs/server.key
caPemPath:
/certs/ca.pem
components:
# mount the certs secret to the milvus container
volumes:
-
name:
certs
secret:
secretName:
certs
volumeMounts:
-
name:
certs
mountPath:
/certs
readOnly:
true
要启用内部 TLS，请在
milvus.yaml
文件中添加以下配置：
切记用证书中的 CommonName 替换
internaltls.sni
字段。
apiVersion:
milvus.io/v1beta1
kind:
Milvus
metadata:
name:
my-release
spec:
config:
proxy:
http:
# for now not support config restful on same port with grpc
# so we set to 8080, grpc will still use 19530
port:
8080
common:
security:
internaltlsEnabled:
true
# whether to enable internal tls
# Configure tls certificates path for internal service
internaltls:
serverPemPath:
/certs/server.pem
serverKeyPath:
/certs/server.key
caPemPath:
/certs/ca.pem
sni:
localhost
# the CommonName in your certificates
components:
# mount the certs secret to the milvus container
volumes:
-
name:
certs
secret:
secretName:
certs
volumeMounts:
-
name:
certs
mountPath:
/certs
readOnly:
true
创建 Milvus CR：
kubectl create -f milvus.yaml
设置为 Milvus Helm
将证书文件放入工作目录。目录结构应如下所示：
├── values.yaml (
to
be created later)
├── server.pem
├── server.
key
└── ca.pem
创建一个包含证书文件的密文：
kubectl create secret generic certs --from-file=server.pem --from-file=server.key --from-file=ca.pem
要启用外部 TLS，请在
values.yaml
文件中添加以下配置：
extraConfigFiles:
user.yaml:
|+
    proxy:
      http:
        # for now not support config restful on same port with grpc
        # so we set to 8080, grpc will still use 19530
        port: 8080 
    common:
      security:
        tlsMode: 1 # tlsMode for external service 1 means set to 2 to enable Mutual TLS
    # Configure tls certificates path for external service
    tls:
      serverPemPath: /certs/server.pem
      serverKeyPath: /certs/server.key
      caPemPath: /certs/ca.pem
# mount the certs secret to the milvus container
volumes:
-
name:
certs
secret:
secretName:
certs
volumeMounts:
-
name:
certs
mountPath:
/certs
readOnly:
true
要启用内部 TLS，请在
values.yaml
文件中添加以下配置：
切记用证书中的 CommonName 替换
internaltls.sni
字段。
extraConfigFiles:
user.yaml:
|+
    common:
      security:
        internaltlsEnabled: true # whether to enable internal tls
    # Configure tls certificates path for internal service
    internaltls:
      serverPemPath: /certs/server.pem
      serverKeyPath: /certs/server.key
      caPemPath: /certs/ca.pem
      sni: localhost
# mount the certs secret to the milvus container
volumes:
-
name:
certs
secret:
secretName:
certs
volumeMounts:
-
name:
certs
mountPath:
/certs
readOnly:
true
创建 milvus 版本：
helm repo add milvus https://zilliztech.github.io/milvus-helm/
helm repo update milvus
helm install my-release milvus/milvus -f values.yaml
验证已启用内部 TLS
很难直接验证内部 TLS。你可以检查 Milvus 日志，查看内部 TLS 是否已启用。
在 Milvus 日志中，如果启用了内部 TLS，你应该看到以下信息：
[...date time...]
[INFO]
[utils/util.go:56]
[
"Internal TLS Enabled"
]
[value=true]
使用 TLS 连接到 Milvus 服务器
对于 SDK 交互，根据 TLS 模式使用以下设置。
单向 TLS 连接
提供
server.pem
的路径，并确保
server_name
与证书中配置的
CommonName
匹配。
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
"https://localhost:19530"
,
    secure=
True
,
    server_pem_path=
"path_to/server.pem"
,
    server_name=
"localhost"
)
双向 TLS 连接
提供
client.pem
、
client.key
和
ca.pem
的路径，并确保
server_name
与证书中配置的
CommonName
匹配。
from
pymilvus
import
MilvusClient

client = MilvusClient(
    uri=
"https://localhost:19530"
,
    secure=
True
,
    client_pem_path=
"path_to/client.pem"
,
    client_key_path=
"path_to/client.key"
,
    ca_pem_path=
"path_to/ca.pem"
,
    server_name=
"localhost"
)
更多信息请参阅
example_tls1.py
和
example_tls2.
py
。
使用 TLS 连接到 Milvus RESTful 服务器
对于 RESTful API，可以使用
curl
命令检查 TLS。
单向 TLS 连接
curl --cacert path_to/ca.pem https://localhost:8080/v2/vectordb/collections/list
双向 TLS 连接
curl --cert path_to/client.pem --key path_to/client.key --cacert path_to/ca.pem https://localhost:8080/v2/vectordb/collections/list