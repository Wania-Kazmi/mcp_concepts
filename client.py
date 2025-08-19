
# ============================================================================
# client.py - Simple Client that Talks to Our Server
# ============================================================================

import asyncio
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_basic_client():
    """
    This demonstrates the exact flow from our diagram:
    User -> Our Server -> MCP Client -> MCP Server -> Response back
    """
    
    print("🤖 Starting Basic MCP Client Demo")
    print("=" * 50)
    
    # Step 1: Connect to our server (like calling the food truck)
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["server.py"],
    )
    
    # Step 2: Start the conversation
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Step 3: Initialize (like introducing yourself to the food truck)
            print("🔗 Connecting to server...")
            await session.initialize()
            print("✅ Connected!")
            
            # Step 4: Ask "What's on your menu?" (ListToolsRequest from diagram)
            print("\n📋 Asking server: 'What tools do you have?'")
            tools_response = await session.list_tools()
            
            print(f"📝 Server has {len(tools_response.tools)} tools:")
            for tool in tools_response.tools:
                print(f"   • {tool.name}: {tool.description}")
            
            # Step 5: Order something! (CallToolRequest from diagram)
            print("\n🛠️ Using the 'say_hello' tool...")
            result = await session.call_tool("say_hello", {"name": "Alice"})
            
            print("💬 Server response:")
            for content in result.content:
                print(f"   '{content.text}'")
            
            # Step 6: Try the other tool
            print("\n⏰ Using the 'get_time' tool...")
            time_result = await session.call_tool("get_time", {})
            
            print("🕐 Time response:")
            for content in time_result.content:
                print(f"   '{content.text}'")
            
            print("\n🎉 Demo complete! You just saw MCP in action!")

if __name__ == "__main__":
    asyncio.run(run_basic_client())