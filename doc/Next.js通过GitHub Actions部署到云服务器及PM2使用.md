
# 全栈项目自动化部署与进程管理完整文档

本文档整合 **Next.js 项目自动化部署**、**主流CI/CD工具对比**、**宝塔面板+PM2运行Next.js** 三大核心内容，采用表格化呈现，清晰易懂，适用于前端/全栈开发者实操参考。

## 目录

1. Next.js 通过 GitHub Actions 部署到云服务器（含完整配置）
2. GitLab CI / Gitee CI 实现CICD 部署方式
3. GitHub Actions / GitLab CI / Gitee CI / Jenkins 核心区别与优缺点
4. 宝塔面板中 PM2 运行 Next.js 项目（含持久化）
5. PM2 与直接 `npm run dev` 运行项目的区别

---

## 一、Next.js 通过 GitHub Actions 部署到云服务器

### 核心原理

GitHub 代码提交后，自动触发流水线：拉取代码 → 安装依赖 → 打包项目 → 通过SSH连接云服务器 → 部署并重启服务。

### 前置条件

1. 云服务器（Linux）开放SSH端口（22）
2. 服务器配置Node.js环境、PM2进程管理器
3. GitHub仓库配置服务器SSH密钥、IP、用户名等密钥信息

### 服务器信息（示例）

| 配置项       | 配置值                                   |
| ------------ | ---------------------------------------- |
| 服务器IP     | 0.0.0.0                                  |
| SSH端口      | 22                                       |
| 登录用户     | root                                     |
| 项目部署路径 | /www/wwwroot/default/fullstack-todo-list |
| 项目名称     | fullstack-todo-list                      |

### GitHub Secrets 配置步骤

1. 进入GitHub仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**，添加以下密钥：

| Secret 名称 | 填写内容                                  |
| ----------- | ----------------------------------------- |
| SERVER_HOST | 0.0.0.0                                   |
| SERVER_PORT | 22                                        |
| SERVER_USER | root                                      |
| SERVER_PATH | /www/wwwroot/default/fullstack-todo-list  |
| SERVER_KEY  | 服务器的SSH私钥（登录服务器的私钥字符串） |

### 完整 GitHub Actions 配置文件

**文件路径**：`.github/workflows/deploy.yml`

```yaml
name: Deploy to Tencent Cloud Server

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
  
    steps:
      # 1. 检出代码
      - name: Checkout code
        uses: actions/checkout@v4

      # 2. 设置Node.js环境
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      # 3. 安装依赖
      - name: Install dependencies
        run: npm ci

      # 4. 构建项目
      - name: Build project
        run: npm run build

      # 5. 部署到腾讯云服务器
      - name: Deploy to Tencent Cloud Server
        uses: easingthemes/ssh-deploy@v4.1.0
        with:
          SSH_PRIVATE_KEY: ${{ secrets.SERVER_KEY }}
          REMOTE_HOST: ${{ secrets.SERVER_HOST }}
          REMOTE_PORT: ${{ secrets.SERVER_PORT || '22' }}
          REMOTE_USER: ${{ secrets.SERVER_USER }}
          TARGET: ${{ secrets.SERVER_PATH }}
          SOURCE: './'
          EXCLUDE: 'node_modules/, .git/, .github/, .next/'

      # 6. 安装依赖并重启服务
      - name: Install dependencies and restart service
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.SERVER_HOST }}
          port: ${{ secrets.SERVER_PORT || '22' }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_KEY }}
          script: |
            cd ${{ secrets.SERVER_PATH }}
            # 安装依赖
            npm install
            # 构建项目
            npm run build
            # 重启服务（生产环境推荐使用 npm run start）
            pm2 restart fullstack-todo-list || pm2 start "npm run start" --name "fullstack-todo-list"
```

### 配置说明

1. 代码推送至 `main`分支自动触发部署
2. 流水线自动跳过 `node_modules`等无关文件，提升部署速度
3. 服务崩溃或未启动时，自动创建PM2进程并命名
4. 生产环境推荐使用 `npm run start`，替代开发模式 `npm run dev`

---

## 二、GitLab CI / Gitee CI 实现CICD部署

### 1. 通用配置规则

两个平台均通过**根目录配置文件**触发流水线，核心逻辑与GitHub Actions一致，仅配置文件名称、语法略有差异。

### 2. 核心配置对比

| 平台   | 配置文件名         | 核心部署逻辑                                                                                       |
| :----- | :----------------- | :------------------------------------------------------------------------------------------------- |
| GitLab | `.gitlab-ci.yml` | 1. 定义运行环境`<br>`2. 拉取代码/安装依赖/打包`<br>`3. SSH连接服务器部署`<br>`4. PM2重启服务 |
| Gitee  | `.gitee-ci.yml`  | 1. 选择Node.js环境`<br>`2. 执行构建命令`<br>`3. 服务器远程部署`<br>`4. 进程重启              |

### 3. 极简配置示例（GitLab）

