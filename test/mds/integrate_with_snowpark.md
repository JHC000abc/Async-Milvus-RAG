在 Snowpark 容器服务上使用 Milvus
本指南演示如何在 Snowpark 容器服务上启动 Milvus 演示。
关于雪园容器服务
Snowpark 容器服务是一种完全托管的容器产品，旨在促进 Snowflake 生态系统内容器化应用程序的部署、管理和扩展。这项服务使用户能够直接在 Snowflake 内运行容器化工作负载，确保数据无需移出 Snowflake 环境进行处理。有关详细信息，请参阅官方介绍：
Snowpark 容器服务
。
配置 Milvus 演示
下面将通过配置和代码让用户了解 Milvus 的功能，以及如何在 SPCS 中使用 Milvus。
1.获取账户信息
下载 SPCS 客户端：
SnowSQL
，然后登录您的账户。
snowsql -a ${instance_name} -u ${user_name}
${instance_name}
的规则是
${org_name}-${acct_name}
。登录
app.snowflake.com
，查看个人账户信息即可获取相关信息。
Snowflake 账户信息
2.配置角色和权限
配置 OAUTH 集成。
USE ROLE ACCOUNTADMIN;
CREATE
SECURITY INTEGRATION SNOWSERVICES_INGRESS_OAUTH
  TYPE
=
oauth
  OAUTH_CLIENT
=
snowservices_ingress
  ENABLED
=
true
;
  
USE ROLE ACCOUNTADMIN;
GRANT
BIND SERVICE ENDPOINT
ON
ACCOUNT
TO
ROLE SYSADMIN;
为服务创建一个角色，注意此处的
${PASSWORD}
部分需要在演示时由用户替换。
USE ROLE SECURITYADMIN;
CREATE
ROLE MILVUS_ROLE;

USE ROLE USERADMIN;
CREATE
USER
milvus_user
  PASSWORD
=
'milvususerok'
DEFAULT_ROLE
=
MILVUS_ROLE
  DEFAULT_SECONDARY_ROLES
=
(
'ALL'
)
  MUST_CHANGE_PASSWORD
=
FALSE
;
  
USE ROLE SECURITYADMIN;
GRANT
ROLE MILVUS_ROLE
TO
USER
milvus_user;
3.创建数据存储配置
创建仓库和数据库
USE ROLE SYSADMIN;
CREATE
OR
REPLACE WAREHOUSE MILVUS_WAREHOUSE
WITH
WAREHOUSE_SIZE
=
'X-SMALL'
AUTO_SUSPEND
=
180
AUTO_RESUME
=
true
INITIALLY_SUSPENDED
=
false
;

