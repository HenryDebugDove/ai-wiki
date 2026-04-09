from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import httpx
import redis
import json

# 确保数据库文件所在目录存在
os.makedirs('data', exist_ok=True)

# Redis 连接
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# 数据库连接函数
def get_db():
    conn = sqlite3.connect('data/payment.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # 创建支付表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        payment_method TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending'
    )
    ''')
    # 插入示例数据
    try:
        cursor.execute('''
        INSERT INTO payments (order_id, amount, payment_method, status) VALUES (?, ?, ?, ?)
        ''', (1, 100.0, 'alipay', 'completed'))
        cursor.execute('''
        INSERT INTO payments (order_id, amount, payment_method, status) VALUES (?, ?, ?, ?)
        ''', (2, 200.0, 'wechat', 'pending'))
        conn.commit()
    except sqlite3.IntegrityError:
        # 数据已存在，跳过
        pass
    conn.close()

# 初始化数据库
init_db()

# 创建 FastAPI 应用
app = FastAPI(
    title="支付服务",
    description="支付管理微服务",
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
class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    status: str = "pending"

class PaymentCreate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    
    class Config:
        from_attributes = True

# 服务间调用 - 获取订单信息
async def get_order_info(order_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8002/api/order/{order_id}")
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"调用订单服务失败: {e}")
        return None

# 路由
@app.get("/")
async def root():
    return {"message": "支付服务运行中"}

@app.get("/api/pay", response_model=list[Payment])
async def get_payments():
    # 尝试从 Redis 缓存获取
    cache_key = "payments:all"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # 从数据库获取
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments')
    payments = cursor.fetchall()
    conn.close()
    
    # 转换为字典列表
    payment_list = [dict(payment) for payment in payments]
    
    # 存入 Redis 缓存，过期时间 5 分钟
    redis_client.setex(cache_key, 300, json.dumps(payment_list))
    
    return payment_list

@app.get("/api/pay/{payment_id}", response_model=Payment)
async def get_payment(payment_id: int):
    # 尝试从 Redis 缓存获取
    cache_key = f"payment:{payment_id}"
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return json.loads(cached_data)
    
    # 从数据库获取
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
    payment = cursor.fetchone()
    conn.close()
    
    if not payment:
        raise HTTPException(status_code=404, detail="支付记录不存在")
    
    # 转换为字典
    payment_dict = dict(payment)
    
    # 存入 Redis 缓存，过期时间 5 分钟
    redis_client.setex(cache_key, 300, json.dumps(payment_dict))
    
    return payment_dict

@app.post("/api/pay", response_model=Payment)
async def create_payment(payment: PaymentCreate):
    # 验证订单是否存在
    order_info = await get_order_info(payment.order_id)
    if not order_info:
        raise HTTPException(status_code=400, detail="订单不存在")
    
    # 验证金额是否匹配
    if payment.amount != order_info['amount']:
        raise HTTPException(status_code=400, detail="支付金额与订单金额不匹配")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO payments (order_id, amount, payment_method, status) VALUES (?, ?, ?, ?)
    ''', (payment.order_id, payment.amount, payment.payment_method, payment.status))
    conn.commit()
    payment_id = cursor.lastrowid
    conn.close()
    
    # 清除缓存
    redis_client.delete("payments:all")
    
    return {"id": payment_id, **payment.dict()}

@app.put("/api/pay/{payment_id}", response_model=Payment)
async def update_payment(payment_id: int, payment: PaymentCreate):
    # 验证订单是否存在
    order_info = await get_order_info(payment.order_id)
    if not order_info:
        raise HTTPException(status_code=400, detail="订单不存在")
    
    # 验证金额是否匹配
    if payment.amount != order_info['amount']:
        raise HTTPException(status_code=400, detail="支付金额与订单金额不匹配")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
    existing_payment = cursor.fetchone()
    if not existing_payment:
        conn.close()
        raise HTTPException(status_code=404, detail="支付记录不存在")
    
    cursor.execute('''
    UPDATE payments SET order_id = ?, amount = ?, payment_method = ?, status = ? WHERE id = ?
    ''', (payment.order_id, payment.amount, payment.payment_method, payment.status, payment_id))
    conn.commit()
    conn.close()
    
    # 清除缓存
    redis_client.delete(f"payment:{payment_id}")
    redis_client.delete("payments:all")
    
    return {"id": payment_id, **payment.dict()}

@app.delete("/api/pay/{payment_id}")
async def delete_payment(payment_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM payments WHERE id = ?', (payment_id,))
    existing_payment = cursor.fetchone()
    if not existing_payment:
        conn.close()
        raise HTTPException(status_code=404, detail="支付记录不存在")
    cursor.execute('DELETE FROM payments WHERE id = ?', (payment_id,))
    conn.commit()
    conn.close()
    
    # 清除缓存
    redis_client.delete(f"payment:{payment_id}")
    redis_client.delete("payments:all")
    
    return {"message": "支付记录删除成功"}
