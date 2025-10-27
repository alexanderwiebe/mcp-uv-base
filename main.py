# main.py
import asyncio
import json
import os
import random
import time
from typing import Any, AsyncGenerator, Dict, Generator

from fastmcp import Context, FastMCP

# Create the MCP server with proper configuration for StreamableHTTP
mcp = FastMCP(
    name="demo",
    version="0.1.0",
    stateless_http=True,  # Enable stateless mode for easier testing and horizontal scaling
    debug=True,  # Enable debug mode for verbose logging
)

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

@mcp.tool()
def live_data_feed(duration: int = 10) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """Stream live data updates for the specified duration in seconds."""
    import random
    start_time = time.time()
    counter = 0
    
    while time.time() - start_time < duration:
        counter += 1
        current_time = time.strftime("%H:%M:%S")
        
        # Simulate different types of streaming data
        data_types = ["temperature", "pressure", "humidity", "cpu_usage"]
        data_type = random.choice(data_types)
        value = round(random.uniform(10, 100), 2)
        
        yield {
            "timestamp": current_time,
            "sequence": counter,
            "data_type": data_type,
            "value": value,
            "status": "streaming",
            "elapsed": round(time.time() - start_time, 1)
        }
        
        time.sleep(1)  # 1 second between updates
    
    return {"status": "completed", "total_updates": counter}

@mcp.tool()
def progress_tracker(task: str = "data_processing", steps: int = 8) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """Track progress of a long-running task with multiple status updates."""
    task_steps = [
        "Initializing...",
        "Loading data...",
        "Validating input...",
        "Processing batch 1/3...",
        "Processing batch 2/3...",
        "Processing batch 3/3...",
        "Generating report...",
        "Finalizing..."
    ]
    
    for i, step_name in enumerate(task_steps[:steps], 1):
        progress = round((i / steps) * 100, 1)
        
        yield {
            "task": task,
            "step": i,
            "total_steps": steps,
            "progress_percent": progress,
            "current_step": step_name,
            "status": "in_progress",
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        # Variable delays to simulate real work
        delay = random.uniform(0.5, 2.0)
        time.sleep(delay)
    
    return {"status": "completed", "task": task, "final_progress": 100}

@mcp.tool()
def simple_counter(count: int = 3) -> Generator[Dict[str, Any], None, Dict[str, Any]]:
    """Simple counter that yields individual numbers - great for testing streaming."""
    for i in range(1, count + 1):
        yield {
            "current_number": i,
            "total_count": count,
            "percentage": round((i / count) * 100, 1),
            "message": f"Processing item {i} of {count}",
            "timestamp": time.strftime("%H:%M:%S")
        }
        time.sleep(1)  # 1 second delay between each yield
    
    return {"status": "counting_completed", "final_count": count}

@mcp.tool()
async def simple_counter2(count: int = 3) -> AsyncGenerator[Dict[str, Any], Dict[str, Any]]:
    """Simple counter that yields individual numbers."""
    for i in range(1, count + 1):
        yield {
            "current_number": i,
            "total_count": count,
            "percentage": round((i / count) * 100, 1),
            "message": f"Processing item {i} of {count}",
            "timestamp": time.strftime("%H:%M:%S"),
        }
        await asyncio.sleep(1)
    yield {"status": "counting_completed", "final_count": count}

@mcp.tool()
async def simple_counter3(ctx: Context, count: int = 3) -> Dict[str, Any]:
    """Simple counter that yields individual numbers in real time."""
    for i in range(1, count + 1):
        # send_event pushes an incremental SSE message immediately
        await ctx.send_event({
            "current_number": i,
            "total_count": count,
            "percentage": round((i / count) * 100, 1),
            "message": f"Processing item {i} of {count}",
            "timestamp": time.strftime("%H:%M:%S"),
        })
        await asyncio.sleep(1)

    # Final return is sent as the last SSE event
    return {"status": "counting_completed", "final_count": count}

# Run the server
if __name__ == "__main__":
    # Configuration based on MCPcat documentation
    host = os.getenv("MCP_HOST", "0.0.0.0")  # Allow external connections
    port = int(os.getenv("MCP_PORT", 3001))
    
    # Run with streamable HTTP transport and proper configuration
    mcp.run(transport="streamable-http", host=host, port=port)

# debug: npx @modelcontextprotocol/inspector uv run fastmcp run main.py:mcp
# execute: uv run fastmcp run main.py:mcp
