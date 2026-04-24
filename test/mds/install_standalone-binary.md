使用 RPM/DEB 软件包安装 Milvus 单机版
本页说明如何使用预置的 RPM/DEB 包安装 Milvus 单机版。
前提条件
已安装 libstdc++ 8.5.0 或更高版本。
安装前
请检查硬件和软件要求
。
下载 RPM/DEB 软件包
你可以根据你的系统架构，从
Milvus Releases 页面
下载 RPM/DEB 包。
对于 x86_64/amd64，下载
milvus_2.6.9-1_amd64.deb
或
milvus_2.6.9-1_amd64.rpm
软件包。
对于 ARM64，请下载
milvus_2.6.9-1_arm64.deb
或
milvus_2.6.9-1_arm64.rpm 软件包
。
以下命令假定你将在 x86_64/amd64 机器上运行 Milvus Standalone。
wget https://github.com/milvus-io/milvus/releases/download/v2.6.9/milvus_2.6.9-1_amd64.rpm -O milvus_2.6.9-1_amd64.rpm
安装 RPM/DEB 软件包
要安装 RPM/DEB 软件包，可以使用系统的软件包管理器。
对于基于 RPM 的系统（如 CentOS、Fedora 和 RHEL），使用
yum
命令安装软件包。
yum install -y ./milvus_2.6.9-1_amd64.rpm
rpm -qa| grep milvus
对于基于 DEB 的系统（如 Ubuntu 和 Debian），使用
apt
命令安装软件包。
apt install -y  ./milvus_2.6.9-1_amd64.deb
dpkg -l | grep milvus
启动 Milvus Standalone
安装完成后，Milvus 被安装为 systemd 服务，可使用以下命令启动：
systemctl start milvus
你可以使用以下命令检查 Milvus 服务的状态：
systemctl status milvus
如果 Milvus 运行成功，你会看到以下输出：
●
milvus.service
-
Milvus
Standalone
Server
Loaded:
loaded
(/lib/systemd/system/milvus.service;
enabled;
vendor preset:
enabled)
Active:
active
(running)
since
Fri
2025-08-10 10:30:00
UTC;
5s
ago
Main PID:
1044122
(milvus)
Tasks: 10 (limit:
4915
)
CGroup:
/system.slice/milvus.service
└─1044122
/usr/bin/milvus
run
standalone
你可以在
/usr/bin/milvus
找到 Milvus 二进制文件，在
/lib/systemd/system/milvus.service
找到 systemd 服务文件，在
/usr/lib/milvus/
找到依赖关系。
(可选）更新 Milvus 配置
你可以修改
/etc/milvus/configs/milvus.yaml
文件中的 Milvus 配置。例如，要将
proxy.healthCheckTimeout
更改为
1000
ms，可以搜索目标参数并进行相应修改。有关适用的配置项目，请参阅
系统配置
。
停止 Milvus Standalone
要停止 Milvus Standalone，可以使用以下命令：
systemctl stop milvus
卸载 Milvus Standalone
要卸载 Milvus Standalone，可以使用以下命令：
对于基于 RPM 的系统
rpm -e milvus
对于基于 DEB 的系统：
apt remove milvus
下一步
安装 Milvus Standalone 后，你可以
查看
快速入门
，了解 Milvus 的功能。
学习 Milvus 的基本操作：
管理数据库
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
使用 Helm 图表升级 Milvus
。
扩展你的 Milvus 集群
。
在云上部署你的 Milvu 集群：
亚马逊 EKS
谷歌云
微软 Azure
探索
Milvus WebUI
，一个用于 Milvus 可观察性和管理的直观 Web 界面。
探索
Milvus 备份
，一个用于 Milvus 数据备份的开源工具。
探索
Birdwatcher
，用于调试 Milvus 和动态配置更新的开源工具。
探索
Attu
，一个用于直观管理 Milvus 的开源图形用户界面工具。
使用 Prometheus 监控 Milvus
。