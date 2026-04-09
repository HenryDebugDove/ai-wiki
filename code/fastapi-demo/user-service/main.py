from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import redis
import json

# 确保数据库文件所在目录存在
os.makedirs('data', exist_ok=True)

# Redis 连接
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 数据库连接函数
def get_db():
    conn = sqlite3.connect('data/user.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # 创建用户表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        age INTEGER
    )
    ''')
    # 插入示例数据
    try:
        cursor.execute('''
        INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        ''', ('张三', 'zhangsan@example.com', 25))
        cursor.execute('''
        INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        ''', ('李四', 'lisi@example.com', 30))
        conn.commit()
    except sqlite3.IntegrityError:
        # 数据已存在，跳过
        pass
    conn.close()

# 初始化数据库
init_db()

# 创建 FastAPI 应用
app = FastAPI(
    title="用户服务",
    description="用户管理微服务",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许的 HTTP 方法
    allow_headers=["*"],  # 允许的 HTTP 头
)

# 数据模型
class UserBase(BaseModel):
    name: str
    email: str
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# 路由
@app.get("/")
async def root():
    return {"message": "用户服务运行中"}

@app.get("/api/user", response_model=list[User])
async def get_users():
    # 尝试从 Redis 缓存获取
    cache_key = "users:all"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # 从数据库获取
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    
    # 转换为字典列表
    user_list = [dict(user) for user in users]
    
    # 存入 Redis 缓存，过期时间 5 分钟
    redis_client.setex(cache_key, 300, json.dumps(user_list))
    
    return user_list

@app.get("/api/user/{user_id}", response_model=User)
async def get_user(user_id: int):
    # 尝试从 Redis 缓存获取
    cache_key = f"user:{user_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # 从数据库获取
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 转换为字典
    user_dict = dict(user)
    
    # 存入 Redis 缓存，过期时间 5 分钟
    redis_client.setex(cache_key, 300, json.dumps(user_dict))
    
    return user_dict

@app.post("/api/user", response_model=User)
async def create_user(user: UserCreate):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute('''
        INSERT INTO users (name, email, age) VALUES (?, ?, ?)
        ''', (user.name, user.email, user.age))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="邮箱已存在")
    conn.close()
    
    # 清除缓存
    redis_client.delete("users:all")
    
    return {"id": user_id, **user.dict()}

@app.put("/api/user/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserCreate):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    existing_user = cursor.fetchone()
    if not existing_user:
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")
    try:
        cursor.execute('''
        UPDATE users SET name = ?, email = ?, age = ? WHERE id = ?
        ''', (user.name, user.email, user.age, user_id))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(status_code=400, detail="邮箱已存在")
    conn.close()
    
    # 清除缓存
    redis_client.delete(f"user:{user_id}")
    redis_client.delete("users:all")
    
    return {"id": user_id, **user.dict()}

@app.delete("/api/user/{user_id}")
async def delete_user(user_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    existing_user = cursor.fetchone()
    if not existing_user:
        conn.close()
        raise HTTPException(status_code=404, detail="用户不存在")
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    # 清除缓存
    redis_client.delete(f"user:{user_id}")
    redis_client.delete("users:all")
    
    return {"message": "用户删除成功"}
