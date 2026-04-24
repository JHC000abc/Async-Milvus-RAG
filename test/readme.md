```sql
create table rag_qa
(
    id            bigint auto_increment comment '主键ID'
        primary key,
    question      varchar(1000)                       not null comment '用户问题文本',
    question_hash varchar(64)                         not null comment '问题文本的哈希值(如SHA256)，用于规避索引长度超限并保证唯一性',
    answer        text                                null comment '系统回答内容',
    update_time   timestamp default CURRENT_TIMESTAMP null on update CURRENT_TIMESTAMP comment '记录更新时间，由数据库自动维护',
    create_time   timestamp default CURRENT_TIMESTAMP null comment '记录创建时间，由数据库自动维护',
    constraint question_hash
        unique (question_hash)
)
    comment 'RAG问答记录表' collate = utf8mb4_unicode_ci;


```

### 导入 rag_qa.sql 文件到数据库中。


```bash
# CLIP_MODEL_TYPE 支持 512 768 1024 三种
docker run -d --name clip-cpu-server -p 8001:8000 -v $(pwd)/clip_model_cache:/root/.cache/clip -e CLIP_MODEL_TYPE=768 --restart always jhc0000abc/clip-server-cpu:latest
```


```bash
#  BAAI/bge-reranker-v2-m3
docker run -itd --restart=always \
   --name bge-reranker \
   --gpus all \
   -p 7997:7997 \
   -e HF_ENDPOINT=https://hf-mirror.com \
   -e HF_HOME=/app/.cache \
   -v /home/jhc/shared/rerankers/model_cache:/app/.cache \
   --entrypoint /bin/sh \
   infinity-gtx1050 \
   -c "/app/.venv/bin/pip uninstall -y flash-attn && /app/.venv/bin/python /app/.venv/bin/infinity_emb v2 --model-id BAAI/bge-reranker-v2-m3 --engine torch --dtype float32 --device cuda --batch-size 4"

```



```bash
# attu
docker run -itd --name attu --restart=always -p 3000:3000 -v /home/jhc/attu/data:/data zilliz/attu:v3.0.0-beta.3

```

