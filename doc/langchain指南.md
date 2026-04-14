## LangChain 在项目中的完整应用

LangChain 可以覆盖项目**核心 RAG 功能**，大大简化开发。

## 一、LangChain 功能全景图

```
┌─────────────────────────────────────────────────────────────┐
│                    LangChain 能力矩阵                         │
├─────────────────────────────────────────────────────────────┤
│ 1. 文档加载    │ 50+ 格式支持（PDF、PPT、Word、网页...）     │
│ 2. 文本拆分    │ 智能 Chunking，多种策略                     │
│ 3. Embedding   │ 集成主流模型（OpenAI、BGE、通义...）        │
│ 4. 向量存储    │ 20+ 向量数据库（Chroma、FAISS、Milvus...）  │
│ 5. 检索器      │ 相似度搜索、MMR、多路召回                   │
│ 6. 重排序      │ 提升检索精度                                │
│ 7. 提示词模板  │ 结构化提示词管理                            │
│ 8. 链式调用    │ LCEL 语法，简洁优雅                         │
│ 9. 对话记忆    │ 内置会话管理                                │
│ 10. Agent     │ 工具调用、决策能力                           │
└─────────────────────────────────────────────────────────────┘
```

## 二、具体功能实现

### 1. **文档加载（50+ 格式）**

```python
from langchain.document_loaders import (
    PyPDFLoader,           # PDF
    UnstructuredPPTLoader, # PPT
    Docx2txtLoader,       # Word
    CSVLoader,            # CSV
    TextLoader,           # TXT
    UnstructuredMarkdownLoader,  # Markdown
    UnstructuredHTMLLoader,      # HTML
    JSONLoader,           # JSON
    SeleniumURLLoader,    # 网页
)

# 统一加载接口
def load_document(file_path):
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith('.pptx'):
        loader = UnstructuredPPTLoader(file_path)
    elif file_path.endswith('.docx'):
        loader = Docx2txtLoader(file_path)
    else:
        loader = TextLoader(file_path, encoding='utf-8')
  
    return loader.load()

# 批量加载
from langchain.document_loaders import DirectoryLoader

loader = DirectoryLoader(
    './docs/',
    glob="**/*.pdf",
    loader_cls=PyPDFLoader
)
documents = loader.load()
```

### 2. **智能文本拆分**

```python
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,  # 递归拆分（最常用）
    SemanticChunker,                  # 语义拆分
    MarkdownHeaderTextSplitter,       # Markdown 标题拆分
    PythonCodeTextSplitter,           # 代码拆分
)

# 基础拆分
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""]
)
chunks = text_splitter.split_documents(documents)

# 语义拆分（效果更好）
from langchain.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-zh")
semantic_splitter = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile"
)
semantic_chunks = semantic_splitter.split_documents(documents)
```

### 3. **Embedding 集成**

```python
from langchain.embeddings import (
    OpenAIEmbeddings,           # OpenAI
    HuggingFaceEmbeddings,      # 本地模型（免费）
    QianfanEmbeddingsEndpoint,  # 百度千帆
    DashScopeEmbeddings,        # 通义千问
)

# 本地 Embedding（推荐）
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-large-zh-v1.5",
    model_kwargs={'device': 'cuda'},
    encode_kwargs={'normalize_embeddings': True}
)

# 获取向量
vector = embeddings.embed_query("你好世界")
print(f"向量维度: {len(vector)}")
```

### 4. **向量存储**

```python
from langchain.vectorstores import (
    Chroma,      # 轻量级，开发用
    FAISS,       # 高性能
    Milvus,      # 分布式
    Qdrant,      # 云原生
)

# Chroma（最简单）
from langchain.vectorstores import Chroma

vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

# 相似度搜索
results = vector_store.similarity_search_with_score(
    "什么是人工智能？",
    k=5
)

for doc, score in results:
    print(f"相似度: {score}")
    print(f"内容: {doc.page_content[:200]}")

# FAISS（高性能）
from langchain.vectorstores import FAISS

vector_store = FAISS.from_documents(
    documents=chunks,
    embedding=embeddings
)

# 保存和加载
vector_store.save_local("faiss_index")
vector_store = FAISS.load_local("faiss_index", embeddings)
```

