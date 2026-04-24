Milvus 备份
Milvus 备份是一个允许用户备份和恢复 Milvus 数据的工具。它同时提供 CLI 和 API，以适应不同的应用场景。
前提条件
在开始使用 Milvus 备份之前，请确保
操作系统为 CentOS 7.5+ 或 Ubuntu LTS 18.04+、
Go 版本为 1.20.2 或更高版本。
架构
Milvus 备份架构
Milvus 备份便于跨 Milvus 实例备份和恢复元数据、段和数据。它提供北向接口，如 CLI、API 和基于 gRPC 的 Go 模块，以便灵活操作备份和还原过程。
Milvus 备份从源 Milvus 实例读取 Collections 元数据和片段，以创建备份。然后，它会从源 Milvus 实例的根路径复制 Collections 数据，并将复制的数据保存到备份根路径。
要从备份中还原，Milvus Backup 会根据备份中的 Collections 元数据和段信息，在目标 Milvus 实例中创建一个新的 Collections。然后，它会将备份数据从备份根路径复制到目标实例的根路径。
兼容性矩阵
下表列出了自 Milvus Backup v0.5.7 以来不同 Milvus 版本之间的备份和还原兼容性。
备份自 ↓ / 还原至 →
Milvus v2.2.x
Milvus v2.3.x
Milvus v2.4.x
Milvus v2.5.x
Milvus v2.6.x
Milvus v2.2.x
无
无
是
是
是
Milvus v2.3.x
无
是
是
是
是
Milvus v2.4.x
无
是
是
是
是
Milvus v2.5.x
无
是
是
是
是
Milvus v2.6.x
无
无
无
无
有
最新版本
v0.5.10