# API 测试示例

## 1. 健康检查
```bash
curl http://localhost:3000/health
```

## 2. 创建用户
```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "张三",
    "email": "zhangsan@example.com",
    "password": "password123"
  }'
```

## 3. 获取用户列表
```bash
curl http://localhost:3000/users
```

## 4. 获取单个用户
```bash
curl http://localhost:3000/users/<user_id>
```

## 5. 更新用户
```bash
curl -X PATCH http://localhost:3000/users/<user_id> \
  -H "Content-Type: application/json" \
  -d '{
    "username": "李四"
  }'
```

## 6. 删除用户
```bash
curl -X DELETE http://localhost:3000/users/<user_id>
```

## 7. 用户登录
```bash
curl -X POST http://localhost:3000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "zhangsan@example.com",
    "password": "password123"
  }'
```

## 8. 获取当前用户信息（需要先登录获取 token）
```bash
curl http://localhost:3000/auth/profile \
  -H "Authorization: Bearer <your_access_token>"
```

## 使用 Postman 测试

你也可以使用 Postman 或其他 API 测试工具来测试这些接口。

### Postman 集合导入

将以下 JSON 导入到 Postman 中：

```json
{
  "info": {
    "name": "NestJS Demo API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "健康检查",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:3000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "3000",
          "path": ["health"]
        }
      }
    },
    {
      "name": "创建用户",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"username\": \"张三\",\n  \"email\": \"zhangsan@example.com\",\n  \"password\": \"password123\"\n}"
        },
        "url": {
          "raw": "http://localhost:3000/users",
          "protocol": "http",
          "host": ["localhost"],
          "port": "3000",
          "path": ["users"]
        }
      }
    },
    {
      "name": "获取用户列表",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:3000/users",
          "protocol": "http",
          "host": ["localhost"],
          "port": "3000",
          "path": ["users"]
        }
      }
    },
    {
      "name": "用户登录",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"email\": \"zhangsan@example.com\",\n  \"password\": \"password123\"\n}"
        },
        "url": {
          "raw": "http://localhost:3000/auth/login",
          "protocol": "http",
          "host": ["localhost"],
          "port": "3000",
          "path": ["auth", "login"]
        }
      }
    },
    {
      "name": "获取当前用户信息",
      "request": {
        "method": "GET",
        "header": [
          {
            "key": "Authorization",
            "value": "Bearer <your_access_token>"
          }
        ],
        "url": {
          "raw": "http://localhost:3000/auth/profile",
          "protocol": "http",
          "host": ["localhost"],
          "port": "3000",
          "path": ["auth", "profile"]
        }
      }
    }
  ]
}
```
