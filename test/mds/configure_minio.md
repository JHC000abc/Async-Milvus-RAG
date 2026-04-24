MinIO 相关配置
MinIO/S3/GCS 或任何其他服务的相关配置都支持 S3 API，它负责 Milvus 的数据持久化。
为简单起见，我们在以下描述中将存储服务称为 MinIO/S3。
minio.address
描述
默认值
MinIO 或 S3 服务的 IP 地址。
环境变量：MINIO_ADDRESS
minio.address 和 minio.port 共同生成对 MinIO 或 S3 服务的有效访问。
启动 Milvus 时，MinIO 优先从环境变量 MINIO_ADDRESS 获取有效 IP 地址。
默认值适用于 MinIO 或 S3 与 Milvus 在同一网络上运行的情况。
本地主机
minio.port
说明
默认值
MinIO 或 S3 服务的端口。
9000
minio.accessKeyID
说明
默认值
MinIO 或 S3 向用户发放的授权访问密钥 ID。
环境变量：MINIO_ACCESS_KEY_ID 或 minio.accessKeyID
minio.accessKeyID 和 minio.secretAccessKey 一起用于身份验证，以访问 MinIO 或 S3 服务。
此配置的设置必须与环境变量 MINIO_ACCESS_KEY_ID 相同，因为 MINIO_ACCESS_KEY_ID 是启动 MinIO 或 S3 所必需的。
默认值适用于使用默认 docker-compose.yml 文件启动的 MinIO 或 S3 服务。
minioadmin
minio.secretAccessKey
说明
默认值
用于加密签名字符串和在服务器上验证签名字符串的密钥。它必须严格保密，只有 MinIO 或 S3 服务器和用户可以访问。
环境变量：MINIO_SECRET_ACCESS_KEY 或 minio.secretAccessKey
minio.accessKeyID 和 minio.secretAccessKey 一起用于身份验证，以访问 MinIO 或 S3 服务。
此配置的设置必须与环境变量 MINIO_SECRET_ACCESS_KEY 相同，这是启动 MinIO 或 S3 所必需的。
默认值适用于使用默认 docker-compose.yml 文件启动的 MinIO 或 S3 服务。
minioadmin
minio.useSSL
说明
默认值
控制是否通过 SSL 访问 MinIO 或 S3 服务的开关值。
假
minio.ssl.tlsCACert
说明
默认值
CACert 文件的路径
/path/to/public.crt
minio.bucketName
描述
默认值
Milvus 在 MinIO 或 S3 中存储数据的存储桶名称。
Milvus 2.0.0 不支持在多个存储桶中存储数据。
如果不存在，将创建具有此名称的存储桶。如果数据桶已经存在并且可以访问，则会直接使用。否则，将出现错误。
要在多个 Milvus 实例之间共享一个 MinIO 实例，可以考虑在启动它们之前，为每个 Milvus 实例将此更改为不同的值。有关详细信息，请参阅操作常见问题。
如果使用 Docker 在本地启动 MinIO 服务，数据将存储在本地 Docker 中。确保有足够的存储空间。
在一个 MinIO 或 S3 实例中，存储桶名称是全局唯一的。
存储桶
minio.rootPath
描述
默认值
Milvus 在 MinIO 或 S3 中存储数据的 key 的根前缀。
建议在首次启动 Milvus 前更改此参数。
若要在多个 Milvus 实例之间共享 MinIO 实例，请考虑在启动 Milvus 实例之前将其更改为每个实例的不同值。有关详细信息，请参阅操作常见问题。
如果已经存在 etcd 服务，为 Milvus 设置一个易于识别的根密钥前缀。
为已运行的 Milvus 实例更改此值可能会导致读取遗留数据失败。
文件
minio.useIAM
文件
默认值
是否使用 IAM 角色访问 S3/GCS，而不是访问/密钥
有关详细信息，请参阅
aws: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
gcp: https://cloud.google.com/storage/docs/access-control/iam
aliyun (ack): https://www.alibabacloud.com/help/en/container-service-for-kubernetes/latest/use-rrsa-to-enforce-access-control
aliyun (ecs): https://www.alibabacloud.com/help/en/elastic-compute-service/latest/attach-an-instance-ram-role
错误
minio.cloudProvider
说明
默认值
S3 的云提供商。支持"AWS"、"GCP"、"阿里云"。
Google 云存储的云提供商。支持"gcpnative"。
如果其他云提供商支持签名为 v4 的 S3 API，则可使用 "aws"，例如：minio。
如果其他云提供商支持签名为 v2 的 S3 API，则可使用 "gcp"。
如果其他云提供商使用虚拟主机风格的存储桶，您可以使用 "aliyun"。
谷歌云平台提供商可使用 "gcpnative"。使用服务帐户凭据
进行身份验证。
启用 useIAM 后，目前只支持 "aws"、"gcp "和 "aliyun"。
aws
minio.gcpCredentialJSON
说明
默认值
JSON 内容包含 gcs 服务账户凭据。
仅用于 "gcpnative "云提供商。
minio.iamEndpoint
说明
默认值
当 useIAM 为 true 且云提供商为 "aws "时，用于获取 IAM 角色凭据的自定义端点。
如果要使用 AWS 默认端点，请将其留空。
minio.logLevel
说明
默认值
aws sdk 日志的日志级别。支持的级别：关闭、致命、错误、警告、信息、调试、跟踪
致命
minio.region
描述
默认值
指定 minio 存储系统位置区域
minio.useVirtualHost
说明
默认值
是否为存储桶使用虚拟主机模式
假
minio.requestTimeoutMs
说明
默认值
请求时间的 minio 超时（毫秒
10000
minio.listObjectsMaxKeys
说明
默认值
minio ListObjects rpc 中每批请求的最大对象数、
0 表示默认使用 oss 客户端，如果 ListObjects 超时，则减少这些配置。
0