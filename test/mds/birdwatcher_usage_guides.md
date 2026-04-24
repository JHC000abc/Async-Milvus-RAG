使用 Birdwatcher
本指南将指导您如何使用 Birdwatcher 查看 Milvus 的状态并进行动态配置。
启动 Birdwatcher
Birdwatcher 是一个命令行工具，您可以按以下步骤启动它：
./birdwatcher
然后会出现以下提示：
Offline >
连接到 etcd
在进行其他操作符之前，您需要使用 Birdwatcher 连接到 etcd。
使用默认设置连接
Offline > connect
Milvus(by-dev) >
从 pod 中的 Birdwatcher 进行连接
如果选择在 Kubernetes pod 中运行 Birdwatcher，首先需要获取 etcd 的 IP 地址，如下所示：
kubectl get pod my-release-etcd-0 -o 'jsonpath={.status.podIP}'
然后访问 pod 的 shell。
kubectl exec --stdin --tty birdwatcher-7f48547ddc-zcbxj -- /bin/sh
最后，使用返回的 IP 地址连接 etcd，如下所示：
Offline > connect --etcd ${ETCD_IP_ADDR}:2379
Milvus(by-dev)
使用不同的根路径连接
如果你的 Milvus 根路径与
by-dev
不同，并且提示你报告根路径不正确的错误，你可以按如下方法连接 etcd：
Offline > connect --rootPath my-release
Milvus(my-release) >
如果您不知道 Milvus 的根路径，请按如下方式连接 etcd：
Offline > connect --dry
using dry mode, ignore rootPath and metaPath
Etcd(127.0.0.1:2379) > find-milvus
1 candidates found:
my-release
Etcd(127.0.0.1:2379) > use my-release
Milvus(my-release) >
检查 Milvus 状态
你可以使用
show
命令检查 Milvus 状态。
Milvus(my-release) > show -h
Usage:
   show [command]

Available Commands:
  alias               list alias meta info
  channel-watch       display channel watching info from data coord meta store
  checkpoint          list checkpoint collection vchannels
  collection-history  display collection change history
  collection-loaded   display information of loaded collection from querycoord
  collections         list current available collection from RootCoord
  config-etcd         list configuations set by etcd source
  configurations      iterate all online components and inspect configuration
  current-version     
  database            display Database info from rootcoord meta
  index               
  partition           list partitions of provided collection
  querycoord-channel  display querynode information from querycoord cluster
  querycoord-cluster  display querynode information from querycoord cluster
  querycoord-task     display task information from querycoord
  replica             list current replica information from QueryCoord
  segment             display segment information from data coord meta store
  segment-index       display segment index information
  segment-loaded      display segment information from querycoordv1 meta
  segment-loaded-grpc list segments loaded information
  session             list online milvus components

Flags:
  -h, --help   help for show

Use " show [command] --help" for more information about a command.
列出会话
列出与 Milvus 不同组件相关的会话：
Milvus(by-dev) > show session
Session:datacoord, ServerID: 3, Version: 2.2.11, Address: 10.244.0.8:13333
Session:datanode, ServerID: 6, Version: 2.2.11, Address: 10.244.0.8:21124
Session:indexcoord, ServerID: 4, Version: 2.2.11, Address: 10.244.0.8:31000
Session:indexnode, ServerID: 5, Version: 2.2.11, Address: 10.244.0.8:21121
Session:proxy, ServerID: 8, Version: 2.2.11, Address: 10.244.0.8:19529
Session:querycoord, ServerID: 7, Version: 2.2.11, Address: 10.244.0.8:19531
Session:querynode, ServerID: 2, Version: 2.2.11, Address: 10.244.0.8:21123
Session:rootcoord, ServerID: 1, Version: 2.2.11, Address: 10.244.0.8:53100
在命令输出中，
show session
列出的每个会话条目都对应当前处于活动状态并在
etcd
中注册的节点或服务。
检查数据库和 Collections
可以列出所有数据库和 Collection。
列出数据库
在命令输出中，您可以找到每个数据库的信息。
Milvus(by-dev) > show database
=============================
ID: 1   Name: default
TenantID:        State: DatabaseCreated
--- Total Database(s): 1
列出 Collections
在命令输出中，可以找到每个 Collection 的详细信息。
Milvus(by-dev) > show collections
================================================================================
DBID: 1
Collection ID: 443407225551410746       Collection Name: medium_articles_2020
Collection State: CollectionCreated     Create Time: 2023-08-08 09:27:08
Fields:
- Field ID: 0   Field Name: RowID       Field Type: Int64
- Field ID: 1   Field Name: Timestamp   Field Type: Int64
- Field ID: 100         Field Name: id          Field Type: Int64
        - Primary Key: true, AutoID: false
