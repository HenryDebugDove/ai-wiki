# FastAPI 项目演示

这是一个使用 FastAPI 和 SQLite 数据库的简单演示项目，用于快速验证和学习 FastAPI 框架。

## 项目结构

```
.
├── main.py          # FastAPI 应用主文件
├── requirements.txt # 项目依赖
└── data/            # 数据库文件目录
    └── db.sqlite    # SQLite 数据库文件
```

## 功能特性

- **RESTful API**：实现了完整的 CRUD 操作
- **SQLite 数据库**：轻量级数据库，无需额外配置
- **自动 API 文档**：FastAPI 自动生成的 Swagger 文档
- **数据验证**：使用 Pydantic 进行数据模型定义和验证
- **错误处理**：基本的错误处理机制

## 安装步骤

1. **克隆项目**（如果需要）
2. **安装依赖**

   ```bash
   cd fastapi-demo
   pip install -r requirements.txt
   ```

## 运行项目

```bash
uvicorn main:app --reload
```

- `--reload` 参数会在代码修改时自动重新加载服务器

## 访问 API 文档

启动服务后，打开浏览器访问：

- **Swagger 文档**：http://127.0.0.1:8000/docs
- **ReDoc 文档**：http://127.0.0.1:8000/redoc

## API 接口

| 方法   | 路径             | 功能                 |
| ------ | ---------------- | -------------------- |
| GET    | /                | 根路径，返回欢迎信息 |
| GET    | /users           | 获取所有用户         |
| GET    | /users/{user_id} | 获取单个用户         |
| POST   | /users           | 创建新用户           |
| PUT    | /users/{user_id} | 更新用户信息         |
| DELETE | /users/{user_id} | 删除用户             |

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

## 示例请求

### 创建用户

```bash
curl -X POST "http://127.0.0.1:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "王五", "email": "wangwu@example.com", "age": 35}'
```

### 获取所有用户

```bash
curl "http://127.0.0.1:8000/users"
```

### 获取单个用户

```bash
curl "http://127.0.0.1:8000/users/1"
```

### 更新用户

```bash
curl -X PUT "http://127.0.0.1:8000/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三（更新）", "email": "zhangsan@example.com", "age": 26}'
```

### 删除用户

```bash
curl -X DELETE "http://127.0.0.1:8000/users/1"
```

## 技术栈

- **FastAPI**：现代、快速的 Web 框架
- **Uvicorn**：ASGI 服务器
- **Pydantic**：数据验证
- **SQLite**：轻量级数据库

## 注意事项

- 本项目使用 SQLite 数据库，适合开发和测试环境
- 生产环境建议使用更强大的数据库，如 PostgreSQL 或 MySQL
- 数据库文件会自动创建在 `data/db.sqlite`
- 项目启动时会自动插入两条示例数据