```yaml
stages:
  - deploy

deploy_job:
  stage: deploy
  image: node:20
  script:
    - npm install
    - npm run build
    # 服务器部署命令（需提前配置SSH信任）
    - ssh root@118.25.152.48 "cd /www/wwwroot/default/fullstack-todo-list && git pull && npm install && npm run build && pm2 restart fullstack-todo-list"
  only:
    - main
```

---

## 三、四大CICD工具 区别与优缺点

| 对比维度           | GitHub Actions                         | GitLab CI                        | Gitee CI                 | Jenkins                              |
| :----------------- | :------------------------------------- | :------------------------------- | :----------------------- | :----------------------------------- |
| **所属平台** | GitHub                                 | GitLab                           | Gitee                    | 开源独立工具                         |
| **部署成本** | 0成本（免费额度）                      | 0成本（内置）                    | 0成本（内置）            | 需自建服务器，有运维成本             |
| **配置难度** | 极低（yml文件，生态丰富）              | 低（内置一体化，无需额外部署）   | 低（国产，中文文档）     | 高（网页配置+脚本，学习成本高）      |
| **适用场景** | GitHub托管项目、中小型项目             | GitLab托管项目、企业内部项目     | 国内项目、轻量化部署     | 大型企业、复杂定制化流水线           |
| **优点**     | 与GitHub深度集成，生态插件极多，上手快 | 代码+CI/CD一体化，无需第三方服务 | 国内访问快，中文支持友好 | 功能无上限，高度定制化，支持复杂流程 |
| **缺点**     | 国内网络不稳定                         | 私有部署复杂，国内访问一般       | 生态插件少，功能有限     | 占用资源高，配置繁琐，维护成本高     |

### 选型建议

- 个人/小型项目：优先 **GitHub Actions / Gitee CI**
- 企业内部项目：优先 **GitLab CI**
- 大型复杂项目、多服务联动：选择 **Jenkins**

---

## 四、宝塔面板 + PM2 运行 Next.js 项目

### 1. 前置准备

1. 宝塔面板安装：**Node.js版本管理**（配置Node.js 16+）
2. 上传Next.js项目到服务器目录：`/www/wwwroot/default/fullstack-todo-list`
3. 项目根目录执行：`npm install` 安装依赖

### 2. PM2 运行 Next.js 并持久化

#### （1）启动命令（生产环境标准格式）

```bash
# 打包生产环境（必须执行）
npm run build

# PM2启动生产服务，命名项目，实现持久化
pm2 start "npm run start" --name "fullstack-todo-list"
```

#### （2）PM2 持久化配置（服务器重启后自动运行）

```bash
# 保存当前所有PM2进程
pm2 save

# 设置开机自启
pm2 startup
```

#### （3）宝塔面板可视化操作

1. 打开宝塔 → 软件商店 → 搜索 **PM2管理器**（一键安装）
2. 进入PM2管理器 → 添加项目
3. 选择项目目录：`/www/wwwroot/default/fullstack-todo-list`
4. 启动命令填 `npm run start` → 填写项目名称 `fullstack-todo-list`
5. 点击启动，开启**开机自启**

### 3. 常用PM2命令

| 命令                                | 作用                 |
| :---------------------------------- | :------------------- |
| `pm2 list`                        | 查看所有运行中的项目 |
| `pm2 restart fullstack-todo-list` | 重启项目             |
| `pm2 stop fullstack-todo-list`    | 停止项目             |
| `pm2 logs fullstack-todo-list`    | 查看项目日志         |
| `pm2 delete fullstack-todo-list`  | 删除项目进程         |
| `pm2 save`                        | 保存进程配置         |
| `pm2 startup`                     | 设置开机自启         |

---

## 五、PM2 与 直接 `npm run dev` 区别

| 对比维度           | PM2 启动项目                    | 直接 `npm run dev`         |
| :----------------- | :------------------------------ | :--------------------------- |
| **运行模式** | 后台守护进程（关闭终端仍运行）  | 前台进程（关闭终端服务停止） |
| **崩溃处理** | 自动重启，保证服务不中断        | 崩溃后直接停止，需手动重启   |
| **性能监控** | 支持CPU/内存监控、日志管理      | 无监控，无日志持久化         |
| **多进程**   | 支持集群模式，充分利用服务器CPU | 单进程运行，性能利用率低     |
| **开机自启** | 支持配置开机自动运行            | 不支持，服务器重启需手动启动 |
| **适用环境** | 生产环境（正式上线使用）        | 开发环境（本地调试使用）     |
| **稳定性**   | 极高，7×24小时稳定运行         | 低，仅适合开发调试           |

---

## 总结

1. **CICD部署**：轻量化项目用 GitHub/GitLab/Gitee CI 零成本实现自动化部署；大型项目用 Jenkins 实现高度定制。
2. **服务器运行**：Next.js 生产环境必须用 `PM2 + npm run start`，禁止使用开发命令 `npm run dev`。
3. **持久化**：PM2 通过 `save` + `startup` 实现项目开机自启、崩溃自愈，是生产环境标准方案。
4. **GitHub Action**：已提供完整可直接使用的配置文件，配合Secrets可实现一键自动部署。
