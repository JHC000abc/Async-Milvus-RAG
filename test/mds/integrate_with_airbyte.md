Airbyte：开源数据移动基础架构
Airbyte 是一种开源数据移动基础架构，用于构建提取和加载（EL）数据管道。它专为多功能性、可扩展性和易用性而设计。Airbyte 的连接器目录 "开箱即用"，预置了 350 多个连接器。使用这些连接器，只需几分钟就能开始从数据源向目的地复制数据。
Airbyte 的主要组件
1.连接器目录
350 多个预建连接器
：Airbyte 的连接器目录 "开箱即用"，包含 350 多个预建连接器。这些连接器可用于在几分钟内开始将数据从源复制到目标。
无代码连接器生成器
：您可以通过
无代码连接器生成器等
工具轻松扩展 Airbyte 的功能，以支持您的自定义用例。
2.平台
Airbyte 平台提供配置和扩展数据移动操作所需的所有水平服务，可作为
云管理
或
自我管理
。
3.用户界面
Airbyte 具有用户界面、
PyAirbyte
（Python 库）、
API
和
Terraform Provider
，可与您偏好的工具和基础设施管理方法集成。
借助 Airbyte 的功能，用户可将数据源整合到 Milvus 集群，进行相似性搜索。
开始之前
您需要
Zendesk 账户（或其他要同步数据的数据源）
Airbyte 账户或本地实例
OpenAI API 密钥
Milvus 集群
本地已安装 Python 3.10
设置 Milvus 集群
如果您已经部署了用于生产的 K8s 集群，则可以跳过此步骤，直接
部署 Milvus Operator
。如果没有，可以按照
步骤
使用 Milvus Operator 部署 Milvus 群集。
单个实体（在我们的例子中是支持票单和知识库文章）存储在 "Collection "中--群集设置完成后，您需要创建一个 Collection。选择一个合适的名称，并将 "维度"（Dimension）设置为 1536，以便与 OpenAI Embeddings 服务生成的向量维度相匹配。
创建后，记录端点和
验证
信息。
在 Airbyte 中设置连接
我们的数据库已经准备就绪，现在就来移动一些数据！为此，我们需要在 Airbyte 中配置连接。要么在
cloud.airbyte.com
注册 Airbyte 云账户，要么按照
文档中的
说明启动本地实例。
设置源
实例运行后，我们需要设置连接--单击 "新建连接 "并选择 "Zendesk Support "连接器作为源。单击 "测试并保存 "按钮后，Airbyte 将检查是否可以建立连接。
在 Airbyte 云上，单击 "验证 "按钮即可轻松进行验证。使用本地 Airbyte 实例时，请遵循
文档
页面上概述的说明。
设置目的地
如果一切正常，下一步就是设置要将数据移动到的目的地。在这里，选择 "Milvus "连接器。
Milvus 连接器能做三件事：
分块和格式化
- 将 Zendesk 记录分割成文本和元数据。如果文本大于指定的分块大小，记录会被分割成多个部分，分别加载到 Collections 中。拆分文本（或分块）可能发生在大型支持票单或知识文章等情况下。通过分割文本，可以确保搜索总是能得到有用的结果。
让我们使用 1000 个标记的分块大小，以及正文、标题、描述和主题等文本字段，因为这些将出现在我们从 Zendesk 收到的数据中。
嵌入
--使用机器学习模型将处理部分生成的文本块转换为向量嵌入，然后就可以搜索语义相似性了。要创建嵌入，您必须提供 OpenAI API 密钥。Airbyte 会将每个文本块发送到 OpenAI，并将生成的向量添加到加载到 Milvus 集群的实体中。
索引
--一旦你将块向量化，你就可以将它们加载到数据库中。为此，请插入您在 Milvus 集群中设置集群和 Collections 时得到的信息。
点击 "测试并保存 "将检查一切是否排列正确（有效凭证、集合存在且与配置的 Embedding 具有相同的向量维度等）。
设置流同步流程
数据流准备就绪前的最后一步是选择要同步的 "流"。流是源中记录的 Collections。由于 Zendesk 支持大量与我们的用例无关的流，因此我们只选择 "票单 "和 "文章"，禁用其他所有流，以节省带宽并确保只有相关信息才会显示在搜索中：
您可以通过单击流名称来选择要从源中提取的字段。增量|追加+删减 "同步模式意味着后续的连接运行会保持 Zendesk 和 Milvus 的同步，同时传输最少的数据（仅传输自上次运行以来发生变化的文章和票单）。
连接建立后，Airbyte 将立即开始同步数据。可能需要几分钟才能出现在你的 Milvus Collections 中。
如果您选择复制频率，Airbyte 将定期运行，使您的 Milvus Collections 与 Zendesk 文章和新创建问题的更改保持同步。
检查流程
您可以在 Milvus 群集用户界面中检查 Collections 中的数据结构，方法是导航到 playground 并执行 "查询数据 "查询，过滤器设置为"_ab_stream == （"票据/"）"。
在结果视图中可以看到，来自 Zendesk 的每条记录都作为独立实体存储在 Milvus 中，并带有所有指定的元数据。嵌入所基于的文本块显示为 "text "属性--这是使用 OpenAI 嵌入的文本，也是我们要搜索的内容。
构建查询 Collections 的 Streamlit 应用程序
我们的数据已经准备就绪--现在我们需要构建应用程序来使用它。在本例中，应用程序将是一个简单的支持表单，供用户提交支持案例。当用户点击提交时，我们将做两件事：
搜索同一组织用户提交的类似单子
搜索可能与用户相关的基于知识的文章
在这两种情况下，我们都将利用 OpenAI Embeddings 进行语义搜索。为此，用户输入的问题描述也会被嵌入，并用于从 Milvus 集群中检索类似的实体。如果有相关结果，则会显示在表单下方。
设置用户界面环境
您需要在本地安装 Python，因为我们将使用 Streamlit 来实现应用程序。
首先，在本地安装 Streamlit、Milvus 客户端库和 OpenAI 客户端库：
pip install streamlit pymilvus openai
要渲染基本的支持表单，请创建一个 python 文件
basic_support_form.py
：
import
streamlit
as
st
with
st.form(
"my_form"
):
    st.write(
"Submit a support case"
)
    text_val = st.text_area(
"Describe your problem"
)

    submitted = st.form_submit_button(
"Submit"
)
if
submitted:
# TODO check for related support cases and articles
st.write(
"Submitted!"
)
使用 Streamlit run 运行应用程序：
streamlit run basic_support_form.py
这将渲染一个基本表单：
本示例的代码也可在
GitHub
上找到。
设置后台查询服务
接下来，让我们检查现有的可能相关的未结票单。为此，我们使用 OpenAI 嵌入了用户输入的文本，然后在我们的 Collections 上进行了相似性搜索，筛选出仍然开放的票单。如果所提供的票单与现有票单之间的距离非常小，就会让用户知道，并且不会提交：
import
streamlit
as
st
import
os
import
pymilvus
import
openai
with
st.form(
"my_form"
):
    st.write(
"Submit a support case"
)
    text_val = st.text_area(
"Describe your problem?"
)

    submitted = st.form_submit_button(
"Submit"
)
if
submitted:
import
os
import
pymilvus
import
openai

        org_id =
