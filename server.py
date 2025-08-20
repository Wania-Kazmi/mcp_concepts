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
import os
from datetime import datetime
import textwrap
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Create our enhanced MCP Server
server = Server("practical-tools-server")

@server.list_tools()
async def list_practical_tools():
    """
    Now we have 5 practical tools that do real work!
    This is still the same ListToolsRequest/Response pattern
    """
    return [
        # Tool 1: Simple greeting (from Step 1)
        Tool(
            name="say_hello",
            description="Says hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Person to greet"}
                },
                "required": ["name"]
            }
        ),
        
        # Tool 2: File operations
        Tool(
            name="read_file",
            description="Read contents of a text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Path to the file to read"}
                },
                "required": ["filename"]
            }
        ),
        
        # Tool 3: Write files
        Tool(
            name="write_file",
            description="Write text to a file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Path to the file to write"},
                    "content": {"type": "string", "description": "Content to write to the file"}
                },
                "required": ["filename", "content"]
            }
        ),
        
        # Tool 4: List directory contents
        Tool(
            name="list_directory",
            description="List files and folders in a directory",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list"}
                },
                "required": ["path"]
            }
        ),
        
        # Tool 5: Create a simple report
        Tool(
            name="create_report",
            description="Create a simple text report with current info",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Report title"}
                },
                "required": ["title"]
            }
        )
    ]

@server.call_tool()
async def handle_practical_tools(name: str, arguments: dict):
    """
    Handle all our practical tools
    This is still the same CallToolRequest/Response pattern
    """
    
    if name == "say_hello":
        # Same as Step 1
        person_name = arguments.get("name", "World")
        message = f"Hello, {person_name}! 👋"
        return [TextContent(type="text", text=message)]
    
    elif name == "read_file":
        # NEW: Read a file from disk
        filename = arguments["filename"]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            return [TextContent(type="text", text=f"File '{filename}' contents:\n\n{content}")]
        except FileNotFoundError:
            return [TextContent(type="text", text=f"❌ File '{filename}' not found")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error reading file: {str(e)}")]
    
    elif name == "write_file":
        # NEW: Write content to a file
        filename = arguments["filename"]
        content = arguments["content"]
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            return [TextContent(type="text", text=f"✅ Successfully wrote to '{filename}'")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error writing file: {str(e)}")]
    
    elif name == "list_directory":
        # NEW: List directory contents
        path = arguments["path"]
        try:
            if not os.path.exists(path):
                return [TextContent(type="text", text=f"❌ Directory '{path}' does not exist")]
            
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    items.append(f"📁 {item}/")
                else:
                    items.append(f"📄 {item}")
            
            result = f"Contents of '{path}':\n" + "\n".join(items)
            return [TextContent(type="text", text=result)]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error listing directory: {str(e)}")]
    
    elif name == "create_report":
        # NEW: Create a simple report
        title = arguments["title"]
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_dir = os.getcwd()
        
        report = textwrap.dedent(f"""
            📊 {title}
            {'=' * (len(title) + 4)}

            Generated: {current_time}
            Working Directory: {current_dir}
            Server: practical-tools-server v1.0

            Summary:
            - This report was generated by an MCP tool
            - The server is running and responding to requests
            - File operations are working correctly

            Status: ✅ All systems operational
            """)
        
        # Also save the report to a file
        report_filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(report_filename, 'w', encoding='utf-8') as f:
                f.write(report.strip())
            
            final_message = report + f"\n\n💾 Report also saved to: {report_filename}"
            return [TextContent(type="text", text=final_message)]
        except Exception as e:
            return [TextContent(type="text", text=report + f"\n\n⚠️ Could not save to file: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]

# Same server startup as before
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="practical-tools-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    NotificationOptions(),
                    {}
                ),
            ),
        )

if __name__ == "__main__":
    logger.info("🚀 Starting Enhanced MCP Server...")
    logger.info("📋 Available tools:")
    logger.info("   • say_hello - Greet someone")
    logger.info("   • read_file - Read file contents")
    logger.info("   • write_file - Write to a file")
    logger.info("   • list_directory - List directory contents")
    logger.info("   • create_report - Generate a report")
    logger.info("Ready for MCP requests!")
    asyncio.run(main())