安装 Milvus_CLI
本主题介绍如何安装 Milvus_CLI。
从 PyPI 安装
你可以从
PyPI
安装 Milvus_CLI。
前提条件
安装
Python 3.9
或更高版本
安装
pip
通过 pip 安装
运行以下命令安装 Milvus_CLI。
pip install milvus-cli
使用 Docker 安装
你可以使用 docker 安装 Milvus_CLI。
前提条件
需要 Docker 19.03 或更高版本。
根据 Docker 映像安装
$
docker run -it zilliz/milvus_cli:latest
从源代码安装
运行以下命令下载
milvus_cli
代码库。
git clone https://github.com/zilliztech/milvus_cli.git
运行以下命令进入
milvus_cli
文件夹。
cd milvus_cli
运行以下命令安装 Milvus_CLI。
python -m pip install --editable .
或者，你也可以从压缩包（
.tar.gz
文件）中安装 Milvus_CLI。下载
压缩包
并运行
python -m pip install milvus_cli-<version>.tar.gz
。