360033549136
# TODO Load from customer login data
pymilvus.connections.connect(uri=os.environ[
"MILVUS_URL"
], token=os.environ[
"MILVUS_TOKEN"
])
        collection = pymilvus.Collection(
"zendesk"
)

        embedding = openai.Embedding.create(
input
=text_val, model=
"text-embedding-ada-002"
)[
'data'
][
0
][
'embedding'
]

        results = collection.search(data=[embedding], anns_field=
"vector"
, param={}, limit=
2
, output_fields=[
"_id"
,
"subject"
,
"description"
], expr=
f'status == "new" and organization_id ==
{org_id}
'
)

        st.write(results[
0
])
if
len
(results[
0
]) >
0
and
results[
0
].distances[
0
] <
0.35
:
            matching_ticket = results[
0
][
0
].entity
            st.write(
f"This case seems very similar to
{matching_ticket.get(
'subject'
)}
(id #
{matching_ticket.get(
'_id'
)}
). Make sure it has not been submitted before"
)
else
:
            st.write(
"Submitted!"
)
这里发生了几件事：
建立与 Milvus 集群的连接。
使用 OpenAI 服务生成用户输入描述的 Embeddings。
执行相似性搜索，根据票单状态和组织 ID 过滤结果（因为只有同一组织的开放票单才相关）。
如果有结果，且现有票单的嵌入向量与新输入文本的嵌入向量之间的距离低于某个阈值，则会指出这一事实。
要运行新应用程序，需要先设置 OpenAI 和 Milvus 的环境变量：
export MILVUS_TOKEN=...
export MILVUS_URL=https://...
export OPENAI_API_KEY=sk-...

streamlit run app.py
当尝试提交已存在的票单时，结果将是这样的：
本示例的代码也可以在
GitHub
上找到。
显示更多相关信息
从隐藏在最终版本中的绿色调试输出中可以看到，有两张票单符合我们的搜索条件（状态为新建、来自当前组织、靠近嵌入向量）。但是，第一张（相关）的排名高于第二张（在这种情况下不相关），这反映在较低的距离值上。嵌入向量中捕捉到了这种关系，而不像常规全文搜索那样直接匹配单词。
最后，让我们在提交票单后显示有用的信息，为用户提供尽可能多的相关信息。
为此，我们将在提交票单后进行第二次搜索，获取匹配度最高的知识库文章：
......
else
:
# TODO Actually send out the ticket
st.write(
"Submitted!"
)
            article_results = collection.search(data=[embedding], anns_field=
"vector"
, param={}, limit=
5
, output_fields=[
"title"
,
"html_url"
], expr=
f'_ab_stream == "articles"'
)
            st.write(article_results[
0
])
if
len
(article_results[
0
]) >
0
:
                st.write(
"We also found some articles that might help you:"
)
for
hit
in
article_results[
0
]:
if
hit.distance <
0.362
:
                        st.write(
f"* [
{hit.entity.get(
'title'
)}
](
{hit.entity.get(
'html_url'
)}
)"
)
如果没有相似度较高的开放支持票单，则提交新票单，相关知识文章将显示在下方：
此示例的代码也可在
Github
上找到。
结论
虽然这里显示的用户界面并不是实际的支持表单，只是用来说明使用案例的一个示例，但 Airbyte 和 Milvus 的结合是非常强大的--它可以轻松地从各种来源（从 Postgres 等数据库到 Zendesk 或 GitHub 等 API，再到使用 Airbyte 的 SDK 或可视化连接器生成器构建的完全自定义来源）加载文本，并以嵌入的形式在 Milvus 中进行索引，Milvus 是一个强大的向量搜索引擎，能够扩展到海量数据。
Airbyte 和 Milvus 是开源的，完全免费，可在您的基础架构上使用，如果需要，还可通过云服务卸载操作符。
除了本文介绍的经典语义搜索用例外，一般设置还可用于使用 RAG 方法（检索增强生成）构建问题解答聊天机器人、推荐系统，或帮助提高广告的相关性和效率。