将 Apache Spark™ 与 Milvus/Zilliz Cloud 用于人工智能流水线
Spark-Milvus 连接器
提供了 Apache Spark 和 Databricks 与 Milvus 和 Zilliz Cloud 的集成。它将 Apache Spark 强大的大数据处理和机器学习（ML）功能与 Milvus 最先进的向量搜索功能连接起来。这种集成能够简化工作流程，实现人工智能驱动的搜索、高级分析、ML 训练以及大规模向量数据的高效管理。
Apache Spark 是一个分布式数据处理平台，专为以高速计算处理海量数据集而设计。与 Milvus 或 Zilliz Cloud 搭配使用时，它能为语义搜索、推荐系统和人工智能驱动的数据分析等用例带来新的可能性。
例如，Spark 可以批量处理大型数据集，通过 ML 模型生成嵌入式数据，然后使用 Spark-Milvus 连接器将这些嵌入式数据直接存储在 Milvus 或 Zilliz Cloud 中。编入索引后，就可以快速搜索或分析这些数据，为人工智能和大数据工作流创建一个强大的管道。
Spark-Milvus 连接器支持迭代和批量数据摄入 Milvus、系统间数据同步以及对存储在 Milvus 中的向量数据进行高级分析等任务。本指南将指导您完成以下步骤，以便在以下用例中有效配置和使用连接器：
高效地将向量数据大批量加载到 Milvus 中、
在 Milvus 和其他存储系统或数据库之间移动数据、
利用 Spark MLlib 和其他人工智能工具分析 Milvus 中的数据。
快速启动
准备工作
Spark-Milvus Connector 支持 Scala 和 Python 编程语言。用户可以使用
Pyspark
或
Spark-shell
。要运行此演示，请按以下步骤设置包含 Spark-Milvus Connector 依赖关系的 Spark 环境：
安装 Apache Spark（版本 >= 3.3.0）
您可以参考
官方文档
安装 Apache Spark。
下载
spark-milvus
jar 文件。
wget https://github.com/zilliztech/spark-milvus/raw/1.0.0-SNAPSHOT/output/spark-milvus-1.0.0-SNAPSHOT.jar
将
spark-milvus
jar 作为依赖项之一启动 Spark 运行时。
要使用 Spark-Milvus 连接器启动 Spark 运行时，请将下载的
spark-milvus
作为依赖项添加到命令中。
pyspark
./bin/pyspark --jars spark-milvus-1.0.0-SNAPSHOT.jar
Spark-shell
./bin/spark-shell --jars spark-milvus-1.0.0-SNAPSHOT.jar
演示
在本演示中，我们将创建一个包含向量数据的 Spark DataFrame 样本，并通过 Spark-Milvus Connector 将其写入 Milvus。根据 Schema 和指定的选项，Milvus 将自动创建一个 Collections。
Python
Scala
from
pyspark.sql
import
SparkSession

columns = [
"id"
,
"text"
,
"vec"
]
data = [(
1
,
"a"
, [
1.0
,
2.0
,
3.0
,
4.0
,
5.0
,
6.0
,
7.0
,
8.0
]),
    (
2
,
"b"
, [
1.0
,
2.0
,
3.0
,
4.0
,
5.0
,
6.0
,
7.0
,
8.0
]),
    (
3
,
"c"
, [
1.0
,
2.0
,
3.0
,
4.0
,
5.0
,
6.0
,
7.0
,
8.0
]),
    (
4
,
"d"
, [
1.0
,
2.0
,
3.0
,
4.0
,
5.0
,
6.0
,
7.0
,
8.0
])]
sample_df = spark.sparkContext.parallelize(data).toDF(columns)
sample_df.write \
    .mode(
"append"
) \
    .option(
"milvus.host"
,
"localhost"
) \
    .option(
"milvus.port"
,
"19530"
) \
    .option(
"milvus.collection.name"
,
"hello_spark_milvus"
) \
    .option(
"milvus.collection.vectorField"
,
"vec"
) \
    .option(
"milvus.collection.vectorDim"
,
"8"
) \
    .option(
"milvus.collection.primaryKeyField"
,
"id"
) \
    .
