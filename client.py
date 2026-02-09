import asyncio
from dedalus_mcp.client import MCPClient
import json

MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

async def main():
    print(f"Connecting to MCP server at {MCP_SERVER_URL}...")
    client = await MCPClient.connect(MCP_SERVER_URL)
    print("Connected.")

    # 1. List all available tools
    print("""
--- Listing all available tools ---""")
    try:
        tools_response = await client.list_tools()
        print("Available tools:")
        for tool_meta in tools_response.tools:
            print(f"- {tool_meta.name}: {tool_meta.description}")
    except Exception as e:
        print(f"Error listing tools: {e}")

    # 2. Get Champion Information
    print("""
--- Getting Champion Information for Aatrox ---""")
    try:
        champion_info_response = await client.call_tool("get_champion_info", {"champion_name": "Aatrox"})
        print("Aatrox Info:")
        # The response from call_tool is a stream of content parts
        full_content = "".join(part.text for part in champion_info_response.content if hasattr(part, 'text'))
        print(full_content)
    except Exception as e:
        print(f"Error getting champion info: {e}")

    # 3. Get Item Information
    print("""
--- Getting Item Information for Blade of the Ruined King ---""")
    try:
        item_info_response = await client.call_tool("get_item_info", {"item_name": "Blade of the Ruined King"})
        print("Blade of the Ruined King Info:")
        full_content = "".join(part.text for part in item_info_response.content if hasattr(part, 'text'))
        print(full_content)
    except Exception as e:
        print(f"Error getting item info: {e}")

    # 4. List All Champions (demonstrating iteration for potentially large results)
    print("""
--- Listing all champions (first 5) ---""")
    try:
        all_champions_response = await client.call_tool("list_all_champions", {})
        champion_list = []
        for part in all_champions_response.content:
            if hasattr(part, 'text'):
                # Assuming the list comes as a JSON string within the text part
                # This might need adjustment based on how the server streams the list
                champion_list.append(part.text)
        print(f"Total champions: {len(champion_list)}")
        print("First 5 champions:", champion_list[:5])
    except Exception as e:
        print(f"Error listing champions: {e}")

    await client.close()
    print("""
Client disconnected.""")

if __name__ == "__main__":
    asyncio.run(main())
