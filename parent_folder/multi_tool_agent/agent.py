import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    此函数模拟获取指定城市的天气信息。目前仅支持纽约市的天气查询，
    其他城市将返回错误信息。在实际应用中，可以扩展此函数以连接到
    真实的天气API服务。

    Args:
        city (str): 要查询天气的城市名称。

    Returns:
        dict: 包含状态和结果的字典。
            成功时返回格式: {"status": "success", "report": "天气信息"}
            失败时返回格式: {"status": "error", "error_message": "错误信息"}
    
    示例:
        >>> get_weather("New York")
        {"status": "success", "report": "The weather in New York is sunny..."}
        
        >>> get_weather("Beijing")
        {"status": "error", "error_message": "Weather information for 'Beijing' is not available."}
    """
    # 检查城市名称是否为纽约（不区分大小写）
    if city.lower() == "new york":
        # 返回纽约的模拟天气数据
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        # 对于不支持的城市，返回错误信息
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    此函数根据指定城市返回当前时间。目前仅支持纽约市的时区查询，
    其他城市将返回错误信息。函数使用Python的datetime和zoneinfo
    模块来处理时区转换。

    Args:
        city (str): 要查询当前时间的城市名称。

    Returns:
        dict: 包含状态和结果的字典。
            成功时返回格式: {"status": "success", "report": "时间信息"}
            失败时返回格式: {"status": "error", "error_message": "错误信息"}
    
    示例:
        >>> get_current_time("New York")
        {"status": "success", "report": "The current time in New York is 2023-04-01 14:30:45 EDT-0400"}
        
        >>> get_current_time("Tokyo")
        {"status": "error", "error_message": "Sorry, I don't have timezone information for Tokyo."}
    """
    # 检查城市名称是否为纽约（不区分大小写）
    if city.lower() == "new york":
        # 设置纽约的时区标识符
        tz_identifier = "America/New_York"
    else:
        # 对于不支持的城市，返回错误信息
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    # 创建指定时区的ZoneInfo对象
    tz = ZoneInfo(tz_identifier)
    # 获取指定时区的当前时间
    now = datetime.datetime.now(tz)
    # 格式化时间字符串，包含年月日、时分秒、时区名称和UTC偏移
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    # 返回成功状态和时间报告
    return {"status": "success", "report": report}

# 创建Google ADK代理实例
root_agent = Agent(
    # 代理名称，用于标识此代理
    name="weather_time_agent",
    # 使用的LLM模型，这里使用Gemini 2.0 Flash版本
    model="gemini-2.0-flash",
    # 代理的简要描述，说明其功能和用途
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    # 代理的详细指令，指导其如何响应用户查询
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    # 注册可用工具函数，使代理能够调用这些函数来获取信息
    tools=[get_weather, get_current_time],
)