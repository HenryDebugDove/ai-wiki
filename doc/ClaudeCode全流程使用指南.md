# Claude Code 全流程使用指南

（含安装、中转配置、第三方模型接入、使用技巧）

---

## 一、Claude Code 是什么？

Claude Code 是 Anthropic 官方推出的**终端/VS Code 一体化 AI 编程助手**，支持代码生成、项目重构、Bug 排查、文档编写等全流程开发工作，可无缝对接 Claude 官方模型，也支持 DeepSeek 等第三方模型，是前端/全栈开发的效率神器。

---

## 二、安装教程（Windows/macOS/Linux 全覆盖）

### 1. 安装方式对比

| 安装方式             | 适用系统            | 核心优势                            | 操作难度 |
| :------------------- | :------------------ | :---------------------------------- | :------- |
| 原生一键安装（推荐） | Windows/macOS/Linux | 不依赖 Node.js，官方原生，安装最快  | 极低     |
| npm 安装             | 全平台              | 适合已有 Node.js 环境的开发者，灵活 | 低       |

### 2. 详细安装步骤

#### （1）原生一键安装（推荐）

##### Windows（PowerShell 管理员权限）

```powershell
# 稳定版安装
irm https://claude.ai/install.ps1 | iex

# 验证安装
claude --version
# 输出类似：2.1.92 (Claude Code) 即成功
```

##### macOS/Linux/WSL

```bash
# 稳定版安装
curl -fsSL https://claude.ai/install.sh | bash

# 验证安装
claude --version
```

#### （2）npm 安装（需 Node.js 18+ 我使用的这种方式）

1. 安装 Node.js（LTS 版）
   - Windows/Linux：官网 https://nodejs.org/ 下载安装
   - macOS：`brew install node@20`
2. 配置国内镜像（解决安装慢）
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```
3. 全局安装 Claude Code
   ```bash
   npm install -g @anthropic-ai/claude-code

   # 验证安装
   claude --version
   ```

### 3. VS Code 官方插件安装

| 步骤 | 操作说明                                        |
| :--- | :---------------------------------------------- |
| 1    | 打开 VS Code → 左侧「扩展」面板                |
| 2    | 搜索 `Claude Code`（发布者：Anthropic, Inc.） |
| 3    | 点击「安装」，重启 VS Code 完成安装             |
| 4    | 插件自动复用终端版的本地配置，无需重复配置      |

---

## 三、常用高性价比中转站推荐（2026 最新）

### 1. 中转站核心选型标准

| 标准   | 说明                                         |
| :----- | :------------------------------------------- |
| 稳定性 | 国内专线，晚高峰不卡顿，99.9% 可用率         |
| 性价比 | 价格为官方 6-8 折，按量计费，无最低消费      |
| 易用性 | 支持人民币/支付宝，兼容 Claude Code 官方 CLI |
| 安全性 | 不存储用户数据，支持企业开票，防封号风控     |

### 2. 主流中转站对比

| 中转站              | 价格优势              | 核心特点                                 | 适合人群                  |
| :------------------ | :-------------------- | :--------------------------------------- | :------------------------ |
| API 易（apiyi.com） | 官方 8 折起，按量计费 | 国内专线低延迟，兼容全功能，新用户送额度 | 重度开发者、追求稳定      |
| 简易API/快快云      | 官方 6-7 折，无订阅   | BGP 多线，防风控，适合个人/小团队        | 性价比优先、轻度/中度使用 |
| WeeLinking          | 官方 7 折左右         | 200+ 模型聚合，一个 Key 通吃所有模型     | 多模型测试、频繁切换模型  |
| 2233.ai/WildAI      | 超低价，按量计费      | 国内直连，支付宝结算，操作简单           | 轻度代码、个人用户        |
| OpenRouter（国际）  | 官方 9 折左右         | 多模型聚合，正规企业级服务               | 海外用户、企业团队        |

---

## 四、BaseURL 配置 & 第三方模型（DeepSeek）接入

### 1. 核心配置逻辑

Claude Code 可通过修改 `ANTHROPIC_BASE_URL`，无缝对接第三方模型，核心要求：

- 第三方接口必须兼容 Anthropic 官方 API 格式
- DeepSeek 需添加 `/anthropic` 后缀，否则 404 报错

### 2. DeepSeek 模型接入配置（最常用 个人使用）

#### （1）关键参数说明

| 参数                       | 配置值                                 | 说明                             |
| :------------------------- | :------------------------------------- | :------------------------------- |
| ANTHROPIC_BASE_URL         | `https://api.deepseek.com/anthropic` | 必须加 `/anthropic` 后缀       |
| ANTHROPIC_AUTH_TOKEN       | `sk-你的DeepSeek API Key`            | 从 platform.deepseek.com 申请    |
| ANTHROPIC_MODEL            | `deepseek-chat`                      | 日常开发首选，代码能力强         |
| ANTHROPIC_SMALL_FAST_MODEL | `deepseek-chat`                      | 快速响应模型统一配置             |
| API_TIMEOUT_MS             | `600000`                             | 超时时间拉长，避免长代码任务超时 |

