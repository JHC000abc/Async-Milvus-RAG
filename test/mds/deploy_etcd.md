使用 Docker Compose 或 Helm 配置元存储
Milvus 使用 etcd 来存储元数据。本主题介绍如何使用 Docker Compose 或 Helm 配置 etcd。
使用 Docker Compose 配置 etcd
1.配置 etcd
要使用 Docker Compose 配置 etcd，请为
milvus.yaml
文件中的
etcd
部分提供值，该文件位于 Milvus/configs 路径下。
etcd:
endpoints:
-
localhost:2379
rootPath:
by-dev
# The root path where data are stored in etcd
metaSubPath:
meta
# metaRootPath = rootPath + '/' + metaSubPath
kvSubPath:
kv
# kvRootPath = rootPath + '/' + kvSubPath
log:
# path is one of:
#  - "default" as os.Stderr,
#  - "stderr" as os.Stderr,
#  - "stdout" as os.Stdout,
#  - file path to append server logs to.
# please adjust in embedded Milvus: /tmp/milvus/logs/etcd.log
path:
stdout
level:
info
# Only supports debug, info, warn, error, panic, or fatal. Default 'info'.
use:
# please adjust in embedded Milvus: true
embed:
false
# Whether to enable embedded Etcd (an in-process EtcdServer).
data:
# Embedded Etcd only.
# please adjust in embedded Milvus: /tmp/milvus/etcdData/
dir:
default.etcd
有关
详细信息，请参阅
etcd 相关配置
。
2.运行 Milvus
运行以下命令启动使用 etcd 配置的 Milvus。
docker
compose up
配置仅在 Milvus 启动后生效。有关详细信息，请参阅
启动 Milvus
。
在 K8s 上配置 etcd
对于 K8s 上的 Milvus 群集，可以在启动 Milvus 的同一命令中配置 etcd。或者，也可以在启动 Milvus 之前，使用
milvus-helm
资源库中 /charts/milvus 路径下的
values.yml
文件配置 etcd。
下表列出了在 YAML 文件中配置 etcd 的键值。
键
描述
值
etcd.enabled
启用或禁用 etcd。
true
/
false
externalEtcd.enabled
启用或禁用外部 etcd。
true
/
false
externalEtcd.endpoints
访问 etcd 的端点。
使用 YAML 文件
使用
values.yaml
文件中的值配置
etcd
部分。
etcd:
enabled:
false
使用
values.yaml
文件中的值配置
externaletcd
部分。
externalEtcd:
enabled:
true
## the endpoints of the external etcd
endpoints:
-
<your_etcd_IP>:2379
配置完前面的部分并保存
values.yaml
文件后，运行以下命令安装使用 etcd 配置的 Milvus。
helm install <your_release_name> milvus/milvus -f values.yaml
使用命令
要安装 Milvus 并配置 etcd，请使用你的值运行以下命令。
helm install <your_release_name> milvus/milvus --set cluster.enabled=true --set etcd.enabled=false --set externaletcd.enabled=true --set externalEtcd.endpoints={<your_etcd_IP>:2379}
下一步
了解如何使用 Docker Compose 或 Helm 配置 Milvus 的其他依赖项：
使用 Docker Compose 或 Helm 配置对象存储
使用 Docker Compose 或 Helm 配置消息存储