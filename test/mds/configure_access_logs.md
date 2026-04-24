配置访问日志
Milvus 的访问日志功能允许服务器管理人员记录和分析用户访问行为，帮助了解查询成功率和失败原因等方面。
本指南提供在 Milvus 中配置访问日志的详细说明。
访问日志的配置取决于 Milvus 的安装方法：
Helm 安装
：在
values.yaml
中配置。有关详细信息，请参阅
使用 Helm 图表配置 Milvus
。
Docker 安装
：在
milvus.yaml
中配置。更多信息，请参阅
使用 Docker Compose 配置 Milvus
。
操作符安装
：修改配置文件中的
spec.components
。更多信息，请参阅
使用 Milvus Operator 配置 Milvus
。
配置选项
根据您的需要从三种配置选项中进行选择：
基本配置
：用于一般用途。
本地访问日志文件配置
：用于在本地存储日志。
将本地访问日志上传到 MinIO 的配置
：用于云存储和备份。
基本配置
基本配置包括启用访问日志、定义日志文件名或使用 stdout。
proxy:
accessLog:
enable:
true
# If `filename` is emtpy, logs will be printed to stdout.
filename:
""
# Additional formatter configurations...
proxy.accessLog.enable
:是否启用访问日志功能。默认为
false
。
proxy.accessLog.filename
:访问日志文件的名称。如果此参数为空，访问日志将打印到 stdout。
配置本地访问日志文件
配置访问日志文件的本地存储，参数包括本地文件路径、文件大小和旋转间隔：
proxy:
accessLog:
enable:
true
filename:
"access_log.txt"
# Name of the access log file
localPath:
"/var/logs/milvus"
# Local file path where the access log file is stored
maxSize:
500
# Max size for each single access log file. Unit: MB
rotatedTime:
24
# Time interval for log rotation. Unit: seconds
maxBackups:
7
# Max number of sealed access log files that can be retained
# Additional formatter configurations...
这些参数在
filename
不为空时指定。
proxy.accessLog.localPath
:存储访问日志文件的本地文件路径。
proxy.accessLog.maxSize
:单个访问日志文件允许的最大大小（MB）。如果日志文件大小达到此限制，将触发一个轮换进程。该过程会封存当前的访问日志文件，创建新的日志文件，并清除原始日志文件的内容。
proxy.accessLog.rotatedTime
:旋转单个访问日志文件的最大时间间隔（秒）。达到指定的时间间隔后，将触发轮换进程，创建新的访问日志文件并封存前一个文件。
proxy.accessLog.maxBackups
:可保留的密封访问日志文件的最大数量。如果封存的访问日志文件数量超过此限制，则会删除最旧的文件。
将本地访问日志文件上传到 MinIO 的配置
启用并配置将本地访问日志文件上传到 MinIO 的设置：
proxy:
accessLog:
enable:
true
filename:
"access_log.txt"
localPath:
"/var/logs/milvus"
maxSize:
500
rotatedTime:
24
maxBackups:
7
minioEnable:
true
remotePath:
"/milvus/logs/access_logs"
remoteMaxTime:
0
# Additional formatter configurations...
配置 MinIO 参数时，请确保已设置
maxSize
或
rotatedTime
。否则可能导致无法成功将本地访问日志文件上传到 MinIO。
proxy.accessLog.minioEnable
:是否将本地访问日志文件上传到 MinIO。默认为
false
。
proxy.accessLog.remotePath
:用于上传访问日志文件的对象存储路径。
proxy.accessLog.remoteMaxTime
:允许上传访问日志文件的时间间隔。如果日志文件的上传时间超过此时间间隔，文件将被删除。将值设为 0 则禁用此功能。
格式配置
所有方法使用的默认日志格式是
base
格式，它不需要特定的方法关联。不过，如果希望自定义特定方法的日志输出，可以定义自定义日志格式并将其应用于相关方法。
proxy:
accessLog:
enable:
true
filename:
"access_log.txt"
localPath:
"/var/logs/milvus"
# Define custom formatters for access logs with format and applicable methods
formatters:
# The `base` formatter applies to all methods by default
# The `base` formatter does not require specific method association
base:
# Format string; an empty string means no log output
format:
"[$time_now] [ACCESS] <$user_name: $user_addr> $method_name-$method_status-$error_code [traceID: $trace_id] [timeCost: $time_cost]"
# Custom formatter for specific methods (e.g., Query, Search)
query:
format:
"[$time_now] [ACCESS] <$user_name: $user_addr> $method_status-$method_name [traceID: $trace_id] [timeCost: $time_cost] [database: $database_name] [collection: $collection_name] [partitions: $partition_name] [expr: $method_expr]"
# Specify the methods to which this custom formatter applies
methods:
[
"Query"
,
"Search"
]
proxy.accessLog.<formatter_name>.format
:使用动态指标定义日志格式。更多信息，请参阅
支持的指标
。
proxy.accessLog.<formatter_name>.methods
:列出使用此格式的 Milvus 操作符。要获取方法名称，请参阅
Milvus 方法
中的
MilvusService
。
参考：支持的度量
指标名称
描述
$method_name
方法名称
$method_status
访问状态：
确定
或
失败
$method_expr
用于查询、搜索或删除操作的表达式
$trace_id
与访问相关的跟踪 ID
$user_addr
用户的 IP 地址
$user_name
用户名
$response_size
响应数据的大小
$error_code
Milvus 特有的错误代码
$error_msg
详细错误信息
$database_name
目标 Milvus 数据库名称
$collection_name
目标 Milvus Collections 的名称
$partition_name
目标 Milvus 分区的名称或名称
$time_cost
完成访问所需的时间
$time_now
打印访问日志的时间（通常相当于
$time_end
)
$time_start
开始访问的时间
$time_end
访问结束时间
$sdk_version
用户使用的 Milvus SDK 版本