流媒体相关配置
与流媒体服务相关的任何配置。
streaming.walBalancer.triggerInterval
说明
默认值
后台平衡任务触发的时间间隔，默认为 1 分钟。
也可将其设置为持续时间字符串，如 30s 或 1m30s，请参阅 time.ParseDuration。
1m
streaming.walBalancer.backoffInitialInterval
说明
默认值
平衡任务触发回退的初始间隔，默认为 50 毫秒。
也可将其设置为持续时间字符串，如 30s 或 1m30s，请参阅 time.ParseDuration。
50 毫秒
streaming.walBalancer.backoffMultiplier
说明
默认值
平衡任务触发延迟的乘数，默认为 2
2
streaming.walBroadcaster.concurrencyRatio
说明
默认值
基于钱包广播器 CPU 数量的并发比率，默认为 1。
1
streaming.txn.defaultKeepaliveTimeout
说明
默认值
wal txn 的默认超时时间，默认为 10 秒
10s