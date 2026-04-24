在 Grafana 中可视化 Milvus 指标
本主题介绍如何使用 Grafana 可视化 Milvus 指标。
如
监控指南
所述，指标包含有用的信息，如特定 Milvus 组件使用了多少内存。监控指标可帮助您更好地了解 Milvus 性能及其运行状态，以便及时调整资源分配。
可视化是显示资源使用量随时间变化的图表，它能让你更容易地快速查看和注意到资源使用量的变化，尤其是在事件发生时。
本教程使用时间序列分析开源平台 Grafana 来可视化部署在 Kubernetes (K8s) 上的 Milvus 集群的各种性能指标。
前提条件
您已
在 K8s 上安装了 Milvus 集群
。）
在使用 Grafana 可视化指标之前，您需要
配置 Prometheus
以监控和收集指标。如果设置成功，您可以从
http://localhost:3000
访问 Grafana。或者也可以使用
admin:admin
的默认 Grafana
user:password
访问 Grafana。
使用 Grafana 可视化指标
1.下载并导入仪表盘
从 JSON 文件下载并导入 Milvus 仪表板。
wget
https://raw.githubusercontent.com/milvus-io/milvus/refs/heads/master/deployments/monitor/grafana/milvus-dashboard.json
下载并导入
2.查看指标
选择要监控的 Milvus 实例。然后就能看到 Milvus 组件面板。
选择实例
面板
下一步
如果你已将 Grafana 设置为可视化 Milvus 指标，你可能还想：
了解如何
为 Milvus 服务创建警报
调整
资源分配
扩大或缩小 Milvus 集群规模
如果你有兴趣升级 Milvus 版本、
阅读
Milvus 集群升级指南
和
Milvus 单机升级
指南
。