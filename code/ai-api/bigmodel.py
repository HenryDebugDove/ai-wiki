"""
项目功能：使用智谱 AI 平台调用大模型

使用说明：
1. 在 .env 文件中设置 ZHIPU_API_KEY=您的API Key
2. 安装依赖：pip install requests python-dotenv
3. 运行代码：python bigmodel.py
"""

import os
import requests
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API Key
ZHIPU_API_KEY = os.environ.get('ZHIPU_API_KEY')

url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

payload = {
    "model": "glm-5",
    "messages": [
        {
            "role": "system",
            "content": "你是一个有用的AI助手。"
        },
        {
            "role": "user",
            "content": "你好 你可以做什么？"
        }
    ],
    "stream": False,
    "temperature": 1
}
headers = {
    "Authorization": f"Bearer {ZHIPU_API_KEY}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)