format
(
"milvus"
) \
    .save()
import org.apache.spark.sql.{SaveMode, SparkSession}

object Hello extends App {

  val spark = SparkSession.builder().master("local[*]")
    .appName("HelloSparkMilvus")
    .getOrCreate()

  import spark.implicits._

  // Create DataFrame
  val sampleDF = Seq(
    (1, "a", Seq(1.0,2.0,3.0,4.0,5.0)),
    (2, "b", Seq(1.0,2.0,3.0,4.0,5.0)),
    (3, "c", Seq(1.0,2.0,3.0,4.0,5.0)),
    (4, "d", Seq(1.0,2.0,3.0,4.0,5.0))
  ).toDF("id", "text", "vec")

  // set milvus options
  val milvusOptions = Map(
      "milvus.host" -> "localhost" -> uri,
      "milvus.port" -> "19530",
      "milvus.collection.name" -> "hello_spark_milvus",
      "milvus.collection.vectorField" -> "vec",
      "milvus.collection.vectorDim" -> "5",
      "milvus.collection.primaryKeyField", "id"
    )
    
  sampleDF.write.format("milvus")
    .options(milvusOptions)
    .mode(SaveMode.Append)
    .save()
}
执行上述代码后，你可以使用 SDK 或 Attu（Milvus 控制面板）在 Milvus 中查看插入的数据。您可以看到一个名为
hello_spark_milvus
的 Collection，其中已插入了 4 个实体。
功能和概念
Milvus 选项
在
快速入门
部分，我们展示了 Milvus 操作符的设置选项。这些选项被抽象为 Milvus 选项。它们用于创建与 Milvus 的连接，并控制 Milvus 的其他行为。并非所有选项都是强制性的。
选项键
默认值
说明
milvus.host
localhost
Milvus 服务器主机。详情请参阅
管理 Milvus 连接
。
milvus.port
19530
Milvus 服务器端口。详见
管理 Milvus 连接
。
milvus.username
root
Milvus 服务器的用户名。详见
管理 Milvus 连接
。
milvus.password
Milvus
Milvus 服务器密码。详见
管理 Milvus 连接
。
milvus.uri
--
Milvus 服务器 URI。详见
管理 Milvus 连接
。
milvus.token
--
Milvus 服务器令牌。详见
管理 Milvus 连接
。
milvus.database.name
default
要读取或写入的 Milvus 数据库名称。
milvus.collection.name
hello_milvus
要读取或写入的 Milvus Collections 的名称。
milvus.collection.primaryKeyField
None
Collections 中主键字段的名称。如果 Collection 不存在，则为必填项。
milvus.collection.vectorField
None
Collections 中向量字段的名称。如果 Collections 不存在，则为必填项。
milvus.collection.vectorDim
None
Collections 中向量字段的尺寸。如果 Collections 不存在，则为必填项。
milvus.collection.autoID
false
如果集合不存在，此选项指定是否自动为实体生成 ID。更多信息，请参阅
create_collection
milvus.bucket
a-bucket
Milvus 存储中的存储桶名称。该名称应与
Milvus.yaml
中的
minio.bucketName
相同。
milvus.rootpath
files
Milvus 存储的根路径。应与
milvus.yaml
中的
minio.rootpath
相同。
milvus.fs
s3a://
Milvus 存储的文件系统。
s3a://
适用于开源 Spark。Databricks 使用
s3://
。
milvus.storage.endpoint
localhost:9000
Milvus 存储的端点。应与
milvus.yaml
中的
minio.address
:
minio.port
相同。
milvus.storage.user
minioadmin
Milvus 存储的用户。应与
milvus.yaml
中的
minio.accessKeyID
相同。
milvus.storage.password
minioadmin
Milvus 存储的密码。应与
Milvus.yaml
中的
minio.secretAccessKey
相同。
milvus.storage.useSSL
false
是否为 Milvus 存储使用 SSL。应与
milvus.yaml
中的
minio.useSSL
相同。
Milvus 数据格式
Spark-Milvus 连接器支持以下列 Milvus 数据格式读写数据：
milvus
:Milvus 数据格式，用于从 Spark DataFrame 到 Milvus 实体的无缝转换。
milvusbinlog
:用于读取 Milvus 内置 binlog 数据的 Milvus 数据格式。
mjson
:用于向 Milvus 批量插入数据的 Milvus JSON 格式。
milvus
在
快速入门
中，我们使用
milvus
格式将样本数据写入 Milvus 集群。
milvus
格式是一种新的数据格式，支持将 Spark DataFrame 数据无缝写入 Milvus Collections。这是通过批量调用 Milvus SDK 的插入 API 实现的。如果某个 Collection 在 Milvus 中不存在，就会根据 Dataframe 的 Schema 创建一个新的 Collection。不过，自动创建的 Collection 可能不支持 Collection Schema 的所有功能。因此，建议先通过 SDK 创建一个 Collection，然后再使用 Spark-milvus 进行编写。有关详细信息，请参阅
演示
。
milvusbinlog
新数据格式
milvusbinlog
用于读取 Milvus 内置的 binlog 数据。Binlog 是 Milvus 基于 parquet 的内部数据存储格式。不幸的是，普通的 parquet 库无法读取它，所以我们实现了这种新的数据格式，以帮助 Spark 作业读取它。 除非你熟悉 Milvus 内部存储的细节，否则不建议直接使用
milvusbinlog
。我们建议使用下一节将介绍的
MilvusUtils
函数。
val df = spark.read
  .format("milvusbinlog")
  .load(path)
  .withColumnRenamed("val", "embedding")
