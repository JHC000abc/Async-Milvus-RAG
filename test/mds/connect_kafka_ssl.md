使用 SASL/SSL 连接到 Kafka
本指南列出了几种连接 Milvus 到 Kafka 的方法，从不带 SASL/SSL 的最简单方法到带 SASL/SSL 的完全安全方法。
不使用 SASL/SSL 连接 Milvus 和 Kafka
要在不使用 SASL/SSL 的情况下启动 Milvus 和 Kafka，需要禁用 Kafka 和 Milvus 的身份验证和加密。仅在受信任的环境中使用它们。
1.不使用 SASL/SSL 启动 Kafka 服务
你可以使用下面的
docker-compose.yaml
文件在没有 SASL/SSL 的情况下启动 Kafka 服务：
version:
'3'
services:
zookeeper:
image:
wurstmeister/zookeeper:latest
container_name:
zookeeper
ports:
-
2181
:2181
restart:
always
kafka:
image:
wurstmeister/kafka:latest
container_name:
kafka
ports:
-
9092
:9092
environment:
-
KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
-
KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092
-
KAFKA_LISTENERS=PLAINTEXT://:9092
volumes:
-
/var/run/docker.sock:/var/run/docker.sock
restart:
always
然后使用以下命令启动 Kafka 服务：
$
docker compose up -d
2.启动 Milvus 并连接到 Kafka
Kafka 服务启动后，你就可以启动 Milvus 并连接到它了。使用以下
docker-compose.yaml
文件，在不使用 SASL/SSL 的情况下启动 Milvus 并连接到 Kafka：
version:
'3.5'
services:
etcd:
......
minio:
......
standalone:
container_name:
milvus-standalone
......
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
-
${DOCKER_VOLUME_DIRECTORY:-.}/milvus.yaml:/milvus/configs/milvus.yaml
使用以下命令下载 Milvus 配置文件模板：
$
wget https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml -O milvus.yaml
并设置以下参数：
mq:
type:
kafka
kafka:
brokerList:
"127.0.0.1:9092"
saslUsername:
saslPassword:
saslMechanisms:
securityProtocol:
readTimeout:
10
# read message timeout in seconds
ssl:
enabled:
false
# Whether to support kafka secure connection mode
tlsCert:
tlsKey:
tlsCACert:
tlsKeyPassword:
然后使用以下命令启动 Milvus：
$
docker compose up -d
使用 SASL/PLAIN Alone 将 Milus 连接到 Kafka
要使用 SASL/PLAIN 身份验证启动 Kafka，需要添加
kafka_server_jass.conf
文件并进行适当设置。
1.使用 SASL/PLAIN 启动 Kafka 服务
将以下
docker-compose.yaml
文件和
kafka_server_jaas.conf
文件放在同一目录下。
version:
'3'
services:
zookeeper:
image:
confluentinc/cp-zookeeper:latest
container_name:
zookeeper
environment:
ZOOKEEPER_CLIENT_PORT:
2181
ZOOKEEPER_TICK_TIME:
2000
ports:
-
2181
:2181
kafka:
image:
confluentinc/cp-kafka:latest
container_name:
kafka
depends_on:
-
zookeeper
ports:
-
9092
:9092
-
9093
:9093
environment:
KAFKA_BROKER_ID:
1
KAFKA_ZOOKEEPER_CONNECT:
'zookeeper:2181'
ZOOKEEPER_SASL_ENABLED:
"false"
KAFKA_ADVERTISED_LISTENERS:
SASL_PLAINTEXT://localhost:9093
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:
SASL_PLAINTEXT:SASL_PLAINTEXT
KAFKA_SECURITY_INTER_BROKER_PROTOCOL:
SASL_PLAINTEXT
KAFKA_SASL_MECHANISM_INTER_BROKER_PROTOCOL:
PLAIN
KAFKA_SASL_ENABLED_MECHANISMS:
PLAIN
KAFKA_CONFLUENT_TOPIC_REPLICATION_FACTOR:
1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR:
1
KAFKA_DEFAULT_REPLICATION_FACTOR:
1
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR:
1
KAFKA_OPTS:
"-Djava.security.auth.login.config=/etc/kafka/configs/kafka_server_jass.conf"
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/kafka_server_jass.conf:/etc/kafka/configs/kafka_server_jass.conf
在
kafka_server_jass.conf
文件中，设置以下参数：
KafkaServer {
    org.apache.kafka.common.security.plain.PlainLoginModule required
    username="kafka"
    password="pass123"
    user_kafka="pass123";
};
然后使用以下命令启动 Kafka 服务：
$
docker compose up -d
2.启动 Milvus 并连接到 Kafka
Kafka 服务启动后，就可以启动 Milvus 并连接到它。使用以下
docker-compose.yaml
文件启动 Milvus 并用 SASL/PLAIN 连接到 Kafka：
version:
'3.5'
services:
etcd:
......
minio:
......
standalone:
container_name:
milvus-standalone
......
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
-
${DOCKER_VOLUME_DIRECTORY:-.}/milvus.yaml:/milvus/configs/milvus.yaml
使用以下命令下载 Milvus 配置文件模板：
$
wget https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml -O milvus.yaml
并设置以下参数：
mq:
type:
kafka
kafka:
brokerList:
"127.0.0.1:9093"
saslUsername:
kafka
saslPassword:
pass123
saslMechanisms:
PLAIN
securityProtocol:
SASL_PLAINTEXT
readTimeout:
10
# read message timeout in seconds
ssl:
enabled:
false
# Whether to support kafka secure connection mode
tlsCert:
# path to client's public key
tlsKey:
# path to client's private key
tlsCACert:
# file or directory path to CA certificate
tlsKeyPassword:
# private key passphrase for use with private key, if any
然后就可以用以下命令启动 Milvus：
$
docker compose up -d
使用 SSL Alone 将 Milvus 连接到 Kafka
要使用 SSL 身份验证启动 Kafka，你需要获取一些证书文件或生成自签名的证书。在本例中，我们使用自签名证书。
1.生成自签名证书
创建一个名为
my_secrets
的文件夹，在其中添加一个名为
gen-ssl-certs.sh
的 bash 脚本，并将以下内容粘贴到其中：
#!/bin/bash
#
#
# This scripts generates:
#  - root CA certificate
#  - server certificate and keystore
#  - client keys
#
# https://cwiki.apache.org/confluence/display/KAFKA/Deploying+SSL+for+Kafka
#
if
[[
"
$1
"
==
"-k"
]];
then
USE_KEYTOOL=1
shift
else
USE_KEYTOOL=0
fi
OP=
"
$1
"
CA_CERT=
"
$2
"
PFX=
"
$3
"
HOST=
"
$4
"
C=NN
ST=NN
L=NN
O=NN
OU=NN
CN=
"kafka-ssl"
# Password
PASS=
"abcdefgh"
# Cert validity, in days
VALIDITY=365
set
-e
export
LC_ALL=C
if
[[
$OP
==
"ca"
&& ! -z
"
$CA_CERT
"
&& ! -z
"
$3
"
]];
then
CN=
"
$3
"
openssl req -new -x509 -keyout
${CA_CERT}
.key -out
$CA_CERT
-days
$VALIDITY
-passin
"pass:
$PASS
"
-passout
"pass:
$PASS
"
<<
EOF
${C}
${ST}
${L}
${O}
${OU}
${CN}
$USER@${CN}
.
.
EOF
elif
[[
$OP
==
"server"
&& ! -z
"
$CA_CERT
"
&& ! -z
"
$PFX
"
&& ! -z
"
$CN
"
]];
then
#Step 1
echo
"############ Generating key"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
server.keystore.jks -
alias
localhost -validity
$VALIDITY
-genkey -keyalg RSA <<
EOF
$CN
$OU
$O
$L
$ST
$C
yes
yes
EOF
#Step 2
echo
"############ Adding CA"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
server.truststore.jks -
alias
CARoot -import -file
$CA_CERT
<<
EOF
yes
EOF
#Step 3
echo
"############ Export certificate"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
server.keystore.jks -
alias
localhost -certreq -file
${PFX}
cert-file
echo
"############ Sign certificate"
openssl x509 -req -CA
$CA_CERT
-CAkey
${CA_CERT}
.key -
in
${PFX}
cert-file -out
${PFX}
cert-signed -days
$VALIDITY
-CAcreateserial -passin
"pass:
$PASS
"
echo
"############ Import CA"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
server.keystore.jks -
alias
CARoot -import -file
$CA_CERT
<<
EOF
yes
EOF
echo
"############ Import signed CA"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
server.keystore.jks -
alias
localhost -import -file
${PFX}
cert-signed
elif
[[
$OP
==
"client"
&& ! -z
"
$CA_CERT
"
&& ! -z
"
$PFX
"
&& ! -z
"
$CN
"
]];
then
if
[[
$USE_KEYTOOL
== 1 ]];
then
echo
"############ Creating client truststore"
[[ -f
${PFX}
client.truststore.jks ]] || keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
client.truststore.jks -
alias
CARoot -import -file
$CA_CERT
<<
EOF
yes
EOF
echo
"############ Generating key"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
client.keystore.jks -
alias
localhost -validity
$VALIDITY
-genkey -keyalg RSA <<
EOF
$CN
$OU
$O
$L
$ST
$C
yes
yes
EOF
echo
"########### Export certificate"
keytool -storepass
"
$PASS
"
-keystore
${PFX}
client.keystore.jks -
alias
localhost -certreq -file
${PFX}
cert-file
echo
"########### Sign certificate"
openssl x509 -req -CA
${CA_CERT}
-CAkey
${CA_CERT}
.key -
in
${PFX}
cert-file -out
${PFX}
cert-signed -days
$VALIDITY
-CAcreateserial -passin pass:
$PASS
echo
"########### Import CA"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
client.keystore.jks -
alias
CARoot -import -file
${CA_CERT}
<<
EOF
yes
EOF
echo
"########### Import signed CA"
keytool -storepass
"
$PASS
"
-keypass
"
$PASS
"
-keystore
${PFX}
client.keystore.jks -
alias
localhost -import -file
${PFX}
cert-signed
else
# Standard OpenSSL keys
echo
"############ Generating key"
openssl genrsa -des3 -passout
"pass:
$PASS
"
-out
${PFX}
client.key 2048
echo
"############ Generating request"
openssl req -passin
"pass:
$PASS
"
-passout
"pass:
$PASS
"
-key
${PFX}
client.key -new -out
${PFX}
client.req \
                <<
