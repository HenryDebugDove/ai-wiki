from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
import httpx

# 确保数据库文件所在目录存在
os.makedirs('data', exist_ok=True)

# 数据库连接函数
def get_db():
    conn = sqlite3.connect('data/order.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db()
    cursor = conn.cursor()
    # 创建订单表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending'
    )
    ''')
    # 插入示例数据
    try:
        cursor.execute('''
        INSERT INTO orders (user_id, product_name, amount, status) VALUES (?, ?, ?, ?)
        ''', (1, '商品1', 100.0, 'completed'))
        cursor.execute('''
        INSERT INTO orders (user_id, product_name, amount, status) VALUES (?, ?, ?, ?)
        ''', (2, '商品2', 200.0, 'pending'))
        conn.commit()
    except sqlite3.IntegrityError:
        # 数据已存在，跳过
        pass
    conn.close()

# 初始化数据库
init_db()

# 创建 FastAPI 应用
app = FastAPI(
    title="订单服务",
    description="处理订单相关操作的微服务",
    version="1.0.0"
)

# 数据模型
class OrderBase(BaseModel):
    user_id: int
    product_name: str
    amount: float
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    
    class Config:
        from_attributes = True

# 服务间调用 - 获取用户信息
async def get_user_info(user_id: int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:8001/api/user/{user_id}")
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"调用用户服务失败: {e}")
        return None

# 路由
@app.get("/")
async def root():
    return {"message": "订单服务运行中"}

@app.get("/api/order", response_model=list[Order])
async def get_orders():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders')
    orders = cursor.fetchall()
    conn.close()
    return [dict(order) for order in orders]

@app.get("/api/order/{order_id}", response_model=Order)
async def get_order(order_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    order = cursor.fetchone()
    conn.close()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    return dict(order)

@app.post("/api/order", response_model=Order)
async def create_order(order: OrderCreate):
    # 验证用户是否存在
    user_info = await get_user_info(order.user_id)
    if not user_info:
        raise HTTPException(status_code=400, detail="用户不存在")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO orders (user_id, product_name, amount, status) VALUES (?, ?, ?, ?)
    ''', (order.user_id, order.product_name, order.amount, order.status))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return {"id": order_id, **order.dict()}

@app.put("/api/order/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderCreate):
    # 验证用户是否存在
    user_info = await get_user_info(order.user_id)
    if not user_info:
        raise HTTPException(status_code=400, detail="用户不存在")
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    existing_order = cursor.fetchone()
    if not existing_order:
        conn.close()
        raise HTTPException(status_code=404, detail="订单不存在")
    
    cursor.execute('''
    UPDATE orders SET user_id = ?, product_name = ?, amount = ?, status = ? WHERE id = ?
    ''', (order.user_id, order.product_name, order.amount, order.status, order_id))
    conn.commit()
    conn.close()
    return {"id": order_id, **order.dict()}

@app.delete("/api/order/{order_id}")
async def delete_order(order_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    existing_order = cursor.fetchone()
    if not existing_order:
        conn.close()
        raise HTTPException(status_code=404, detail="订单不存在")
    cursor.execute('DELETE FROM orders WHERE id = ?', (order_id,))
    conn.commit()
    conn.close()
    return {"message": "订单删除成功"}