USE ROLE SYSADMIN;
CREATE
DATABASE IF
NOT
EXISTS
MILVUS_DEMO;
USE DATABASE MILVUS_DEMO;
CREATE
IMAGE REPOSITORY MILVUS_DEMO.PUBLIC.MILVUS_REPO;
CREATE
OR
REPLACE STAGE YAML_STAGE;
CREATE
OR
REPLACE STAGE DATA ENCRYPTION
=
(TYPE
=
'SNOWFLAKE_SSE'
);
CREATE
OR
REPLACE STAGE FILES ENCRYPTION
=
(TYPE
=
'SNOWFLAKE_SSE'
);
授予角色权限
USE ROLE SECURITYADMIN;
GRANT
ALL
PRIVILEGES
ON
DATABASE MILVUS_DEMO
TO
MILVUS_ROLE;
GRANT
ALL
PRIVILEGES
ON
SCHEMA MILVUS_DEMO.PUBLIC
TO
MILVUS_ROLE;
GRANT
ALL
PRIVILEGES
ON
WAREHOUSE MILVUS_WAREHOUSE
TO
MILVUS_ROLE;
GRANT
ALL
PRIVILEGES
ON
STAGE MILVUS_DEMO.PUBLIC.FILES
TO
MILVUS_ROLE;
配置 ACL
USE ROLE ACCOUNTADMIN;
USE DATABASE MILVUS_DEMO;
USE SCHEMA PUBLIC;
CREATE
NETWORK RULE allow_all_rule
TYPE
=
'HOST_PORT'
MODE
=
'EGRESS'
VALUE_LIST
=
(
'0.0.0.0:443'
,
'0.0.0.0:80'
);
CREATE
EXTERNAL
ACCESS INTEGRATION allow_all_eai
ALLOWED_NETWORK_RULES
=
(allow_all_rule)
ENABLED
=
TRUE
;
GRANT
USAGE
ON
INTEGRATION allow_all_eai
TO
ROLE SYSADMIN;
4.创建镜像
Milvus 使用的镜像需要在本地构建，然后由用户上传。有关镜像的相关配置，请参考
此 repo
。克隆代码后，进入项目根目录，准备构建镜像。
本地构建镜像
打开本地 shell，开始构建镜像。
cd ${repo_git_root_path}
docker build --rm --no-cache --platform linux/amd64 -t milvus ./images/milvus
docker build --rm --no-cache --platform linux/amd64 -t jupyter ./images/jupyter
这里有两个镜像，第一个是运行 Milvus 数据库，第二个是用于显示的笔记本。
本地图像构建完成后，准备标记和上传它们。
标记已构建的镜像
登录 SPCS 的 docker hub。
docker login ${instance_name}.registry.snowflakecomputing.com -u ${user_name}
现在就可以为 spcs 标记图像了。
docker tag milvus ${instance_name}.registry.snowflakecomputing.com/milvus_demo/public/milvus_repo/milvus
docker tag jupyter ${instance_name}.registry.snowflakecomputing.com/milvus_demo/public/milvus_repo/jupyter
然后在本地 shell 中使用
docker images | grep milvus
检查图像是否已成功打包和标记。
docker images | grep milvus
$
{instance_name}.registry.snowflakecomputing.com/milvus_demo/public/milvus_repo/milvus    latest        3721bbb8f62b   2 days ago    2.95GB
$
{instance_name}.registry.snowflakecomputing.com/milvus_demo/public/milvus_repo/jupyter   latest        20633f5bcadf   2 days ago    2GB
将图像推送到 SPCS
docker push ${instance_name}.registry.snowflakecomputing.com/milvus_demo/public/milvus_repo/milvus
docker push ${instance_name}.registry.snowflakecomputing.com/milvus_demo/public/milvus_repo/jupyter
5.创建并启动服务
让我们回到 SnowSQL shell。
创建计算池
USE ROLE SYSADMIN;
CREATE
COMPUTE POOL IF
NOT
EXISTS
MILVUS_COMPUTE_POOL
  MIN_NODES
=
1
MAX_NODES
=
1
INSTANCE_FAMILY
=
CPU_X64_S
  AUTO_RESUME
=
true
;
CREATE
COMPUTE POOL IF
NOT
EXISTS
JUPYTER_COMPUTE_POOL
  MIN_NODES
=
1
MAX_NODES
=
1
INSTANCE_FAMILY
=
CPU_X64_S
  AUTO_RESUME
