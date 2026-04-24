Milvus OperatorMilvus
OperatorMilvus
OperatorHelmDocker
ComposeHelmDocker
ComposeHelm
使用 Docker Compose 升级 Milvus 群集
本主题介绍如何使用 Docker Compose 升级 Milvus。
在正常情况下，你可以
通过更改映像来升级 Milvus
。不过，在从 v2.1.x 升级到 v2.6.13 之前，您需要
迁移元数据
。
消息队列限制
：升级到 Milvus v2.6.13 时，必须保持当前的消息队列选择。不支持在升级过程中在不同的消息队列系统之间切换。未来版本将支持更换消息队列系统。
通过更改映像升级 Milvus
在正常情况下，你可以按以下方法升级 Milvus：
在
docker-compose.yaml
中更改 Milvus 图像标签。
请注意，您需要更改代理、所有协调器和所有工作节点的映像标签。
...
rootcoord:
container_name:
milvus-rootcoord
image:
milvusdb/milvus:v2.6.13
...
proxy:
container_name:
milvus-proxy
image:
milvusdb/milvus:v2.6.13
...
querycoord:
container_name:
milvus-querycoord
image:
milvusdb/milvus:v2.6.13
...
querynode:
container_name:
milvus-querynode
image:
milvusdb/milvus:v2.6.13
...
indexcoord:
container_name:
milvus-indexcoord
image:
milvusdb/milvus:v2.6.13
...
indexnode:
container_name:
milvus-indexnode
image:
milvusdb/milvus:v2.6.13
...
datacoord:
container_name:
milvus-datacoord
image:
milvusdb/milvus:v2.6.13
...
datanode:
container_name:
milvus-datanode
image:
milvusdb/milvus:v2.6.13
运行以下命令执行升级。
docker compose down
docker compose up -d
迁移元数据
停止所有 Milvus 组件。
docker stop
<
milvus-component-docker-container-name
>
为元迁移准备配置文件
migrate.yaml
。
# migration.yaml
cmd:
# Option: run/backup/rollback
type:
run
runWithBackup:
true
config:
sourceVersion:
2.1
.4
# Specify your milvus version
targetVersion:
2.6
.13
backupFilePath:
/tmp/migration.bak
metastore:
type:
etcd
etcd:
endpoints:
-
milvus-etcd:2379
# Use the etcd container name
rootPath:
by-dev
# The root path where data is stored in etcd
metaSubPath:
meta
kvSubPath:
kv
运行迁移容器。
# Suppose your docker-compose run with the default milvus network,
# and you put migration.yaml in the same directory with docker-compose.yaml.
docker run --
rm
-it --network milvus -v $(
pwd
)/migration.yaml:/milvus/configs/migration.yaml milvus/meta-migration:v2.2.0 /milvus/bin/meta-migration -config=/milvus/configs/migration.yaml
使用新的 Milvus 映像重新启动 Milvus 组件。
Update the milvus
image
tag in the docker-compose
.yaml
docker compose down
docker compose up -d
下一步
你可能还想了解如何
扩展 Milvus 集群
如果你准备在云上部署集群，请学习如何在亚马逊 Eclipse 上部署 Milvus：
了解如何
使用 Terraform 在亚马逊 EKS 上部署 Milvus
学习如何
使用 Kubernetes 在 GCP 上部署 Milvus 集群
了解如何
使用 Kubernetes 在 Microsoft Azure 上部署 Milvus