在 Docker 中运行 Milvus (Linux)
本页说明如何在 Docker 中启动 Milvus 实例。
前提条件
安装 Docker
。
安装前
请检查硬件和软件要求
。
在 Docker 中安装 Milvus
Milvus 提供了一个安装脚本，可将其安装为 docker 容器。该脚本可在
Milvus 存储库中
找到。要在 Docker 中安装 Milvus，只需运行
#
Download the installation script
$
curl -sfL https://raw.githubusercontent.com/milvus-io/milvus/master/scripts/standalone_embed.sh -o standalone_embed.sh
#
Start the Docker container
$
bash standalone_embed.sh start
版本 2.6.13 的新功能：
流节点
增强数据处理能力
啄木鸟 MQ
：改进了消息队列，减少了维护开销，详情请参阅
使用啄木鸟
优化架构
：整合组件，提高性能
请始终下载最新脚本，以确保获得最新配置和架构改进。
如果要在独立部署模式下使用
备份
，建议使用
Docker Compose
部署方法。
如果在拉取镜像时遇到任何问题，请通过
community@zilliz.com
联系我们并提供有关问题的详细信息，我们将为您提供必要的支持。
运行安装脚本后
一个名为 Milvus 的 docker 容器已在
19530
端口启动。
嵌入式 etcd 与 Milvus 安装在同一个容器中，服务端口为
2379
。它的配置文件被映射到当前文件夹中的
embedEtcd.yaml。
要更改 Milvus 的默认配置，请将您的设置添加到当前文件夹中的
user.yaml
文件，然后重新启动服务。
Milvus 数据卷被映射到当前文件夹中的
volumes/milvus
。
你可以访问 Milvus WebUI，网址是
http://127.0.0.1:9091/webui/
，了解有关 Milvus 实例的更多信息。有关详细信息，请参阅
Milvus WebUI
。
(可选）更新 Milvus 配置
您可以修改当前文件夹下
user.yaml
文件中的 Milvus 配置。例如，要将
proxy.healthCheckTimeout
更改为
1000
ms，可按如下方式修改文件：
cat << EOF > user.yaml
#
Extra config to override default milvus.yaml
proxy:
  healthCheckTimeout: 1000 # ms, the interval that to do component healthy check
EOF
然后按如下步骤重启服务：
$
bash standalone_embed.sh restart
有关适用的配置项，请参阅
系统配置
。
升级 Milvus
您可以使用内置的升级命令升级到最新版本的 Milvus。它会自动下载最新配置和 Milvus 映像：
#
Upgrade Milvus to the latest version
$
bash standalone_embed.sh upgrade
升级命令会自动
下载带有更新配置的最新安装脚本
调用最新的 Milvus Docker 映像
使用新版本重启容器
保留现有数据和配置
这是升级 Milvus 独立部署的推荐方法。
停止和删除 Milvus
你可以按如下方式停止和删除该容器
#
Stop Milvus
$
bash standalone_embed.sh stop
#
Delete Milvus data
$
bash standalone_embed.sh delete
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
在云上部署你的 Milvu 集群：
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