mjson
Milvus 提供
Bulkinsert
功能，以便在操作大型数据集时获得更好的写入性能。然而，Milvus 使用的 JSON 格式与 Spark 的默认 JSON 输出格式略有不同。 为了解决这个问题，我们引入了
mjson
数据格式，以生成符合 Milvus 要求的数据。下面的示例展示了 JSON-lines 和
mjson
之间的区别：
JSON-lines：
{
"book_id"
:
101
,
"word_count"
:
13
,
"book_intro"
:
[
1.1
,
1.2
]
}
{
"book_id"
:
102
,
"word_count"
:
25
,
"book_intro"
:
[
2.1
,
2.2
]
}
{
"book_id"
:
103
,
"word_count"
:
7
,
"book_intro"
:
[
3.1
,
3.2
]
}
{
"book_id"
:
104
,
"word_count"
:
12
,
"book_intro"
:
[
4.1
,
4.2
]
}
{
"book_id"
:
105
,
"word_count"
:
34
,
"book_intro"
:
[
5.1
,
5.2
]
}
mjson （Milvus Bulkinsert 要求）：
{
"rows"
:
[
{
"book_id"
:
101
,
"word_count"
:
13
,
"book_intro"
:
[
1.1
,
1.2
]
}
,
{
"book_id"
:
102
,
"word_count"
:
25
,
"book_intro"
:
[
2.1
,
2.2
]
}
,
{
"book_id"
:
103
,
"word_count"
:
7
,
"book_intro"
:
[
3.1
,
3.2
]
}
,
{
"book_id"
:
104
,
"word_count"
:
12
,
"book_intro"
:
[
4.1
,
4.2
]
}
,
{
"book_id"
:
105
,
"word_count"
:
34
,
"book_intro"
:
[
5.1
,
5.2
]
}
]
}
未来将对此进行改进。我们建议在 Spark-milvus 集成中使用 parquet 格式，如果你的 Milvus 版本是 v2.3.7 以上，支持使用 Parquet 格式的 Bulkinsert。请参见 Github 上的
演示
。
MilvusUtils
MilvusUtils 包含多个有用的 util 函数。目前仅支持 Scala 语言。更多使用示例请参见
高级使用
部分。
MilvusUtils.readMilvusCollection
MilvusUtils.readMilvusCollection
是一个简单的接口，用于将整个 Milvus Collections 加载到 Spark 数据帧中。它封装了各种操作符，包括调用 Milvus SDK、读取
milvusbinlog
和常见的联合/连接操作。
val collectionDF = MilvusUtils.readMilvusCollection(spark, milvusOptions)
MilvusUtils.bulkInsertFromSpark
MilvusUtils.bulkInsertFromSpark
提供了一种将 Spark 输出文件大批量导入 Milvus 的便捷方法。它封装了 Milvus SDK 的
Bullkinsert
API。
df.write.format("parquet").save(outputPath)
MilvusUtils.bulkInsertFromSpark(spark, milvusOptions, outputPath, "parquet")
高级用法
在本节中，您将找到 Spark-Milvus 连接器用于数据分析和迁移的高级使用示例。更多演示，请参阅
示例
。
MySQL -> Embeddings -> Milvus
在本演示中，我们将
通过 Spark-MySQL 连接器从 MySQL 读取数据、
生成嵌入（以 Word2Vec 为例），以及
将嵌入数据写入 Milvus。
要启用 Spark-MySQL 连接器，需要在 Spark 环境中添加以下依赖项：
spark-shell
--jars
spark-milvus-
1.0
.
0
-SNAPSHOT
.jar
,mysql-connector-j-
x
.x
.x
.jar
import org.apache.spark.ml.feature.{Tokenizer, Word2Vec}
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.{SaveMode, SparkSession}
import zilliztech.spark.milvus.MilvusOptions._

