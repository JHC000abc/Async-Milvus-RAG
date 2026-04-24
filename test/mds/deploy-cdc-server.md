部署 CDC 服务器
本指南提供部署 Milvus-CDC 服务器的分步流程。
先决条件
在部署 Milvus-CDC 服务器之前，确保满足以下条件：
Milvus 实例
：源 Milvus 和至少一个目标 Milvus 都应部署并操作符。
源和目标 Milvus 版本都必须是 2.3.2 或更高，最好是 2.4.x。我们建议源和目标 Milvus 使用相同的版本，以确保兼容性。
将目标 Milvus 的
common.ttMsgEnabled
配置设为
false
。
用不同的元和消息存储设置配置源和目标 Milvus，以防止冲突。例如，避免在多个 Milvus 实例中使用相同的 etcd 和 rootPath 配置，以及相同的 Pulsar 服务和
chanNamePrefix
。
元存储
：为 Milvus-CDC 元存储准备一个 etcd 或 MySQL 数据库。
步骤
获取 Milvus-CDC 配置文件
克隆
Milvus-CDC repo
并导航到
milvus-cdc/server/configs
目录，访问
cdc.yaml
配置文件。
git
clone
https://github.com/zilliztech/milvus-cdc.git
cd
milvus-cdc/server/configs
编辑配置文件
在
milvus-cdc/server/configs
目录中，修改
cdc.yaml
文件，自定义与 Milvus-CDC 元存储和源 Milvus 的连接详细信息相关的配置。
元存储配置
：
metaStoreConfig.storeType
:Milvus-CDC 的元存储类型。可能的值是
etcd
或
mysql
。
metaStoreConfig.etcdEndpoints
:用于连接 Milvus-CDC etcd 的地址。如果
storeType
设置为
etcd
则必须使用。
metaStoreConfig.mysqlSourceUrl
:Milvus-CDC 服务器 MySQL 数据库的连接地址。如果
storeType
设置为
mysql
，则为必填项。
metaStoreConfig.rootPath
:Milvus-CDC 元存储的根路径。此配置可实现多租户，允许多个 CDC 服务使用相同的 etcd 或 MySQL 实例，同时通过不同的根路径实现隔离。
配置示例：
# cdc meta data config
metaStoreConfig:
# the metastore type, available value: etcd, mysql
storeType:
etcd
# etcd address
etcdEndpoints:
-
localhost:2379
# mysql connection address
# mysqlSourceUrl: root:root@tcp(127.0.0.1:3306)/milvus-cdc?charset=utf8
# meta data prefix, if multiple cdc services use the same store service, you can set different rootPaths to achieve multi-tenancy
rootPath:
cdc
源 Milvus 配置：
指定源 Milvus 的连接详细信息，包括 etcd 和消息存储，以便在 Milvus-CDC 服务器和源 Milvus 之间建立连接。
sourceConfig.etcdAddress
:用于连接源 Milvus 的 etcd 的地址。更多信息，请参阅
etcd 相关配置
。
sourceConfig.etcdRootPath
:源 Milvus 在 etcd 中存储数据的键的根前缀。根据 Milvus 实例的部署方法，该值可能会有所不同：
Helm
或
Docker Compose
：默认为
by-dev
。
操作符
：默认为
<release_name>
。
replicateChan
：Milvus 复制通道名称，在 milvus.yaml 文件中为
{msgChannel.chanNamePrefix.cluster}/{msgChannel.chanNamePrefix.replicateMsg}
。
sourceConfig.pulsar
:源 Milvus 的 Pulsar 配置。如果源 Milvus 使用 Kafka 进行消息存储，请移除所有与 Pulsar 相关的配置。更多信息，请参阅
Pulsar 相关配置
。
sourceConfig.kafka.address
:Milvus 源的 Kafka 地址。如果源 Milvus 使用 Kafka 进行消息存储，则取消注释此配置。
配置示例：
# milvus-source config, these settings are basically the same as the corresponding configuration of milvus.yaml in milvus source.
sourceConfig:
# etcd config
etcdAddress:
-
localhost:2379
etcdRootPath:
by-dev
etcdMetaSubPath:
meta
# default partition name
defaultPartitionName:
_default
# read buffer length, mainly used for buffering if writing data to milvus-target is slow.
readChanLen:
10
replicateChan:
by-dev-replicate-msg
# milvus-source mq config, which is pulsar or kafka
pulsar:
address:
pulsar://localhost:6650
webAddress:
localhost:80
maxMessageSize:
5242880
tenant:
public
namespace:
default
#    authPlugin: org.apache.pulsar.client.impl.auth.AuthenticationToken
#    authParams: token:xxx
#  kafka:
#    address: 127.0.0.1:9092
编译 Milvus-CDC 服务器
保存
cdc.yaml
文件后，导航到
milvus-cdc
目录，运行以下命令之一编译服务器：
对于二进制文件
make build
对于 Docker 映像
bash build_image.sh
对于 Docker 映像，将编译后的文件挂载到容器内的
/app/server/configs/cdc.yaml
。
启动服务器
使用二进制文件
导航到包含
milvus-cdc
二进制文件的目录和包含
cdc.yaml
文件的
configs
目录，然后启动服务器：
# dir tree
.
├── milvus-cdc
# build from source code or download from release page
├── configs
│   └── cdc.yaml
# config for cdc and source milvus
# start milvus cdc
./milvus-cdc server
使用 Docker Compose：
docker compose up -d