- Field ID: 101         Field Name: title       Field Type: VarChar
        - Type Param max_length: 512
- Field ID: 102         Field Name: title_vector        Field Type: FloatVector
        - Type Param dim: 768
- Field ID: 103         Field Name: link        Field Type: VarChar
        - Type Param max_length: 512
- Field ID: 104         Field Name: reading_time        Field Type: Int64
- Field ID: 105         Field Name: publication         Field Type: VarChar
        - Type Param max_length: 512
- Field ID: 106         Field Name: claps       Field Type: Int64
- Field ID: 107         Field Name: responses   Field Type: Int64
Enable Dynamic Schema: false
Consistency Level: Bounded
Start position for channel by-dev-rootcoord-dml_0(by-dev-rootcoord-dml_0_443407225551410746v0): [1 0 28 175 133 76 39 6]
--- Total collections:  1        Matched collections:  1
--- Total channel: 1     Healthy collections: 1
================================================================================
查看特定 Collections
您可以通过指定某个 Collection 的 ID 来查看该 Collection。
Milvus(by-dev) > show collection-history --id 443407225551410746
================================================================================
DBID: 1
Collection ID: 443407225551410746       Collection Name: medium_articles_2020
Collection State: CollectionCreated     Create Time: 2023-08-08 09:27:08
Fields:
- Field ID: 0   Field Name: RowID       Field Type: Int64
- Field ID: 1   Field Name: Timestamp   Field Type: Int64
- Field ID: 100         Field Name: id          Field Type: Int64
        - Primary Key: true, AutoID: false
- Field ID: 101         Field Name: title       Field Type: VarChar
        - Type Param max_length: 512
- Field ID: 102         Field Name: title_vector        Field Type: FloatVector
        - Type Param dim: 768
- Field ID: 103         Field Name: link        Field Type: VarChar
        - Type Param max_length: 512
- Field ID: 104         Field Name: reading_time        Field Type: Int64
- Field ID: 105         Field Name: publication         Field Type: VarChar
        - Type Param max_length: 512
