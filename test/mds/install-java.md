安装 Milvus Java SDK
本主题介绍如何为 Milvus 安装 Milvus Java SDK。
当前版本的 Milvus 支持 Python、Node.js、GO 和 Java SDK。
要求
Java（8 或更高版本）
Apache Maven 或 Gradle/Grails
安装 Milvus Java SDK
运行以下命令安装 Milvus Java SDK。
Apache Maven
<
dependency
>
<
groupId
>
io.milvus
</
groupId
>
<
artifactId
>
milvus-sdk-java
</
artifactId
>
<
version
>
2.6.16
</
version
>
</
dependency
>
Gradle/Grails
implementation
'io.milvus:milvus-sdk-java:2.6.16'
下一步
安装 Milvus Java SDK 后，您可以
学习 Milvus 的基本操作：
管理 Collections
管理分区
插入、倒置和删除
单向量搜索
混合搜索
探索
Milvus Java 应用程序接口参考