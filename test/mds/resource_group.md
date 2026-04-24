管理资源组
在 Milvus 中，您可以使用资源组将某些查询节点与其他节点物理隔离。本指南将向您介绍如何创建和管理自定义资源组，以及如何在资源组之间传输节点。
什么是资源组
一个资源组可以容纳 Milvus 集群中的多个或全部查询节点。如何在资源组之间分配查询节点，由您根据最合理的方式来决定。例如，在多集合场景中，可以为每个资源组分配适当数量的查询节点，并将集合加载到不同的资源组中，这样每个集合中的操作与其他集合中的操作在物理上是独立的。
请注意，Milvus 实例在启动时会维护一个默认资源组来容纳所有查询节点，并将其命名为
__default_resource_group
。
从 2.4.1 版开始，Milvus 提供了声明式资源组 API，而旧的资源组 API 已被弃用。新的声明式 API 使用户能够实现惰性，从而更轻松地在云原生环境中进行二次开发。
资源组的概念
资源组由资源组 config 描述：
{
"requests"
:
{
"nodeNum"
:
1
}
,
"limits"
:
{
"nodeNum"
:
1
}
,
"transfer_from"
:
[
{
"resource_group"
:
"rg1"
}
]
,
"transfer_to"
:
[
{
"resource_group"
:
"rg2"
}
]
}
requests
属性指定了资源组必须满足的条件。
limits
属性指定资源组的最大限制。
transfer_from
和
transfer_to
属性分别描述了资源组应优先从哪些资源组获取资源，以及应向哪些资源组转移资源。
一旦资源组的配置发生变化，Milvus 会根据新的配置尽可能调整当前查询节点的资源，确保所有资源组最终满足以下条件：
.requests.nodeNum < nodeNumOfResourceGroup < .limits.nodeNum.
以下情况除外：
当 Milvus 集群中的 QueryNodes 数量不足时，即
NumOfQueryNode < sum(.requests.nodeNum)
，总会有资源组没有足够的 QueryNodes。
当 Milvus 集群中的 QueryNodes 数量过多时，即
NumOfQueryNode > sum(.limits.nodeNum)
，多余的 QueryNodes 总是会先被放置在__default_
resource
_group。
当然，如果集群中的 QueryNodes 数量发生变化，Milvus 会不断尝试调整以满足最终条件。因此，可以先应用资源组配置更改，然后再执行 QueryNode 扩展。
使用声明式 api 管理资源组
本页面上的所有代码示例都在 PyMilvus 2.6.10 中。运行这些示例之前，请升级您的 PyMilvus 安装。
创建资源组。
要创建资源组，请在连接到 Milvus 实例后运行以下代码。以下代码段假定
default
是 Milvus 连接的别名。
import
pymilvus
# A resource group name should be a string of 1 to 255 characters, starting with a letter or an underscore (_) and containing only numbers, letters, and underscores (_).
name =
"rg"
node_num =
0
# create a resource group that exactly hold no query node.
try
:
    milvus_client.create_resource_group(name, config=ResourceGroupConfig(
        requests={
"node_num"
: node_num},
        limits={
"node_num"
: node_num},
    ))
print
(
f"Succeeded in creating resource group
{name}
."
)
except
Exception:
print
(
"Failed to create the resource group."
)
列出资源组。
创建资源组后，就可以在资源组列表中看到它。
要查看 Milvus 实例中的资源组列表，请执行以下操作：
rgs = milvus_client.list_resource_groups()
print
(
f"Resource group list:
{rgs}
"
)
# Resource group list: ['__default_resource_group', 'rg']
描述资源组。
您可以让 Milvus 以如下方式描述一个资源组：
info = milvus_client.describe_resource_group(name)
print
(
f"Resource group description:
{info}
"
)
# Resource group description:
# ResourceGroupInfo:
#   <name:rg1>,     // resource group name
#   <capacity:0>,   // resource group capacity
#   <num_available_node:1>,  // resource group node num
#   <num_loaded_replica:{}>, // collection loaded replica num in resource group
#   <num_outgoing_node:{}>, // node num which still in use by replica in other resource group
#   <num_incoming_node:{}>, // node num which is in use by replica but belong to other resource group
#   <config:{}>,            // resource group config
#   <nodes:[]>              // node detail info
在资源组之间转移节点。
您可能会注意到，所描述的资源组还没有任何查询节点。将一些节点从默认资源组转移到你创建的资源组，如下所示： 假设集群的__default_
resource
_group 中目前有 1 个查询节点，我们想将一个节点转移到创建的
rg
中。
update_resource_groups
，确保多次配置更改的原子性，因此 Milvus 不会看到中间状态。
source =
'__default_resource_group'
target =
'rg'
expected_num_nodes_in_default =
0
expected_num_nodes_in_rg =
1
try
:
    milvus_client.update_resource_groups({
        source: ResourceGroupConfig(
            requests={
"node_num"
: expected_num_nodes_in_default},
            limits={
"node_num"
: expected_num_nodes_in_default},
        ),
        target: ResourceGroupConfig(
            requests={
"node_num"
: expected_num_nodes_in_rg},
            limits={
"node_num"
: expected_num_nodes_in_rg},
        )
    })
