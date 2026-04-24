导入数据
本页演示导入准备好的数据的步骤。
开始之前
您已经准备好数据并将其放入 Milvus 存储桶。
如果没有，您应该先使用
RemoteBulkWriter
准备数据，并确保准备好的数据已经传输到与您的 Milvus 实例一起启动的 MinIO 实例上的 Milvus 数据桶中。有关详细信息，请参阅
准备源数据
。
您已经使用用于准备数据的 Schema 创建了一个 Collections。如果没有，请参阅
管理 Collections
。
下面的代码片段使用给定的 Schema 创建了一个简单的 Collections。有关参数的更多信息，请参阅
create_schema()
和
create_collection()
SDK 参考资料。
以下代码片段使用给定的 Schema 创建一个简单集合。有关参数的更多信息，请参阅
createCollection()
有关参数的更多信息，请参阅 SDK 参考资料中的
导入数据
要导入准备好的数据，必须创建如下导入任务：
Python
Java
cURL
from
pymilvus.bulk_writer
import
bulk_import

url =
f"http://127.0.0.1:19530"
# Bulk-insert data from a set of JSON files already uploaded to the MinIO server
resp = bulk_import(
    url=url,
    collection_name=
"quick_setup"
,
    files=[[
'a1e18323-a658-4d1b-95a7-9907a4391bcf/1.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/2.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/3.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/4.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/5.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/6.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/7.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/8.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/9.parquet'
],
           [
'a1e18323-a658-4d1b-95a7-9907a4391bcf/10.parquet'
]],
)

job_id = resp.json()[
'data'
][
'jobId'
]
print
(job_id)
private
static
String
bulkImport
(List<List<String>> batchFiles)
throws
InterruptedException {
MilvusImportRequest
milvusImportRequest
=
MilvusImportRequest.builder()
            .collectionName(
"quick_setup"
)
            .files(batchFiles)
            .build();
String
bulkImportResult
=
BulkImport.bulkImport(
"http://localhost:19530"
, milvusImportRequest);
    System.out.println(bulkImportResult);
JsonObject
bulkImportObject
=
new
Gson
().fromJson(bulkImportResult, JsonObject.class);
String
jobId
=
bulkImportObject.getAsJsonObject(
"data"
).get(
"jobId"
).getAsString();
    System.out.println(
"Create a bulkInert task, job id: "
+ jobId);
return
jobId;
}
public
static
void
main
(String[] args)
throws
Exception {
    List<List<String>> batchFiles = uploadData();
String
jobId
=
bulkImport(batchFiles);
}
export MILVUS_URI="localhost:19530"

curl --request POST "http://${MILVUS_URI}/v2/vectordb/jobs/import/create" \
--header "Content-Type: application/json" \
--data-raw '{
    "files": [
        [
            "/8ca44f28-47f7-40ba-9604-98918afe26d1/1.parquet"
        ],
        [
            "/8ca44f28-47f7-40ba-9604-98918afe26d1/2.parquet"
        ]
    ],
    "collectionName": "quick_setup"
}'
请求体包含两个字段：
collectionName
目标 Collections 的名称。
files
与 Milvus 实例一起启动的 MioIO 实例上相对于 Milvus 存储桶根路径的文件路径列表。可能的子列表如下：
JSON 文件
如果准备的文件是 JSON 格式，则
每个子列表都应包含单个准备的 JSON 文件的路径
。
[
"/d1782fa1-6b65-4ff3-b05a-43a436342445/1.json"
],
Parquet 文件
如果准备的文件是 Parquet 格式，则
每个子列表都应包含单个准备的 parquet 文件的路径
。
[
"/a6fb2d1c-7b1b-427c-a8a3-178944e3b66d/1.parquet"
]
可能的返回值如下：
{
"code"
:
200
,
"data"
:
{
"jobId"
:
"448707763884413158"
}
}
检查导入进度
获得导入任务 ID 后，可以按如下方式检查导入进度：
Python
Java
cURL
import
json
from
pymilvus.bulk_writer
import
get_import_progress

url =
f"http://127.0.0.1:19530"
# Get bulk-insert job progress
resp = get_import_progress(
    url=url,
    job_id=
"453265736269038336"
,
)
print
(json.dumps(resp.json(), indent=
4
))
private
static
void
getImportProgress
(String jobId)
{
while
(
true
) {
        System.out.println(
"Wait 5 second to check bulkInsert job state..."
);
try
{
            TimeUnit.SECONDS.sleep(
5
);
        }
catch
(InterruptedException e) {
break
;
        }
MilvusDescribeImportRequest
request
=
MilvusDescribeImportRequest.builder()
                .jobId(jobId)
                .build();
String
getImportProgressResult
=
BulkImport.getImportProgress(
"http://localhost:19530"
, request);
JsonObject
getImportProgressObject
=
new
Gson
().fromJson(getImportProgressResult, JsonObject.class);
String
state
=
getImportProgressObject.getAsJsonObject(
"data"
).get(
"state"
).getAsString();
String
progress
=
getImportProgressObject.getAsJsonObject(
"data"
).get(
"progress"
).getAsString();
if
(
"Failed"
.equals(state)) {
String
reason
=
getImportProgressObject.getAsJsonObject(
"data"
).get(
"reason"
).getAsString();
            System.out.printf(
"The job %s failed, reason: %s%n"
, jobId, reason);
break
;
        }
else
if
(
"Completed"
.equals(state)) {
            System.out.printf(
"The job %s completed%n"
, jobId);
break
;
        }
else
{
            System.out.printf(
"The job %s is running, state:%s progress:%s%n"
, jobId, state, progress);
        }
    }
}
public
static
void
main
(String[] args)
throws
Exception {
    List<List<String>> batchFiles = uploadData();
String
jobId
=
bulkImport(batchFiles);
    getImportProgress(jobId);
}
export MILVUS_URI="localhost:19530"

