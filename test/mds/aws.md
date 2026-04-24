(已弃用）在 EC2 上部署 Milvus 群集
本主题介绍如何使用 Terraform 和 Ansible 在
亚马逊 EC2
上部署 Milvus 群集。
此主题已过时，即将删除。建议你参考
在 EKS 上部署 Milvus 群集
。
配置 Milvus 群集
本节介绍如何使用 Terraform 配置 Milvus 群集。
Terraform
是一种基础设施即代码（IaC）软件工具。使用 Terraform，你可以通过声明式配置文件来配置基础设施。
前提条件
安装和配置
Terraform
安装和配置
AWS CLI
准备配置
你可以从
Google Drive
下载模板配置文件。
main.tf
该文件包含用于配置 Milvus 集群的配置。
variables.tf
该文件允许快速编辑用于设置或更新 Milvus 群集的变量。
output.tf
和
inventory.tmpl
这些文件存储 Milvus 群集的元数据。本主题中使用的元数据包括每个节点实例的
public_ip
、每个节点实例的
private_ip
以及所有 EC2 实例 ID。
准备变量.tf
本节介绍
variables.tf
文件包含的配置。
节点数
下面的模板声明了一个
index_count
变量，用于设置索引节点数。
index_count
的值必须大于或等于 1。
variable "index_count" {
  description = "Amount of index instances to run"
  type        = number
  default     = 5
}
节点类型的实例类型
以下模板声明了一个
index_ec2_type
变量，用于设置索引节点的
实例类型
。
variable "index_ec2_type" {
  description = "Which server type"
  type        = string
  default     = "c5.2xlarge"
}
访问权限
以下模板声明了一个
key_name
变量和一个
my_ip
变量。
key_name
变量代表 AWS 访问密钥。
my_ip
变量表示安全组的 IP 地址范围。
variable "key_name" {
  description = "Which aws key to use for access into instances, needs to be uploaded already"
  type        = string
  default     = ""
}

variable "my_ip" {
  description = "my_ip for security group. used so that ansible and terraform can ssh in"
  type        = string
  default     = "x.x.x.x/32"
}
准备 main.tf
本节介绍
main.tf
文件包含的配置。
云提供商和区域
以下模板使用
us-east-2
区域。有关详细信息，请参阅
可用区域
。
provider "aws" {
  profile = "default"
  region  = "us-east-2"
}
安全组
以下模板声明了一个安全组，允许从
variables.tf
中声明的
my_ip
所代表的 CIDR 地址范围传入流量。
resource "aws_security_group" "cluster_sg" {
  name        = "cluster_sg"
  description = "Allows only me to access"
  vpc_id      = aws_vpc.cluster_vpc.id

  ingress {
    description      = "All ports from my IP"
    from_port        = 0
    to_port          = 65535
    protocol         = "tcp"
    cidr_blocks      = [var.my_ip]
  }

  ingress {
    description      = "Full subnet communication"
    from_port        = 0
    to_port          = 65535
    protocol         = "all"
    self             = true
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = {
    Name = "cluster_sg"
  }
}
VPC
以下模板在 Milvus 集群上指定了一个具有 10.0.0.0/24 CIDR 块的 VPC。
resource "aws_vpc" "cluster_vpc" {
  cidr_block = "10.0.0.0/24"
  tags = {
    Name = "cluster_vpc"
  }
}

resource "aws_internet_gateway" "cluster_gateway" {
  vpc_id = aws_vpc.cluster_vpc.id

  tags = {
    Name = "cluster_gateway"
  }
}
子网（可选）
以下模板声明了一个子网，其流量将路由到互联网网关。在这种情况下，子网 CIDR 块的大小与 VPC 的 CIDR 块相同。
resource "aws_subnet" "cluster_subnet" {
  vpc_id                  = aws_vpc.cluster_vpc.id
  cidr_block              = "10.0.0.0/24"
  map_public_ip_on_launch = true

  tags = {
    Name = "cluster_subnet"
  }
}

resource "aws_route_table" "cluster_subnet_gateway_route" {
  vpc_id       = aws_vpc.cluster_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.cluster_gateway.id
  }

  tags = {
    Name = "cluster_subnet_gateway_route"
  }
}

resource "aws_route_table_association" "cluster_subnet_add_gateway" {
  subnet_id      = aws_subnet.cluster_subnet.id
  route_table_id = aws_route_table.cluster_subnet_gateway_route.id
}
节点实例（节点）
以下模板声明了 MinIO 节点实例。
main.tf
模板文件声明了 11 种节点类型的节点。对于某些节点类型，需要设置
root_block_device
。有关详细信息，请参阅
EBS、Ephemeral 和 Root Block Devices
。
resource "aws_instance" "minio_node" {
  count         = var.minio_count
  ami           = "ami-0d8d212151031f51c"
  instance_type = var.minio_ec2_type
  key_name      = var.key_name
  subnet_id     = aws_subnet.cluster_subnet.id 
  vpc_security_group_ids = [aws_security_group.cluster_sg.id]

  root_block_device {
    volume_type = "gp2"
    volume_size = 1000
  }
  
  tags = {
    Name = "minio-${count.index + 1}"
  }
}
应用配置
打开终端并导航到存储
main.tf
的文件夹。
要初始化配置，请运行
terraform init
。
要应用配置，请运行
terraform apply
并在出现提示时输入
yes
。
现在，您已使用 Terraform 配置了 Milvus 群集。
启动 Milvus 群集
本节介绍如何使用 Ansible 启动已配置的 Milvus 群集。
Ansible
是一个配置管理工具，用于自动化云供应和配置管理。
前提条件
已安装
Ansible 控制器
。
下载 Ansible Milvus 节点部署手册
从 GitHub 克隆 Milvus 存储库，下载 Ansible Milvus 节点部署手册。
git
clone
https://github.com/milvus-io/milvus.git
配置安装文件
inventory.ini
和
ansible.cfg
文件用于控制 Ansible playbook 中的环境变量和登录验证方法。在
inventory.ini
文件中，
dockernodes
部分定义了 docker 引擎的所有服务器。
ansible.cfg
部分定义了 Milvus 协调器的所有服务器。
node
部分定义了 Milvus 节点的所有服务器。
输入 Playbook 的本地路径并配置安装文件。
$
cd
./milvus/deployments/docker/cluster-distributed-deployment
inventory.ini
配置
inventory.ini
，按照主机在 Milvus 系统中的角色将其划分为若干组。
添加主机名，并定义
docker
组和
vars
。
[dockernodes]
#Add docker host names.
dockernode01
dockernode02
dockernode03

[admin]
#Add Ansible controller name.
ansible-controller

[coords]
#Add the host names of Milvus coordinators.
; Take note the IP of this host VM, and replace 10.170.0.17 with it.
dockernode01

[nodes]
#Add the host names of Milvus nodes.
dockernode02

[dependencies]
#Add the host names of Milvus dependencies.
; dependencies node will host etcd, minio, pulsar, these 3 roles are the foundation of Milvus. 
; Take note the IP of this host VM, and replace 10.170.0.19 with it.
dockernode03
[docker:children]
dockernodes
coords
nodes
dependencies
[docker:vars]
ansible_python_interpreter= /usr/bin/python3
StrictHostKeyChecking= no

; Setup variables to control what type of network to use when creating containers.
dependencies_network= host
nodes_network= host

; Setup varibale to control what version of Milvus image to use.
image= milvusdb/milvus-dev:master-20220412-4781db8a

; Setup static IP addresses of the docker hosts as variable for container environment variable config.
; Before running the playbook, below 4 IP addresses need to be replaced with the IP of your host VM
; on which the etcd, minio, pulsar, coordinators will be hosted.
etcd_ip= 10.170.0.19
minio_ip= 10.170.0.19
pulsar_ip= 10.170.0.19
coords_ip= 10.170.0.17

; Setup container environment which later will be used in container creation.
ETCD_ENDPOINTS= {{etcd_ip}}:2379 
MINIO_ADDRESS= {{minio_ip}}:9000
PULSAR_ADDRESS= pulsar://{{pulsar_ip}}:6650
QUERY_COORD_ADDRESS= {{coords_ip}}:19531
DATA_COORD_ADDRESS= {{coords_ip}}:13333
ROOT_COORD_ADDRESS= {{coords_ip}}:53100
INDEX_COORD_ADDRESS= {{coords_ip}}:31000
ansible.cfg
ansible.cfg
控制 playbook 的操作，例如 SSH 密钥等。不要在 docker 主机上通过 SSH 密钥设置口令。否则，Ansible SSH 连接会失败。我们建议在三台主机上设置相同的用户名和 SSH 密钥，并将新用户账户设置为无需密码即可执行 sudo。否则，在运行 Ansible playbook 时，你会收到用户名与密码不符或未被授予高级权限的错误信息。
[defaults]
host_key_checking
=
False
inventory
= inventory.ini
# Specify the Inventory file
private_key_file
=~/.my_ssh_keys/gpc_sshkey
# Specify the SSH key that Ansible uses to access Docker host
deploy-docker.yml
deploy-docker.yml
定义 Docker 安装过程中的任务。有关详细信息，请参阅文件中的代码注释。
---
-
name:
setup
pre-requisites
# Install prerequisite
hosts:
all
become:
yes
become_user:
root
roles:
-
install-modules
-
configure-hosts-file
-
name:
install
docker
become:
yes
become_user:
root
hosts:
dockernodes
roles:
-
docker-installation
测试 Ansible 的连接性
测试与 Ansible 的连接。
$
ansible all -m ping
如果在
ansible.cfg
中没有指定清单文件的路径，请在命令中添加
-i
，否则 Ansible 会使用
/etc/ansible/hosts
。
终端返回如下：
dockernode01 |
SUCCESS
=>
{
"changed"
:
false
,
"ping"
:
"pong"
}
ansible-controller |
SUCCESS
=>
{
"ansible_facts"
: {
"discovered_interpreter_python"
:
"/usr/bin/python3"
},
"changed"
:
false
,
"ping"
:
"pong"
}
dockernode03 |
SUCCESS
=>
{
"changed"
:
false
,
"ping"
:
"pong"
}
dockernode02 |
SUCCESS
=>
{
"changed"
:
false
,
"ping"
:
"pong"
}
检查 Playbook 语法
检查 Playbook 的语法。
$
ansible-playbook deploy-docker.yml --syntax-check
通常，终端返回如下内容：
playbook: deploy-docker.yml
安装 Docker
使用 Playbook 安装 Docker。
$
ansible-playbook deploy-docker.yml
如果在三台主机上成功安装了 Docker，终端会返回如下信息：
TASK [docker-installation : Install Docker-CE]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
***
ok: [dockernode01]
ok: [dockernode03]
ok: [dockernode02]

TASK [docker-installation : Install python3-docker] **
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
ok: [dockernode01]
ok: [dockernode02]
ok: [dockernode03]

TASK [docker-installation : Install docker-compose python3 library]
****
****
****
****
****
****
****
****
****
****
****
**
changed: [dockernode01]
changed: [dockernode03]
changed: [dockernode02]

PLAY RECAP
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
***
ansible-controller         : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode01               : ok=10   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode02               : ok=10   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode03               : ok=10   changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
验证安装
使用 SSH 密钥登录三台主机，并验证主机上的安装。
对于根主机
$
docker -v
对于非 root 主机：
$
sudo
docker -v
正常情况下，终端返回如下信息：
Docker
version
20
.
10
.
14
, build a224086
检查容器的运行状态。
$
docker ps
检查语法
检查
deploy-milvus.yml
的语法。
$
ansible-playbook deploy-milvus.yml --syntax-check
通常，终端返回如下信息：
playbook: deploy-milvus.yml
创建 Milvus 容器
创建 Milvus 容器的任务在
deploy-milvus.yml
中定义。
$
ansible-playbook deploy-milvus.yml
终端返回
PLAY [Create milvus-etcd, minio, pulsar]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
*

TASK [Gathering Facts]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
ok: [dockernode03]

TASK [etcd]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
***
changed: [dockernode03]

TASK [pulsar] **
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
***
changed: [dockernode03]

TASK [minio] **
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
changed: [dockernode03]

PLAY [Create milvus nodes]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
TASK [Gathering Facts]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
ok: [dockernode02]

TASK [querynode]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
**
changed: [dockernode02]

TASK [datanode]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
***
changed: [dockernode02]

TASK [indexnode] **
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
changed: [dockernode02]

PLAY [Create milvus coords]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
***

TASK [Gathering Facts] **
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
**
ok: [dockernode01]

TASK [rootcoord]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
**
changed: [dockernode01]

TASK [datacoord]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
**
changed: [dockernode01]

TASK [querycoord]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
*
changed: [dockernode01]

TASK [indexcoord]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
*
changed: [dockernode01]

TASK [proxy]
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
**
changed: [dockernode01]

PLAY RECAP
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
****
dockernode01               : ok=6    changed=5    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode02               : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
dockernode03               : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
现在，你已经在三台主机上部署了 Milvus。
停止节点
不再需要 Milvus 集群后，可以停止所有节点。
确保
terraform
二进制文件在
PATH
上可用。
运行
terraform destroy
，并在出现提示时输入
yes
。
如果成功，所有节点实例都将停止。
下一步
如果你想了解如何在其他云上部署 Milvus：
在 EKS 上部署 Milvus 群集
使用 Kubernetes 在 GCP 上部署 Milvus 群集
使用 Kubernetes 在 Microsoft Azure 上部署 Milvus 指南