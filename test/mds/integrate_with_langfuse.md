使用 Langfuse 在 RAG 中跟踪查询
这是一本简单的烹饪手册，演示了如何使用 Langfuse 在 RAG 中跟踪查询。RAG 管道是通过 LlamaIndex 和 Milvus Lite 来实现文档的存储和检索的。
在本快速入门中，我们将向您展示如何使用 Milvus Lite 作为向量存储设置 LlamaIndex 应用程序。我们还将向你展示如何使用 Langfuse LlamaIndex 集成来跟踪你的应用程序。
Langfuse
是一个开源 LLM 工程平台，可帮助团队协作调试、分析和迭代 LLM 应用程序。所有平台功能均已集成，以加快开发工作流程。
Milvus Lite
是 Milvus 的轻量级版本，
Milvus
是一个开源向量数据库，可通过向量嵌入和相似性搜索为人工智能应用提供支持。
设置
确保已安装
llama-index
和
langfuse
。
$ pip install llama-index langfuse llama-index-vector-stores-milvus --upgrade
初始化集成。从
Langfuse 项目设置
中获取 API 密钥，并用密钥值替换 public_key secret_key。本示例使用 OpenAI 进行嵌入和聊天完成，因此还需要在环境变量中指定 OpenAI 密钥。
import
os
# Get keys for your project from the project settings page
# https://cloud.langfuse.com
os.environ[
"LANGFUSE_PUBLIC_KEY"
] =
""
os.environ[
"LANGFUSE_SECRET_KEY"
] =
""
os.environ[
"LANGFUSE_HOST"
] =
"https://cloud.langfuse.com"
# 🇪🇺 EU region
# os.environ["LANGFUSE_HOST"] = "https://us.cloud.langfuse.com" # 🇺🇸 US region
# Your openai key
os.environ[
"OPENAI_API_KEY"
] =
""
from
llama_index.core
import
Settings
from
llama_index.core.callbacks
import
CallbackManager
from
langfuse.llama_index
import
LlamaIndexCallbackHandler
 
langfuse_callback_handler = LlamaIndexCallbackHandler()
Settings.callback_manager = CallbackManager([langfuse_callback_handler])
使用 Milvus Lite 索引
from
llama_index.core
import
Document

doc1 = Document(text=
"""
Maxwell "Max" Silverstein, a lauded movie director, screenwriter, and producer, was born on October 25, 1978, in Boston, Massachusetts. A film enthusiast from a young age, his journey began with home movies shot on a Super 8 camera. His passion led him to the University of Southern California (USC), majoring in Film Production. Eventually, he started his career as an assistant director at Paramount Pictures. Silverstein's directorial debut, “Doors Unseen,” a psychological thriller, earned him recognition at the Sundance Film Festival and marked the beginning of a successful directing career.
"""
)
doc2 = Document(text=
"""
Throughout his career, Silverstein has been celebrated for his diverse range of filmography and unique narrative technique. He masterfully blends suspense, human emotion, and subtle humor in his storylines. Among his notable works are "Fleeting Echoes," "Halcyon Dusk," and the Academy Award-winning sci-fi epic, "Event Horizon's Brink." His contribution to cinema revolves around examining human nature, the complexity of relationships, and probing reality and perception. Off-camera, he is a dedicated philanthropist living in Los Angeles with his wife and two children.
"""
)
# Example index construction + LLM query
from
llama_index.core
import
VectorStoreIndex
from
llama_index.core
import
StorageContext
from
llama_index.vector_stores.milvus
import
MilvusVectorStore


vector_store = MilvusVectorStore(
    uri=
"tmp/milvus_demo.db"
, dim=
1536
, overwrite=
False
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    [doc1,doc2], storage_context=storage_context
)
查询
# Query
response = index.as_query_engine().query(
"What did he do growing up?"
)
print
(response)
# Chat
response = index.as_chat_engine().chat(
"What did he do growing up?"
)
print
(response)
在 Langfuse 中探索痕迹
# As we want to immediately see result in Langfuse, we need to flush the callback handler
langfuse_callback_handler.flush()
完成！您可以在 Langfuse 项目中看到索引和查询的痕迹。
示例跟踪（公开链接）：
查询
查询（聊天）
Langfuse 中的跟踪：
Langfuse 跟踪
对更多高级功能感兴趣？
请参阅完整的
集成文档
，了解更多高级功能和使用方法：
与 Langfuse Python SDK 和其他集成的互操作性
为痕迹添加自定义元数据和属性