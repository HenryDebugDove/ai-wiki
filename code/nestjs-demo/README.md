# NestJS 学习演示项目

这是一个用于学习 NestJS 框架的演示项目，包含了基础的 CRUD 操作和用户认证功能。

## 项目功能

### 1. 用户管理模块 (Users Module)

- 用户注册
- 获取用户列表
- 获取单个用户信息
- 更新用户信息
- 删除用户

### 2. 认证模块 (Auth Module)

- 用户登录（JWT 认证）
- 获取当前用户信息

### 3. 基础功能

- 健康检查接口
- CORS 跨域支持
- 全局数据验证
- 密码加密存储

## 项目结构

```
src/
├── main.ts                    # 应用入口文件
├── app.module.ts              # 根模块
├── app.controller.ts          # 根控制器
├── app.service.ts             # 根服务
├── users/                     # 用户模块
│   ├── dto/                   # 数据传输对象
│   │   └── create-user.dto.ts # 创建用户 DTO
│   ├── entities/              # 实体类
│   │   └── user.entity.ts     # 用户实体
│   ├── users.controller.ts    # 用户控制器
│   ├── users.service.ts       # 用户服务
│   └── users.module.ts        # 用户模块
└── auth/                      # 认证模块
    ├── dto/                   # 数据传输对象
    │   └── login.dto.ts       # 登录 DTO
    ├── guards/                # 守卫
    │   └── jwt-auth.guard.ts  # JWT 认证守卫
    ├── strategies/            # 策略
    │   └── jwt.strategy.ts    # JWT 策略
    ├── auth.controller.ts     # 认证控制器
    ├── auth.service.ts        # 认证服务
    └── auth.module.ts         # 认证模块
```

## 安装依赖

```bash
npm install
```

## 运行项目

### 开发模式（热重载）

```bash
npm run start:dev
```

### 生产模式

```bash
npm run build
npm run start:prod
```

## API 接口文档

### 基础接口

#### 健康检查

```bash
GET http://localhost:3000/health
```

响应：

```json
{
  "status": "ok",
  "message": "服务运行正常",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

### 用户接口

#### 创建用户

```bash
POST http://localhost:3000/users
Content-Type: application/json

{
  "username": "张三",
  "email": "zhangsan@example.com",
  "password": "password123"
}
```

#### 获取用户列表

```bash
GET http://localhost:3000/users
```

#### 获取单个用户

```bash
GET http://localhost:3000/users/:id
```

#### 更新用户

```bash
PATCH http://localhost:3000/users/:id
Content-Type: application/json

{
  "username": "李四"
}
```

#### 删除用户

```bash
DELETE http://localhost:3000/users/:id
```

### 认证接口

#### 用户登录

```bash
POST http://localhost:3000/auth/login
Content-Type: application/json

{
  "email": "zhangsan@example.com",
  "password": "password123"
}
```

响应：

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "abc123",
    "username": "张三",
    "email": "zhangsan@example.com"
  }
}
```

#### 获取当前用户信息（需要认证）

```bash
GET http://localhost:3000/auth/profile
Authorization: Bearer <access_token>
```

## 技术栈

- **框架**: NestJS
- **语言**: TypeScript
- **认证**: JWT (JSON Web Token)
- **密码加密**: bcrypt
- **数据验证**: class-validator, class-transformer
- **配置管理**: @nestjs/config

## 学习要点

### 1. 模块化架构

NestJS 采用模块化架构，每个功能都是一个独立的模块，便于维护和扩展。

### 2. 依赖注入

使用 NestJS 的依赖注入系统，实现松耦合的代码结构。

### 3. 装饰器

大量使用装饰器来简化代码，如 `@Controller`、`@Get`、`@Post` 等。

### 4. DTO 和验证

使用 DTO (Data Transfer Object) 进行数据传输和验证，确保数据的安全性。

### 5. 守卫和策略

使用守卫和策略实现认证和授权功能。

## 环境变量

在 `.env` 文件中配置以下变量：

```env
PORT=3000
JWT_SECRET=your-secret-key-change-this-in-production
```

## 注意事项

1. 本项目使用内存存储数据，重启后数据会丢失
2. 生产环境请使用真实的数据库（如 MySQL、PostgreSQL、MongoDB 等）
3. 生产环境请修改 JWT_SECRET 为更安全的密钥
4. 密码使用 bcrypt 加密存储，确保安全性
