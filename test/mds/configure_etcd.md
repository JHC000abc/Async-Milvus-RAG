etcd 相关配置
用于存储 Milvus 元数据和服务发现的 etcd 相关配置。
etcd.endpoints
说明
默认值
用于访问 etcd 服务的端点。可以根据自己的 etcd 集群的端点更改此参数。
环境变量：ETCD_ENDPOINTS
启动 milvus 时，etcd 优先从环境变量 ETCD_ENDPOINTS 获取有效地址。
本地主机：2379
etcd.rootPath
默认值
默认值
Milvus 在 etcd 中存储数据的键的根前缀。
建议在首次启动 Milvus 前更改此参数。
要在多个 Milvus 实例之间共享一个 etcd 实例，可考虑在启动每个 Milvus 实例之前将其更改为不同的值。
如果已经存在 etcd 服务，为 Milvus 设置一个易于识别的根路径。
为已运行的 Milvus 实例更改此值可能会导致读取遗留数据失败。
by-dev
etcd.metaSubPath
说明
默认值
Milvus 在 etcd 中存储元数据相关信息的关键字的子前缀。
注意：在使用 Milvus 一段时间后更改此参数将影响对旧数据的访问。
建议在首次启动 Milvus 之前更改此参数。
元
etcd.kvSubPath
说明
默认值
Milvus 在 etcd 中存储时间戳的键的子前缀。
注意：在使用 Milvus 一段时间后更改此参数将影响您对旧数据的访问。
如果没有特殊原因，建议不要更改此参数。
kv
etcd.log.level
说明
默认值
仅支持 debug、info、warn、error、panic 或 fatal。默认为 "info"。
info
etcd.log.path
描述
默认值
路径为
- "default "为 os.Stderr、
- "stderr "为 os.Stderr、
- "stdout "为 os.Stdout、
- 附加服务器日志的文件路径。
请在嵌入式 Milvus 中调整：/tmp/milvus/logs/etcd.log
stdout
etcd.ssl.enabled
说明
默认值
是否支持 ETCD 安全连接模式
假
etcd.ssl.tlsCert
描述
默认值
证书文件的路径
/path/to/etcd-client.pem
etcd.ssl.tlsKey
说明
默认值
密钥文件的路径
/path/to/etcd-client-key.pem
etcd.ssl.tlsCACert
说明
默认值
CACert 文件的路径
/path/to/ca.pem
etcd.ssl.tlsMinVersion
说明
默认值
TLS 最小版本
可选值：1.0, 1.1, 1.2, 1.3。
建议使用 1.2 及以上版本。
1.3
etcd.requestTimeout
说明
默认值
Etcd 操作符超时（毫秒
10000
etcd.use.embed
说明
默认值
是否启用嵌入式 Etcd（进程内 EtcdServer）。
假
etcd.data.dir
说明
默认值
仅限嵌入式 Etcd。请在嵌入式 Milvus 中调整：/tmp/milvus/etcdData/
default.etcd
etcd.auth.enabled
说明
默认值
是否启用身份验证
假
etcd.auth.userName
说明
默认值
用于 etcd 身份验证的用户名
etcd.auth.password
说明
默认值
用于 etcd 身份验证的密码