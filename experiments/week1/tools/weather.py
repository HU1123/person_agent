"""模拟天气工具 — 硬编码数据，用于 Function Calling 实验。"""

# 预设城市天气数据（摄氏度）
WEATHER_DATA: dict[str, dict[str, str | int]] = {
    "北京": {"temperature": 15, "condition": "晴", "humidity": "30%"},
    "上海": {"temperature": 22, "condition": "多云", "humidity": "65%"},
    "广州": {"temperature": 28, "condition": "阴", "humidity": "80%"},
    "深圳": {"temperature": 27, "condition": "晴", "humidity": "70%"},
    "成都": {"temperature": 18, "condition": "雾", "humidity": "85%"},
}

WEATHER_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "查询指定城市的当前天气信息，包括温度、天气状况和湿度",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如：北京、上海",
                }
            },
            "required": ["city"],
        },
    },
}


def get_weather(city: str) -> str:
    """查询城市天气，返回自然语言描述。"""
    data = WEATHER_DATA.get(city)
    if data is None:
        available = "、".join(WEATHER_DATA.keys())
        return f"未找到城市「{city}」的天气数据。可用城市：{available}"
    return (
        f"{city}当前天气：{data['condition']}，"
        f"温度 {data['temperature']}°C，湿度 {data['humidity']}"
    )
