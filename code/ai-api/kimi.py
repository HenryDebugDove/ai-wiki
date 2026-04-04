"""
项目功能：使用 Moonshot AI 平台调用 Kimi 模型

使用说明：
1. 在 .env 文件中设置 KIMI_API_KEY=您的API Key
2. 安装依赖：pip install openai python-dotenv
3. 运行代码：python kimi.py
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API Key
KIMI_API_KEY = os.environ.get('KIMI_API_KEY')

client = OpenAI(
    api_key = KIMI_API_KEY,
    base_url = "https://api.moonshot.cn/v1",
)
 
completion = client.chat.completions.create(
    model = "kimi-k2.5",
    messages = [
        {"role": "system", "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"},
        {"role": "user", "content": "你好，我叫李雷，1+1等于多少？"}
    ]
)
 
print(completion.choices[0].message.content)