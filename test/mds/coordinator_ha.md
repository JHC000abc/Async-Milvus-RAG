协调器 HA
如
Milvus 架构
所示，Milvus 由许多组件组成，并以分布式方式工作。在所有组件中，Milvus 通过
扩大和缩小
节点来确保工作者的高可用性，使协调者成为链条中唯一的薄弱环节。
概述
在 2.2.3 版中，Milvus 为协调器实现了高可用性，使其在主动-备用模式下工作，减轻了可能导致服务不可用的单点故障（SpoF）。
协调器 HA
上图说明了协调器如何在主动-备用模式下工作。当一对协调器启动时，它们会使用自己的服务器 ID 向 etcd 注册，并竞争主动角色。成功从 etcd 租用主动角色的协调器将开始提供服务，而这对协调器中的其他协调器将保持待机状态，观察主动角色，并随时准备在主动协调器死亡时提供服务。
启用协调器 HA
使用 Helm
要启动多个协调器并让它们以主动-备用模式工作，应在
values.yaml
文件中做出以下更改。
将
xxxCoordinator.replicas
设置为
2
。
将
xxxCoordinator.activeStandby.enabled
设置为
true
。
以下代码片段以 RootCoord 为例。你也可以对其他类型的协调器做同样的操作。
rootCoordinator:
enabled:
true
# You can set the number of replicas greater than 1 only if you also need to set activeStandby.enabled to true.
replicas:
2
# Otherwise, remove this configuration item.
resources:
{}
nodeSelector:
{}
affinity:
{}
tolerations:
[]
extraEnv:
[]
heaptrack:
enabled:
false
profiling:
enabled:
false
# Enable live profiling
activeStandby:
enabled:
true
# Set this to true to have RootCoordinators work in active-standby mode.
使用 Docker
要启动多个协调器并让它们在主动-备用模式下工作，可以在用于启动 Milvus 集群的
docker-compose
文件中添加一些定义。
下面的代码片段以 RootCoord 为例。其他类型的协调器也可以这样做。
rootcoord:
container_name:
milvus-rootcoord
image:
milvusdb/milvus:v2.2.3
command:
[
"milvus"
,
"run"
,
"rootcoord"
]
environment:
ETCD_ENDPOINTS:
etcd:2379
MINIO_ADDRESS:
minio:9000
PULSAR_ADDRESS:
pulsar://pulsar:6650
ROOT_COORD_ADDRESS:
rootcoord:53100
# add ROOT_COORD_ENABLE_ACTIVE_STANDBY to enable active standby
ROOT_COORD_ENABLE_ACTIVE_STANDBY:
true
depends_on:
-
"etcd"
-
"pulsar"
-
"minio"
#   add the following to have RootCoords work in active-standby mode
#   rootcoord-1:
#    container_name: milvus-rootcoord-1
#    image: milvusdb/milvus:v2.2.3
#    command: ["milvus", "run", "rootcoord"]
#    environment:
#      ETCD_ENDPOINTS: etcd:2379
#      MINIO_ADDRESS: minio:9000
#      PULSAR_ADDRESS: pulsar://pulsar:6650
#      ROOT_COORD_ADDRESS: rootcoord-1:53100
#      # add ROOT_COORD_ENABLE_ACTIVE_STANDBY to enable active standby
#      ROOT_COORD_ENABLE_ACTIVE_STANDBY: true
#    depends_on:
#      - "etcd"
#      - "pulsar"
#      - "minio"
使用 Mac/Linux shell
要启动多个协调器，并让它们以活动-待机模式工作，你可以
下载 Milvus 源代码到本地硬盘，然后按如下方法
从源代码启动 Milvus 集群
：
sudo ./scripts/start_cluster.sh
在本步骤结束时，Milvus 运行时每种类型只有一个协调器。
更新
milvus.yaml
以更改每种类型协调器的端口号。下面以
rootCoord
为例。
rootCoord:
address:
localhost
port:
53100
# change to 53001
启动备用协调器。
sudo nohup ./bin/milvus run rootcoord > /tmp/rootcoord2.log 2>&1 &
在此步骤结束时，运行以下命令验证是否存在两个协调程序。
ps aux|grep milvus
输出结果应类似于
>
ps aux|grep milvus
root        12813   0.7 0.2 410709648   82432   ??  S   5:18PM  0:33.28 ./bin/milvus run rootcoord
root        12816   0.5 0.2 409487968   62352   ??  S   5:18PM  0:22.69 ./bin/milvus run proxy
root        17739   0.1 0.3 410289872   91792 s003  SN  6:01PM  0:00.30 ./bin/milvus run rootcoord
...
备用协调器每十秒输出一条日志记录，如下所示：
[INFO] [sessionutil/session_util.go:649] ["serverName: rootcoord is in STANDBY ..."]
杀死一对协调器中的主动协调器，观察备用协调器的行为。
您可以发现，备用协调程序接管主动角色需要 60 秒。
[2022/09/21 11:58:33.855 +08:00] [DEBUG] [sessionutil/session_util.go:677] ["watch the ACTIVE key"] [DELETE="key:\"by-dev/meta/session/rootcoord\" mod_revision:167 "]
[2022/09/21 11:58:33.856 +08:00] [DEBUG] [sessionutil/session_util.go:677] ["watch the ACTIVE key"] [DELETE="key:\"by-dev/meta/session/rootcoord-15\" mod_revision:167 "]
[2022/09/21 11:58:33.856 +08:00] [INFO] [sessionutil/session_util.go:683] ["stop watching ACTIVE key"]
[2022/09/21 11:58:33.856 +08:00] [INFO] [sessionutil/session_util.go:655] ["start retrying to register as ACTIVE service..."]
[2022/09/21 11:58:33.859 +08:00] [INFO] [sessionutil/session_util.go:641] ["register ACTIVE service successfully"] [ServerID=19]
[2022/09/21 11:58:33.859 +08:00] [INFO] [sessionutil/session_util.go:690] ["quit STANDBY mode, this node will become ACTIVE"]
[2022/09/21 11:58:33.859 +08:00] [INFO] [rootcoord/root_coord.go:638] ["rootcoord switch from standby to active, activating"]
[2022/09/21 11:58:33.859 +08:00] [INFO] [rootcoord/root_coord.go:306] ["RootCoord Register Finished"]
[2022/09/21 11:58:33.859 +08:00] [DEBUG] [rootcoord/service.go:148] ["RootCoord start done ..."]
[2022/09/21 11:58:33.859 +08:00] [DEBUG] [components/root_coord.go:58] ["RootCoord successfully started"]
相关配置项目
协调器 HA 默认为禁用。您可以通过更改 Milvus 配置文件中的以下项目手动启用该功能。
rootCoord.activeStandby.enabled
queryCoord.activeStandby.enabled
dataCoord.activeStandby.enabled
限制
目前，主动服务和备用服务之间没有很强的一致性保证。因此，备用协调器在接管主动角色时需要重新加载元数据。
Etcd 只有在当前会话超时后才会释放租约。会话超时默认为 60 秒。因此，从活动协调器死亡到备用协调器接管活动角色之间有 60 秒的间隔。