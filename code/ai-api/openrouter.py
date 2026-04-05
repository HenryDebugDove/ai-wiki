"""
项目功能：使用 OpenRouter API 调用大语言模型

OpenRouter 使用说明：
1. 注册 OpenRouter 账号：访问 https://openrouter.ai/ 注册并登录
2. 获取 API Key：在个人设置页面生成 API Key
3. 替换 API Key：将下方的 "替换为自己在OpenRouter的申请的API Key" 替换为你的实际 API Key
4. 安装依赖：pip install openai python-dotenv
5. 运行代码：python index.py

OpenRouter 优势：
- 聚合了多个大模型，支持多种模型选择
- 提供免费模型选项 (openrouter/free)
- 调用方式与 OpenAI API 完全兼容
- 响应速度快，稳定性高
"""

# 安装依赖：pip install openai python-dotenv
import os
from openai import OpenAI

# 直接填入你的 OpenRouter API Key 
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="替换为自己在OpenRouter的申请的API Key"
)

# 发送请求
response = client.chat.completions.create(
    model="openrouter/free",  # 免费模型
    messages=[
        {"role": "user", "content": "你好，介绍一下提示词工程"}
    ]
)

# 输出结果
print(response.choices[0].message.content)