#### （2）3 种配置方式（选其一即可）

##### 方式1：临时生效（当前终端）

**Windows PowerShell**

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = "sk-你的DeepSeek Key"
$env:ANTHROPIC_MODEL = "deepseek-chat"
$env:ANTHROPIC_SMALL_FAST_MODEL = "deepseek-chat"
$env:API_TIMEOUT_MS = 600000

# 启动 Claude Code
claude
```

**macOS/Linux**

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-你的DeepSeek Key"
export ANTHROPIC_MODEL="deepseek-chat"
export ANTHROPIC_SMALL_FAST_MODEL="deepseek-chat"
export API_TIMEOUT_MS=600000

# 启动 Claude Code
claude
```

##### 方式2：永久生效（系统环境变量，全局生效 个人采用方式）

**Windows PowerShell（管理员）**

```powershell
# 替换 sk-xxx 为你的 DeepSeek Key
[Environment]::SetEnvironmentVariable("ANTHROPIC_BASE_URL", "https://api.deepseek.com/anthropic", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_AUTH_TOKEN", "sk-你的DeepSeek Key", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_MODEL", "deepseek-chat", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_SMALL_FAST_MODEL", "deepseek-chat", "User")
[Environment]::SetEnvironmentVariable("API_TIMEOUT_MS", "600000", "User")
[Environment]::SetEnvironmentVariable("CLAUDE_CODE_USE_LOCAL_API", "1", "User")
```

执行后**关闭所有终端/VS Code，重新打开**，全局永久生效。

##### 方式3：配置文件永久生效（官方推荐，最稳定）

**Windows PowerShell**

```powershell
# 创建配置目录
mkdir -Force $HOME\.claude

# 写入配置（替换 sk-xxx 为你的 DeepSeek Key）
Set-Content $HOME\.claude\config.json @'
{
  "apiBaseUrl": "https://api.deepseek.com/anthropic",
  "primaryApiKey": "sk-你的DeepSeek Key",
  "defaultModel": "deepseek-chat",
  "apiTimeoutMs": 600000
}
'@
```

**macOS/Linux**

```bash
mkdir -p ~/.claude
echo '{
  "apiBaseUrl": "https://api.deepseek.com/anthropic",
  "primaryApiKey": "sk-你的DeepSeek Key",
  "defaultModel": "deepseek-chat",
  "apiTimeoutMs": 600000
}' > ~/.claude/config.json
```

### 3. 其他第三方模型配置（通用模板）

| 模型     | BaseURL 配置                                           | 模型名              |
| :------- | :----------------------------------------------------- | :------------------ |
| 通义千问 | `https://dashscope.aliyuncs.com/api/v1/anthropic`    | `qwen-coder-plus` |
| 智谱 GLM | `https://open.bigmodel.cn/api/anthropic`             | `glm-4.7`         |
| 豆包     | `https://ark.cn-beijing.volces.com/api/v3/anthropic` | `doubao-code`     |

---

## 五、VS Code 插件跳过登录配置（必看）

### 1. 登录页选项说明

| 选项                        | 本质                | 适用场景                 |
| :-------------------------- | :------------------ | :----------------------- |
| Claude.ai Subscription      | Claude Pro 订阅登录 | 海外用户、官方账号使用   |
| Anthropic Console           | 官方 API 账号登录   | 海外企业、国际信用卡用户 |
| Bedrock, Foundry, or Vertex | 云厂商企业级服务    | 企业团队、国内不适用     |

### 2. 跳过登录、启用本地模式步骤

