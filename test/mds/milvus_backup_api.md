使用 API 备份和恢复数据
Milvus 备份提供数据备份和恢复功能，以确保您的 Milvus 数据安全。
获取 Milvus 备份程序
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
启动 API 服务器
然后按如下步骤启动 API 服务器：
./milvus-backup server
API 服务器默认侦听 8080 端口。您可以通过使用
-p
标志运行来更改端口。要启动通过 443 端口监听的 API 服务器，请按以下步骤操作：
./milvus-backup server -p 443
您可以使用 http://localhost 访问 Swagger UI：
/api/v1/docs/index.html。
准备数据
如果运行一个空的本地 Milvus 实例，监听默认端口 19530，请使用示例 Python 脚本在实例中生成一些数据。请根据自己的需要对脚本进行必要的修改。
获取
脚本
。然后运行脚本生成数据。确保已安装官方的 Milvus Python SDK
PyMilvus
。
python example/prepare_data.py
这一步是可选的。如果跳过这一步，请确保您的 Milvus 实例中已经有一些数据。
备份数据
请注意，针对 Milvus 实例运行 Milvus 备份通常不会影响实例的运行。在备份或还原期间，你的 Milvus 实例是完全正常的。
运行以下命令创建备份。如有必要，请更改
collection_names
和
backup_name
。
curl --location --request POST 'http://localhost:8080/api/v1/create' \
--header 'Content-Type: application/json' \
--data-raw '{
  "async": true,
  "backup_name": "my_backup",
  "collection_names": [
    "hello_milvus"
  ]
}'
执行命令后，您可以在 Minio 设置中指定的存储桶中列出备份，如下所示：
curl --location --request GET 'http://localhost:8080/api/v1/list' \
--header 'Content-Type: application/json'
并按如下方式下载备份文件：
curl --location --request GET 'http://localhost:8080/api/v1/get_backup?backup_id=<test_backup_id>&backup_name=my_backup' \
--header 'Content-Type: application/json'
运行上述命令时，将
backup_id
和
backup_name
更改为列表 API 返回的值。
现在，您可以将备份文件保存到安全的地方，以便将来还原，也可以将其上传到
Zilliz Cloud
，用您的数据创建受管向量数据库。详情请参阅
从 Milvus 迁移到 Zilliz Cloud
。
还原数据
您可以调用带有
collection_suffix
选项的 restore API 命令，通过还原备份中的数据来创建新的 Collections。如有必要，请更改
collection_names
和
backup_name
。
curl --location --request POST 'http://localhost:8080/api/v1/restore' \
--header 'Content-Type: application/json' \
--data-raw '{
    "async": true,
    "collection_names": [
    "hello_milvus"
  ],
    "collection_suffix": "_recover",
    "backup_name":"my_backup"
}'
通过
collection_suffix
选项，可以为要创建的新 Collection 设置后缀。上述命令将在你的
Milvus
实例中创建一个名为
hello_milvus_recover
的新 Collection。
如果你希望在不更改名称的情况下恢复备份的 Collections，请在从备份恢复之前删除 Collections。现在，您可以运行以下命令清理在 "
准备数据
"中生成的数据。
python example/clean_data.py
然后运行以下命令从备份中还原数据。
curl --location --request POST 'http://localhost:8080/api/v1/restore' \
--header 'Content-Type: application/json' \
--data-raw '{
    "async": true,
    "collection_names": [
    "hello_milvus"
  ],
    "collection_suffix": "",
    "backup_name":"my_backup"
}'
还原过程可能很耗时，这取决于要还原的数据大小。因此，所有还原任务都是异步运行的。您可以通过运行以下命令来检查还原任务的状态：
curl --location --request GET 'http://localhost:8080/api/v1/get_restore?id=<test_restore_id>' \
--header 'Content-Type: application/json'
切记将
test_restore_id
更改为通过还原 API 还原的数据。
验证还原的数据
还原完成后，可以通过对已还原的 Collections 编制索引来验证已还原的数据，方法如下：
python example/verify_data.py
请注意，上述脚本假定您在运行
restore
命令时使用了
-s
标志，且后缀设置为
-recover
。请根据需要对脚本进行必要的修改。