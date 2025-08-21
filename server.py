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

Resources in MCP are like "readable data sources" that AI can access:
- Files, databases, web pages, APIs
- Different from Tools (which DO things)
- Resources provide DATA for AI to read and understand
"""

import asyncio
import os
from datetime import datetime
import json
from pathlib import Path
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool, 
    TextContent, 
    Resource,  # NEW: For resources
    ReadResourceResult,  # NEW: For resource responses
    TextResourceContents,  # NEW: For text resource content
)


import logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Create our enhanced MCP Server
server = Server("tools-and-resources-server")

# ============================================================================
# TOOLS SECTION 
# ============================================================================

@server.list_tools()
async def list_tools():
    """List available tools (same as before)"""
    return [
        Tool(
            name="say_hello",
            description="Says hello to someone",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"]
            }
        ),
        Tool(
            name="create_sample_data",
            description="Create sample JSON data files for testing resources",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string", "description": "Name for the JSON file"}
                },
                "required": ["filename"]
            }
        ),
        Tool(
            name="write_note",
            description="Write a note to a text file",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["filename", "content"]
            }
        )
    ]

@server.call_tool()
async def handle_tools(name: str, arguments: dict):
    """Handle tool calls (enhanced from Step 3)"""
    
    if name == "say_hello":
        person_name = arguments.get("name", "World")
        return [TextContent(type="text", text=f"Hello, {person_name}! 👋")]
    
    elif name == "create_sample_data":
        filename = arguments["filename"]
        if not filename.endswith('.json'):
            filename += '.json'
        
        # Create sample data
        sample_data = {
            "created_at": datetime.now().isoformat(),
            "server": "tools-and-resources-server",
            "data": {
                "users": [
                    {"id": 1, "name": "Alice", "role": "admin"},
                    {"id": 2, "name": "Bob", "role": "user"},
                    {"id": 3, "name": "Charlie", "role": "user"}
                ],
                "settings": {
                    "theme": "dark",
                    "notifications": True,
                    "language": "en"
                }
            }
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(sample_data, f, indent=2)
            return [TextContent(type="text", text=f"✅ Created sample data file: {filename}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error creating file: {str(e)}")]
    
    elif name == "write_note":
        filename = arguments["filename"]
        content = arguments["content"]
        try:
            with open(filename, 'w') as f:
                f.write(f"Note created: {datetime.now()}\n\n{content}")
            return [TextContent(type="text", text=f"✅ Note saved to: {filename}")]
        except Exception as e:
            return [TextContent(type="text", text=f"❌ Error writing note: {str(e)}")]
    
    else:
        return [TextContent(type="text", text=f"❌ Unknown tool: {name}")]
    

# ============================================================================
# RESOURCES SECTION (NEW IN STEP 4!)
# ============================================================================


@server.list_resources()
async def list_resources():
    """
    NEW: List available resources
    Resources are data sources that AI can read (like a library catalog)
    """
    resources = []
    
    # Resource 1: Current directory listing
    resources.append(Resource(
        uri="file://current-directory",
        name="Current Directory",
        description="List of files in the current directory",
        mimeType="text/plain"
    ))
    
    # Resource 2: Server status info
    resources.append(Resource(
        uri="server://status",
        name="Server Status", 
        description="Current server status and information",
        mimeType="application/json"
    ))
    
    # Resource 3: Any JSON files we find
    for json_file in Path('.').glob('*.json'):
        resources.append(Resource(
            uri=f"file://{json_file}",
            name=f"JSON Data: {json_file.name}",
            description=f"JSON data from {json_file.name}",
            mimeType="application/json"
        ))
    
    # Resource 4: Any text files we find  
    for txt_file in Path('.').glob('*.txt'):
        resources.append(Resource(
            uri=f"file://{txt_file}",
            name=f"Text File: {txt_file.name}",
            description=f"Text content from {txt_file.name}",
            mimeType="text/plain"
        ))
    
    return resources


@server.read_resource()
async def read_resource(uri: str):
    """
    NEW: Handle resource reading requests
    When AI wants to read a resource, this function provides the data
    """
    # Convert URI to string if it's a Pydantic AnyUrl object
    uri_str = str(uri)
    # Normalize trivial trailing slash differences (some URL parsers will append a trailing slash)
    normalized_uri = uri_str.rstrip('/')
    
    if normalized_uri == "file://current-directory":
        # Provide directory listing
        files = []
        for item in os.listdir('.'):
            if os.path.isdir(item):
                files.append(f"📁 {item}/")
            else:
                files.append(f"📄 {item}")
        
        content = "Current Directory Contents:\n" + "\n".join(files)
        return ReadResourceResult(contents=[TextResourceContents(uri=uri_str, text=content)])
    
    elif normalized_uri == "server://status":
        # Provide server status as JSON
        # Compute available resources without invoking the decorated handler to avoid wrapper return shapes
        json_count = len(list(Path('.').glob('*.json')))
        txt_count = len(list(Path('.').glob('*.txt')))
        # Base resources: current-directory and server status
        base_resources = 2
        total_resources = base_resources + json_count + txt_count
        status_data = {
            "server_name": "tools-and-resources-server",
            "version": "1.0.0",
            "status": "running",
            "uptime": "active",
            "capabilities": ["tools", "resources"],
            "tools_count": 3,
            "resources_available": total_resources,
            "current_time": datetime.now().isoformat()
        }
        
        return ReadResourceResult(contents=[TextResourceContents(uri=uri_str, text=json.dumps(status_data, indent=2))])
    
    elif normalized_uri.startswith("file://"):
        # Read actual files
        filename = uri_str.replace("file://", "", 1)
        # Remove a trailing slash if present (e.g., file://users.json/)
        if filename.endswith('/') or filename.endswith('\\'):
            filename = filename[:-1]
        try:
            with open(filename, 'r') as f:
                content = f.read()
            return ReadResourceResult(contents=[TextResourceContents(uri=uri_str, text=content)])
        except FileNotFoundError:
            return ReadResourceResult(contents=[TextResourceContents(uri=uri_str, text=f"❌ File not found: {filename}")])
        except Exception as e:
            return ReadResourceResult(contents=[TextResourceContents(uri=uri_str, text=f"❌ Error reading file: {str(e)}")])
    
    else:
        return ReadResourceResult(contents=[TextResourceContents(uri=uri_str, text=f"❌ Unknown resource URI: {uri_str}")])


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
    logging.info("🚀 Starting MCP Server with Tools AND Resources...")
    logging.info("🔧 Tools Available:")
    logging.info("   • say_hello - Greet someone")
    logging.info("   • create_sample_data - Create test JSON files")
    logging.info("   • write_note - Write notes to files")
    logging.info("📚 Resources Available:")
    logging.info("   • Current directory listing")
    logging.info("   • Server status information")  
    logging.info("   • Any JSON/TXT files in current directory")
    logging.info("Ready for MCP requests!")
    asyncio.run(main())

    
"""
🆕 NEW CONCEPTS:

1. RESOURCES vs TOOLS:
   - Tools = DO things (write files, send emails, etc.)
   - Resources = PROVIDE DATA (files, databases, status info, etc.)

2. NEW MCP MESSAGE TYPES:
   - ListResourcesRequest/Response (like ListToolsRequest but for data)
   - ReadResourceRequest/Response (like CallToolRequest but for reading data)

3. RESOURCE STRUCTURE:
   - URI: Unique identifier (like file://data.json)
   - Name: Human-readable name
   - Description: What this resource contains
   - MimeType: Type of data (text/plain, application/json, etc.)

4. REAL-WORLD PARALLEL:
   - Tools = Kitchen equipment (can cook food)
   - Resources = Ingredients/Recipe books (provide information)
   - AI can read resources to understand context, then use tools to take action
"""