import org.apache.spark.ml.linalg.Vector

object Mysql2MilvusDemo  extends App {

  val spark = SparkSession.builder().master("local[*]")
    .appName("Mysql2MilvusDemo")
    .getOrCreate()

  import spark.implicits._

  // Create DataFrame
  val sampleDF = Seq(
    (1, "Milvus was created in 2019 with a singular goal: store, index, and manage massive embedding vectors generated by deep neural networks and other machine learning (ML) models."),
    (2, "As a database specifically designed to handle queries over input vectors, it is capable of indexing vectors on a trillion scale. "),
    (3, "Unlike existing relational databases which mainly deal with structured data following a pre-defined pattern, Milvus is designed from the bottom-up to handle embedding vectors converted from unstructured data."),
    (4, "As the Internet grew and evolved, unstructured data became more and more common, including emails, papers, IoT sensor data, Facebook photos, protein structures, and much more.")
  ).toDF("id", "text")

  // Write to MySQL Table
  sampleDF.write
    .mode(SaveMode.Append)
    .format("jdbc")
    .option("driver","com.mysql.cj.jdbc.Driver")
    .option("url", "jdbc:mysql://localhost:3306/test")
    .option("dbtable", "demo")
    .option("user", "root")
    .option("password", "123456")
    .save()

  // Read from MySQL Table
  val dfMysql = spark.read
    .format("jdbc")
    .option("driver","com.mysql.cj.jdbc.Driver")
    .option("url", "jdbc:mysql://localhost:3306/test")
    .option("dbtable", "demo")
    .option("user", "root")
    .option("password", "123456")
    .load()

  val tokenizer = new Tokenizer().setInputCol("text").setOutputCol("tokens")
  val tokenizedDf = tokenizer.transform(dfMysql)

  // Learn a mapping from words to Vectors.
  val word2Vec = new Word2Vec()
    .setInputCol("tokens")
    .setOutputCol("vectors")
    .setVectorSize(128)
    .setMinCount(0)
  val model = word2Vec.fit(tokenizedDf)

  val result = model.transform(tokenizedDf)

  val vectorToArrayUDF = udf((v: Vector) => v.toArray)
  // Apply the UDF to the DataFrame
  val resultDF = result.withColumn("embedding", vectorToArrayUDF($"vectors"))
  val milvusDf = resultDF.drop("tokens").drop("vectors")

