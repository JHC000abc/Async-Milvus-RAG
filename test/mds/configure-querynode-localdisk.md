使用本地磁盘配置 Milvus QueryNode
本文介绍如何配置 Milvus QueryNode 使用本地磁盘存储。
概述
Milvus 是一个以人工智能为重点的向量数据库，专为高效存储和检索大量向量数据而量身定制。它是图像和视频分析、自然语言处理和推荐系统等任务的理想选择。为确保最佳性能，最大限度地减少磁盘读取延迟至关重要。强烈建议使用本地 NVMe SSD，以防止延迟并保持系统稳定性。
本地磁盘存储发挥作用的主要功能包括
大块缓存
：将数据预加载到本地磁盘缓存中，以加快搜索速度。
MMap
：将文件内容直接映射到内存中，提高内存效率。
DiskANN 索引
：需要磁盘存储，以便高效管理索引。
本文将重点介绍在云平台上部署
Milvus Distributed
，以及如何配置 QueryNode 以使用 NVMe 磁盘存储。下表列出了各种云提供商推荐的机器类型。
云提供商
机器类型
AWS
R6id 系列
GCP
N2 系列
Azure
Lsv3 系列
阿里云
i3 系列
腾讯云
IT5 系列
这些机器类型提供 NVMe 磁盘存储。您可以在这些机器类型的实例上使用
lsblk
命令检查它们是否有 NVMe 磁盘存储。如果有，就可以进行下一步。
$ lsblk | grep nvme
nvme0n1     259:0    0 250.0G  0 disk 
nvme1n1     259:1    0 250.0G  0 disk
配置 Kubernetes 以使用本地磁盘
要配置 Milvus Distributed 的 QueryNode 使用 NVMe 磁盘存储，你需要配置目标 Kubernetes 集群的工作节点，将容器和映像存储在 NVMe 磁盘上。具体步骤因云提供商而异。
亚马逊
使用亚马逊 EKS 时，您可以使用启动模板自定义受管节点，在其中为节点组指定配置设置。以下示例说明了如何在 Amazon EKS 群集的工作节点上加载 NVMe 磁盘：
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary=
"==MYBOUNDARY=="
--==MYBOUNDARY==
Content-Type: text/x-shellscript; charset=
"us-ascii"
#!/bin/bash
echo
"Running custom user data script"
if
( lsblk | fgrep -q nvme1n1 );
then
mkdir
-p /mnt/data /var/lib/kubelet /var/lib/docker
    mkfs.xfs /dev/nvme1n1
    mount /dev/nvme1n1 /mnt/data
chmod
0755 /mnt/data
mv
/var/lib/kubelet /mnt/data/
mv
/var/lib/docker /mnt/data/
ln
-sf /mnt/data/kubelet /var/lib/kubelet
ln
-sf /mnt/data/docker /var/lib/docker
    UUID=$(lsblk -f | grep nvme1n1 | awk
'{print $3}'
)
echo
"UUID=
$UUID
/mnt/data   xfs    defaults,noatime  1   1"
>> /etc/fstab
fi
echo
10485760 > /proc/sys/fs/aio-max-nr

--==MYBOUNDARY==--
在上述示例中，我们假设 NVMe 磁盘为
/dev/nvme1n1
。您需要根据具体配置修改脚本。
有关详细信息，请参阅
使用启动模板自定义托管节点
。
GCP
要在 Google Kubernetes Engine (GKE) 集群上配置本地固态盘存储，并配置工作负载从连接到集群中节点的本地固态盘支持的短暂存储中消耗数据，请运行以下命令：
gcloud container node-pools create
${POOL_NAME}
\
    --cluster=
${CLUSTER_NAME}
\
    --ephemeral-storage-local-ssd count=
${NUMBER_OF_DISKS}
\
    --machine-type=