curl --request POST "http://${MILVUS_URI}/v2/vectordb/jobs/import/describe" \
--header "Content-Type: application/json" \
--data-raw '{
    "jobId": "449839014328146739"
}'
可能的返回如下
{
"code"
:
200
,
"data"
: {
"collectionName"
:
"quick_setup"
,
"completeTime"
:
"2024-05-18T02:57:13Z"
,
"details"
: [
            {
"completeTime"
:
"2024-05-18T02:57:11Z"
,
"fileName"
:
"id:449839014328146740 paths:
\"
/8ca44f28-47f7-40ba-9604-98918afe26d1/1.parquet
\"
"
,
"fileSize"
:
31567874
,
"importedRows"
:
100000
,
"progress"
:
100
,
"state"
:
"Completed"
,
"totalRows"
:
100000
},
            {
"completeTime"
:
"2024-05-18T02:57:11Z"
,
"fileName"
:
"id:449839014328146741 paths:
\"
/8ca44f28-47f7-40ba-9604-98918afe26d1/2.parquet
\"
"
,
"fileSize"
:
31517224
,
"importedRows"
:
100000
,
"progress"
:
100
,
"state"
:
"Completed"
,
"totalRows"
:
200000
}
        ],
"fileSize"
:
63085098
,
"importedRows"
:
200000
,
"jobId"
:
"449839014328146739"
,
"progress"
:
100
,
"state"
:
"Completed"
,
"totalRows"
:
200000
}
}
列出导入任务
您可以按如下方式列出相对于特定 Collections 的所有导入任务：
Python
Java
cURL
import
json
from
pymilvus.bulk_writer
import
list_import_jobs

url =
f"http://127.0.0.1:19530"
# List bulk-insert jobs
resp = list_import_jobs(
    url=url,
    collection_name=
"quick_setup"
,
)
print
(json.dumps(resp.json(), indent=
4
))
private
static
void
listImportJobs
()
{
MilvusListImportJobsRequest
listImportJobsRequest
=
MilvusListImportJobsRequest.builder().collectionName(
"quick_setup"
).build();
String
listImportJobsResult
=
BulkImport.listImportJobs(
"http://localhost:19530"
, listImportJobsRequest);
    System.out.println(listImportJobsResult);
}
public
static
void
main
(String[] args)
throws
Exception {
    listImportJobs();
}
export MILVUS_URI="localhost:19530"

curl --request POST "http://${MILVUS_URI}/v2/vectordb/jobs/import/list" \
--header "Content-Type: application/json" \
--data-raw '{
    "collectionName": "quick_setup"
}'
可能的值如下：
{
"code"
:
200
,
"data"
:
{
"records"
:
[
{
"collectionName"
:
"quick_setup"
,
"jobId"
:
"448761313698322011"
,
"progress"
:
50
,
"state"
:
"Importing"
}
]
}
}
限制
每个导入文件的大小不得超过
16 GB
。
每个导入请求的最大文件数不能超过
1024
。每个导入请求最多可导入 16GB 文件 * 1024 个文件 = 16TB 数据。
并发导入请求的最大数量限制为
1024
。
导入请求中只能指定一个分区名称。如果没有指定分区名称，数据将插入默认分区。此外，如果在目标 Collections 中设置了 Partition Key，则无法在导入请求中设置分区名称。
限制条件
导入数据前，请确保已确认以下 Milvus 行为方面的约束：
有关加载行为的限制：
如果在导入之前已经加载了一个 Collections，则可以在导入完成后使用
refresh_load
函数加载新导入的数据。
有关查询和搜索行为的限制：
在导入任务状态为 "
已完成 "
之前，保证新导入的数据对查询和搜索是不可见的。
一旦任务状态为
完成
、
如果 Collections 尚未加载，可以使用
load
函数加载新导入的数据。
如果 Collections 已加载，则可调用
load(is_refresh=True)
加载导入的数据。
有关删除行为的限制：
在导入任务状态为 "
已完成 "
之前，不保证删除成功。
在任务状态为 "
已完成
"后，则保证删除成功。
建议
我们强烈建议使用多文件导入功能，该功能允许您在单个请求中上传多个文件。这种方法不仅简化了导入过程，还能显著提高导入性能。同时，通过合并上传，您可以减少用于数据管理的时间，提高工作流程的效率。