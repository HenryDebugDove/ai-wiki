### 一、支持 MCP 的 AI 编辑器

自定义 MCP 就是升级的Function Calling


**MCP（Model Context Protocol，模型上下文协议）** 是 Anthropic 推出的 AI 工具交互标准。以下是主流支持 MCP 的编辑器/IDE：

| AI 编辑器 / IDE                     | 支持程度 | 核心特性                      | 接入方式                  |
| :---------------------------------- | :------- | :---------------------------- | :------------------------ |
| **Cursor**                    | 完全支持 | 原生 MCP，可连外部工具/数据源 | 设置 → MCP → 添加服务器 |
| **Trae IDE**                  | 完全支持 | 内置 MCP 市场，一键启用       | 设置 → MCP → 添加 MCP   |
| **Windsurf**                  | 完全支持 | 官方兼容，工具丰富            | 配置文件（JSON/TOML）     |
| **GitHub Copilot**            | 部分支持 | 支持 Extensions 与 MCP 互通   | 插件配置 + 权限授权       |
| **Zed**                       | 原生支持 | 高性能、提示词模板、工具集成  | 内置 MCP 配置面板         |
| **Cline / Continue**          | 完全支持 | VS Code 插件，MCP 兼容        | 插件设置 → MCP 配置      |
| **JetBrains IDE**             | 插件支持 | 支持配置 MCP 服务器           | 插件市场安装 + 配置       |
| **Claude Desktop**            | 官方原生 | Anthropic 官方，MCP 发起端    | 设置 → MCP 服务器        |
| **Lobe Chat / Cherry Studio** | 完全支持 | 聊天客户端，MCP 市场          | 插件中心 → MCP           |

---

### 二、MCP 的核心作用

**MCP = AI 的“USB 接口”**，解决大模型与外部世界的连接问题：

| 核心作用               | 解决痛点                         | 价值                               |
| :--------------------- | :------------------------------- | :--------------------------------- |
| **统一接口标准** | 多模型×多工具需重复适配（m×n） | 一次适配，全生态通用（m+n）        |
| **扩展 AI 能力** | 模型只能“回答”，不能“操作”   | 读文件、查数据库、发邮件、调用 API |
| **安全可控**     | 直接 API 调用权限过大            | 沙箱、权限控制、审计日志           |
| **上下文互通**   | 工具间数据割裂                   | 跨工具共享上下文，完成复杂任务     |
| **即插即用**     | 集成开发周期长                   | 5 分钟接入第三方服务               |

**架构**：Client（AI 编辑器）→ Host（协议层）→ Server（工具/数据源）

---

### 三、常用 MCP 插件（Server）

#### 1. 开发工具类

| 插件名称                           | 功能                          | 适用场景           | 依赖           |
| :--------------------------------- | :---------------------------- | :----------------- | :------------- |
| **Filesystem MCP**           | 读写本地文件、搜索、目录管理  | 代码审查、日志分析 | Node.js/Python |
| **GitHub MCP**               | 操作 Issues、PR、仓库         | 项目管理、自动化   | GitHub Token   |
| **Chrome DevTools MCP**      | 前端调试、网络请求、性能分析  | Web 开发、Bug 定位 | Chrome         |
| **Playwright/Puppeteer MCP** | 浏览器自动化、测试、截图      | E2E 测试、爬虫     | Playwright     |
| **AWS MCP**                  | 管理 EC2/S3/RDS 等 15000+ API | 云资源运维、自动化 | AWS 密钥       |

#### 2. 生产力工具类

| 插件名称                   | 功能                     | 适用场景           |
| :------------------------- | :----------------------- | :----------------- |
| **Notion MCP**       | 读写数据库、页面、文档   | 知识库、笔记同步   |
| **Slack/飞书 MCP**   | 发消息、查历史、管理频道 | 团队通知、报告推送 |
| **Google Drive MCP** | 访问文档、表格、文件     | 办公数据处理       |
| **Trello/Asana MCP** | 管理任务、看板、项目     | 工作流自动化       |

#### 3. 数据与搜索类

