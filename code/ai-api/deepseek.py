"""
项目功能：使用 DeepSeek API 调用大语言模型

使用说明：
1. 在 .env 文件中设置 DEEPSEEK_API_KEY=您的API Key
2. 安装依赖：pip install openai python-dotenv
3. 运行代码：python deepseek.py
"""

# Please install OpenAI SDK first: `pip3 install openai`
import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API Key
DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是我的个人生活助手"},
        {"role": "user", "content": "你可以做什么？"},
    ],
    stream=False
)

print(response.choices[0].message.content)