### 5. **检索器增强**

```python
from langchain.retrievers import (
    ContextualCompressionRetriever,  # 上下文压缩
    MergerRetriever,                  # 多路召回合并
    MultiQueryRetriever,              # 多查询生成
)
from langchain.retrievers.document_compressors import LLMChainExtractor

# 多查询检索（生成多个相似问题，提高召回）
from langchain.retrievers import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=llm
)

# 上下文压缩检索（先检索，再压缩）
compressor = LLMChainExtractor.from_llm(llm)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_store.as_retriever()
)
```

### 6. **重排序（Rerank）**

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import (
    CrossEncoderReranker,
    DocumentCompressorPipeline,
)

# 使用 BGE Reranker
from langchain.retrievers.document_compressors import CrossEncoderReranker

reranker = CrossEncoderReranker(
    model="BAAI/bge-reranker-large",
    top_n=3
)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=vector_store.as_retriever(search_kwargs={"k": 10})
)

# 检索时自动重排序
results = compression_retriever.get_relevant_documents("查询内容")
```

### 7. **提示词模板**

```python
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)

# 基础模板
prompt = PromptTemplate.from_template(
    "基于以下内容回答问题：\n\n{context}\n\n问题：{question}"
)

# 聊天模板（支持历史）
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是 FabosAI 助手，基于以下知识库回答：\n{context}"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{question}"),
])

# 格式化
formatted = chat_prompt.format(
    context="知识库内容...",
    history=[("user", "你好"), ("assistant", "你好！")],
    question="帮我解释一下"
)
```

### 8. **链式调用（LCEL）**

```python
from langchain.chat_models import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# 构建 RAG 链（简洁优雅）
def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

# LCEL 方式
rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)

# 使用
response = rag_chain.invoke("什么是人工智能？")
print(response)

# 流式输出
for chunk in rag_chain.stream("解释一下深度学习"):
    print(chunk, end="")
```

### 9. **对话记忆**

```python
from langchain.memory import (
    ConversationBufferMemory,      # 简单缓存
    ConversationSummaryMemory,      # 摘要记忆
    ConversationBufferWindowMemory, # 滑动窗口
    ConversationTokenBufferMemory,  # Token 限制
)

# 滑动窗口记忆（保留最近5轮）
memory = ConversationBufferWindowMemory(
    k=5,
    return_messages=True
)

# 添加对话
memory.save_context({"input": "你好"}, {"output": "你好！有什么可以帮助你的？"})
memory.save_context({"input": "我叫张三"}, {"output": "你好张三！"})

# 获取历史
history = memory.load_memory_variables({})
print(history)

# 在链中使用
from langchain.chains import ConversationChain

conversation = ConversationChain(
    llm=llm,
    memory=memory
)

conversation.predict(input="我叫什么名字？")  # 能记住
```

### 10. **Agent（智能体）**

```python
from langchain.agents import (
    Tool,
    initialize_agent,
    AgentType,
)
from langchain.tools import tool

# 定义工具
@tool
def search_knowledge_base(query: str) -> str:
    """搜索知识库"""
    docs = vector_store.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])

@tool
def get_current_time() -> str:
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@tool
def calculator(expression: str) -> str:
    """计算数学表达式"""
    return str(eval(expression))

# 创建 Agent
tools = [search_knowledge_base, get_current_time, calculator]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# 使用 Agent（自动决定调用哪个工具）
response = agent.run("现在几点了？")
response = agent.run("帮我查一下人工智能相关的知识")
response = agent.run("计算 123 * 456")
```

### 11. **完整 RAG Chain 示例**

```python
# 完整的 RAG 问答系统
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# 方式1：使用 RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # stuff, map_reduce, refine, map_rerank
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    return_source_documents=True,
    verbose=True
)

