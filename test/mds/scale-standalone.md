扩展 Milvus Standalone
Milvus Standalone 是一种单机服务器部署方式。Milvus Standalone 的所有组件都打包到一个
Docker 镜像
中，因此部署非常方便。本主题介绍如何扩展在此模式下运行的 Milvus 实例。
前提条件
使用
Docker
或
Docker Compose
部署 Milvus Standalone 时，部署脚本 (
standalone_embed.sh
) 或配置文件 (
docker-compose.yml
) 会创建多个卷，并将它们映射到主机目录，以确保数据的持久性。
要扩展以这种方式部署的 Milvus 实例，必须停止并移除现有容器或容器堆栈，使用更新的配置设置重新部署 Milvus Standalone，并重新使用主机上的持久化数据来启动新实例。
下表列出了主机和容器之间的卷映射。
部署选项
主机路径
容器路径
Docker
$(pwd)/volumes/milvus
/var/lib/milvus
$(pwd)/embedEtcd.yaml
/milvus/configs/embedEtcd.yaml
$(pwd)/user.yaml
/milvus/configs/user.yaml
Docker Compose
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/etcd
(milvus-etcd)
/etcd
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/minio
(milvus-minio)
/minio_data
${DOCKER_VOLUME_DIRECTORY:-.}/volumes/milvus
(milvus-standalone)
/var/lib/milvus
在运行本指南中的程序之前，请确保您的数据持久存在上述主机路径中。
扩展使用 Docker 部署的实例
要扩展当前正在运行的 Milvus 实例，必须停止实例、移除容器，然后使用新的设置和持久化数据重新部署实例。
具体步骤如下：
运行
docker stats milvus-standalone
查看分配给 Milvus 实例的 CPU 和内存。输出结果应与下图类似：
CONTAINER ID   NAME                CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O         PIDS
917da667f2ff   milvus-standalone   6.10%     171.8MiB / 3.886GiB   4.32%     1.57kB / 0B   1.01GB / 1.79MB   31
在命令输出中，您可以找到 Milvus 实例的当前资源使用情况。
停止并移除容器。
$ docker stop milvus-standalone
$ docker
rm
milvus-standalone
找到
standalone_embed.sh
脚本文件，找到
docker run
命令，并添加资源限制。
...
sudo
docker
run
-d
\
--name
milvus-standalone
\
--security-opt
seccomp:unconfined
\
-e
ETCD_USE_EMBED=true
\
-e
ETCD_DATA_DIR=/var/lib/milvus/etcd
\
-e
ETCD_CONFIG_PATH=/milvus/configs/embedEtcd.yaml
\
-e
COMMON_STORAGETYPE=local
\
-v
$(pwd)/volumes/milvus:/var/lib/milvus
\
-v
$(pwd)/embedEtcd.yaml:/milvus/configs/embedEtcd.yaml
\
-v
$(pwd)/user.yaml:/milvus/configs/user.yaml
\
-p
19530
:19530
\
-p
9091
:9091
\
-p
2379
:2379
\
--health-cmd="curl
-f
http://localhost:9091/healthz"
\
--health-interval=30s
\
--health-start-period=90s
\
--health-timeout=20s
\
--health-retries=3
\
--memory="4g"
\
# New memory limit
--cpus="2.0"
\
# New CPU limit
milvusdb/milvus:v2.5.11
\
milvus
run
standalone
1
>
/dev/null
确保持久化数据与
standalone_embed.sh
脚本在同一文件夹中，并按如下步骤运行脚本：
sudo
bash standalone_embed.sh start
运行
docker stats milvus-standalone
，查看缩放后分配给 Milvus 实例的 CPU 和内存。输出结果应类似于下面的内容：
CONTAINER ID   NAME                CPU %     MEM USAGE / LIMIT   MEM %     NET I/O       BLOCK I/O        PIDS
7aea450f87ce   milvus-standalone   7.52%     210.9MiB / 4GiB     5.15%     1.05kB / 0B   610kB / 8.19kB   29
扩展使用 Docker Compose 部署的实例
要对当前运行的 Milvus 实例进行缩放，必须停止实例、移除容器堆栈，然后使用新的设置和持久化数据重新部署实例。
具体步骤如下：
运行
docker stats milvus-standalone
查看分配给 Milvus 实例的 CPU 和内存。输出结果应与下图类似：
CONTAINER ID   NAME                CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O         PIDS
917da667f2ff   milvus-standalone   6.10%     171.8MiB / 3.886GiB   4.32%     1.57kB / 0B   1.01GB / 1.79MB   31
在命令输出中，可以找到 Milvus 实例的当前资源使用情况。
停止并移除容器堆栈。
$ docker compose down
找到
docker-compose.yml
配置文件，找到独立部分并添加资源限制。
...
standalone:
container_name:
milvus-standalone
image:
milvusdb/milvus:v2.5.8
command:
[
"milvus"
,
"run"
,
"standalone"
]
deploy:
resources:
limits:
cpus:
"2"
# new cpu limits
memory:
4G
# new memory limits
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
healthcheck:
test:
[
"CMD"
,
"curl"
,
"-f"
,
"http://localhost:9091/healthz"
]
interval:
30s
start_period:
90s
timeout:
20s
retries:
3
ports:
-
"19530:19530"
-
"9091:9091"
depends_on:
-
"etcd"
-
"minio"
确保持久化数据可用，然后运行
docker compose
，如下所示：
docker compose up -d
运行
docker stats milvus-standalone
，查看缩放后分配给 Milvus 实例的 CPU 和内存。输出结果应类似于下面的内容：
CONTAINER ID   NAME                CPU %     MEM USAGE / LIMIT   MEM %     NET I/O       BLOCK I/O        PIDS
7aea450f87ce   milvus-standalone   7.52%     210.9MiB / 4GiB     5.15%     1.05kB / 0B   610kB / 8.19kB   29