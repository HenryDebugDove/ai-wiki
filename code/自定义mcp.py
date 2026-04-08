from mcp.server.fastmcp import FastMCP
import requests

# 初始化
mcp = FastMCP("CustomTools", version="1.0.0")

# 工具1：天气查询
@mcp.tool(description="查询城市天气（需API Key）")
def get_weather(city: str, api_key: str) -> dict:
    """查询指定城市天气"""
    try:
        res = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"}
        )
        res.raise_for_status()
        data = res.json()
        return {
            "city": data["name"],
            "temp": f"{data['main']['temp']}°C",
            "desc": data["weather"][0]["description"]
        }
    except Exception as e:
        return {"error": str(e)}

# 工具2：计算器
@mcp.tool(description="简单数学计算")
def calculate(a: float, b: float, op: str) -> float:
    """支持 + - * /"""
    if op == "+":
        return a + b
    elif op == "-":
        return a - b
    elif op == "*":
        return a * b
    elif op == "/":
        return a / b if b != 0 else "除数不能为0"
    else:
        return "不支持的运算符"

if __name__ == "__main__":
    mcp.run()  # 默认stdio