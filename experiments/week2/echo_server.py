"""最小 MCP Server（路线 B）：用官方 FastMCP SDK 暴露一个 echo 工具。

依赖：pip install "mcp[cli]"
运行：python echo_server.py        # 默认 stdio 传输，供 Cursor 等 Host 拉起

stdio 模式下 stdout 是协议通道，日志必须走 stderr，切勿用 print 污染 stdout。
"""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("echo-demo")


@mcp.tool()
def echo(text: str) -> str:
    """原样返回输入文本，用于验证 MCP 连接是否跑通。"""
    return f"echo: {text}"


@mcp.tool()
def reverse(text: str) -> str:
    """返回反转后的文本，多一个工具便于在 Host 里观察工具列表。"""
    return text[::-1]


if __name__ == "__main__":
    mcp.run()