result = qa_chain({"query": "什么是机器学习？"})
print(f"答案: {result['result']}")
print(f"来源: {result['source_documents']}")

# 方式2：自定义 RAG 链
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# 创建文档组合链
combine_docs_chain = create_stuff_documents_chain(llm, prompt)

# 创建检索链
rag_chain = create_retrieval_chain(
    retriever=vector_store.as_retriever(),
    combine_docs_chain=combine_docs_chain
)

# 使用
response = rag_chain.invoke({"input": "什么是人工智能？"})
print(response['answer'])
```

## 三、你的 FabosAI 项目架构

```python
# fabos_rag.py - 完整的 LangChain 实现
from langchain.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import ChatPromptTemplate
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

class FabosRAG:
    def __init__(self):
        # 1. Embedding 模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-large-zh-v1.5",
            model_kwargs={'device': 'cuda'}
        )
      
        # 2. 向量存储
        self.vector_store = Chroma(
            persist_directory="./chroma_db",
            embedding_function=self.embeddings
        )
      
        # 3. 文本拆分器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
      
        # 4. 对话记忆
        self.memory = ConversationBufferWindowMemory(
            k=5,
            return_messages=True
        )
      
        # 5. 提示词模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是 FabosAI，基于以下知识库回答问题：\n{context}"),
            ("human", "{question}")
        ])
  
    def add_document(self, file_path):
        """添加文档到知识库"""
        # 加载
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        else:
            loader = Docx2txtLoader(file_path)
      
        docs = loader.load()
      
        # 拆分
        chunks = self.text_splitter.split_documents(docs)
      
        # 存储
        self.vector_store.add_documents(chunks)
        self.vector_store.persist()
      
        return len(chunks)
  
    def search(self, query, k=5):
        """搜索知识库"""
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return [(doc.page_content, score) for doc, score in results]
  
    def ask(self, question):
        """基于知识库问答"""
        # 检索
        docs = self.vector_store.similarity_search(question, k=3)
        context = "\n\n".join([doc.page_content for doc in docs])
      
        # 生成回答
        prompt = self.prompt.format(context=context, question=question)
        response = self.llm.invoke(prompt)
      
        # 保存记忆
        self.memory.save_context({"input": question}, {"output": response})
      
        return response

# 使用
rag = FabosRAG()
rag.add_document("knowledge.pdf")
answer = rag.ask("介绍一下这个产品")
```

## 四、LangChain vs 原生实现对比

| 功能      | 原生实现       | LangChain    | 推荐         |
| --------- | -------------- | ------------ | ------------ |
| 文档加载  | 每个格式自己写 | 50+ 格式内置 | ✅ LangChain |
| 文本拆分  | 自己写算法     | 多种策略     | ✅ LangChain |
| Embedding | 自己调用模型   | 统一接口     | ✅ LangChain |
| 向量存储  | 自己封装       | 20+ 数据库   | ✅ LangChain |
| 检索      | 自己写         | 多种检索器   | ✅ LangChain |
| 链式调用  | 自己编排       | LCEL 语法    | ✅ LangChain |
| 记忆管理  | 自己实现 Redis | 内置记忆     | ✅ LangChain |

## 五、总结

**LangChain 可以做：**

- ✅ 文档加载（所有格式）
- ✅ 文本拆分（智能 chunking）
- ✅ Embedding（集成各种模型）
- ✅ 向量存储（20+ 数据库）
- ✅ 检索（相似度、MMR、多路召回）
- ✅ 重排序（提升精度）
- ✅ 提示词管理
- ✅ 对话记忆
- ✅ Agent（工具调用）
- ✅ 完整 RAG 链


- **用 LangChain**，快速实现 RAG 核心功能
- 不需要重复造轮子
- 需要自定义的部分可以扩展

**一句话**：LangChain 就是你 RAG 项目的**一站式解决方案**！