EOF
$C
$ST
$L
$O
$OU
$CN
.
$PASS
.
EOF
echo
"########### Signing key"
openssl x509 -req -passin
"pass:
$PASS
"
-
in
${PFX}
client.req -CA
$CA_CERT
-CAkey
${CA_CERT}
.key -CAcreateserial -out
${PFX}
client.pem -days
$VALIDITY
fi
else
echo
"Usage:
$0
ca <ca-cert-file> <CN>"
echo
"
$0
[-k] server|client <ca-cert-file> <file_prefix> <hostname>"
echo
""
echo
"       -k = Use keytool/Java Keystore, else standard SSL keys"
exit
1
fi
在上述脚本中，默认密码为
abcdefgh
。要更改密码，请创建一个名为
cert_creds
的文本文件，并在第一行输入密码。
然后运行以下命令生成证书：
生成 CA 证书：
以下假设 CA 证书文件名为
ca-cert
，代理的主机名为
kafka-ssl
：
$
./gen-ssl-certs.sh ca ca-cert kafka-ssl
生成服务器证书和密钥库：
以下假设 CA 证书文件名为
ca-cert
，所有输出文件的前缀均为
kafka_
，代理的主机名为
kafka-ssl
：
$
./gen-ssl-certs.sh -k server ca-cert kafka_ kafka-ssl
生成客户端密钥：
以下假设 CA 证书文件名为
ca-cert
，所有输出文件的前缀为
kafka_
，客户端名称为
kafka-client
：
$
./gen-ssl-certs.sh client ca-cert kafka_ kafka-client
生成所有必要的证书后，您可以在
my_secrets
文件夹中看到以下文件：
$
ls
-l my_secrets
total 12
-rw-rw-r-- 1 1.4K Feb 26 11:53 ca-cert
-rw------- 1 1.9K Feb 26 11:53 ca-cert.key
-rw-rw-r-- 1   41 Feb 26 11:54 ca-cert.srl
-rw-rw-r-- 1    9 Feb 26 12:08 cert_creds
-rwxrwxr-x 1 3.9K Feb 26 17:26 gen-ssl-certs.sh
-rw-rw-r-- 1 1.4K Feb 26 11:54 kafka_cert-file
-rw-rw-r-- 1 1.4K Feb 26 11:54 kafka_cert-signed
-rw------- 1 1.8K Feb 26 11:54 kafka_client.key
-rw-rw-r-- 1 1.2K Feb 26 11:54 kafka_client.pem
-rw-rw-r-- 1 1013 Feb 26 11:54 kafka_client.req
-rw-rw-r-- 1 5.6K Feb 26 11:54 kafka_server.keystore.jks
-rw-rw-r-- 1 1.4K Feb 26 11:54 kafka_server.truststore.jks
2.使用 SSL 启动 Kafka 服务
使用以下
docker-compose.yaml
文件以 SSL 启动 Kafka 服务：
version:
'3'
services:
zookeeper:
image:
confluentinc/cp-zookeeper:latest
container_name:
zookeeper
hostname:
zookeeper
ports:
-
2181
:2181
environment:
ZOOKEEPER_SERVER_ID:
1
ZOOKEEPER_CLIENT_PORT:
2181
kafka-ssl:
image:
confluentinc/cp-kafka:latest
container_name:
kafka-ssl
hostname:
kafka-ssl
ports:
-
9093
:9093
depends_on:
-
zookeeper
environment:
KAFKA_BROKER_ID:
1
KAFKA_ZOOKEEPER_CONNECT:
'zookeeper:2181'
ZOOKEEPER_SASL_ENABLED:
"false"
KAFKA_ADVERTISED_LISTENERS:
SSL://kafka-ssl:9093
KAFKA_SSL_KEYSTORE_FILENAME:
kafka_server.keystore.jks
KAFKA_SSL_KEYSTORE_CREDENTIALS:
cert_creds
KAFKA_SSL_KEY_CREDENTIALS:
cert_creds
KAFKA_SSL_TRUSTSTORE_FILENAME:
kafka_server.truststore.jks
KAFKA_SSL_TRUSTSTORE_CREDENTIALS:
cert_creds
KAFKA_SSL_CLIENT_AUTH:
'required'
KAFKA_SECURITY_PROTOCOL:
SSL
KAFKA_SECURITY_INTER_BROKER_PROTOCOL:
SSL
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR:
1
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/my_secrets:/etc/kafka/secrets
然后使用以下命令启动 Kafka 服务：
$
docker compose up -d
3.启动 Milvus 并使用 SSL 连接到 Kafka
启动 Kafka 服务后，就可以启动 Milvus 并连接到它。使用以下
docker-compose.yaml
文件启动 Milvus 并用 SSL 连接到 Kafka：
version:
'3.5'
services:
etcd:
......
minio:
......
standalone:
container_name:
milvus-standalone
......
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
-
${DOCKER_VOLUME_DIRECTORY:-.}/milvus.yaml:/milvus/configs/milvus.yaml
-
${DOCKER_VOLUME_DIRECTORY:-.}/my_secrets:/milvus/secrets
使用以下命令下载 Milvus 配置文件模板：
$
wget https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml -O milvus.yaml
并设置以下参数：
mq:
type:
kafka
kafka:
brokerList:
"127.0.0.1:9093"
saslUsername:
saslPassword:
saslMechanisms:
securityProtocol:
SSL
readTimeout:
10
# read message timeout in seconds
ssl:
enabled:
true
# Whether to support kafka secure connection mode
tlsCert:
/milvus/secrets/kafka_client.pem
# path to client's public key
tlsKey:
/milvus/secrets/kafka_client.key
# path to client's private key
tlsCACert:
/milvus/secrets/ca-cert
# file or directory path to CA certificate
tlsKeyPassword:
abcdefgh
# private key passphrase for use with private key, if any
然后用以下命令启动 Milvus：
$
docker compose up -d
使用 SASL/PLAIN 和 SSL 连接 Milvus 到 Kafka
要使用 SASL/PLAIN 和 SSL 将 Milvus 连接到 Kafka，需要重复
仅使用 SASL/PLAIN 将 Milv
us 连接到
Kafka 和
仅使用 SSL 将 Milvus 连接到 Kafka
中的步骤。
1.使用 SASL/PLAIN 和 SSL 启动 Kafka 服务
使用《
Connect Milus to Kafka with SASL/PLAIN Alone
》中提到的
kafka_server_jass.conf
文件和《
Connect Milus to Kafka with SSL Alone
》中生成的
my_secrets
文件夹，以 SASL/PLAIN 和 SSL 启动 Kafka 服务。
以下
docker-compose.yaml
文件可用于使用 SASL/PLAIN 和 SSL 启动 Kafka 服务：
version:
'3'
services:
zookeeper:
image:
confluentinc/cp-zookeeper:latest
container_name:
zookeeper
hostname:
zookeeper
ports:
-
2181
:2181
environment:
ZOOKEEPER_SERVER_ID:
1
ZOOKEEPER_CLIENT_PORT:
2181
ZOOKEEPER_TICK_TIME:
2000
kafka-ssl:
image:
confluentinc/cp-kafka:latest
container_name:
kafka-ssl
hostname:
kafka-ssl
ports:
-
9093
:9093
depends_on:
-
zookeeper
environment:
KAFKA_BROKER_ID:
1
KAFKA_ZOOKEEPER_CONNECT:
'zookeeper:2181'
ZOOKEEPER_SASL_ENABLED:
"false"
KAFKA_ADVERTISED_LISTENERS:
SASL_SSL://kafka-ssl:9093
KAFKA_SSL_KEYSTORE_FILENAME:
kafka_server.keystore.jks
KAFKA_SSL_KEYSTORE_CREDENTIALS:
cert_creds
KAFKA_SSL_KEY_CREDENTIALS:
cert_creds
KAFKA_SSL_TRUSTSTORE_FILENAME:
kafka_server.truststore.jks
KAFKA_SSL_TRUSTSTORE_CREDENTIALS:
cert_creds
KAFKA_SSL_CLIENT_AUTH:
'required'
KAFKA_SECURITY_PROTOCOL:
SASL_SSL
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR:
1
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP:
SASL_SSL:SASL_SSL
KAFKA_SECURITY_INTER_BROKER_PROTOCOL:
SASL_SSL
KAFKA_SASL_MECHANISM_INTER_BROKER_PROTOCOL:
PLAIN
KAFKA_SASL_ENABLED_MECHANISMS:
PLAIN
KAFKA_CONFLUENT_TOPIC_REPLICATION_FACTOR:
1
KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR:
1
KAFKA_DEFAULT_REPLICATION_FACTOR:
1
KAFKA_OPTS:
"-Djava.security.auth.login.config=/etc/kafka/configs/kafka_server_jass.conf"
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/my_secrets:/etc/kafka/secrets
-
${DOCKER_VOLUME_DIRECTORY:-.}/kafka_server_jass.conf:/etc/kafka/configs/kafka_server_jass.conf
然后使用以下命令启动 Kafka 服务：
$
docker compose up -d
2.使用 SASL/PLAIN 和 SSL 启动 Milvus 并连接到 Kafka
启动 Kafka 服务后，就可以启动 Milvus 并连接到它。使用以下
docker-compose.yaml
文件启动 Milvus 并用 SASL/PLAIN 和 SSL 连接到 Kafka：
version:
'3.5'
services:
etcd:
......
minio:
......
standalone:
container_name:
milvus-standalone
......
volumes:
-
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus:/var/lib/milvus
-
${DOCKER_VOLUME_DIRECTORY:-.}/milvus.yaml:/milvus/configs/milvus.yaml
-
${DOCKER_VOLUME_DIRECTORY:-.}/my_secrets:/milvus/secrets
使用以下命令下载 Milvus 配置文件模板：
$
wget https://raw.githubusercontent.com/zilliztech/milvus-operator/main/config/samples/milvus_cluster_default.yaml -O milvus.yaml
并设置以下参数：
mq:
type:
kafka
kafka:
brokerList:
"127.0.0.1:9093"
saslUsername:
kafka
saslPassword:
pass123
saslMechanisms:
PLAIN
securityProtocol:
SASL_SSL
readTimeout:
10
# read message timeout in seconds
ssl:
enabled:
true
# Whether to support kafka secure connection mode
tlsCert:
/milvus/secrets/kafka_client.pem
# path to client's public key
tlsKey:
/milvus/secrets/kafka_client.key
# path to client's private key
tlsCACert:
/milvus/secrets/ca-cert
# file or directory path to CA certificate
tlsKeyPassword:
abcdefgh
# private key passphrase for use with private key, if any