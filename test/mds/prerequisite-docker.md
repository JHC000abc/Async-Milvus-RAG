安装 Milvus Standalone 的要求
在安装 Milvus Standalone 实例之前，请检查您的硬件和软件是否符合要求。
硬件要求
组件
要求
建议
备注
中央处理器
英特尔第二代酷睿处理器或更高版本
苹果硅
独立：4 核或更高
集群：8 核或更多
CPU 指令集
SSE4.2
AVX
AVX2
AVX-512
SSE4.2
AVX
AVX2
AVX-512
Milvus 中的向量相似性搜索和索引建立需要 CPU 支持单指令、多数据（SIMD）扩展集。确保 CPU 至少支持所列 SIMD 扩展之一。更多信息，请参阅
带 AVX 的 CPU
。
内存
单机：8G
集群：32G
单机：16G
集群： 128G128G
内存大小取决于数据量。
硬盘
SATA 3.0 固态硬盘或更高版本
NVMe SSD 或更高版本
硬盘大小取决于数据量。
软件要求
操作系统
软件
备注
macOS 10.14 或更高版本
Docker 桌面
将 Docker 虚拟机 (VM) 设置为至少使用 2 个虚拟 CPU (vCPU) 和 8 GB 初始内存。否则，安装可能会失败。
更多信息，请参阅
在 Mac 上安装 Docker Desktop
。
Linux 平台
Docker 19.03 或更高版本
Docker Compose 1.25.1 或更高版本
更多信息，请参阅
安装 Docker Engine
和
安装 Docker Compose
。
已启用 WSL 2 的 Windows
Docker 桌面
我们建议您将绑定挂载到 Linux 容器中的源代码和其他数据存储在 Linux 文件系统中，而不是 Windows 文件系统中。更多信息，请参见
在 Windows 上安装带有 WSL 2 后端的 Docker Desktop
。
使用 Docker 脚本或 Docker Compose 配置安装 Milvus Standalone 时，将自动获取并配置以下依赖项：
软件
版本
备注
etcd
3.5.0
请参阅
其他磁盘要求
。
MinIO
RELEASE.2024-12-18T13-15-44Z
脉冲星
2.8.2
其他磁盘要求
磁盘性能对 etcd 至关重要。强烈建议使用本地 NVMe SSD。较慢的磁盘响应速度可能会导致频繁的群集选举，最终降低 etcd 服务的性能。
要测试磁盘是否合格，请使用
fio
。
mkdir
test-data
fio --rw=write --ioengine=
sync
--fdatasync=1 --directory=test-data --size=2200m --bs=2300 --name=mytest
理想情况下，专用于 etcd 的磁盘应达到 500 IOPS 以上，第 99 百分位数 fsync 延迟应低于 10 毫秒。阅读 etcd
文档
，了解更多详细要求。
下一步
如果您的硬件和软件符合上述要求，您可以
在 Docker 中运行 Milvus
使用 Docker Compose 运行 Milvus