"""
Think of this like setting up a simple food truck:

🚚 SERVER = Your food truck
📋 LIST_TOOLS = Your menu (shows "say_hello sandwich")
🍽️ CALL_TOOL = Actually making the sandwich when someone orders

When someone asks "What do you serve?" → You show them the menu
When someone orders "say_hello sandwich with name=John" → You make "Hello, John!" sandwich

The MCP protocol is just the standard way food trucks and customers communicate:
- Standard way to ask for menu (ListToolsRequest)
- Standard way to place orders (CallToolRequest)
- Standard way to deliver food (CallToolResult)
"""


import asyncio
import sys
from datetime import datetime, timezone
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Step 1: Create a server with a name
server = Server("my-first-server")

# Step 2: Tell the server what tools it has
@server.list_tools()
async def list_my_tools():
    """This is like showing your toolbox to someone"""
    return [
        Tool(
            name="say_hello",
            description="Says hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                }
            }
        ),
        Tool(
            name="get_time",
            description="Returns the current UTC time in ISO 8601",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
    ]



# Step 3: Tell the server what to do when someone uses a tool
@server.call_tool()
async def use_tool(name: str, arguments: dict):
    """This is like actually using the tool from your toolbox"""
    if name == "say_hello":
        person_name = arguments.get("name", "World")
        message = f"Hello, {person_name}!"
        return [TextContent(type="text", text=message)]
    elif name == "get_time":
        now = datetime.now(timezone.utc).isoformat()
        return [TextContent(type="text", text=f"Current UTC time: {now}")]
    else:
        return [TextContent(type="text", text=f"Unknown tool: {name}")]

# Step 4: Start the server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="my-first-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    NotificationOptions(),
                    {}
                ),
            ),
        )

if __name__ == "__main__":
    print("🚀 Starting basic MCP server...", file=sys.stderr)
    print("This server has 2 tools: say_hello, get_time", file=sys.stderr)
    asyncio.run(main())
