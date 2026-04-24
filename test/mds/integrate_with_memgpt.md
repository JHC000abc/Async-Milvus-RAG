与 Milvus 集成的 MemGPT
MemGPT
可轻松构建和部署有状态 LLM 代理。通过 Milvus 集成，您可以构建与外部数据源（RAG）连接的 Agents。
在本例中，我们将使用 MemGPT 与存储在 Milvus 中的自定义数据源聊天。
配置
要运行 MemGPT，应确保 Python 版本大于等于 3.10。
要启用 Milvus 后端，请确保安装了所需的依赖项：
$
pip install
'pymemgpt[milvus]'
你可以通过命令配置 Milvus 连接。
$
memgpt configure
...
? Select storage backend for archival data: milvus
? Enter the Milvus connection URI (Default: ~/.memgpt/milvus.db): ~/.memgpt/milvus.db
只需将 URI 设置为本地文件路径，例如
~/.memgpt/milvus.db
，就会通过 Milvus Lite 自动调用本地 Milvus 服务实例。
如果你有大规模数据，比如超过一百万个文档，我们建议在
docker 或 kubenetes
上设置性能更强的 Milvus 服务器。 在这种情况下，你的 URI 应该是服务器 URI，比如
http://localhost:19530
。
创建外部数据源
要将外部数据输入 MemGPT 聊天机器人，我们首先需要创建一个数据源。
我们将使用
curl
下载 MemGPT 研究论文（也可以直接从浏览器下载 PDF）：
#
we
're saving the file as "memgpt_research_paper.pdf"
$
curl -L -o memgpt_research_paper.pdf https://arxiv.org/pdf/2310.08560.pdf
下载论文后，我们可以使用
memgpt load
创建 MemGPT 数据源：
$
memgpt load directory --name memgpt_research_paper --input-files=memgpt_research_paper.pdf
Loading files: 100%|███████████████████████████████████| 1/1 [00:00<00:00,  3.94file/s]
Loaded 74 passages and 13 documents from memgpt_research_paper
将数据源连接到 MemGPT Agents
现在我们已经创建了数据源，可以随时将其附加到 MemGPT 聊天机器人上。
让我们使用
memgpt_doc
角色（也可以使用任何角色）创建一个新的聊天机器人：
#
reminder: `memgpt run --persona memgpt_doc` will create a new MemGPT agent using the `memgpt_doc` persona
$
memgpt run --persona memgpt_doc
与 Agents 聊天后，我们就可以将数据源 "附加 "到代理的存档内存中：
? Would you like to select an existing agent? No

🧬 Creating new agent...
->  🤖 Using persona profile: 'sam_pov'
->  🧑 Using human profile: 'basic'
🎉 Created new agent 'PoliteButterfly' (id=d26e1981-ff36-4095-97a0-61a1601dfb5d)

Hit enter to begin (will request first MemGPT message)

💭 Interesting, I've got a first-time user. Time to present myself and get to understand the user's needs. I wonder what brings Chad here today.
🤖 Greetings Chad! I'm MemGPT. How may I assist you today?

> Enter your message: /attach
? Select data source memgpt_research_paper
100%|███████████████████████████████████| 1/1 [00:00<00:00,  4.81it/s]
测试我们的新聊天机器人
既然数据已经加载到聊天机器人的内存中，我们就可以开始提问了：
> Enter your message: The paper I loaded into your archival memory is called MemGPT. Can you tell me more about it?

💭 It seems Chad would like to know more about the paper titled 'MemGPT' that's stored in my archival memory. It's time to search the archival memory for details and background data to provide a comprehensive
understanding of the paper. Let's remember to page through results until I've gathered enough information to answer Chad's enquiry.
⚡🧠 [function] searching memory with archival_memory_search
💭 Based on the found results, MemGPT is an AI system designed for tasks like extended conversations and document analysis. It efficiently manages different tiers of storage to provide extended context within
the LLM’s limited cap. Also, noteworthy from my findings is that MemGPT performs impressively in deep memory retrieval (DMR) and document QA tasks. Let's prepare a comprehensive response for Chad.
🤖 Certainly, Chad. MemGPT, or MemoryGPT, is a system specially designed for tasks like extended conversations and document analysis which are traditionally hindered by the limited context windows of modern 
Large Language Models (LLMs). It uses a technique inspired by hierarchical memory systems in traditional operating systems, called virtual context management. This technique allows for an effective provision 
of extended context within an LLM’s limited context window by intelligently managing different storage tiers, much like paging between physical memory and disk. Notably, MemGPT outperforms the fixed-context 
baselines in deep memory retrieval and it's able to analyze large documents with precision.