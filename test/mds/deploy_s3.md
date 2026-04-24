使用 Docker Compose 或 Helm 配置对象存储
Milvus 默认使用 MinIO 进行对象存储，但它也支持使用
亚马逊简单存储服务（S3）
作为日志和索引文件的持久化对象存储。本主题介绍如何为 Milvus 配置 S3。如果您对 MinIO 感兴趣，可以跳过此主题。
您可以使用
Docker Compose
或在 K8s 上配置 S3。
使用 Docker Compose 配置 S3
1.配置 S3
MinIO
与 S3 兼容。要使用 Docker Compose 配置 S3，请在 Milvus/configs 路径上的
milvus.yaml
文件中提供
minio
部分的值。
minio:
address:
<your_s3_endpoint>
port:
<your_s3_port>
accessKeyID:
<your_s3_access_key_id>
secretAccessKey:
<your_s3_secret_access_key>
useSSL:
<true/false>
bucketName:
"<your_bucket_name>"
有关详细信息，请参阅
MinIO/S3 配置
。
2.完善 docker-compose.yaml
你还会删除
MINIO_ADDRESS
环境变量，用于 Milvus 服务，地址是
docker-compose.yaml
。默认情况下，milvus 会使用本地 minio 而不是外部 S3。
3.运行 Milvus
运行以下命令启动使用 S3 配置的 Milvus。
docker compose up
配置仅在 Milvus 启动后生效。有关详细信息，请参阅
启动 Milvus
。
在 K8s 上配置 S3
对于 K8s 上的 Milvus 群集，可以在启动 Milvus 的同一命令中配置 S3。或者，也可以在启动 Milvus 之前，使用
Milvus-helm
资源库中 /charts/milvus 路径下的
values.yml
文件配置 S3。
下表列出了在 YAML 文件中配置 S3 的关键字。
键
描述
值
minio.enabled
启用或禁用 MinIO。
true
/
false
externalS3.enabled
启用或禁用 S3。
true
/
false
externalS3.host
访问 S3 的端点。
externalS3.port
访问 S3 的端口。
externalS3.rootPath
S3 存储的根路径。
默认为 emtpy 字符串。
externalS3.accessKey
S3 的访问密钥 ID。
externalS3.secretKey
S3 的秘密访问密钥。
externalS3.bucketName
S3 存储桶的名称。
externalS3.useSSL
连接时是否使用 SSL
默认值为
false
使用 YAML 文件
在
values.yaml
文件中配置
minio
部分。
minio:
enabled:
false
使用
values.yaml
文件中的值配置
externalS3
部分。
externalS3:
enabled:
true
host:
"<your_s3_endpoint>"
port:
"<your_s3_port>"
accessKey:
"<your_s3_access_key_id>"
secretKey:
"<your_s3_secret_key>"
useSSL:
<true/false>
bucketName:
"<your_bucket_name>"
配置完前面的部分并保存
values.yaml
文件后，运行以下命令安装使用 S3 配置的 Milvus。
helm install <your_release_name> milvus/milvus -f values.yaml
使用命令
要安装 Milvus 并配置 S3，请使用你的值运行以下命令。
helm install <your_release_name> milvus/milvus --set cluster.enabled=true  --set minio.enabled=false --set externalS3.enabled=true --set externalS3.host=<your_s3_endpoint> --set externalS3.port=<your_s3_port> --set externalS3.accessKey=<your_s3_access_key_id> --set externalS3.secretKey=<your_s3_secret_key> --set externalS3.bucketName=<your_bucket_name>
下一步
了解如何使用 Docker Compose 或 Helm 配置 Milvus 的其他依赖项：
使用 Docker Compose 或 Helm 配置元存储
使用 Docker Compose 或 Helm 配置消息存储