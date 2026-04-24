跨存储桶在实例间迁移
本主题详细介绍从一个 Milvus 实例备份一个 Collections 并将其还原到另一个实例的过程，每个实例在同一对象存储中使用不同的存储桶。
概述
下图说明了在同一对象存储中使用不同存储桶进行备份和恢复的过程。
跨存储桶备份和恢复.png
假设我们有两个 Milvus 实例，
milvus_A
和
milvus_B
，它们都使用默认的 MinIO 存储引擎进行对象存储。这些实例在同一对象存储中使用不同的存储桶 bucket_A 和
bucket_B
。在这个示例中，我们的目标是完成以下任务：
在
bucket_A
中为 Collections
coll
创建备份 (
my_backup
) 并将备份存储在
bucket_B
中。
在
bucket_B
中，从备份中还原，并将还原后的 Collections 命名为
coll_bak
。
前提条件**
确保已安装
Milvus-backup
工具。
熟悉配置 Milvus 对象存储设置，详情请参阅对象
存储
。
从 milvus_A 备份 Collections
步骤 1：准备配置
进入 milvus-backup 项目目录，创建名为 configs 的目录：
mkdir configs
cd configs
下载备份配置文件
backup.yaml
：
wget https://raw.githubusercontent.com/zilliztech/milvus-backup/main/configs/backup.yaml
文件结构如下：
├── configs
│   └── backup.yaml
├── milvus-backup
└── README.md
第 2 步：编辑配置文件
修改 backup.yaml 文件，为
milvus_A
设置适当的配置：
连接配置
# milvus proxy address, compatible to milvus.yaml
milvus:
address:
milvus_A
port:
19530
authorizationEnabled:
false
# tls mode values [0, 1, 2]
# 0 is close, 1 is one-way authentication, 2 is two-way authentication.
tlsMode:
0
user:
"root"
password:
"Milvus"
milvus.address
:
milvus_A
服务器的 IP 地址或主机名。
milvus.port
:Milvus 服务器监听的 TCP 端口（默认 19530）。
存储配置（MinIO/S3 设置）
# Related configuration of minio, which is responsible for data persistence for Milvus.
minio:
# cloudProvider: "minio" # deprecated use storageType instead
storageType:
"minio"
# support storage type: local, minio, s3, aws, gcp, ali(aliyun), azure, tc(tencent)
address:
localhost
# Address of MinIO/S3
port:
9000
# Port of MinIO/S3
accessKeyID:
minioadmin
# accessKeyID of MinIO/S3
secretAccessKey:
minioadmin
# MinIO/S3 encryption string
useSSL:
false
# Access to MinIO/S3 with SSL
useIAM:
false
iamEndpoint:
""
bucketName:
"bucket_A"
# Milvus Bucket name in MinIO/S3, make it the same as your milvus instance
rootPath:
"files"
# Milvus storage root path in MinIO/S3, make it the same as your milvus instance
# only for azure
backupAccessKeyID:
minioadmin
# accessKeyID of MinIO/S3
backupSecretAccessKey:
minioadmin
# MinIO/S3 encryption string
backupBucketName:
"bucket_B"
# Bucket name to store backup data. Backup data will store to backupBucketName/backupRootPath
backupRootPath:
"backup"
# Rootpath to store backup data. Backup data will store to backupBucketName/backupRootPath
minio.bucketName
:
milvus_A
中数据存储桶的名称。在本例中，设置为
bucket_A
。
minio.rootPath
:存储
milvus_A
数据的存储桶根路径。在本例中，设置为
files
。
minio.backupBucketName
:
milvus_B
中用于备份存储的存储桶名称。在本例中，
milvus_A
和
milvus_B
使用不同的存储桶。因此，设置为
bucket_B
.
minio.backupRootPath
:指定用于在
milvus_B
中存储备份文件的存储桶内的根路径。在本例中，设置为
backup
。
第 3 步：创建备份
保存 backup.yaml 后，创建名为
my_backup
的备份：
./milvus-backup create -c coll -n my_backup
此命令在对象存储中为 Collections coll 创建备份
bucket_B/backup/my_backup
。
将备份还原到 milvus_B
步骤 1：配置恢复设置
重复步骤 2，修改配置以还原到
milvus_B
，确保
minio.bucketName
设置为
bucket_B
。
下面是一个配置示例：
...
# milvus proxy address, compatible to milvus.yaml
milvus:
address:
milvus_B
port:
19530
authorizationEnabled:
false
# tls mode values [0, 1, 2]
# 0 is close, 1 is one-way authentication, 2 is two-way authentication.
tlsMode:
0
user:
"root"
password:
"Milvus"
# Related configuration of minio, which is responsible for data persistence for Milvus.
minio:
# cloudProvider: "minio" # deprecated use storageType instead
storageType:
"minio"
# support storage type: local, minio, s3, aws, gcp, ali(aliyun), azure, tc(tencent)
address:
localhost
# Address of MinIO/S3
port:
9000
# Port of MinIO/S3
accessKeyID:
minioadmin
# accessKeyID of MinIO/S3
secretAccessKey:
minioadmin
# MinIO/S3 encryption string
useSSL:
false
# Access to MinIO/S3 with SSL
useIAM:
false
iamEndpoint:
""
bucketName:
"bucket_B"
# Milvus Bucket name in MinIO/S3, make it the same as your milvus instance
rootPath:
"files"
# Milvus storage root path in MinIO/S3, make it the same as your milvus instance
# only for azure
backupAccessKeyID:
minioadmin
# accessKeyID of MinIO/S3
backupSecretAccessKey:
minioadmin
# MinIO/S3 encryption string
backupBucketName:
"bucket_B"
# Bucket name to store backup data. Backup data will store to backupBucketName/backupRootPath
backupRootPath:
"backup"
# Rootpath to store backup data. Backup data will store to backupBucketName/backupRootPath
...
步骤 2：恢复备份
将备份还原到
milvus_B
：
./milvus-backup restore -c coll -n my_backup -s _bak
此命令将备份还原到
milvus_B
中名为
coll_bak
的新 Collections 中，数据存储在
bucket_B/files/insert_log/[ID of new collection]
中。