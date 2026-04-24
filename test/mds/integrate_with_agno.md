将 Milvus 与 Agno 相集成
Agno
（前身为 Phidata）是一个用于构建多模态代理的轻量级库。通过它，您可以创建能够理解文本、图像、音频和视频的多模态代理，并利用各种工具和知识源来完成复杂的任务。Agno 支持多代理协调，使代理团队能够协作并共同解决问题。它还提供了一个漂亮的 Agents UI，用于与您的代理进行交互。
Milvus 向量数据库可以高效地存储和检索嵌入信息。有了 Milvus 和 Agents，您可以轻松地将知识整合到 Agent 工作流程中。本文档是如何使用 Milvus 与 Agno 集成的基本指南。
准备工作
安装必要的依赖项：
$ pip install --upgrade agno pymilvus milvus-lite openai
如果您使用的是 Google Colab，要启用刚刚安装的依赖项，可能需要
重启运行时
（点击屏幕上方的 "运行时 "菜单，从下拉菜单中选择 "重启会话"）。
在本例中，我们将使用 OpenAI 作为 LLM。请将
api key
OPENAI_API_KEY
作为环境变量。
import
os

os.environ[
"OPENAI_API_KEY"
] =
"sk-xxxx"
初始化 Milvus
导入软件包并初始化 Milvus 向量数据库实例。
from
agno.agent
import
Agent
from
agno.knowledge.pdf_url
import
PDFUrlKnowledgeBase
from
agno.vectordb.milvus
import
Milvus
# Initialize Milvus
vector_db = Milvus(
    collection=
"recipes"
,
    uri=
"./milvus.db"
,
)
为 Milvus 服务器指定 Collections 名称、uri 和 token（选项）。
以下是设置 uri 和标记的方法：
如果你只需要一个本地向量数据库用于小规模数据或原型设计，将 uri 设置为一个本地文件，如
./milvus.db
，是最方便的方法，因为它会自动利用
Milvus Lite
将所有数据存储在这个文件中。
如果你有大规模数据，比如超过一百万个向量，你可以在
Docker 或 Kubernetes
上设置性能更强的 Milvus 服务器。在此设置中，请使用服务器地址和端口作为 uri，例如
http://localhost:19530
。如果在 Milvus 上启用了身份验证功能，请使用 "
:
" 作为令牌，否则不要设置令牌。
如果您使用
Zilliz Cloud
（Milvus 的全托管云服务），请调整
uri
和
token
，它们与 Zilliz Cloud 中的
公共端点和 API 密钥
相对应。
加载数据
创建 PDF url Knowledage 基础实例，并将数据加载到实例中。我们使用公共食谱 pdf 数据作为示例。
# Create knowledge base
knowledge_base = PDFUrlKnowledgeBase(
    urls=[
"https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"
],
    vector_db=vector_db,
)

knowledge_base.load(recreate=
False
)
# Comment out after first run
INFO    Creating
INFO    Loading knowledge  
INFO    Reading: https://phi-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf       
INFO    Added documents to knowledge base
使用 Agents 回答问题
将知识库集成到 Agents 中，然后我们就可以向 Agents 提出问题并得到回复。
# Create and use the agent
agent = Agent(knowledge=knowledge_base, show_tool_calls=
True
)
# Query the agent
agent.print_response(
"How to make Tom Kha Gai"
, markdown=
True
)
Output()


┏━ Message ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                                                             ┃
┃ How to make Tom Kha Gai                                                                                                                                     ┃
┃                                                                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
┏━ Response (6.9s) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                                                                                                             ┃
┃ Running:                                                                                                                                                    ┃
┃                                                                                                                                                             ┃
┃  • search_knowledge_base(query=Tom Kha Gai recipe)                                                                                                          ┃
┃                                                                                                                                                             ┃
┃ Here's a recipe for Tom Kha Gai, a delicious Thai chicken and galangal soup made with coconut milk:                                                         ┃
┃                                                                                                                                                             ┃
┃ Ingredients (One serving):                                                                                                                                  ┃
┃                                                                                                                                                             ┃
┃  • 150 grams chicken, cut into bite-size pieces                                                                                                             ┃
┃  • 50 grams sliced young galangal                                                                                                                           ┃
┃  • 100 grams lightly crushed lemongrass, julienned                                                                                                          ┃
┃  • 100 grams straw mushrooms                                                                                                                                ┃
┃  • 250 grams coconut milk                                                                                                                                   ┃
┃  • 100 grams chicken stock                                                                                                                                  ┃
┃  • 3 tbsp lime juice                                                                                                                                        ┃
┃  • 3 tbsp fish sauce                                                                                                                                        ┃
┃  • 2 leaves kaffir lime, shredded                                                                                                                           ┃
┃  • 1-2 bird’s eye chilies, pounded                                                                                                                          ┃
┃  • 3 leaves coriander                                                                                                                                       ┃
┃                                                                                                                                                             ┃
┃ Directions:                                                                                                                                                 ┃
┃                                                                                                                                                             ┃
┃  1 Bring the chicken stock and coconut milk to a slow boil.                                                                                                 ┃
┃  2 Add galangal, lemongrass, chicken, and mushrooms. Once the soup returns to a boil, season it with fish sauce.                                            ┃
┃  3 Wait until the chicken is cooked, then add the kaffir lime leaves and bird’s eye chilies.                                                                ┃
┃  4 Remove the pot from heat and add lime juice.                                                                                                             ┃
┃  5 Garnish with coriander leaves.                                                                                                                           ┃
┃                                                                                                                                                             ┃
┃ Tips:                                                                                                                                                       ┃
┃                                                                                                                                                             ┃
┃  • Keep the heat low throughout the cooking process to prevent the oil in the coconut milk from separating.                                                 ┃
┃  • If using mature galangal, reduce the amount.                                                                                                             ┃
┃  • Adding lime juice after removing the pot from heat makes it more aromatic.                                                                               ┃
┃  • Reduce the number of chilies for a milder taste.                                                                                                         ┃
┃                                                                                                                                                             ┃
┃ Enjoy making and savoring this flavorful Thai soup!                                                                                                         ┃
┃                                                                                                                                                             ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
恭喜你，你已经学会了在 Agno 中使用 Milvus 的基础知识。如果您想进一步了解如何使用 Agno，请参阅
官方文档
。