# main.py
import time
from typing import Any, Dict, Generator

from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP(name="demo", version="0.1.0")

# Define tools
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers."""
    return a + b

@mcp.tool()
def greet(name: str) -> str:
    """Return a friendly greeting."""
    return f"Hello, {name}!"

@mcp.tool()
def stream_numbers(n: int = 5) -> Generator[Dict[str, Any], None, Dict[str, bool]]:
    """Emit numbers 1..n with a short delay."""
    for i in range(1, n + 1):
        yield {"step": i, "message": f"Counting {i}"}
        time.sleep(0.5)
    return {"done": True}

# Run the server
if __name__ == "__main__":
    print("🚀 Starting FastMCP Server...")
    print("📍 Server will run on: http://localhost:3001")
    print("🔗 SSE endpoint available at: http://localhost:3001/sse")
    print("🛠️  Available tools: add, greet, stream_numbers")
    print("🔍 For MCP Inspector, connect to: http://localhost:3001/sse")
    
    # Run with streamable HTTP transport for SSE support
    mcp.run(transport="streamable-http", host="localhost", port=3001)