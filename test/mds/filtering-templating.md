过滤器模板
在 Milvus 中，包含大量元素的复杂过滤表达式，尤其是那些涉及非 ASCII 字符（如中日韩字符）的表达式，会严重影响查询性能。为了解决这个问题，Milvus 引入了过滤表达式模板机制，旨在通过减少解析复杂表达式所花费的时间来提高效率。本页介绍了在搜索、查询和删除操作中使用过滤表达式模板的方法。
概述
过滤表达式模板化允许你创建带有占位符的过滤表达式，这些占位符可以在查询执行过程中动态替换为值。使用模板，可以避免直接在过滤器中嵌入大型数组或复杂表达式，从而减少解析时间并提高查询性能。
假设有一个涉及两个字段
age
和
city
的过滤器表达式，要查找所有年龄大于 25 岁且居住在 "北京"（北京）或 "上海"（上海）的人。您可以使用模板来代替直接在筛选表达式中嵌入值：
filter
=
"age > {age} AND city IN {city}"
filter_params = {
"age"
:
25
,
"city"
: [
"北京"
,
"上海"
]}
在这里，
{age}
和
{city}
是占位符，在执行查询时将被替换为
filter_params
中的实际值。
在 Milvus 中使用过滤表达式模板有几个主要优点：
减少解析时间
：通过用占位符替换大型或复杂的过滤器表达式，系统可以减少解析和处理过滤器的时间。
提高查询性能
：解析开销减少后，查询性能就会提高，从而获得更高的 QPS 和更快的响应时间。
可扩展性
：随着数据集的增长和过滤器表达式的复杂化，模板化可确保性能保持高效和可扩展。
搜索操作符
对于 Milvus 中的搜索操作，
filter
表达式用于定义过滤条件，
filter_params
参数用于指定占位符的值。
filter_params
字典包含 Milvus 将用于代入过滤表达式的动态值。
expr =
"age > {age} AND city IN {city}"
filter_params = {
"age"
:
25
,
"city"
: [
"北京"
,
"上海"
]}
res = client.search(
"hello_milvus"
,
    vectors[:nq],
filter
=expr,
    limit=
10
,
    output_fields=[
"age"
,
"city"
],
    search_params={
"metric_type"
:
"COSINE"
,
"params"
: {
"search_list"
:
100
}},
    filter_params=filter_params,
)
在本例中，Milvus 将在执行搜索时用
25
动态替换
{age}
，用
["北京", "上海"]
动态替换
{city}
。
查询操作符
同样的模板机制也可应用于 Milvus 的查询操作符。在
query
函数中，您可以定义过滤表达式，并使用
filter_params
指定要替换的值。
expr =
"age > {age} AND city IN {city}"
filter_params = {
"age"
:
25
,
"city"
: [
"北京"
,
"上海"
]}
res = client.query(
"hello_milvus"
,
filter
=expr,
    output_fields=[
"age"
,
"city"
],
    filter_params=filter_params
)
通过使用
filter_params
，Milvus 可以有效处理值的动态插入，提高查询执行速度。
删除操作符
在删除操作中也可以使用过滤表达式模板。与搜索和查询类似，
filter
表达式定义条件，
filter_params
为占位符提供动态值。
expr =
"age > {age} AND city IN {city}"
filter_params = {
"age"
:
25
,
"city"
: [
"北京"
,
"上海"
]}
res = client.delete(
"hello_milvus"
,
filter
=expr,
    filter_params=filter_params
)
这种方法可以提高删除操作的性能，尤其是在处理复杂的过滤条件时。
结论
过滤器表达式模板化是优化 Milvus 查询性能的重要工具。通过使用占位符和
filter_params
字典，可以大大减少解析复杂过滤器表达式所花费的时间。这将加快查询执行速度，提高整体性能。