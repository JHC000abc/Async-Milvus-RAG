在一个存储桶中的不同实例之间迁移（不同的根路径）
本主题详细介绍从一个 Milvus 实例备份 Collections 并将其还原到另一个实例的过程，同时使用共享桶进行对象存储，每个实例有不同的根路径。
概述
下图说明了使用共享存储桶进行备份和恢复的过程。
shared-bucket-backup-and-restore.png
假设我们有两个 Milvus 实例：
milvus_A
和
milvus_B
，它们都使用默认的 MinIO 存储引擎进行对象存储。这些实例共享同一个存储桶
bucket_A
，但将数据存储在不同的根路径中：
files_A
对应
milvus_A
，files_B 对应
milvus_B
。在本例中，我们的目标是完成以下任务：
为 Collection coll 创建一个备份（my_backup），该备份存储在
files_A
路径下，用于
milvus_A
。
从备份恢复并存储到
milvus_B
的 files_B 中。
前提条件
确保已安装
Milvus-backup
工具。
熟悉配置 Milvus 对象存储设置，详情请参阅对象
存储
。
从以下地址备份 Collections
milvus_A
步骤 1：准备配置
进入 milvus-backup 项目目录，创建名为 configs 的目录：
mkdir configs
cd configs
下载备份配置文件 backup.yaml：
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
milvus_A
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
"files_A"
# Milvus storage root path in MinIO/S3, make it the same as your milvus instance
# only for azure
backupAccessKeyID:
minioadmin
# accessKeyID of MinIO/S3
backupSecretAccessKey:
minioadmin
# MinIO/S3 encryption string
backupBucketName:
"bucket_A"
# Bucket name to store backup data. Backup data will store to backupBucketName/backupRootPath
backupRootPath:
"backup"
# Rootpath to store backup data. Backup data will store to backupBucketName/backupRootPath
minio.bucketName
:用于
milvus_A
存储的存储桶名称。在本例中，设置为
bucket_A
。
minio.rootPath
:存储
milvus_A
数据的存储桶根路径。在本例中，设置为
files_A
。
minio.backupBucketName
:用于存储的存储桶名称。在本例中，
milvus_A
和
milvus_B
共享一个存储桶。因此，设置为
bucket_A
。
minio.backupRootPath
:指定用于在
milvus_B
中存储备份文件的存储桶内的根路径。在本例中，使用与
milvus_A
不同的路径。因此，设置为
backup
。
步骤 3：创建备份
保存
backup.yaml
后，创建名为 my_backup 的备份：
./milvus-backup create -c coll -n my_backup
此命令在对象存储中为 Collections
coll
创建备份
bucket_A/backup/my_backup
。
将备份恢复到
milvus_B
步骤 1：配置恢复设置
重复第 2 步，修改恢复到
milvus_B
的配置，确保
minio.bucketName
设置为
bucket_A
，
minio.rootPath
设置为
files_B
，以区分两个实例的存储位置。
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
milvus_B
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
"files_B"
# Milvus storage root path in MinIO/S3, make it the same as your milvus instance
...
第 2 步：恢复备份
将备份恢复到
milvus_B
：
./milvus-backup restore -c coll -n my_backup -s _bak
此命令将备份还原到
milvus_B
中名为
coll_bak
的新 Collections 中，数据存储在
bucket_A/files_B/insert_log/[ID of new collection]
中。