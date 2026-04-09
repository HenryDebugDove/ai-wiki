# FastAPI 微服务项目

这是一个使用 FastAPI 实现的微服务架构演示项目，包含用户服务、订单服务和支付服务三个独立的微服务，使用 SQLite 作为数据库，通过 Nginx 作为统一入口。

## 项目结构

```
.
├── user-service/         # 用户服务
│   ├── data/             # 数据库目录
│   ├── main.py           # 服务代码
│   ├── requirements.txt  # 依赖文件
│   └── Dockerfile        # Docker 配置
├── order-service/        # 订单服务
│   ├── data/             # 数据库目录
│   ├── main.py           # 服务代码
│   ├── requirements.txt  # 依赖文件
│   └── Dockerfile        # Docker 配置
├── payment-service/      # 支付服务
│   ├── data/             # 数据库目录
│   ├── main.py           # 服务代码
│   ├── requirements.txt  # 依赖文件
│   └── Dockerfile        # Docker 配置
├── nginx.conf            # Nginx 配置文件
├── docker-compose.yml    # Docker Compose 配置
└── README.md             # 项目说明文档
```

## 功能特性

- **微服务架构**：拆分为用户、订单、支付三个独立服务
- **RESTful API**：每个服务都实现了完整的 CRUD 操作
- **服务间调用**：订单服务调用用户服务，支付服务调用订单服务
- **SQLite 数据库**：每个服务使用独立的 SQLite 数据库
- **Redis 缓存**：使用 Redis 缓存提高系统性能，缓存过期时间为 5 分钟
- **自动 API 文档**：FastAPI 自动生成的 Swagger 文档
- **数据验证**：使用 Pydantic 进行数据模型定义和验证
- **错误处理**：基本的错误处理机制
- **Docker 支持**：每个服务都有 Docker 配置，支持容器化部署
- **Nginx 统一入口**：通过 Nginx 反向代理实现统一访问入口

## 服务说明

### 1. 用户服务 (user-service)
- **端口**：8001
- **功能**：用户的 CRUD 操作
- **API 路径**：`/api/user/*`
- **数据库**：`user-service/data/user.db`

### 2. 订单服务 (order-service)
- **端口**：8002
- **功能**：订单的 CRUD 操作
- **API 路径**：`/api/order/*`
- **数据库**：`order-service/data/order.db`
- **服务间调用**：调用用户服务验证用户是否存在

### 3. 支付服务 (payment-service)
- **端口**：8003
- **功能**：支付的 CRUD 操作
- **API 路径**：`/api/pay/*`
- **数据库**：`payment-service/data/payment.db`
- **服务间调用**：调用订单服务验证订单是否存在和金额是否匹配

## 安装步骤

### 方法一：直接运行（本地开发）

1. **安装依赖**

   ```bash
   # 为用户服务安装依赖
   cd user-service
   pip install -r requirements.txt
   
   # 为订单服务安装依赖
   cd ../order-service
   pip install -r requirements.txt
   
   # 为支付服务安装依赖
   cd ../payment-service
   pip install -r requirements.txt
   ```

### 方法二：使用 Docker 部署（推荐）

1. **安装 Docker**
   - 下载并安装 Docker Desktop：https://www.docker.com/products/docker-desktop
   - 启动 Docker 服务

## 运行项目

### 方法一：直接运行（本地开发）

1. **启动用户服务**
   ```bash
   cd user-service
   uvicorn main:app --host 0.0.0.0 --port 8001
   ```

2. **启动订单服务**
   ```bash
   cd order-service
   uvicorn main:app --host 0.0.0.0 --port 8002
   ```

3. **启动支付服务**
   ```bash
   cd payment-service
   uvicorn main:app --host 0.0.0.0 --port 8003
   ```

4. **启动 Nginx**（可选，用于统一入口）
   - 安装 Nginx：https://nginx.org/en/download.html
   - 配置 Nginx：使用项目根目录的 `nginx.conf` 文件
   - 启动 Nginx 服务

### 方法二：使用 Docker Compose 运行（推荐）

1. **构建并启动所有服务**
   ```bash
   docker-compose up --build
   ```