=
true
;
通过
DESCRIBE
检查计算池，直到状态为
ACTIVE
或
IDLE
。
DESCRIBE
COMPUTE POOL MILVUS_COMPUTE_POOL;
DESCRIBE
COMPUTE POOL JUPYTER_COMPUTE_POOL;
计算池状态
上传规范文件
创建计算池后，开始为服务准备 spce 文件。这些文件也在
此 repo
中。请参考规格目录。
打开这两个服务的规格文件，在规格文件中找到
${org_name}-${acct_name}
，并用自己账户的 ${instance_name} 替换。修改后，使用 SnowSQL 完成上传。
PUT file:
/
/
${path
/
to
/
jupyter.yaml}
@yaml_stage
overwrite
=
true
auto_compress
=
false
;
PUT file:
/
/
${path
/
to
/
milvus.yaml}
@yaml_stage
overwrite
=
true
auto_compress
=
false
;
创建服务
上传完成后，就可以创建服务了，继续完成创建服务的过程。
USE ROLE SYSADMIN;
USE DATABASE MILVUS_DEMO;
USE SCHEMA PUBLIC;
CREATE
SERVICE MILVUS
IN
COMPUTE POOL MILVUS_COMPUTE_POOL
FROM
@YAML_STAGE
SPEC
=
'milvus.yaml'
MIN_INSTANCES
=
1
MAX_INSTANCES
=
1
;
CREATE
SERVICE JUPYTER
IN
COMPUTE POOL JUPYTER_COMPUTE_POOL
FROM
@YAML_STAGE
SPEC
=
'jupyter.yaml'
MIN_INSTANCES
=
1
MAX_INSTANCES
=
1
;
也可通过
SHOW SERVICES;
查看服务。
SHOW
SERVICES;
+
---------+---------------+-------------+----------+----------------------+--------------------------------------------------------+-----------------
|
name
|
database_name
|
schema_name
|
owner
|
compute_pool
|
dns_name
|
......
|
---------+---------------+-------------+----------+----------------------+--------------------------------------------------------+-----------------
|
JUPYTER
|
MILVUS_DEMO
|
PUBLIC
|
SYSADMIN
|
JUPYTER_COMPUTE_POOL
|
jupyter.public.milvus
-
demo.snowflakecomputing.internal
|
......
|
MILVUS
|
MILVUS_DEMO
|
PUBLIC
|
SYSADMIN
|
MILVUS_COMPUTE_POOL
|
milvus.public.milvus
-
demo.snowflakecomputing.internal
|
......
+
---------+---------------+-------------+----------+----------------------+--------------------------------------------------------+-----------------
如果在启动服务时遇到问题，可通过
CALL SYSTEM$GET_SERVICE_STATUS('milvus');
查看服务信息。
服务状态
可通过
CALL SYSTEM$GET_SERVICE_LOGS('milvus', '0', 'milvus', 10);
获取更多信息。
使用笔记本
使用
SnowSQL
授予权限。
USE ROLE SECURITYADMIN;
GRANT
USAGE
ON
SERVICE MILVUS_DEMO.PUBLIC.JUPYTER
TO
ROLE MILVUS_ROLE;
然后查看并记录 Jupyter nootbook 的端点。
USE ROLE SYSADMIN;
SHOW
ENDPOINTS
IN
SERVICE MILVUS_DEMO.PUBLIC.JUPYTER;
记录
ingress_url
部分信息，然后打开浏览器并输入
ingress_url
，使用 milvus_user 账户登录网站。
获取入口 URL
通过
ingress_url
打开笔记本，双击页面上的
TestMilvus.ipynb
文件试用 Milvus。选择代码块的第一部分，点击
运行
按钮开始建立连接并初始化 Embeddings 函数。
在笔记本中运行 TestMilvus.ipynb
建立连接后，继续点击
运行
。代码会将一段文本经过嵌入处理后变成向量数据，然后插入到 Milvus 中。
docs = [
"Artificial intelligence was founded as an academic discipline in 1956."
,
"Alan Turing was the first person to conduct substantial research in AI."
,
"Born in Maida Vale, London, Turing was raised in southern England."
,
]
然后使用一段文本作为查询："谁开始了人工智能研究？"，进行嵌入处理后执行查询，最后获取并显示最相关的结果。
获取并显示最相关的结果
有关 Milvus 客户端使用方法的更多信息，可以参考
Milvus 文档
部分。
7.清理
验证后，您可以使用 SnowSQL 清理服务、角色和数据资源。
USE ROLE ACCOUNTADMIN;
DROP
USER
milvus_user;

USE ROLE SYSADMIN;
DROP
SERVICE MILVUS;
DROP
SERVICE JUPYTER;
DROP
COMPUTE POOL MILVUS_COMPUTE_POOL;
DROP
COMPUTE POOL JUPYTER_COMPUTE_POOL;
DROP
IMAGE REPOSITORY MILVUS_DEMO.PUBLIC.MILVUS_REPO;
DROP
DATABASE MILVUS_DEMO;
DROP
WAREHOUSE MILVUS_WAREHOUSE;

USE ROLE ACCOUNTADMIN;
DROP
ROLE MILVUS_ROLE;
DROP
SECURITY INTEGRATION SNOWSERVICES_INGRESS_OAUTH;
关于 Milvus
有关 Milvus 的更多信息，可以从
Milvus 介绍
和
快速入门
开始。当然，还有更详细的 API 介绍，可参考
Python
和
Java
版本，还有关于
Embeddings
和
Integrations
的信息可供参考。