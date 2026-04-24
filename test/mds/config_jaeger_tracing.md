配置跟踪
本指南说明如何配置 Jaeger 为 Milvus 收集跟踪。
前提条件
已安装必要的工具，包括
Helm
和
Kubectl
。
必须安装 Cert-manager 1.6.1 或更高版本。请
点击此处
查看安装指南。
部署 Jaeger
Jaeger 是
Uber Technologies
发布的开源分布式跟踪平台。
1.在 Kubernetes 上安装 Jaeger 操作符
要安装操作符，请运行：
$
kubectl create namespace observability
$
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.62.0/jaeger-operator.yaml -n observability
此时，应该有一个
jaeger-operator
部署可用。运行以下命令即可查看：
$
kubectl get deployment jaeger-operator -n observability
NAME              DESIRED   CURRENT   UP-TO-DATE   AVAILABLE   AGE
jaeger-operator   1         1         1            1           48s
2.部署 Jaeger
创建 Jaeger 实例的最简单方法是创建类似下面示例的 YAML 文件。这将安装默认的 AllInOne 策略，在单个 pod 中部署
一体化
镜像（结合了
jaeger-agents
、
jaeger-collector
、
jaeger
-query
和 Jaeger UI），默认使用
内存存储
。
如果你想长期存储跟踪信息，请参考
生产策略
。
apiVersion:
jaegertracing.io/v1
kind:
Jaeger
metadata:
name:
jaeger
然后，YAML 文件可与
kubectl
一起使用：
$
kubectl apply -f simplest.yaml
几秒钟后，一个新的内存一体化 Jaeger 实例就会可用，适用于快速演示和开发目的。要检查已创建的实例，请列出 Jaeger 对象：
$
kubectl get jaegers
NAME     STATUS    VERSION   STRATEGY   STORAGE   AGE
jaeger   Running   1.62.0    allinone   memory    13s
使用 Helm 图表安装 Milvus
您可以使用 Helm Chart 安装或升级 Milvus，设置如下：
extraConfigFiles:
user.yaml:
|+
    trace:
      exporter: jaeger
      sampleFraction: 1
      jaeger:
        url: "http://jaeger-collector:14268/api/traces"
要将上述设置应用到新的 Milvus 部署，可以运行以下命令：
$
helm repo add zilliztech https://zilliztech.github.io/milvus-helm
$
helm repo update
$
helm upgrade --install -f values.yaml my-release milvus/milvus
要将上述设置应用到现有的 Milvus 部署，可以运行以下命令：
$
helm upgrade my-release -f values.yaml milvus/milvus
查看跟踪
一旦使用 Helm Chart 部署了 Jaeger 和 Milvus，dfault 就会启用入口。您可以运行以下命令查看入口：
$
kubectl get ingress
NAME           CLASS    HOSTS   ADDRESS         PORTS   AGE
jaeger-query   <none>   *       192.168.122.34  80      14m
一旦入口可用，就可以通过导航到
http://${ADDRESS}
访问 Jaeger 用户界面。将
${ADDRESS}
替换为入口的实际 IP 地址。
下面的截图显示了 Jaeger UI，其中有 Milvus 在搜索操作和加载 Collections 操作符期间的痕迹：
跟踪搜索请求
跟踪负载收集请求