- Field ID: 106         Field Name: claps       Field Type: Int64
- Field ID: 107         Field Name: responses   Field Type: Int64
Enable Dynamic Schema: false
Consistency Level: Bounded
Start position for channel by-dev-rootcoord-dml_0(by-dev-rootcoord-dml_0_443407225551410746v0): [1 0 28 175 133 76 39 6]
查看所有加载的 Collections
您可以让 Birdwatcher 过滤所有已加载的 Collection。
Milvus(by-dev) > show collection-loaded
Version: [>= 2.2.0]     CollectionID: 443407225551410746
ReplicaNumber: 1        LoadStatus: Loaded
--- Collections Loaded: 1
列出某个 Collection 的所有通道检查点
您可以让 Birdwatcher 列出特定 Collections 的所有检查点。
Milvus(by-dev) > show checkpoint --collection 443407225551410746
vchannel by-dev-rootcoord-dml_0_443407225551410746v0 seek to 2023-08-08 09:36:09.54 +0000 UTC, cp channel: by-dev-rootcoord-dml_0_443407225551410746v0, Source: Channel Checkpoint
检查索引详情
运行以下命令详细列出所有索引文件。
Milvus(by-dev) > show index
*************2.1.x***************
*************2.2.x***************
==================================================================
Index ID: 443407225551410801    Index Name: _default_idx_102    CollectionID:443407225551410746
Create Time: 2023-08-08 09:27:19.139 +0000      Deleted: false
Index Type: HNSW        Metric Type: L2
Index Params: 
==================================================================
列出分区
运行以下命令可列出特定 Collections 中的所有分区。
Milvus(by-dev) > show partition --collection 443407225551410746
Parition ID: 443407225551410747 Name: _default  State: PartitionCreated
--- Total Database(s): 1
检查通道状态
运行以下命令查看通道状态
Milvus(by-dev) > show channel-watch
=============================
key: by-dev/meta/channelwatch/6/by-dev-rootcoord-dml_0_443407225551410746v0
Channel Name:by-dev-rootcoord-dml_0_443407225551410746v0         WatchState: WatchSuccess
Channel Watch start from: 2023-08-08 09:27:09 +0000, timeout at: 1970-01-01 00:00:00 +0000
Start Position ID: [1 0 28 175 133 76 39 6], time: 1970-01-01 00:00:00 +0000
Unflushed segments: []
Flushed segments: []
Dropped segments: []
--- Total Channels: 1
列出所有副本和分区
列出所有副本
运行以下命令列出所有副本及其对应的 Collections。
Milvus(by-dev) > show replica
================================================================================
ReplicaID: 443407225685278721 CollectionID: 443407225551410746 version:>=2.2.0
All Nodes:[2]
列出所有网段
运行以下命令列出所有分段及其状态
SegmentID: 443407225551610865 State: Flushed, Row Count:5979
--- Growing: 0, Sealed: 0, Flushed: 1
--- Total Segments: 1, row count: 5979
运行以下命令详细列出所有加载的段。对于 Milvus 2.1.x，请使用
show segment-loaded
代替。
Milvus(by-dev) > show segment-loaded-grpc
===========
ServerID 2
Channel by-dev-rootcoord-dml_0_443407225551410746v0, collection: 443407225551410746, version 1691486840680656937
Leader view for channel: by-dev-rootcoord-dml_0_443407225551410746v0
Growing segments number: 0 , ids: []
SegmentID: 443407225551610865 CollectionID: 443407225551410746 Channel: by-dev-rootcoord-dml_0_443407225551410746v0
Sealed segments number: 1
列出配置
您可以让 Birdwatcher 列出 Milvus 各组件的当前配置。
Milvus(by-dev) > show configurations
client nil Session:proxy, ServerID: 8, Version: 2.2.11, Address: 10.244.0.8:19529
Component rootcoord-1
rootcoord.importtaskexpiration: 900
rootcoord.enableactivestandby: false
rootcoord.importtaskretention: 86400
rootcoord.maxpartitionnum: 4096
rootcoord.dmlchannelnum: 16
rootcoord.minsegmentsizetoenableindex: 1024
rootcoord.port: 53100
rootcoord.address: localhost
rootcoord.maxdatabasenum: 64
Component datacoord-3
...
querynode.gracefulstoptimeout: 30
querynode.cache.enabled: true
querynode.cache.memorylimit: 2147483648
querynode.scheduler.maxreadconcurrentratio: 2
或者，您也可以访问每个 Milvus 组件，查找其配置。下面演示如何列出 ID 为 7 的 QueryCoord 的配置。
Milvus(by-dev) > show session
Session:datacoord, ServerID: 3, Version: 2.2.11, Address: 10.244.0.8:13333
Session:datanode, ServerID: 6, Version: 2.2.11, Address: 10.244.0.8:21124
Session:indexcoord, ServerID: 4, Version: 2.2.11, Address: 10.244.0.8:31000
Session:indexnode, ServerID: 5, Version: 2.2.11, Address: 10.244.0.8:21121
Session:proxy, ServerID: 8, Version: 2.2.11, Address: 10.244.0.8:19529
Session:querycoord, ServerID: 7, Version: 2.2.11, Address: 10.244.0.8:19531
Session:querynode, ServerID: 2, Version: 2.2.11, Address: 10.244.0.8:21123
Session:rootcoord, ServerID: 1, Version: 2.2.11, Address: 10.244.0.8:53100

