GPU 相关配置
#使用 GPU 索引时，Milvus 将利用内存池来避免频繁的内存分配和删除。
#在这里，你可以设置内存池占用内存的大小，单位为 MB。
#注意，当实际内存需求超过 maxMemSize 设置的值时，Milvus 有可能崩溃。
#如果 initMemSize 和 MaxMemSize 都设置为零、
#milvus 将自动初始化 GPU 可用内存的一半、
#maxMemSize则为全部可用 GPU 内存。
gpu.initMemSize
说明
默认值
GPU 内存池初始大小
2048
gpu.maxMemSize
说明
默认值
Gpu 内存池最大大小
4096