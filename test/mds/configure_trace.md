跟踪相关配置
trace.exporter
说明
默认值
跟踪输出类型，默认为 stdout、
可选值：['noop'、'stdout'、'jaeger'、'otlp'] 可选值
无
trace.sampleFraction
说明
默认值
基于 traceID 的采样器的分数、
可选值：[0, 1]
分数 >= 1 将始终采样。小于 0 的分数视为 0。
0
trace.jaeger.url
说明
默认值
当输出者为 jaeger 时，应设置 jaeger 的 URL
trace.otlp.endpoint
说明
默认值
例如"127.0.0.1:4317 "表示 grpc，"127.0.0.1:4318 "表示 http
trace.otlp.method
说明
默认值
otlp 导出方法，可接受值：["grpc"、"http"]，默认使用 "grpc"。
trace.initTimeoutSeconds
说明
默认值
segcore 初始化超时（秒），防止 otlp grpc 永远挂起
10