2. **停止服务**
   ```bash
   docker-compose down
   ```

3. **查看服务状态**
   ```bash
   docker-compose ps
   ```

## 访问 API 文档

### 单个服务的 API 文档

- **用户服务**：http://localhost:8001/docs
- **订单服务**：http://localhost:8002/docs
- **支付服务**：http://localhost:8003/docs

### 通过 Nginx 访问（如果使用 Nginx）

- **用户服务**：http://localhost/api/user/docs
- **订单服务**：http://localhost/api/order/docs
- **支付服务**：http://localhost/api/pay/docs

## API 接口

### 用户服务

| 方法   | 路径             | 功能                 |
| ------ | ---------------- | -------------------- |
| GET    | /                | 根路径，返回服务状态 |
| GET    | /api/user        | 获取所有用户         |
| GET    | /api/user/{id}   | 获取单个用户         |
| POST   | /api/user        | 创建新用户           |
| PUT    | /api/user/{id}   | 更新用户信息         |
| DELETE | /api/user/{id}   | 删除用户             |

### 订单服务

| 方法   | 路径             | 功能                 |
| ------ | ---------------- | -------------------- |
| GET    | /                | 根路径，返回服务状态 |
| GET    | /api/order       | 获取所有订单         |
| GET    | /api/order/{id}  | 获取单个订单         |
| POST   | /api/order       | 创建新订单           |
| PUT    | /api/order/{id}  | 更新订单信息         |
| DELETE | /api/order/{id}  | 删除订单             |

### 支付服务

| 方法   | 路径             | 功能                 |
| ------ | ---------------- | -------------------- |
| GET    | /                | 根路径，返回服务状态 |
| GET    | /api/pay         | 获取所有支付         |
| GET    | /api/pay/{id}    | 获取单个支付         |
| POST   | /api/pay         | 创建新支付           |
| PUT    | /api/pay/{id}    | 更新支付信息         |
| DELETE | /api/pay/{id}    | 删除支付             |

## 数据模型

### User

```json
{
  "id": 1,
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25
}
```

### Order

```json
{
  "id": 1,
  "user_id": 1,
  "product_name": "商品1",
  "amount": 100.0,
  "status": "completed"
}
```

### Payment

```json
{
  "id": 1,
  "order_id": 1,
  "amount": 100.0,
  "payment_method": "alipay",
  "status": "completed"
}
```

## 示例请求

### 创建用户

```bash
curl -X POST "http://localhost:8001/api/user" \
  -H "Content-Type: application/json" \
  -d '{"name": "王五", "email": "wangwu@example.com", "age": 35}'
```

### 创建订单

```bash
curl -X POST "http://localhost:8002/api/order" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "product_name": "商品3", "amount": 300.0, "status": "pending"}'
```

### 创建支付

```bash
curl -X POST "http://localhost:8003/api/pay" \
  -H "Content-Type: application/json" \
  -d '{"order_id": 1, "amount": 100.0, "payment_method": "wechat", "status": "completed"}'
```

## Docker 的作用及使用

### Docker 的作用

1. **环境隔离**：每个服务运行在独立的容器中，避免环境冲突
2. **简化部署**：通过 Dockerfile 定义服务环境，确保环境一致性
3. **快速扩展**：可以快速复制容器实现服务扩容
4. **跨平台**：在不同系统上运行相同的容器，保证部署一致性

### Docker 的使用

1. **构建镜像**
   ```bash
   # 构建用户服务镜像
   cd user-service
   docker build -t user-service .
   
   # 构建订单服务镜像
   cd ../order-service
   docker build -t order-service .
   
   # 构建支付服务镜像
   cd ../payment-service
   docker build -t payment-service .
   ```

2. **运行容器**
   ```bash
   # 运行用户服务容器
   docker run -d -p 8001:8000 --name user-service user-service
   
   # 运行订单服务容器
   docker run -d -p 8002:8000 --name order-service order-service
   
   # 运行支付服务容器
   docker run -d -p 8003:8000 --name payment-service payment-service
   ```

3. **使用 Docker Compose**
   - Docker Compose 可以同时管理多个容器
   - 配置文件：`docker-compose.yml`
   - 启动所有服务：`docker-compose up --build`
   - 停止所有服务：`docker-compose down`