| 插件名称                       | 功能                      | 特点               |
| :----------------------------- | :------------------------ | :----------------- |
| **PostgreSQL/MySQL MCP** | 执行 SQL、查询表结构      | 只读/读写权限控制  |
| **Qdrant MCP**           | 向量数据库、语义搜索      | RAG、知识库检索    |
| **Brave/Tavily Search**  | 实时网络搜索、隐私保护    | 事实核查、最新资讯 |
| **Memory MCP**           | AI 长期记忆、项目规范存储 | 复杂项目、持续开发 |

#### 4. 设计与多媒体类

| 插件名称              | 功能                   | 场景                 |
| :-------------------- | :--------------------- | :------------------- |
| **Figma MCP**   | 读取设计稿、尺寸、样式 | 设计转代码、自动布局 |
| **Minimax MCP** | 文本转语音、图像生成   | 内容创作、多媒体     |

---

### 四、MCP 使用方法（通用步骤）

#### 1. 编辑器启用 MCP

- **Cursor**：设置 → MCP → 启用 → 添加服务器
- **Trae**：设置 → MCP → 添加 MCP → 选择/输入配置
- **Claude Desktop**：Settings → MCP Servers → Add

#### 2. 安装 MCP Server（以 Filesystem 为例）

```bash
# Node.js 环境
npm install -g @modelcontextprotocol/server-filesystem

# 运行（允许访问 ~/projects）
mcp-server-filesystem ~/projects
```

#### 3. 配置连接（JSON 示例）

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "~/projects"]
    }
  }
}
```

#### 4. AI 调用 MCP

- 自然语言指令：
  > "读取 ~/projects/README.md，总结核心功能"
  > "检查 GitHub 仓库的新 Issues，分配给我"
  >
- AI 自动调用对应 MCP 工具并返回结果。

---

### 五、自定义 MCP（可以自定义）

**支持完全自定义**，可用 Python/Node.js/Go 开发。

#### 1. 开发方式对比

| 方式                      | 难度 | 语言      | 适用             |
| :------------------------ | :--- | :-------- | :--------------- |
| **FastMCP（推荐）** | 低   | Python    | 快速开发工具     |
| **官方 SDK**        | 中   | Python/TS | 标准实现         |
| **原生手写**        | 高   | 任意      | 无依赖、极致兼容 |

#### 2. FastMCP 快速示例（Python）

```python
# 1. 安装
# pip install fastmcp

from fastmcp import FastMCP

# 2. 初始化
mcp = FastMCP("My Custom Tools")

# 3. 定义工具（@mcp.tool() 装饰器）
@mcp.tool()
def add(a: float, b: float) -> float:
    """两数相加"""
    return a + b

@mcp.tool()
def get_system_info() -> dict:
    """获取系统信息"""
    import platform
    return {
        "system": platform.system(),
        "version": platform.version()
    }

# 4. 运行服务器
if __name__ == "__main__":
    mcp.run()
```

#### 3. 配置到编辑器

```json
// Cursor/Trae 配置
{
  "mcpServers": {
    "my-custom": {
      "command": "python",
      "args": ["path/to/custom_mcp.py"]
    }
  }}
```

#### 4. 核心三要素（必须实现）

- **Tools**：可执行函数（增删改查、API 调用）
- **Resources**：只读数据（文件、数据库视图）
- **Prompts**：预定义提示模板（工作流）

#### 5. 调试与测试

- 使用 **MCP Inspector** 工具查看日志
- 命令行运行 Server，检查标准输入输出
- 编辑器内测试工具调用

---

### 六、MCP 自定义开发流程（总结）

1. **需求分析**：确定暴露的工具/资源
2. **环境搭建**：Python ≥3.10 或 Node.js
3. **编码实现**：用 FastMCP 定义工具函数
4. **本地测试**：命令行运行 + Inspector 调试
5. **编辑器配置**：添加 MCP 服务器配置
6. **权限控制**：设置只读/读写、目录白名单
7. **发布共享**：打包为 npm/pip 包，或分享配置
