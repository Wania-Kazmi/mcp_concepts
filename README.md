# MCP Hello World

A beginner-friendly introduction to the Model Context Protocol (MCP) with practical examples.

## 📖 What is MCP?

The Model Context Protocol (MCP) is an open standard that enables AI applications to securely connect with external data sources and tools. Think of it as a "universal USB port" for AI integrations.

### Key Benefits

- **Standardized Communication**: One protocol works with any AI model or external service
- **Reusable Integrations**: Build once, use with multiple AI applications
- **Secure Connections**: Built-in security and permission management
- **Extensible**: Easy to add new tools and capabilities

## 🎯 What This Project Demonstrates

This tutorial shows MCP concepts through a simple client-server example:

1. **MCP Server**: Provides tools that can be called remotely
2. **MCP Client**: Discovers and uses tools from MCP servers
3. **Standard Protocol**: Both follow the same communication patterns used in production systems

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (fast Python package manager)

### Installation

```bash
# 1. Create project
uv init mcp-hello-world
cd mcp-hello-world

# 2. Install dependencies
uv add mcp

# 3. Create the files (see Project Structure below)
```

### Running the Demo

```bash
# Run the complete client-server demo
uv run client.py
```

Expected output:

```markdown
🤖 Starting Basic MCP Client Demo
==================================================
🔗 Connecting to server...
✅ Connected!
📋 Asking server: 'What tools do you have?'
📝 Server has 2 tools:
   • say_hello: Says hello to someone
   • get_time: Gets the current time
🛠️ Using the 'say_hello' tool...
💬 Server response:
   'Hello, Alice!'
⏰ Using the 'get_time' tool...
🕐 Time response:
   'The current time is: 2025-08-19 17:30:45'
🎉 Demo complete! You just saw MCP in action!
```

## 📁 Project Structure

```markdown
mcp-hello-world/
├── pyproject.toml          # Project configuration
├── server.py               # MCP Server implementation
├── client.py               # MCP Client implementation
└── README.md               # This file
```

## 🔧 How It Works

### MCP Server (`server.py`)

The server demonstrates two core MCP concepts:

1. **Tool Discovery** (`@server.list_tools()`):
   - Responds to `ListToolsRequest` messages
   - Returns available tools and their schemas
   - Like showing a menu to customers

2. **Tool Execution** (`@server.call_tool()`):
   - Handles `CallToolRequest` messages
   - Executes the requested tool with provided arguments
   - Returns results via `CallToolResult`

### MCP Client (`client.py`)

The client demonstrates the complete MCP workflow:

1. **Connection**: Establishes stdio communication with server
2. **Discovery**: Sends `ListToolsRequest` to discover available tools
3. **Execution**: Calls tools using `CallToolRequest` with parameters
4. **Results**: Processes `CallToolResult` responses

## 📚 MCP Message Flow

This example implements the standard MCP message exchange pattern:

```markdown
Client                    Server
  │                         │
  ├─ ListToolsRequest ────► │
  │                         │
  │ ◄──── ListToolsResult ─┤
  │                         │
  ├─ CallToolRequest ─────► │
  │                         │
  │ ◄───── CallToolResult ──┤
```

## 🛠️ Available Tools

| Tool Name | Description | Parameters |
|-----------|-------------|------------|
| `say_hello` | Returns a personalized greeting | `name` (string): Person to greet |
| `get_time` | Returns current timestamp | None |

## 🎓 Learning Path

This project is designed for progressive learning:

- **Step 1** ✅: Basic server with simple tools (current)
- **Step 2**: Add file system operations
- **Step 3**: Connect to external APIs
- **Step 4**: Add resources and prompts
- **Step 5**: Build a complete application integration

## 🔍 Key Concepts Illustrated

### Standardization

Both client and server use the same message types (`ListToolsRequest`, `CallToolRequest`, etc.) regardless of what the tools actually do. This means any MCP client can work with any MCP server.

### Modularity

The server can be easily extended with new tools without changing the client code. The client can work with any MCP server without knowing the internal implementation.

### Real-World Parallel

Replace our simple tools with:

- `create_github_repo` instead of `say_hello`
- `query_database` instead of `get_time`

The communication pattern remains identical!

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'mcp'"

```bash
# Make sure you're in the project directory and run:
uv add mcp
```

#### "Permission denied" errors

```bash
# On Unix systems, you might need:
chmod +x server.py client.py
```

#### Server doesn't respond

- Ensure `server.py` runs without errors first
- Check that both files are in the same directory

## 📖 Further Reading

- [Official MCP Documentation](https://modelcontextprotocol.io/)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Anthropic MCP Guide](https://docs.anthropic.com/en/docs/build-with-claude/mcp)