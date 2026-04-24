管理 CDC 任务
捕获数据更改（CDC）任务可实现从源 Milvus 实例到目标 Milvus 实例的数据同步。它监控源操作日志，并将插入、删除和索引操作等数据变更实时复制到目标。这有助于 Milvus 部署之间的实时灾难恢复或主动-主动负载平衡。
本指南介绍如何管理 CDC 任务，包括通过 HTTP 请求创建、暂停、恢复、检索详细信息、列表和删除。
创建任务
创建 CDC 任务可将源 Milvus 中的数据更改操作同步到目标 Milvus。
创建 CDC 任务：
curl -X POST http:_//localhost:8444/cdc \
-H
"Content-Type: application/json"
\
-d
'{
  "request_type": "create",
  "request_data": {
    "milvus_connect_param": {
      "uri": "http://localhost:19530",
      "token":"root:Milvus",
      "connect_timeout": 10
    },
    "collection_infos": [
      {
        "name": "*"
      }
    ]
  }
}'
用目标 Milvus 服务器的 IP 地址替换
localhost
。
参数
：
milvus_connect_param
：目标 Milvus 的连接参数。
host
：Milvus 服务器的主机名或 IP 地址。
port：端口号
：Milvus 服务器监听的端口号。
username
：用于验证 Milvus 服务器的用户名。
password
：用于验证 Milvus 服务器的密码。
enable_tls
：是否为连接使用 TLS/SSL 加密。
connect_timeout（连接超时）
：建立连接的超时时间（秒）。
collection_infos
：要同步的 Collection。目前只支持星号
(*
)，因为 Milvus-CDC 同步的是集群级别，而不是单个 Collections。
预期响应：
{
"code"
:
200
,
"data"
:
{
"task_id"
:
"xxxx"
}
}
列出任务
列出所有已创建的 CDC 任务：
curl -X POST -H
"Content-Type: application/json"
-d
'{
  "request_type": "list"
}'
http://localhost:8444/cdc
用目标 Milvus 服务器的 IP 地址替换
localhost
。
预期响应
{
"code"
:
200
,
"data"
:
{
"tasks"
:
[
{
"task_id"
:
"xxxxx"
,
"milvus_connect_param"
:
{
"uri"
:
"http://localhost:19530"
,
"connect_timeout"
:
10
}
,
"collection_infos"
:
[
{
"name"
:
"*"
}
]
,
"state"
:
"Running"
}
]
}
}
暂停任务
要暂停 CDC 任务：
curl -X POST -H
"Content-Type: application/json"
-d
'{
  "request_type":"pause",
  "request_data": {
    "task_id": "xxxx"
  }
}'
http://localhost:8444/cdc
用目标 Milvus 服务器的 IP 地址替换
localhost
。
参数
task_id
：要暂停的 CDC 任务的 ID。
预期响应：
{
"code"
: 200,
"data"
: {}
}
恢复任务
恢复已暂停的 CDC 任务：
curl -X POST -H
"Content-Type: application/json"
-d
'{
  "request_type":"resume",
  "request_data": {
    "task_id": "xxxx"
  }
}'
http://localhost:8444/cdc
用目标 Milvus 服务器的 IP 地址替换
localhost
。
参数
task_id
：要恢复的 CDC 任务的 ID。
预期响应：
{
"code"
: 200,
"data"
: {}
}
检索任务详细信息
检索特定 CDC 任务的详细信息：
curl -X POST -H
"Content-Type: application/json"
-d
'{
  "request_type":"get",
  "request_data": {
    "task_id": "xxxx"
  }
}'
http://localhost:8444/cdc
用目标 Milvus 服务器的 IP 地址替换
localhost
。
参数
task_id
：要查询的 CDC 任务的 ID。
预期响应：
{
"code"
: 200,
"data"
: {
"Task"
: {
"collection_infos"
: [
        {
"name"
:
"*"
}
      ],
"milvus_connect_param"
: {
"connect_timeout"
: 10,
"uri"
:
"http://localhost:19530"
},
"state"
:
"Running"
,
"task_id"
:
"xxxx"
}
  }
}
删除任务
删除 CDC 任务：
curl -X POST -H
"Content-Type: application/json"
-d
'{
  "request_type":"delete",
  "request_data": {
    "task_id": "30d1e325df604ebb99e14c2a335a1421"
  }
}'
http://localhost:8444/cdc
用目标 Milvus 服务器的 IP 地址替换
localhost
。
参数
task_id
：要删除的 CDC 任务的 ID。
预期响应：
{
"code"
:
200
,
"data"
:
{
}
}