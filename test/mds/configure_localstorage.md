本地存储相关配置
localStorage.path
说明
默认值
在搜索或查询过程中存储向量数据的本地路径，以避免重复访问 MinIO 或 S3 服务。
注意：在使用 Milvus 一段时间后更改此参数将影响对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
/var/lib/milvus/data/