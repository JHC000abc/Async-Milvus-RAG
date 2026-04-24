Milvus
OperatorHelmDocker
Compose
使用 Docker Compose 升级 Milvus 单机版
本指南介绍如何使用 Docker Compose 将 Milvus Standalone 部署从 v2.5.x 升级到 v2.6.13。
开始之前
v2.6.13 中的新功能
从 Milvus 2.5.x 升级到 2.6.13 涉及重大架构变更：
协调器整合
：传统的独立协调器 (
dataCoord
,
queryCoord
,
indexCoord
) 已合并为单一的协调器。
mixCoord
新组件
：引入流节点，增强数据处理能力
删除组件
：删除并合并
indexNode
此升级过程可确保向新架构的正常迁移。有关架构变化的更多信息，请参阅
Milvus 架构概述
。
系统要求
系统要求：
已安装 Docker 和 Docker Compose
通过 Docker Compose 部署 Milvus 单机版
兼容性要求：
Milvus v2.6.0-rc1 与 v2.6.13
不兼容
。不支持从候选版本直接升级。
如果您当前正在运行 v2.6.0-rc1，并需要保留数据，请参考
本社区指南
以获取迁移帮助。
在升级到 v2.6.13 之前，您
必须
升级到 v2.5.16 或更高版本。
消息队列限制
：升级到 Milvus v2.6.13 时，您必须保持当前的消息队列选择。不支持在升级过程中在不同的消息队列系统之间切换。未来版本将支持更换消息队列系统。
出于安全考虑，Milvus 在发布 v2.6.13 时将 MinIO 升级为 RELEASE.2024-12-18T13-15-44Z。
升级过程
步骤 1：升级到 v2.5.16
如果您的单机部署已运行 v2.5.16 或更高版本，请跳过此步骤。
编辑现有的
docker-compose.yaml
文件，将 Milvus 映像标记更新为 v2.5.16：
...
standalone:
container_name:
milvus-standalone
image:
milvusdb/milvus:v2.5.16
...
应用升级到 v2.5.16：
docker compose down
docker compose up -d
验证 v2.5.16 升级：
docker compose ps
步骤 2：升级至 v2.6.13
v2.5.16 成功运行后，升级到 v2.6.13：
编辑现有的
docker-compose.yaml
文件，更新 Milvus 和 MinIO 图像标签：
...
minio:
container_name:
milvus-minio
image:
minio/minio:RELEASE.2024-12-18T13-15-44Z
...
standalone:
container_name:
milvus-standalone
image:
milvusdb/milvus:v2.6.13
应用最终升级：
docker compose down
docker compose up -d
验证升级
确认单机部署正在运行新版本：
# Check container status
docker compose ps
# Check Milvus version
docker compose logs standalone | grep
"version"
下一步
你可能还想了解如何
扩展 Milvus 集群
如果你准备在云上部署你的集群：
了解如何
使用 Terraform 在亚马逊 EKS 上部署 Milvus
学习如何
使用 Kubernetes 在 GCP 上部署 Milvus 集群
了解如何
使用 Kubernetes 在 Microsoft Azure 上部署 Milvus