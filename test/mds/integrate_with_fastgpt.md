使用 Milvus 部署 FastGPT
FastGPT
是一个基于知识的问答系统，建立在 LLM 大型语言模型之上，为数据处理和模型调用提供了随时可用的功能。此外，它还能通过 Flow 可视化实现工作流协调，从而为复杂的问答场景提供便利。本教程将指导您如何使用
Milvus
迅速部署自己专属的 FastGPT 应用程序。
下载 docker-compose.yml
确保已安装
Docker Compose
。
执行下面的命令下载 docker-compose.yml 文件。
$
mkdir
fastgpt
$
cd
fastgpt
$
curl -O https://raw.githubusercontent.com/labring/FastGPT/main/projects/app/data/config.json
#
milvus version
$
curl -o docker-compose.yml https://raw.githubusercontent.com/labring/FastGPT/main/files/docker/docker-compose-milvus.yml
#
zilliz version
#
curl -o docker-compose.yml https://raw.githubusercontent.com/labring/FastGPT/main/files/docker/docker-compose-zilliz.yml
如果你使用的是 Zilliz 版本，请调整 docker-compose.yml 文件中的
MILVUS_ADDRESS
和
MILVUS_TOKEN
链接参数，这两个参数与
Zilliz Cloud
中的
公共端点和 Api 密钥
相对应。
启动容器
在与 docker-compose.yml 文件相同的目录下执行。确保 docker-compose 的版本最好在 2.17 以上，否则某些自动化命令可能无法运行。
#
Launch the container
$
docker compose up -d
#
Wait
for
10s, OneAPI typically needs to restart a few
times
to initially connect to Mysql
$
sleep
10
#
Restart oneapi (Due to certain issues with the default Key of OneAPI, it will display
'channel not found'
if
not restarted, this can be temporarily resolved by manually restarting once,
while
waiting
for
the author
's fix)
$
docker restart oneapi
访问 OneAPI 添加模型
访问 OneAPI 的网址是
ip:3001
。默认用户名为 root，密码为 123456。登录后可更改密码。
以 OpenAI 的模型为例，点击 "Channel"（频道）选项卡，在 "Models"（模型）下选择聊天模型和 Embeddings 模型。
在 "
密钥
"部分输入
OpenAI API 密钥
。
有关 OpenAI 以外模型的使用和更多信息，请查阅
One API
。
设置令牌
点击 "令牌 "选项卡。默认情况下，有一个令牌
Initial Root Token
。您也可以创建一个新的令牌，并自行设置配额。
点击令牌上的 "复制"（Copy），确保该令牌的值与在 docker-compose.yml 文件中设置的
CHAT_API_KEY
值一致。
访问 FastGPT
目前，可以通过
ip:3000
直接访问 FastGPT（请注意防火墙）。登录用户名为 root，密码在 docker-compose.yml 环境变量中设置为
DEFAULT_ROOT_PSW
。如果需要域名访问，则需要自行安装和配置
Nginx
。
停止容器
运行以下命令停止容器。
$
docker compose down