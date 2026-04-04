from openai import OpenAI

# 直接在这里填写你的火山方舟 API Key
ARK_API_KEY = "这里替换成你的真实API Key"

# 初始化客户端（从变量读取，不从环境变量读取）
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=ARK_API_KEY,  # 直接使用文件内的变量
)

if __name__ == "__main__":
    resp = client.chat.completions.create(
        model="doubao-seed-2-0-code-preview-260215",
        messages=[{"content": "天空为什么是蓝色的？", "role": "user"}],
    )

    print(resp.choices[0].message.content)