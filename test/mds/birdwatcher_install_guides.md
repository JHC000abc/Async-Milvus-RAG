安装 Birdwatcher
本页演示如何安装 Birdwatcher。
本地安装
如果您
使用 docker
安装了 Milvus Standalone，最好下载并安装已构建的二进制文件，将 Birdwatcher 作为普通 Go 模块安装，或者从源代码构建 Birdwatcher。
将其作为普通 Go 模块安装。
git clone https://github.com/milvus-io/birdwatcher.git
cd birdwatcher
go install github.com/milvus-io/birdwatcher
然后你就可以按如下方法运行 Birdwatcher：
go run main.go
从源代码构建。
git clone https://github.com/milvus-io/birdwatcher.git
cd birdwatcher
go build -o birdwatcher main.go
然后按以下步骤运行 Birdwatcher：
./birdwatcher
下载已构建的二进制文件
首先，打开
最新发布页面
，找到准备好的二进制文件。
wget -O birdwatcher.tar.gz \
https://github.com/milvus-io/birdwatcher/releases/download/latest/birdwatcher_<os>_<arch>.tar.gz
然后解压压缩包，按如下方法使用 Birdwatcher：
tar -xvzf birdwatcher.tar.gz
./birdwatcher
作为 Kubernetes pod 安装
如果您
使用 Helm 图表
或
Milvus Operator
安装了 Milvus Standalone 或
使用 Helm 图表
或 Milvus
Operator
安装了 Milvus Cluster，建议您将 Birdwatcher 安装为 Kubernetes pod。
准备部署文件
apiVersion:
apps/v1
kind:
Deployment
metadata:
name:
birdwatcher
spec:
selector:
matchLabels:
app:
birdwatcher
template:
metadata:
labels:
app:
birdwatcher
spec:
containers:
-
name:
birdwatcher
image:
milvusdb/birdwatcher
resources:
limits:
memory:
"128Mi"
cpu:
"500m"
如果 DockerHub 上提供的镜像不是最新的，您可以使用源代码提供的 Dockerfile 构建 Birdwatcher 的镜像，如下所示：
git clone https://github.com/milvus-io/birdwatcher.git
cd birdwatcher
docker build -t milvusdb/birdwatcher .
要部署本地构建的镜像，需要在上述规格中添加
imagePullPolicy
，并将其设置为
Never
。
...
-
name:
birdwatcher
image:
milvusdb/birdwatcher
imagePullPolicy:
Never
...
应用 deployment.yml
将上述 YAML 保存在一个文件中并命名为
deployment.yml
，然后运行以下命令
kubectl apply -f deployment.yml