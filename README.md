# FastMCP Server

A Model Context Protocol (MCP) server built with FastMCP, demonstrating streamable HTTP transport and Server-Sent Events (SSE) capabilities.

## Features

- ✨ **StreamableHTTP Transport** - HTTP-based MCP server with SSE support
- 🔧 **Multiple Tools** - Add integers, greet users, and stream live data
- 🚀 **Real-time Streaming** - Generator functions with time-based processing
- ⚡ **Stateless Mode** - Horizontally scalable, no session management
- 🐳 **Dev Container Ready** - Complete development environment

## Quick Start

### Local Development

```bash
# Install dependencies
uv sync

# Start the FastMCP server
uv run python main.py

# Server runs on http://localhost:3001
# MCP endpoint: http://localhost:3001/mcp
# SSE endpoint: http://localhost:3001/sse
```

### Using Dev Container

This repository includes a complete development container setup for consistent development across environments.

#### Prerequisites
- [VS Code](https://code.visualstudio.com/)
- [Docker](https://www.docker.com/get-started/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

#### Quick Setup
1. Clone this repository
2. Open in VS Code
3. When prompted, click "Reopen in Container" (or use Command Palette: "Dev Containers: Reopen in Container")
4. Wait for the container to build and dependencies to install
5. Run the server: `uv run python main.py`

The dev container includes:
- Python 3.12 with uv package manager
- Pre-configured VS Code extensions (Python, Pylance, etc.)
- Zsh with Oh My Zsh
- Git and GitHub CLI
- Port forwarding for FastMCP server (3001, 8000, 8080)

## Available Tools

### `add(a: int, b: int) -> int`
Add two integers together.

### `greet(name: str) -> str` 
Return a friendly greeting message.

### `stream_numbers(n: int = 5) -> Generator`
Emit numbers 1..n with delays, demonstrating streaming capabilities.

### `live_data_feed(duration: int = 10) -> Generator`
Stream live system metrics (CPU, memory, etc.) for the specified duration.

### `progress_tracker(task: str, steps: int = 8) -> Generator`
Track progress of a long-running task with status updates.

## Testing the Server

### Using MCP Inspector
```bash
# Install and run MCP Inspector
npx @modelcontextprotocol/inspector

# Connect to: http://localhost:3001/sse
```

### Using curl
```bash
# Initialize session
curl -X POST http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test-client", "version": "1.0.0"}
    }
  }'

# List available tools
curl -X POST http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list"
  }'

# Call the add tool
curl -X POST http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "add",
      "arguments": {"a": 15, "b": 27}
    }
  }'

# Test streaming (use -N for real-time output)
curl -N -X POST http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 4,
    "method": "tools/call",
    "params": {
      "name": "stream_numbers",
      "arguments": {"n": 5}
    }
  }'
```

## Configuration

Environment variables:
- `MCP_HOST` - Server host (default: "0.0.0.0")
- `MCP_PORT` - Server port (default: 3001)

## Architecture

This server uses:
- **FastMCP** - Modern MCP server framework
- **StreamableHTTP Transport** - HTTP-based with SSE support
- **Stateless Mode** - For horizontal scaling
- **Generator Functions** - For streaming data over time

The server consolidates all client-server interactions through:
- `POST /mcp` - For immediate JSON responses
- `GET /sse` - For Server-Sent Events (streaming)

## Development

### Project Structure
```
mcp-uv-base/
├── .devcontainer/          # Dev container configuration
│   ├── devcontainer.json   # VS Code dev container settings
│   └── Dockerfile          # Container image definition
├── main.py                 # FastMCP server implementation
├── pyproject.toml          # Python project configuration
├── uv.lock                 # Locked dependencies
└── README.md               # This file
```

### Adding New Tools

```python
@mcp.tool()
def your_new_tool(param: str) -> str:
    \"\"\"Description of your tool.\"\"\"
    # Your implementation here
    return f"Result: {param}"
```

For streaming tools, use generators:

```python
@mcp.tool()
def your_streaming_tool(count: int) -> Generator[Dict[str, Any], None, Dict[str, str]]:
    \"\"\"A streaming tool example.\"\"\"
    for i in range(count):
        yield {"step": i, "data": f"Processing {i}"}
        time.sleep(1)
    return {"status": "completed"}
```

## License

MIT License - feel free to use this as a starting point for your own MCP servers.
