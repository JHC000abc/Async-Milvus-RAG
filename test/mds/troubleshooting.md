故障排除
本页列出运行 Milvus 时可能出现的常见问题，以及可能的故障排除提示。本页面的问题分为以下几类：
启动问题
运行时问题
API 问题
etcd 崩溃问题
启动问题
启动错误通常是致命的。运行以下命令可查看错误详情：
$
docker logs <your milvus container
id
>
运行时问题
运行时发生的错误可能会导致服务崩溃。要排除此问题，请先检查服务器与客户端之间的兼容性，然后再继续操作。
API 问题
这些问题发生在 Milvus 服务器和客户端之间的 API 方法调用期间。它们将同步或非同步返回客户端。
etcd 崩溃问题
1. etcd pod 挂起
etcd 集群默认使用 pvc。需要为 Kubernetes 集群预先配置 StorageClass。
2. etcd pod 崩溃
当 etcd pod 崩溃时，
Error: bad member ID arg (strconv.ParseUint: parsing "": invalid syntax), expecting ID in Hex
，可以登录该 pod 并删除
/bitnami/etcd/data/member_id
文件。
3.当
etcd-0
仍在运行时，多个 pod 不断崩溃
如果多个 pod 在
etcd-0
仍在运行时不断崩溃，您可以运行以下代码。
kubectl scale sts
<
etcd
-
sts
>
--replicas=1
#
delete
the pvc
for
etcd
-1
and
etcd
-2
kubectl scale sts
<
etcd
-
sts
>
--replicas=3
4.所有 pod 均崩溃
当所有 pod 崩溃时，请尝试复制
/bitnami/etcd/data/member/snap/db
文件。使用
https://github.com/etcd-io/bbolt
修改数据库数据。
所有 Milvus 元数据都保存在
key
数据桶中。备份该数据桶中的数据并运行以下命令。请注意，
by-dev/meta/session
文件中的前缀数据不需要备份。
kubectl
kubectl scale sts <etcd-sts> --replicas=
0
# delete the pvc for etcd-0, etcd-1, etcd-2
kubectl kubectl scale sts <etcd-sts> --replicas=
1
# restore the backup data
如果您在解决问题时需要帮助，请随时
加入我们的
Discord 频道
，寻求 Milvus 团队的支持。
在 GitHub 上
提交问题
，并详细说明您的问题。