${MACHINE_TYPE}
有关详细信息，请参阅
在 GKE 上配置 Local SSD 存储
。
Azure
要创建具有本地 NVMe 磁盘存储的虚拟机扩展集 (VMSS)，需要将自定义数据传递给虚拟机实例。下面的示例说明了如何将 NVMe 磁盘附加到 VMSS 中的虚拟机实例：
mdadm -Cv /dev/md0 -l0 -n2 /dev/nvme0n1 /dev/nvme1n1
mdadm -Ds > /etc/mdadm/mdadm.conf 
update-initramfs -u

mkfs.xfs /dev/md0
mkdir
-p /var/lib/kubelet
echo
'/dev/md0 /var/lib/kubelet xfs defaults 0 0'
>> /etc/fstab
mount -a
在上述示例中，我们假设 NVMe 磁盘为
/dev/nvme0n1
和
/dev/nvme1n1
。您需要修改脚本以匹配您的特定配置。
阿里云和 TecentCloud
要创建使用本地 SSD 卷的节点池，我们需要传递自定义数据。以下是自定义数据的示例。
#!/bin/bash
echo
"nvme init start..."
mkfs.xfs /dev/nvme0n1
mkdir
-p /mnt/data
echo
'/dev/nvme0n1 /mnt/data/ xfs defaults 0 0'
>> /etc/fstab
mount -a
mkdir
-p /mnt/data/kubelet /mnt/data/containerd /mnt/data/log/pods
mkdir
-p  /var/lib/kubelet /var/lib/containerd /var/log/pods
echo
'/mnt/data/kubelet /var/lib/kubelet none defaults,bind 0 0'
>> /etc/fstab
echo
'/mnt/data/containerd /var/lib/containerd none defaults,bind 0 0'
>> /etc/fstab
echo
'/mnt/data/log/pods /var/log/pods none defaults,bind 0 0'
>> /etc/fstab
mount -a
echo
"nvme init end..."
在上述示例中，我们假设 NVMe 磁盘为
/dev/nvme0n1
。您需要修改脚本以符合您的具体配置。
自己的 IDC
如果您正在运行自己的 IDC，并希望将容器配置为默认在 containerd 中使用新挂载的 NVMe 磁盘上的文件系统，请按照以下步骤操作：
挂载 NVMe 磁盘。
确保 NVMe 磁盘已正确挂载到主机上。您可以将其挂载到自己选择的目录。例如，如果将其挂载到
/mnt/nvme
，请确保已正确设置，并且可以通过运行
lsblk
或
df -h
查看
/mnt/nvme
中的可用磁盘。
更新 containerd 配置。
修改 containerd 配置，将新挂载用作容器存储的根目录。
sudo
mkdir
-p /mnt/nvme/containerd /mnt/nvme/containerd/state
sudo
vim /etc/containerd/config.toml
找到
[plugins."io.containerd.grpc.v1.cri".containerd]
部分，并修改
snapshotter
和
root
设置，如下所示： 重新启动 containerd。
[plugins."io.containerd.grpc.v1.cri".containerd]
snapshotter
=
"overlayfs"
root
=
"/mnt/nvme/containerd"
state
=
"/mnt/nvme/containerd/state"
重新启动 containerd。
重新启动 containerd 服务以应用更改。
sudo
systemctl restart containerd
验证磁盘性能
建议你使用
Fio
来验证磁盘性能，它是一种常用的磁盘性能基准测试工具。下面是一个如何运行 Fio 测试磁盘性能的示例。
将测试 pod 部署到装有 NVMe 磁盘的节点。
kubectl create -f ubuntu.yaml
ubuntu.yaml
文件如下：
apiVersion:
v1
kind:
Pod
metadata:
name:
ubuntu
spec:
containers:
-
name:
ubuntu
image:
ubuntu:latest
command:
[
"sleep"
,
"86400"
]
volumeMounts:
-
name:
data-volume
mountPath:
/data
volumes:
-
name:
data-volume
emptyDir:
{}
运行 Fio 测试磁盘性能。
# enter the container
kubectl
exec
pod/ubuntu -it bash
# in container
apt-get update
apt-get install fio -y
# change to the mounted dir
cd
/data
# write 10GB
fio -direct=1 -iodepth=128 -rw=randwrite -ioengine=libaio -bs=4K -size=10G -numjobs=10 -runtime=600 -group_reporting -filename=
test
-name=Rand_Write_IOPS_Test
# verify the read speed
# compare with the disk performance indicators provided by various cloud providers.
fio --filename=
test
--direct=1 --rw=randread --bs=4k --ioengine=libaio --iodepth=64 --runtime=120 --numjobs=128 --time_based --group_reporting --name=iops-test-job --eta-newline=1  --
readonly
输出结果应如下所示：
Jobs: 128 (f=128): [r(128)][100.0%][r=1458MiB/s][r=373k IOPS][eta 00m:00s]
iops-test-job: (groupid=0,
jobs
=128): err= 0: pid=768: Mon Jun 24 09:35:06 2024
read
: IOPS=349k, BW=1364MiB/s (1430MB/s)(160GiB/120067msec)
    slat (nsec): min=765, max=530621k, avg=365836.09, stdev=4765464.96
    clat (usec): min=35, max=1476.0k, avg=23096.78, stdev=45409.13
    lat (usec): min=36, max=1571.6k, avg=23462.62, stdev=46296.74
    clat percentiles (usec):
    |  1.00th=[    69],  5.00th=[    79], 10.00th=[    85], 20.00th=[    95],
    | 30.00th=[   106], 40.00th=[   123], 50.00th=[   149], 60.00th=[ 11469],
    | 70.00th=[ 23462], 80.00th=[ 39584], 90.00th=[ 70779], 95.00th=[103285],
    | 99.00th=[189793], 99.50th=[244319], 99.90th=[497026], 99.95th=[591397],
    | 99.99th=[767558]