Milvus(by-dev) > visit querycoord 7
QueryCoord-7(10.244.0.8:19531) > configuration
Key: querycoord.enableactivestandby, Value: false
Key: querycoord.channeltasktimeout, Value: 60000
Key: querycoord.overloadedmemorythresholdpercentage, Value: 90
Key: querycoord.distpullinterval, Value: 500
Key: querycoord.checkinterval, Value: 10000
Key: querycoord.checkhandoffinterval, Value: 5000
Key: querycoord.taskexecutioncap, Value: 256
Key: querycoord.taskmergecap, Value: 8
Key: querycoord.autohandoff, Value: true
Key: querycoord.address, Value: localhost
Key: querycoord.port, Value: 19531
Key: querycoord.memoryusagemaxdifferencepercentage, Value: 30
Key: querycoord.refreshtargetsintervalseconds, Value: 300
Key: querycoord.balanceintervalseconds, Value: 60
Key: querycoord.loadtimeoutseconds, Value: 1800
Key: querycoord.globalrowcountfactor, Value: 0.1
Key: querycoord.scoreunbalancetolerationfactor, Value: 0.05
Key: querycoord.reverseunbalancetolerationfactor, Value: 1.3
Key: querycoord.balancer, Value: ScoreBasedBalancer
Key: querycoord.autobalance, Value: true
Key: querycoord.segmenttasktimeout, Value: 120000
备份指标
您可以让 Birdwatcher 备份所有组件的指标。
Milvus(my-release) > backup
Backing up ... 100%(2452/2451)
backup etcd for prefix  done
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
http://10.244.0.10:9091/metrics
backup for prefix done, stored in file: bw_etcd_ALL.230810-075211.bak.gz
然后您可以在启动 Birdwatcher 的目录中查看该文件。
探测 Collections
您可以让 Birdwatcher 用指定的主键或模拟查询探测已加载的 Collections 的状态。
探查带有已知主键的 Collections
在
probe
命令中，应使用
pk
标志指定主键，使用
collection
标志指定集合 ID。
Milvus(by-dev) > probe pk --pk 110 --collection 442844725212299747
PK 110 found on segment 442844725212299830
Field id, value: &{long_data:<data:110 > }
Field title, value: &{string_data:<data:"Human Resources Datafication" > }
Field title_vector, value: &{dim:768 float_vector:<data:0.022454707 data:0.007861045 data:0.0063843643 data:0.024065714 data:0.013782166 data:0.018483251 data:-0.026526336 ... data:-0.06579628 data:0.00033906146 data:0.030992996 data:-0.028134001 data:-0.01311325 data:0.012471594 > }
Field article_meta, value: &{json_data:<data:"{\"link\":\"https:\\/\\/towardsdatascience.com\\/human-resources-datafication-d44c8f7cb365\",\"reading_time\":6,\"publication\":\"Towards Data Science\",\"claps\":256,\"responses\":0}" > }
使用模拟查询探测所有集合
您还可以让 Birdwatcher 使用模拟查询探测所有集合。
Milvus(by-dev) > probe query
probing collection 442682158191982314
Found vector field vector(103) with dim[384], indexID: 442682158191990455
failed to generated mock request probing index type IVF_FLAT not supported yet
probing collection 442844725212086932
Found vector field title_vector(102) with dim[768], indexID: 442844725212086936
Shard my-release-rootcoord-dml_1_442844725212086932v0 leader[298] probe with search success.
probing collection 442844725212299747
Found vector field title_vector(102) with dim[768], indexID: 442844725212299751
Shard my-release-rootcoord-dml_4_442844725212299747v0 leader[298] probe with search success.
probing collection 443294505839900248
Found vector field vector(101) with dim[256], indexID: 443294505839900251
Shard my-release-rootcoord-dml_5_443294505839900248v0 leader[298] probe with search success.