  milvusDf.write.format("milvus")
    .option(MILVUS_HOST, "localhost")
    .option(MILVUS_PORT, "19530")
    .option(MILVUS_COLLECTION_NAME, "text_embedding")
    .option(MILVUS_COLLECTION_VECTOR_FIELD, "embedding")
    .option(MILVUS_COLLECTION_VECTOR_DIM, "128")
    .option(MILVUS_COLLECTION_PRIMARY_KEY, "id")
    .mode(SaveMode.Append)
    .save()
}
Milvus -> 转换 -> Milvus
在本演示中，我们将
从一个 Milvus Collections 中读取数据、
应用转换（以 PCA 为例），以及
通过 Bulkinsert API 将转换后的数据写入另一个 Milvus。
PCA 模型是一种可降低嵌入向量维度的变换模型，是机器学习中的常见操作。 你可以在变换步骤中添加任何其他处理操作，如过滤、连接或归一化。
import org.apache.spark.ml.feature.PCA
import org.apache.spark.ml.linalg.{Vector, Vectors}
import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions.udf
import org.apache.spark.sql.util.CaseInsensitiveStringMap
import zilliztech.spark.milvus.{MilvusOptions, MilvusUtils}

import scala.collection.JavaConverters._

object TransformDemo extends App {
  val sparkConf = new SparkConf().setMaster("local")
  val spark = SparkSession.builder().config(sparkConf).getOrCreate()

  import spark.implicits._

  val host = "localhost"
  val port = 19530
  val user = "root"
  val password = "Milvus"
  val fs = "s3a://"
  val bucketName = "a-bucket"
  val rootPath = "files"
  val minioAK = "minioadmin"
  val minioSK = "minioadmin"
  val minioEndpoint = "localhost:9000"
  val collectionName = "hello_spark_milvus1"
  val targetCollectionName = "hello_spark_milvus2"

  val properties = Map(
    MilvusOptions.MILVUS_HOST -> host,
    MilvusOptions.MILVUS_PORT -> port.toString,
    MilvusOptions.MILVUS_COLLECTION_NAME -> collectionName,
    MilvusOptions.MILVUS_BUCKET -> bucketName,
    MilvusOptions.MILVUS_ROOTPATH -> rootPath,
    MilvusOptions.MILVUS_FS -> fs,
    MilvusOptions.MILVUS_STORAGE_ENDPOINT -> minioEndpoint,
    MilvusOptions.MILVUS_STORAGE_USER -> minioAK,
    MilvusOptions.MILVUS_STORAGE_PASSWORD -> minioSK,
  )

  // 1, configurations
  val milvusOptions = new MilvusOptions(new CaseInsensitiveStringMap(properties.asJava))

  // 2, batch read milvus collection data to dataframe
  //  Schema: dim of `embeddings` is 8
  // +-+------------+------------+------------------+
  // | | field name | field type | other attributes |
  // +-+------------+------------+------------------+
  // |1|    "pk"    |    Int64   |  is_primary=True |
  // | |            |            |   auto_id=False  |
  // +-+------------+------------+------------------+
  // |2|  "random"  |    Double  |                  |
  // +-+------------+------------+------------------+
  // |3|"embeddings"| FloatVector|     dim=8        |
  // +-+------------+------------+------------------+
  val arrayToVectorUDF = udf((arr: Seq[Double]) => Vectors.dense(arr.toArray[Double]))
  val collectionDF = MilvusUtils.readMilvusCollection(spark, milvusOptions)
    .withColumn("embeddings_vec", arrayToVectorUDF($"embeddings"))
    .drop("embeddings")
  
  // 3. Use PCA to reduce dim of vector
  val dim = 4
  val pca = new PCA()
    .setInputCol("embeddings_vec")
    .setOutputCol("pca_vec")
    .setK(dim)
    .fit(collectionDF)
  val vectorToArrayUDF = udf((v: Vector) => v.toArray)
  // embeddings dim number reduce to 4
  // +-+------------+------------+------------------+
  // | | field name | field type | other attributes |
  // +-+------------+------------+------------------+
  // |1|    "pk"    |    Int64   |  is_primary=True |
  // | |            |            |   auto_id=False  |
  // +-+------------+------------+------------------+
  // |2|  "random"  |    Double  |                  |
  // +-+------------+------------+------------------+
  // |3|"embeddings"| FloatVector|     dim=4        |
  // +-+------------+------------+------------------+
  val pcaDf = pca.transform(collectionDF)
    .withColumn("embeddings", vectorToArrayUDF($"pca_vec"))
    .select("pk", "random", "embeddings")

