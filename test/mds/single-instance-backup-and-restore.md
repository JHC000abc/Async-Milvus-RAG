在一个实例中备份和还原
本主题详细介绍在同一 Milvus 实例中备份 Collections 并从备份中还原的过程。
概述
下图说明了在一个 Milvus 实例中的备份和还原过程。
单实例备份和恢复.png
假设我们有一个 Milvus 实例
milvus_A
，使用名为
bucket_A
的存储桶存储数据。在这个示例中，我们的目标是完成以下任务：
为
bucket_A
中的 Collections coll 创建备份 (
my_backup
) 。
从备份中还原，并将还原后的 Collections 命名为
coll_bak
。
前提条件
确保已安装
Milvus-backup
工具。
熟悉配置 Milvus 对象存储设置，详情请参阅对象
存储
。
备份 Collections
步骤 1：准备配置
进入 milvus-backup 项目目录，创建名为
configs
的目录：
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
设置适当的配置。以下是存储配置示例：
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
"bucket_A"
# Bucket name to store backup data. Backup data will store to backupBucketName/backupRootPath
backupRootPath:
"backup"
# Rootpath to store backup data. Backup data will store to backupBucketName/backupRootPath
第 3 步：创建备份
保存 backup.yaml 文件后，创建一个名为
my_backup
的备份：
./milvus-backup create -c coll -n my_backup
此命令在
milvus_A
的对象存储中创建备份
bucket_A/backup/my_backup
。
在 milvus_A 中从备份进行恢复
创建备份后，可以使用下面的命令从备份中还原：
./milvus-backup restore -c coll -n my_backup -s _bak
此命令从备份还原并在
milvus_A
中创建名为 coll_bak 的新 Collections，数据存储在
bucket_A/files/insert_log/[ID of new collection]
中。