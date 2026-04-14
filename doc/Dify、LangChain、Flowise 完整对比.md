# Dify、LangChain、Flowise 完整对比

## 一、Dify

### 1. 是什么

Dify 是一套**开箱即用的企业级 AI 应用搭建平台**，不用写大量代码，通过可视化界面就能做 AI 问答机器人、知识库、智能客服等，自带部署、监控、权限管理。

### 2. 优缺点

| 优点                           | 缺点                        |
| ------------------------------ | --------------------------- |
| 上手快，低代码就能做生产级应用 | 极致灵活度不如纯代码框架    |
| 自带 RAG、工作流、日志、权限   | 部署需要数据库、Redis，稍重 |
| 一键发布 API/网页，适合商用    | 复杂深度定制仍需开发        |
| 支持多模型切换，企业功能完善   | 小众模型适配需要手动配置    |

### 3. 业务场景举例

- 公司内部制度文档问答机器人
- 电商/门店智能客服自动回复
- 批量生成商品文案、营销内容
- 多部门 AI 应用统一管理（多租户）

### 4. 支持语言

- 代码节点：Python、JavaScript
- 外部调用：所有支持 HTTP 的语言（Java、Go、PHP 等）
- SDK：Python

### 5. 简单代码示例（Python 调用 Dify API）

```python
import requests

response = requests.post(
    "https://api.dify.ai/v1/chat-messages",
    headers={"Authorization": "Bearer app-你的API密钥"},
    json={"query": "公司年假有几天？", "user": "user_001"}
)
print(response.json()["answer"])
```

---

## 二、LangChain

### 1. 是什么

LangChain 是**纯代码框架**，相当于一套 AI 开发工具包，用代码把大模型、文档、数据库、工具等拼在一起，适合做高度定制化的 AI 系统。

### 2. 优缺点

| 优点                              | 缺点                   |
| --------------------------------- | ---------------------- |
| 灵活性极强，想怎么实现就怎么写    | 必须会写代码，门槛高   |
| 生态最全，支持几乎所有模型/向量库 | 胶水代码多，结构容易乱 |
| 适合复杂 Agent、多步骤任务        | 上线部署、监控要自己搭 |
| 迭代快，新功能第一时间支持        | 版本变动大，容易不兼容 |

### 3. 业务场景举例

- 定制化金融数据分析助手
- 能自主查数据库、调接口的复杂智能体
- 科研/算法场景的模型实验流程
- 深度嵌入现有业务系统的 AI 模块

### 4. 支持语言

- 主力：Python
- 次主力：JavaScript / TypeScript
- 其他语言：通过 API 间接使用

### 5. 简单代码示例（Python RAG）

```python
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

loader = TextLoader("公司手册.txt")
docs = loader.load()
db = FAISS.from_documents(docs, OpenAIEmbeddings())
qa = RetrievalQA.from_llm(llm=OpenAI(), retriever=db.as_retriever())
print(qa.run("报销流程是什么？"))
```

---

## 三、Flowise

### 1. 是什么

Flowise 是**基于 LangChain 做的可视化拖拽平台**，完全零代码，把 LangChain 的功能变成一个个节点，拖一拖就能搭建 AI 应用。

### 2. 优缺点

| 优点                            | 缺点                             |
| ------------------------------- | -------------------------------- |
| 上手极快，纯拖拽，几分钟出 Demo | 只适合简单场景，复杂逻辑吃力     |
| 部署轻量，不用数据库            | 企业级功能（权限、审计）几乎没有 |
| 完美兼容 LangChain 生态         | 高并发、大规模场景不稳定         |
| 本地模型支持友好（Ollama 等）   | 生产环境监控能力弱               |

### 3. 业务场景举例

- 快速做一个个人 AI 助手
- 班级/小团队内部简易知识库
- 本地离线 AI 问答（数据不出内网）
- 新手学习 AI 工作流原理

### 4. 支持语言

- 代码节点：Python、JavaScript
- 外部调用：HTTP API（所有语言）
- 底层：TypeScript / Node.js

### 5. 简单代码示例（Flowise 内置 JS 节点）

```javascript
function main(input) {
  // 把文本转成大写
  return { result: input.text.toUpperCase() };
}
```

---

## 四、三者核心对比表（最精简）

| 对比项   | Dify                 | LangChain            | Flowise              |
| -------- | -------------------- | -------------------- | -------------------- |
| 定位     | 企业级 AI 搭建平台   | AI 代码开发框架      | LangChain 可视化工具 |
| 开发方式 | 低代码 + 少量代码    | 纯代码               | 零代码拖拽           |
| 上手难度 | 中等                 | 很高                 | 很低                 |
| 灵活度   | 较高                 | 最高                 | 一般                 |
| 部署难度 | 中等                 | 自行处理             | 很简单               |
| 适合上线 | 适合生产/商用        | 适合深度定制项目     | 适合原型/小工具      |
| 适用人群 | 产品、全栈、企业团队 | 算法、后端开发       | 新手、非技术人员     |
| 典型用途 | 客服、知识库、SaaS   | 复杂 Agent、定制系统 | 快速 Demo、小应用    |

---

## 五、一句话怎么选

- 要**快速上线、给公司用、少写代码** → 选 **Dify**
- 要**高度定制、复杂逻辑、自己完全掌控代码** → 选 **LangChain**
- 要**纯拖拽、快速做 Demo、本地简单使用** → 选 **Flowise**
