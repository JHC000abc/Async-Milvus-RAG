使用 Docker Compose 运行支持 GPU 的 Milvus
本页说明如何使用 Docker Compose 启动支持 GPU 的 Milvus 实例。
前提条件
安装 Docker
。
安装前
请检查硬件和软件要求
。
如果在拉动映像时遇到任何问题，请通过
community@zilliz.com
联系我们并提供有关问题的详细信息，我们将为您提供必要的支持。
安装 Milvus
要使用 Docker Compose 安装支持 GPU 的 Milvus，请按照以下步骤操作。
1.下载并配置 YAML 文件
下载
milvus-standalone-docker-compose-gpu.yml
并手动将其保存为 docker-compose.yml，或使用以下命令。
$
wget https://github.com/milvus-io/milvus/releases/download/v2.6.13/milvus-standalone-docker-compose-gpu.yml -O docker-compose.yml
您需要对 YAML 文件中单机服务的环境变量做如下修改：
要为 Milvus 分配特定的 GPU 设备，请找到
standalone
服务定义中的
deploy.resources.reservations.devices[0].devices_ids
字段，并将其值替换为所需 GPU 的 ID。您可以使用英伟达™（NVIDIA®）GPU 显示驱动程序随附的
nvidia-smi
工具来确定 GPU 设备的 ID。Milvus 支持多个 GPU 设备。
为 Milvus 分配单个 GPU 设备：
...
standalone:
...
deploy:
resources:
reservations:
devices:
-
driver:
nvidia
capabilities:
[
"gpu"
]
device_ids:
[
"0"
]
...
将多个 GPU 设备分配给 Milvus：
...
standalone:
...
deploy:
resources:
reservations:
devices:
-
driver:
nvidia
capabilities:
[
"gpu"
]
device_ids:
[
'0'
,
'1'
]
...
2.启动 Milvus
在保存 docker-compose.yml 的目录下，通过运行启动 Milvus：
$
sudo
docker compose up -d
Creating milvus-etcd  ... done
Creating milvus-minio ... done
Creating milvus-standalone ... done
如果运行上述命令失败，请检查系统是否安装了 Docker Compose V1。如果是这种情况，建议你根据
本页
的说明迁移到 Docker Compose V2。
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
docker compose ps
Name                     Command                  State                            Ports
--------------------------------------------------------------------------------------------------------------------
milvus-etcd         etcd -advertise-client-url ...   Up             2379/tcp, 2380/tcp
milvus-minio        /usr/bin/docker-entrypoint ...   Up (healthy)   9000/tcp
milvus-standalone   /tini -- milvus run standalone   Up             0.0.0.0:19530->19530/tcp, 0.0.0.0:9091->9091/tcp
你还可以访问 Milvus WebUI，网址是
http://127.0.0.1:9091/webui/
，了解有关 Milvus 实例的更多信息。详情请参阅
Milvus WebUI
。
如果在 docker-compose.yml 中为 Milvus 分配了多个 GPU 设备，可以指定哪个 GPU 设备可见或可用。
让 GPU 设备
0
对 Milvus 可见：
$
CUDA_VISIBLE_DEVICES=0 ./milvus run standalone
让 GPU 设备
0
和
1
对 Milvus 可见：
$
CUDA_VISIBLE_DEVICES=0,1 ./milvus run standalone
您可以按以下步骤停止和删除此容器。
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
配置内存池
Milvus 启动并运行后，您可以通过修改
milvus.yaml
文件中的
initMemSize
和
maxMemSize
设置来定制内存池。
milvus.yaml
文件位于 Milvus 容器内的
/milvus/configs/
目录中。
要配置内存池，请按如下方法修改
milvus.yaml
文件中的
initMemSize
和
maxMemSize
设置。
使用以下命令将
milvus.yaml
从 Milvus 容器复制到本地计算机。用实际的 Milvus 容器 ID 替换
<milvus_container_id>
。
docker cp <milvus_container_id>:/milvus/configs/milvus.yaml milvus.yaml
用你喜欢的文本编辑器打开复制的
milvus.yaml
文件。例如，使用 vim：
vim milvus.yaml
根据需要编辑
initMemSize
和
maxMemSize
设置，并保存更改：
...
gpu:
initMemSize:
0
maxMemSize:
0
...
initMemSize
:内存池的初始大小。默认为 1024。
maxMemSize
:内存池的最大容量。默认为 2048。
使用以下命令将修改后的
milvus.yaml
文件复制回 Milvus 容器。用实际的 Milvus 容器 ID 替换
<milvus_container_id>
。
docker cp milvus.yaml <milvus_container_id>:/milvus/configs/milvus.yaml
重新启动 Milvus 容器以应用更改：
docker stop <milvus_container_id>
docker start <milvus_container_id>
下一步
在 Docker 中安装 Milvus 后，你可以
查看
快速入门
，了解 Milvus 的功能。
查看
Milvus WebUI
，了解有关 Milvus 实例的更多信息。
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