| 步骤 | 操作说明                                                                                                    |
| :--- | :---------------------------------------------------------------------------------------------------------- |
| 1    | 完全关闭 VS Code（所有窗口+进程）                                                                           |
| 2    | 管理员 PowerShell 执行：`[Environment]::SetEnvironmentVariable("CLAUDE_CODE_USE_LOCAL_API", "1", "User")` |
| 3    | 重新打开 VS Code，插件自动读取本地配置，跳过登录                                                            |
| 4    | 聊天框输入 `/model`，显示 `deepseek-chat` 即配置成功                                                    |

---

## 六、核心使用技巧（前端开发专属）

### 1. 基础操作命令

| 命令                   | 作用                                       |
| :--------------------- | :----------------------------------------- |
| `claude`             | 启动 Claude Code（建议进入项目目录后启动） |
| `/exit` / `Ctrl+C` | 退出 Claude Code                           |
| `/clear`             | 清空对话历史，重新开始                     |
| `/model`             | 查看/切换当前模型                          |
| `/context`           | 查看当前加载的上下文文件                   |
| `/approve`           | 同意 AI 的代码修改，自动执行               |
| `/reject`            | 拒绝 AI 的代码修改                         |
| `/help`              | 查看所有可用命令                           |

### 2. 前端开发高频指令模板

| 场景       | 指令示例                                                                                                    |
| :--------- | :---------------------------------------------------------------------------------------------------------- |
| 项目初始化 | `帮我用 Vite + React + TypeScript 初始化项目，配置 ESLint、Prettier、Tailwind CSS，生成完整 package.json` |
| 组件开发   | `帮我写一个 React 登录组件，包含表单验证、错误提示、防抖提交，适配移动端`                                 |
| 代码重构   | `重构 src/components 下的所有组件，提取公共逻辑，优化性能，修复潜在 Bug，保持功能不变`                    |
| Bug 排查   | `分析项目报错：Uncaught TypeError: Cannot read properties of undefined (reading 'map')，定位问题并修复`   |
| 文档生成   | `给项目所有组件写完整 JSDoc 注释，生成 README.md，包含安装、使用、部署说明`                               |
| 性能优化   | `分析项目性能瓶颈，优化打包体积，提升首屏加载速度，给出具体修改方案`                                      |

### 3. 效率提升技巧

| 技巧       | 说明                                                                           |
| :--------- | :----------------------------------------------------------------------------- |
| 目录启动   | 进入项目目录后启动 `claude`，自动加载全项目上下文，理解更精准                |
| 模型选择   | 日常开发用 `deepseek-chat`，复杂架构用 `deepseek-reasoner`，平衡效果与成本 |
| 上下文管理 | 大项目用 `claude --dir src` 只加载源码目录，减少 Token 浪费                  |
| Git 联动   | 每次 AI 修改前提交 Git，用 `git diff` 检查修改，避免误改代码                 |
| 批量执行   | 将指令写入 `prompt.txt`，执行 `claude < prompt.txt` 一键批量处理任务       |

---

## 七、常见问题排查

| 问题                          | 原因                                   | 解决方案                                                  |
| :---------------------------- | :------------------------------------- | :-------------------------------------------------------- |
| `command not found: claude` | 安装后未重启终端，环境变量未加载       | 重启终端，重新执行安装命令                                |
| 安装慢/失败                   | npm 源问题，网络限制                   | 切换国内镜像，改用原生一键安装                            |
| 认证失败/404                  | BaseURL 错误，未加 `/anthropic` 后缀 | 修正 BaseURL 为 `https://api.deepseek.com/anthropic`    |
| VS Code 插件弹登录            | 默认走官方云端登录                     | 配置 `CLAUDE_CODE_USE_LOCAL_API=1` 环境变量             |
| 响应慢/超时                   | 模型选择不当，超时时间过短             | 切换 `deepseek-chat`，拉长 `API_TIMEOUT_MS` 为 600000 |
| 代码误改                      | 未检查修改直接同意                     | 每次修改前用 `git diff` 检查，重要项目先提交 Git        |

---

## 八、方案选型总结

| 使用场景               | 推荐方案                                        |
| :--------------------- | :---------------------------------------------- |
| 个人前端开发、预算有限 | 原生安装 + DeepSeek 本地配置 + VS Code 插件     |
| 企业团队、稳定优先     | API 易 中转 + Claude 3.5 Sonnet + 终端/插件双端 |
| 多模型测试、灵活切换   | WeeLinking 聚合 API + Claude Code 终端          |
| 离线/隐私需求          | 开源平替 Roo Code + 本地大模型                  |

---