  // 4. Write PCAed data to S3
  val outputPath = "s3a://a-bucket/result"
  pcaDf.write
    .mode("overwrite")
    .format("parquet")
    .save(outputPath)

  // 5. Config MilvusOptions of target table  
  val targetProperties = Map(
    MilvusOptions.MILVUS_HOST -> host,
    MilvusOptions.MILVUS_PORT -> port.toString,
    MilvusOptions.MILVUS_COLLECTION_NAME -> targetCollectionName,
    MilvusOptions.MILVUS_BUCKET -> bucketName,
    MilvusOptions.MILVUS_ROOTPATH -> rootPath,
    MilvusOptions.MILVUS_FS -> fs,
    MilvusOptions.MILVUS_STORAGE_ENDPOINT -> minioEndpoint,
    MilvusOptions.MILVUS_STORAGE_USER -> minioAK,
    MilvusOptions.MILVUS_STORAGE_PASSWORD -> minioSK,
  )
  val targetMilvusOptions = new MilvusOptions(new CaseInsensitiveStringMap(targetProperties.asJava))
  
  // 6. Bulkinsert Spark output files into milvus
  MilvusUtils.bulkInsertFromSpark(spark, targetMilvusOptions, outputPath, "parquet")
}
Databricks -> Zilliz Cloud
如果您使用的是 Zilliz Cloud（Milvus 托管服务），您可以利用其便捷的数据导入 API。Zilliz Cloud 提供全面的工具和文档，帮助您高效地从 Spark 和 Databricks 等各种数据源移动数据。只需设置一个 S3 桶作为中介，并开放其对 Zilliz Cloud 账户的访问。Zilliz Cloud 的数据导入 API 会自动将 S3 桶中的整批数据加载到您的 Zilliz Cloud 集群。
准备工作
通过向 Databricks 集群添加 jar 文件来加载 Spark 运行时。
您可以通过不同方式安装库。该截图显示的是从本地向集群上传 jar 文件。更多信息，请参阅 Databricks 文档中的
集群库
。
安装 Databricks 库
创建一个 S3 bucket，并将其配置为 Databricks 集群的外部存储位置。
Bulkinsert 要求将数据存储在临时存储桶中，以便 Zilliz Cloud 可以批量导入数据。您可以创建一个 S3 存储桶，并将其配置为 Databricks 的外部位置。详情请参阅
外部位置
。
确保 Databricks 凭据的安全。
有关详细信息，请参阅博客 "
在 Databricks 中安全管理凭据 "中
的说明。
演示
下面的代码片段展示了批量数据迁移过程。与上述 Milvus 示例类似，你只需替换凭证和 S3 存储桶地址。
// Write the data in batch into the Milvus bucket storage.
val outputPath = "s3://my-temp-bucket/result"
df.write
  .mode("overwrite")
  .format("mjson")
  .save(outputPath)
// Specify Milvus options.
val targetProperties = Map(
  MilvusOptions.MILVUS_URI -> zilliz_uri,
  MilvusOptions.MILVUS_TOKEN -> zilliz_token,
  MilvusOptions.MILVUS_COLLECTION_NAME -> targetCollectionName,
  MilvusOptions.MILVUS_BUCKET -> bucketName,
  MilvusOptions.MILVUS_ROOTPATH -> rootPath,
  MilvusOptions.MILVUS_FS -> fs,
  MilvusOptions.MILVUS_STORAGE_ENDPOINT -> minioEndpoint,
  MilvusOptions.MILVUS_STORAGE_USER -> minioAK,
  MilvusOptions.MILVUS_STORAGE_PASSWORD -> minioSK,
)
val targetMilvusOptions = new MilvusOptions(new CaseInsensitiveStringMap(targetProperties.asJava))
  
// Bulk insert Spark output files into Milvus
MilvusUtils.bulkInsertFromSpark(spark, targetMilvusOptions, outputPath, "mjson")
实践笔记本
为了帮助您快速上手 Spark-Milvus Connector，您可以查看笔记本，其中有指导您完成 Spark 到 Milvus 和 Zilliz Cloud 的流式和批量数据摄取示例。
Spark-Milvus 连接器实践