print
(
f"Succeeded in move 1 node(s) from
{source}
to
{target}
."
)
except
Exception:
print
(
"Something went wrong while moving nodes."
)
# After a while, succeeded in moving 1 node(s) from __default_resource_group to rg.
向资源组加载 Collections 和分区。
一旦资源组中有了查询节点，就可以向该资源组加载 Collections。下面的代码段假定已经存在名为
demo
的 Collections。
from
pymilvus
import
Collection

collection_name =
"demo"
# Milvus loads the collection to the default resource group.
milvus_client.load_collection(collection_name, replica_number=
2
)
# Or, you can ask Milvus load the collection to the desired resource group.
# make sure that query nodes num should be greater or equal to replica_number
resource_groups = [
'rg'
]
milvus_client.load_collection(replica_number=
2
, _resource_groups=resource_groups)
此外，您还可以将一个分区加载到一个资源组中，并将其副本分布到多个资源组中。下面假定已经存在名为
Books
的 Collections，并且它有一个名为
Novels
的分区。
collection =
"Books"
partition =
"Novels"
# Use the load method of a collection to load one of its partition
milvus_client.load_partitions(collection, [partition], replica_number=
2
, _resource_groups=resource_groups)
请注意，
_resource_groups
是一个可选参数，如果不指定，Milvus 将把副本加载到默认资源组中的查询节点上。
要让 Milus 在单独的资源组中加载 Collections 的每个副本，请确保资源组的数量等于副本的数量。
在资源组之间传输副本。
Milvus 使用
副本
来实现分布在多个查询节点上的
网段
之间的负载平衡。您可以按以下方式将某个 Collection 的某些副本从一个资源组转移到另一个资源组：
source =
'__default_resource_group'
target =
'rg'
collection_name =
'c'
num_replicas =
1
try
:
    milvus_client.transfer_replica(source, target, collection_name, num_replicas)
