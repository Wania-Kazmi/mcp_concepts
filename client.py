
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

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_practical_tools():
    print("🧪 Testing Practical MCP Tools")
    print("=" * 40)
    
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"]  # Use our enhanced server
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Test 1: List all available tools
            print("\\n1️⃣ Discovering available tools...")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"   📋 {tool.name}: {tool.description}")
            
            # Test 2: Create a simple file
            print("\\n2️⃣ Creating a test file...")
            result = await session.call_tool("write_file", {
                "filename": "test.txt",
                "content": "Hello from MCP!\\nThis file was created by an MCP tool."
            })
            print(f"   {result.content[0].text}")
            
            # Test 3: Read the file back
            print("\\n3️⃣ Reading the file back...")
            result = await session.call_tool("read_file", {"filename": "test.txt"})
            print(f"   {result.content[0].text}")
            
            # Test 4: List current directory
            print("\\n4️⃣ Listing current directory...")
            result = await session.call_tool("list_directory", {"path": "."})
            print(f"   {result.content[0].text}")
            
            # Test 5: Create a report
            print("\\n5️⃣ Generating a report...")
            result = await session.call_tool("create_report", {"title": "MCP Demo Report"})
            print(f"   {result.content[0].text}")
            
            print("\\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(test_practical_tools())

