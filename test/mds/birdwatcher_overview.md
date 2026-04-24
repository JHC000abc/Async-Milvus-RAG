Birdwatcher
Milvus 是一个无状态向量数据库，它将读写分离，并让 etcd 扮演单一状态源的角色。所有协调人员都必须先从 etcd 中查询状态，然后才能对其进行任何更改。一旦用户需要检查或清理状态，他们就需要一个与 etcd 通信的工具。这就是 Birdwatcher 的用武之地。
Birdwatcher 是 Milvus 的调试工具。使用它连接到 etcd，你就可以检查 Milvus 系统的状态或动态配置它。
前提条件
已安装
Go 1.18 或更高版本
。
架构
Birdwatcher 架构
最新版本
版本 v1.0.2