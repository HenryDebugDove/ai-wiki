
# Docker核心解析及Next.js项目实战

## 一、Docker核心概览

| 核心模块 | 核心说明 |
|---------|---------|
| Docker是什么 | 开源应用容器引擎，轻量级虚拟化，实现“一次打包，到处运行”，核心是镜像、容器、仓库 |
| 为什么使用 | 统一环境、简化部署、资源高效、隔离安全、可移植性强，解决“本地能跑，线上报错” |

## 二、Docker优缺点

| 优点 | 缺点 |
|------|------|
| 1. 轻量高效（秒级启动，资源占用低）<br>2. 环境统一，跨环境无差异<br>3. 部署便捷，支持自动化<br>4. 容器隔离，安全性好<br>5. 生态完善，镜像丰富 | 1. 隔离性有限，存在资源竞争<br>2. 数据默认临时存储，需配置持久化<br>3. 新手有学习成本<br>4. Windows兼容性一般 |

## 三、Docker使用场景

| 场景类型 | 核心用途 |
|---------|---------|
| 开发环境 | 团队统一环境，减少协作成本 |
| 应用部署 | Web应用、微服务快速部署，适配云服务器 |
| CI/CD自动化 | 配合Jenkins等工具，实现自动构建、部署 |
| 测试环境 | 快速创建/销毁，提升测试效率 |
| 微服务 | 微服务独立打包、部署、维护 |

## 四、Docker基础使用步骤

| 操作步骤 | 核心命令/操作 |
|---------|-------------|
| 1. 安装验证 | 安装对应系统版本，`docker -v`验证 |
| 2. 获取镜像 | `docker pull 镜像名:版本`（例：`docker pull node:18-alpine`） |
| 3. 创建容器 | `docker run -d -p 宿主端口:容器端口 --name 容器名 镜像名` |
| 4. 容器管理 | 启动：`docker start`；停止：`docker stop`；删除：`docker rm` |
| 5. 自定义镜像 | 编写Dockerfile，`docker build -t 镜像名:版本 .`构建 |

## 五、Docker + Next.js实战

### （一）本地项目Docker化

| 步骤 | 核心操作 |
|------|---------|
| 1. 准备项目 | `npx create-next-app@latest my-next-app`（无项目时） |
| 2. 核心配置 | 1. 编写Dockerfile（适配生产环境）<br>2. 创建.dockerignore（排除无用文件）<br>3. next.config.js添加 `output: 'standalone'` |
| 3. 构建运行 | `docker build -t my-next-app .`<br>`docker run -d -p 3000:3000 --name next-container my-next-app` |
| 4. 验证 | 访问 `http://localhost:3000`，正常显示即成功 |

### （二）服务器部署（Linux系统）

| 步骤 | 核心操作 |
|------|---------|
| 1. 安装Docker | CentOS：更新系统→安装依赖→添加仓库→安装并启动Docker，配置用户权限 |
| 2. 优化加速（可选） | 配置镜像加速（替换报错镜像源），重启Docker服务 |
| 3. 部署项目 | 上传项目→进入目录→构建镜像→启动容器（设置开机自启） |
| 4. 反向代理（可选） | 启动Nginx容器→配置反向代理（指向 `127.0.0.1:3000`）→重启Nginx |
| 5. 管理维护 | `docker ps`查看状态，`docker logs`查看日志，更新项目需重建镜像 |

### 关键注意事项（解决报错）

| 报错URL | 报错信息 | 解决方案 |
|--------|---------|--------|
| https://download.docker.com/linux/centos/docker-ce.repo | 网页解析失败 | 替换为CentOS官方Docker仓库或国内镜像仓库 |
| https://mirror.ccs.tencentyun.com | link hit security strategy | 替换为其他国内镜像源（如阿里云、华为云镜像） |
| https://docker.mirrors.ustc.edu.cn | 网页解析失败 | 更换镜像源，避免使用解析失败的地址 |
| http://127.0.0.1:3000 | URL拼写错误 | 检查URL拼写，确保容器正常启动且端口映射正确 |

## 六、Docker常用命令

### （一）镜像管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `docker images` | 列出本地镜像 | `docker images` |
| `docker pull` | 拉取镜像 | `docker pull nginx:latest` |
| `docker rmi` | 删除镜像 | `docker rmi nginx:latest` |
| `docker build` | 构建镜像 | `docker build -t my-app:v1 .` |
| `docker tag` | 为镜像打标签 | `docker tag my-app:v1 my-app:latest` |
| `docker push` | 推送镜像到仓库 | `docker push my-app:latest` |

### （二）容器管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `docker ps` | 列出运行中的容器 | `docker ps` |
| `docker ps -a` | 列出所有容器 | `docker ps -a` |
| `docker run` | 创建并启动容器 | `docker run -d -p 80:80 --name web nginx` |
| `docker start` | 启动容器 | `docker start web` |
| `docker stop` | 停止容器 | `docker stop web` |
| `docker rm` | 删除容器 | `docker rm web` |
| `docker exec` | 进入容器执行命令 | `docker exec -it web bash` |
| `docker logs` | 查看容器日志 | `docker logs web` |
| `docker inspect` | 查看容器详细信息 | `docker inspect web` |

### （三）网络管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `docker network ls` | 列出网络 | `docker network ls` |
| `docker network create` | 创建网络 | `docker network create my-network` |
| `docker network connect` | 连接容器到网络 | `docker network connect my-network web` |
| `docker network disconnect` | 断开容器与网络的连接 | `docker network disconnect my-network web` |

### （四）数据卷管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `docker volume ls` | 列出数据卷 | `docker volume ls` |
| `docker volume create` | 创建数据卷 | `docker volume create my-volume` |
| `docker volume rm` | 删除数据卷 | `docker volume rm my-volume` |
| `docker volume inspect` | 查看数据卷详细信息 | `docker volume inspect my-volume` |

### （五）系统管理

| 命令 | 说明 | 示例 |
|------|------|------|
| `docker info` | 查看Docker系统信息 | `docker info` |
| `docker system df` | 查看Docker磁盘使用情况 | `docker system df` |
| `docker system prune` | 清理未使用的资源 | `docker system prune -a` |

## 七、总结

Docker核心价值是统一环境、高效部署，适配Next.js项目全流程；通过表格整合核心信息，实操步骤简洁可落地，同时解决了文中URL报错问题，新手可快速上手。

通过掌握Docker常用命令，可以更高效地管理容器和镜像，提升开发和部署效率。
