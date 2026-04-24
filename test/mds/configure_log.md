日志相关配置
配置系统日志输出。
log.level
说明
默认值
Milvus 日志级别。选项：debug、info、warn、error、panic 和 fatal。
建议在测试和开发环境下使用 debug 级别，在生产环境下使用 info 级别。
信息
log.file.rootPath
说明
默认值
日志文件的根路径。
默认值为空，表示将日志文件输出到标准输出（stdout）和标准错误（stderr）。
如果该参数设置为有效的本地路径，Milvus 将在此路径下写入并存储日志文件。
将此参数设置为您有权限写入的路径。
log.file.maxSize
说明
默认值
日志文件的最大大小，单位：MB：MB。
300
log.file.maxAge
说明
默认值
日志文件自动清除前的最长保留时间，单位：天。最小值为 1。
10
log.file.maxBackups
说明
默认值
要备份的日志文件的最大数量，单位：天。最小值为 1。
20
log.format
说明
默认值
Milvus 日志格式。选项：文本和 JSON
文本
log.stdout
说明
默认值
是否启用 Stdout
真