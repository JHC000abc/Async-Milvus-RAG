使用命令备份和恢复数据
Milvus 备份提供数据备份和恢复功能，以确保您的 Milvus 数据安全。
获取 Milvus 备份工具
您可以下载编译后的二进制文件，也可以从源代码中构建。
要下载编译后的二进制文件，请访问
发布页面
，在那里可以找到所有正式发布的版本。记住，一定要使用标记为
最新的
版本中的二进制文件。
从源代码编译的步骤如下：
git clone git@github.com:zilliztech/milvus-backup.git
go get
go build
准备配置文件
下载
示例配置文件
，并根据自己的需要进行调整。
然后在下载或构建的 Milvus Backup 二进制文件旁创建一个文件夹，将文件夹命名为
configs
，并将配置文件放在
configs
文件夹中。
你的文件夹结构应类似于下图：
workspace
  ├── milvus-backup
  └── configs
      └── backup.yaml
由于 Milvus Backup 无法将数据备份到本地路径，因此在定制配置文件时要确保 Minio 设置正确。
默认 Minio 文件桶的名称随安装 Milvus 的方式而不同。更改 Minio 设置时，请参阅下表。
字段
Docker Compose
Helm / Milvus 操作符
bucketName
a-bucket
milvus-bucket
rootPath
文件
文件
准备数据
如果你在默认端口运行一个空的本地 Milvus 实例，请使用示例 Python 脚本在你的实例中生成一些数据。请根据自己的需要对脚本进行必要的修改。
获取
脚本
。然后运行脚本生成数据。确保已安装官方的 Milvus Python SDK
PyMilvus
。
python example/prepare_data.py
这一步是可选的。如果跳过这一步，请确保您的 Milvus 实例中已经有一些数据。
备份数据
请注意，针对 Milvus 实例运行 Milvus 备份通常不会影响实例的运行。在备份或还原期间，你的 Milvus 实例是完全正常的。
运行以下命令创建备份。
./milvus-backup create -n <backup_name>
执行命令后，您可以在 Minio 设置中指定的存储桶中检查备份文件。具体来说，您可以使用
Minio 控制台
或
mc
客户端下载它们。
要从 Minio
控制台
下载，请登录 Minio 控制台，找到
minio.address
中指定的备份桶，选择备份桶中的文件，然后单击 "
下载 "
进行下载。
如果您喜欢
使用 mc 客户端
，请按以下步骤操作：
#
configure a Minio host
mc alias set my_minio https://<minio_endpoint> <accessKey> <secretKey>
#
List the available buckets
mc ls my_minio
#
Download a bucket recursively
mc cp --recursive my_minio/<your-bucket-path> <local_dir_path>
现在，您可以将备份文件保存到安全的地方以便将来还原，或者将它们上传到
Zilliz Cloud
以创建一个包含您的数据的受管向量数据库。详情请参阅
从 Milvus 迁移到 Zilliz Cloud
。
恢复数据
您可以运行带有
-s
标志的
restore
命令，通过从备份中恢复数据来创建新的 Collections：
./milvus-backup restore -n my_backup -s _recover
-s
标志允许你为要创建的新 Collection 设置后缀。上述命令将在你的
Milvus
实例中创建一个名为
hello_milvus_recover
的新 Collection。
如果你希望在不更改名称的情况下恢复已备份的 Collection，请在从备份恢复之前删除 Collection。现在，您可以运行以下命令清理在 "
准备数据
"中生成的数据。
python example/clean_data.py
然后运行以下命令从备份中还原数据。
./milvus-backup restore -n my_backup
验证恢复的数据
还原完成后，您可以通过对已还原的 Collections 编制索引来验证已还原的数据，方法如下：
python example/verify_data.py
请注意，上述脚本假定您在运行
restore
命令时使用了
-s
标志，且后缀设置为
-recover
。请根据需要对脚本进行必要的修改。