使用 Docker Compose 运行 Milvus (Linux)
本页说明如何使用 Docker Compose 在 Docker 中启动 Milvus 实例。
前提条件
安装 Docker
。
安装前
请检查硬件和软件要求
。
安装 Milvus
Milvus 在 Milvus 资源库中提供了 Docker Compose 配置文件。要使用 Docker Compose 安装 Milvus，只需运行
#
Download the configuration file
$
wget https://github.com/milvus-io/milvus/releases/download/v2.6.13/milvus-standalone-docker-compose.yml -O docker-compose.yml
#
Start Milvus
$
sudo
docker compose up -d
Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
v2.6.13 中的新功能：
增强的架构
：采用新的流节点和优化组件
更新了依赖关系
：包括最新的 MinIO 和 etcd 版本
改进了配置
：优化设置以提高性能
请务必下载最新的 Docker Compose 配置，以确保与 v2.6.13 功能兼容。
如果运行上述命令失败，请检查您的系统是否安装了 Docker Compose V1。如果是这种情况，建议您根据
本页面
的说明迁移到 Docker Compose V2。
如果您在拉取镜像时遇到任何问题，请通过
community@zilliz.com
联系我们，并提供有关问题的详细信息，我们将为您提供必要的支持。
启动 Milvus 后、
名为
milvus-
standalone
、
milvus-minio
和
milvus-etcd
的容器启动。
milvus-etcd
容器不向主机暴露任何端口，并将其数据映射到当前文件夹中的
volumes/etcd
。
milvus-minio
容器使用默认身份验证凭据在本地为端口
9090
和
9091
提供服务，并将其数据映射到当前文件夹中的
volumes/minio
。
Milvus-standalone
容器使用默认设置为本地
19530
端口提供服务，并将其数据映射到当前文件夹中的
volumes/milvus
。
你可以使用以下命令检查容器是否启动并运行：
$
sudo
docker-compose ps
Name                     Command                  State                            Ports
--------------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -advertise-client-url ...   Up             2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp, 0.0.0.0:9091->9091/tcp
你还可以访问 Milvus WebUI，网址是
http://127.0.0.1:9091/webui/
，了解有关 Milvus 实例的更多信息。有关详细信息，请参阅
Milvus WebUI
。
(可选）更新 Milvus 配置
要根据需要更新 Milvus 配置，需要修改
milvus-standalone
容器中的
/milvus/configs/user.yaml
文件。
访问
milvus-standalone
容器。
docker exec -it milvus-standalone bash
添加额外配置以覆盖默认配置。 以下假设您需要覆盖默认的
proxy.healthCheckTimeout
。有关适用的配置项，请参阅
系统配置
。
cat << EOF > /milvus/configs/user.yaml
#
Extra config to override default milvus.yaml
proxy:
  healthCheckTimeout: 1000 # ms, the interval that to do component healthy check
EOF
重新启动
milvus-standalone
容器以应用更改。
docker restart milvus-standalone
停止和删除 Milvus
您可以按如下步骤停止和删除此容器
#
Stop Milvus
$
sudo
docker compose down
#
Delete service data
$
sudo
rm
-rf volumes
下一步
在 Docker 中安装 Milvus 后，你可以
查看
快速入门
，了解 Milvus 的功能。
了解 Milvus 的基本操作：
管理数据库
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
使用 Helm 图表升级 Milvus
。
扩展你的 Milvus 集群
。
在云上部署你的 Milvus 集群：
亚马逊 EKS
谷歌云
微软 Azure
探索
Milvus WebUI
，一个用于 Milvus 可观察性和管理的直观 Web 界面。
探索
Milvus 备份
，一个用于 Milvus 数据备份的开源工具。
探索
Birdwatcher
，用于调试 Milvus 和动态配置更新的开源工具。
探索
Attu
，一个用于直观管理 Milvus 的开源图形用户界面工具。
使用 Prometheus 监控 Milvus
。