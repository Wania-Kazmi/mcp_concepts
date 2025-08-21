
# ============================================================================
# client.py - Simple Client that Talks to Our Server
# ========================================================================

"""
🎯 Key Improvements:

1. REAL FILE OPERATIONS:
   - read_file: Actually reads files from your computer
   - write_file: Creates/modifies files on your computer
   - list_directory: Shows folder contents

2. PRACTICAL TOOLS:
   - create_report: Generates useful reports with current info
   - Error handling: Proper error messages when things go wrong

3. SAME MCP PATTERN:
   - Still uses ListToolsRequest/Response
   - Still uses CallToolRequest/Response
   - Just the tools do more interesting things!

4. REAL WORLD READY:
   - These tools could be used by AI assistants
   - File operations are fundamental for many applications
   - Shows how MCP scales from simple to complex
"""

# import asyncio
# import sys
# from mcp import ClientSession, StdioServerParameters
# from mcp.client.stdio import stdio_client

# async def test_practical_tools():
#     print("🧪 Testing Practical MCP Tools")
#     print("=" * 40)
    
#     server_params = StdioServerParameters(
#         command=sys.executable,
#         args=["server.py"]  # Use our enhanced server
#     )
    
#     async with stdio_client(server_params) as (read, write):
#         async with ClientSession(read, write) as session:
#             await session.initialize()
            
#             # Test 1: List all available tools
#             print("\\n1️⃣ Discovering available tools...")
#             tools = await session.list_tools()
#             for tool in tools.tools:
#                 print(f"   📋 {tool.name}: {tool.description}")
            
#             # Test 2: Create a simple file
#             print("\\n2️⃣ Creating a test file...")
#             result = await session.call_tool("write_file", {
#                 "filename": "test.txt",
#                 "content": "Hello from MCP!\\nThis file was created by an MCP tool."
#             })
#             print(f"   {result.content[0].text}")
            
#             # Test 3: Read the file back
#             print("\\n3️⃣ Reading the file back...")
#             result = await session.call_tool("read_file", {"filename": "test.txt"})
#             print(f"   {result.content[0].text}")
            
#             # Test 4: List current directory
#             print("\\n4️⃣ Listing current directory...")
#             result = await session.call_tool("list_directory", {"path": "."})
#             print(f"   {result.content[0].text}")
            
#             # Test 5: Create a report
#             print("\\n5️⃣ Generating a report...")
#             result = await session.call_tool("create_report", {"title": "MCP Demo Report"})
#             print(f"   {result.content[0].text}")
            
#             print("\\n🎉 All tests completed!")

# if __name__ == "__main__":
#     asyncio.run(test_practical_tools())

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_tools_and_resources():
    print("🧪 Testing MCP Server with Tools AND Resources")
    print("=" * 50)
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 1: List available tools
            print("\\n🔧 TOOLS AVAILABLE:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"   • {tool.name}: {tool.description}")
            
            # Test 2: List available resources  
            print("\\n📚 RESOURCES AVAILABLE:")
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"   • {resource.name} ({resource.uri})")
                print(f"     {resource.description}")
            
            # Test 3: Create some sample data (using TOOL)
            print("\\n🔧 Creating sample data...")
            result = await session.call_tool("create_sample_data", {"filename": "users"})
            print(f"   {result.content[0].text}")
            
            # Test 4: Read server status (using RESOURCE)
            print("\\n📖 Reading server status resource...")
            result = await session.read_resource("server://status")
            print(f"   {result.contents[0].text}")
            
            # Test 5: Read the JSON file we created (using RESOURCE)
            print("\\n📖 Reading JSON file resource...")
            result = await session.read_resource("file://users.json")
            print(f"   First 200 characters: {result.contents[0].text[:200]}...")
            
            print("\\n🎉 Demonstrated both Tools AND Resources!")

if __name__ == "__main__":
    asyncio.run(test_tools_and_resources())