bw (  MiB/s): min=  236, max= 4439, per=100.00%, avg=1365.82, stdev= 5.02, samples=30591
iops        : min=60447, max=1136488, avg=349640.62, stdev=1284.65, samples=30591
lat (usec)   : 50=0.01%, 100=24.90%, 250=30.47%, 500=0.09%, 750=0.31%
lat (usec)   : 1000=0.08%
lat (msec)   : 2=0.32%, 4=0.59%, 10=1.86%, 20=8.20%, 50=17.29%
lat (msec)   : 100=10.62%, 250=4.80%, 500=0.38%, 750=0.09%, 1000=0.01%
lat (msec)   : 2000=0.01%
cpu          : usr=0.20%, sys=0.48%, ctx=838085, majf=0, minf=9665
IO depths    : 1=0.1%, 2=0.1%, 4=0.1%, 8=0.1%, 16=0.1%, 32=0.1%, >=64=100.0%
    submit    : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.0%, >=64=0.0%
    complete  : 0=0.0%, 4=100.0%, 8=0.0%, 16=0.0%, 32=0.0%, 64=0.1%, >=64=0.0%
    issued rwts: total=41910256,0,0,0 short=0,0,0,0 dropped=0,0,0,0
    latency   : target=0, window=0, percentile=100.00%, depth=64
部署 Milvus Distributed
验证结果令人满意后，就可以按以下步骤部署 Milvus Distributed：
使用 Helm 部署 Milvus Distributed 的提示
QueryNode pod 默认使用 NVMe 磁盘作为 EmptyDir 卷。建议在 QueryNode pod 中将 NVMe 磁盘挂载到
/var/lib/milvus/data
，以确保最佳性能。
有关如何使用 Helm 部署 Milvus Distributed 的详细信息，请参阅使用
Helm 在 Kubernetes 中运行 Milvus
。
使用 Milvus Operator 部署 Milvus Distributed 的提示
Milvus Operator 会自动配置 QueryNode pod 将 NVMe 磁盘用作 EmptyDir 卷。建议将以下配置添加到
MilvusCluster
自定义资源：
...
spec:
components:
queryNode:
volumeMounts:
-
mountPath:
/var/lib/milvus/data
name:
data
volumes:
-
emptyDir:
name:
data
这将确保 QueryNode pod 将 NVMe 磁盘用作数据卷。有关如何使用 Milvus Operator 部署
Milvus
Distributed 的详细信息，请参阅
使用 Milvus Operator 在 Kubernetes 中运行 Milvus
。