## Nginx 的作用及使用

### Nginx 的作用

1. **统一入口**：提供单一的访问入口，隐藏后端服务的具体地址
2. **反向代理**：将请求转发到对应的微服务
3. **负载均衡**：可以在多个服务实例之间分配请求
4. **静态资源服务**：可以直接服务静态文件

### Nginx 的使用

1. **配置文件**：`nginx.conf`
   - 定义了不同路径的转发规则
   - 将 `/api/user/` 转发到用户服务
   - 将 `/api/order/` 转发到订单服务
   - 将 `/api/pay/` 转发到支付服务

2. **本地运行 Nginx**
   - 安装 Nginx：https://nginx.org/en/download.html
   - 复制 `nginx.conf` 到 Nginx 配置目录
   - 启动 Nginx 服务

3. **使用 Docker 运行 Nginx**
   - Docker Compose 配置中已经包含了 Nginx 服务
   - 启动后可以通过 http://localhost 访问

## 服务间调用

### 订单服务调用用户服务

- 当创建订单时，订单服务会调用用户服务验证用户是否存在
- 使用 httpx 库发送 HTTP 请求
- 调用地址：`http://localhost:8001/api/user/{user_id}`

### 支付服务调用订单服务

- 当创建支付时，支付服务会调用订单服务验证订单是否存在
- 同时验证支付金额与订单金额是否匹配
- 使用 httpx 库发送 HTTP 请求
- 调用地址：`http://localhost:8002/api/order/{order_id}`

## 技术栈

- **FastAPI**：现代、快速的 Web 框架
- **Uvicorn**：ASGI 服务器
- **Pydantic**：数据验证
- **SQLite**：轻量级数据库
- **Redis**：缓存服务，提高系统性能
- **httpx**：HTTP 客户端，用于服务间调用
- **Docker**：容器化部署
- **Nginx**：反向代理和统一入口

## 注意事项

1. **数据库**：
   - 本项目使用 SQLite 数据库，适合开发和测试环境
   - 生产环境建议使用更强大的数据库，如 PostgreSQL 或 MySQL
   - 数据库文件会自动创建在各服务的 `data` 目录中
   - 服务启动时会自动插入示例数据

2. **Redis 缓存**：
   - 本项目使用 Redis 作为缓存服务，提高系统性能
   - 缓存过期时间设置为 5 分钟
   - 服务启动前需要确保 Redis 服务正在运行
   - Redis 默认端口为 6379，若修改端口需要在各服务代码中相应修改

3. **服务间调用**：
   - 服务间通过 HTTP 接口调用
   - 调用地址使用 `localhost`，适用于本地开发
   - 在 Docker 环境中，应使用服务名称作为主机名

4. **Docker 网络**：
   - Docker Compose 会自动创建网络，服务间可以通过服务名称访问
   - 例如：订单服务可以通过 `http://user-service:8000/api/user/{user_id}` 访问用户服务

5. **扩展建议**：
   - 可以添加配置中心管理服务配置
   - 可以添加服务注册与发现机制
   - 可以添加监控和日志系统

## 部署建议

### 开发环境

- 使用直接运行的方式，便于调试和开发
- 启用 `--reload` 参数，实现代码热更新
- 安装并运行本地 Redis 服务：`docker run --name redis -p 6379:6379 -d redis`

### 测试环境

- 使用 Docker Compose 部署
- 可以模拟生产环境的配置
- 确保 Redis 服务正常运行

### 生产环境

- 使用 Docker Compose 或 Kubernetes 部署
- 配置环境变量管理敏感信息
- 启用 HTTPS
- 配置负载均衡和高可用
- 定期备份数据库
- 为 Redis 配置持久化存储，确保缓存数据安全
- 考虑使用 Redis 集群，提高可用性和性能

## 总结

本项目展示了如何使用 FastAPI 构建微服务架构，包含了三个独立的服务，通过服务间调用实现业务逻辑，使用 Docker 实现容器化部署，通过 Nginx 实现统一入口。这是一个完整的微服务架构示例，适合作为学习和参考。