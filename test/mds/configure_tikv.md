tikv 相关配置
tikv 的相关配置，用于存储 Milvus 元数据。
请注意，启用 TiKV 作为元数据存储时，仍需要使用 etcd 来发现服务。
当元数据大小需要更好的横向扩展性时，TiKV 是一个不错的选择。
tikv.endpoints
说明
默认值
请注意，tikv 的默认 pd 端口是 2379，这与 etcd 冲突。
127.0.0.1:2389
tikv.rootPath
说明
默认值
tikv 中存储数据的根路径
by-dev
tikv.metaSubPath
说明
默认值
metaRootPath = rootPath + '/' + metaSubPath
元
tikv.kvSubPath
说明
默认值
kvRootPath = rootPath + '/' + kvSubPath
kv
tikv.requestTimeout
描述
默认值
ms，tikv 请求超时
10000
tikv.snapshotScanSize
说明
默认值
tikv 快照扫描的批量大小
256
tikv.ssl.enabled
说明
默认值
是否支持 TiKV 安全连接模式
假
tikv.ssl.tlsCert
描述
默认值
证书文件的路径
tikv.ssl.tlsKey
描述
默认值
密钥文件的路径
tikv.ssl.tlsCACert
说明
默认值
CACert 文件的路径