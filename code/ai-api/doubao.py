"""
项目功能：使用火山引擎方舟平台调用豆包模型

使用说明：
1. 在 .env 文件中设置 ARK_API_KEY=您的API Key
2. 安装依赖：pip install openai python-dotenv
3. 运行代码：python doubao.py
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取 API Key
ARK_API_KEY = os.environ.get('ARK_API_KEY')

# 初始化客户端（从环境变量读取 API Key）
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=ARK_API_KEY,  # 从环境变量读取
)

if __name__ == "__main__":
    resp = client.chat.completions.create(
        model="doubao-seed-2-0-code-preview-260215",
        messages=[{"content": "你好", "role": "user"}],
    )

    print(resp.choices[0].message.content)