print
(
f"Succeeded in moving
{num_replicas}
replica(s) of
{collection_name}
from
{source}
to
{target}
."
)
except
Exception:
print
(
"Something went wrong while moving replicas."
)
# Succeeded in moving 1 replica(s) of c from __default_resource_group to rg.
删除一个资源组。
您可以随时放弃一个没有查询节点的资源组 (
limits.node_num = 0
)。在本指南中，资源组
rg
现在有一个查询节点。您需要先将资源组
limits.node_num
的配置更改为零。
resource_group =
"rg
try:
    milvus_client.update_resource_groups({
        resource_group: ResourceGroupConfig(
            requests={"
node_num
": 0},
            limits={"
node_num
": 0},
        ),
    })
    milvus_client.drop_resource_group(resource_group)
    print(f"
Succeeded
in
dropping {resource_group}.
")
except Exception:
    print(f"
Something went wrong
while
dropping {resource_group}.
")
有关详细信息，请参阅
pymilvus 中的相关示例
。
管理集群扩展的良好做法
目前，Milvus 无法在云原生环境中独立地伸缩。不过，通过将
声明式资源组 API
与容器协调结合使用，Milvus 可以轻松实现 QueryNodes 的资源隔离和管理。 以下是在云环境中管理 QueryNodes 的良好实践：
默认情况下，Milvus 会创建一个__default_
resource
_group。该资源组不能删除，同时也作为所有 Collections 的默认加载资源组，冗余的 QueryNodes 总是分配给它。因此，我们可以创建一个待定资源组来保存未使用的 QueryNode 资源，防止 QueryNode 资源被__
default
_resource_group 占用。
此外，如果我们严格执行
sum(.requests.nodeNum) <= queryNodeNum
这一约束，就能精确控制集群中 QueryNode 的分配。下面是一个设置示例：
from
pymilvus.client.types
import
ResourceGroupConfig

_PENDING_NODES_RESOURCE_GROUP=
"__pending_nodes"
def
init_cluster
(
node_num:
int
):
print
(
f"Init cluster with
{node_num}
nodes, all nodes will be put in default resource group"
)
# create a pending resource group, which can used to hold the pending nodes that do not hold any data.
milvus_client.create_resource_group(name=_PENDING_NODES_RESOURCE_GROUP, config=ResourceGroupConfig(
        requests={
"node_num"
:
0
},
# this resource group can hold 0 nodes, no data will be load on it.
limits={
"node_num"
:
10000
},
# this resource group can hold at most 10000 nodes
))
# update default resource group, which can used to hold the nodes that all initial node in it.
milvus_client.update_resource_groups({
"__default_resource_group"
: ResourceGroupConfig(
            requests={
"node_num"
: node_num},
            limits={
"node_num"
: node_num},
            transfer_from=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
# recover missing node from pending resource group at high priority.
transfer_to=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
# recover redundant node to pending resource group at low priority.
)})
    milvus_client.create_resource_group(name=
"rg1"
, config=ResourceGroupConfig(
        requests={
"node_num"
:
0
},
        limits={
"node_num"
:
0
},
        transfer_from=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}], 
        transfer_to=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
    ))
    milvus_client.create_resource_group(name=
"rg2"
, config=ResourceGroupConfig(
        requests={
"node_num"
:
0
},
        limits={
"node_num"
:
0
},
        transfer_from=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}], 
        transfer_to=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
    ))

init_cluster(
1
)
使用上面的示例代码，我们创建了一个名为
__pending_nodes
的资源组，用于容纳更多的 QueryNodes。我们还创建了名为
rg1
和
rg2
的两个特定于用户的资源组。此外，我们还确保其他资源组优先从
_
_pending_nodes 中恢复丢失或多余的 QueryNodes。
集群扩展
假设我们有以下缩放功能：
def
scale_to
(
node_num:
int
):
# scale the querynode number in Milvus into node_num.
pass
我们可以使用 API 将特定资源组的 QueryNodes 扩展到指定数量，而不会影响其他任何资源组。
# scale rg1 into 3 nodes, rg2 into 1 nodes
milvus_client.update_resource_groups({
"rg1"
: ResourceGroupConfig(
        requests={
"node_num"
:
3
},
        limits={
"node_num"
:
3
},
        transfer_from=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
        transfer_to=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
    ),
"rg2"
: ResourceGroupConfig(
        requests={
"node_num"
:
1
},
        limits={
"node_num"
:
1
},
        transfer_from=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
        transfer_to=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
    ),
})
scale_to(
5
)
# rg1 has 3 nodes, rg2 has 1 node, __default_resource_group has 1 node.
群集向内扩展
同样，我们也可以建立缩放规则，优先从
__pending_nodes
资源组中选择 QueryNodes。这一信息可通过
describe_resource_group
API 获取。实现扩展到指定资源组的目标。
# scale rg1 from 3 nodes into 2 nodes
milvus_client.update_resource_groups({
"rg1"
: ResourceGroupConfig(
        requests={
"node_num"
:
2
},
        limits={
"node_num"
:
2
},
        transfer_from=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
        transfer_to=[{
"resource_group"
: _PENDING_NODES_RESOURCE_GROUP}],
    ),
})
# rg1 has 2 nodes, rg2 has 1 node, __default_resource_group has 1 node, __pending_nodes has 1 node.
scale_to(
4
)
# scale the node in __pending_nodes
资源组如何与多个副本交互
单个 Collections 的副本和资源组之间是 N 对 N 的关系。
当单个 Collections 的多个副本加载到一个资源组时，该资源组的 QueryNodes 会平均分配给各个副本，确保每个副本拥有的 QueryNodes 数量之差不超过 1。
下一步
要部署多租户 Milvus 实例，请阅读以下内容：
启用 RBAC
用户和角色