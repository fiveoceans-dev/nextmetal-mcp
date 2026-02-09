import json
from pathlib import Path
from dedalus_mcp import MCPServer, tool
import sys
import uvicorn
import asyncio

# --- Data Loading ---
def load_json_data(path: Path):
    """Loads JSON data from a file, exiting if not found."""
    if not path.exists():
        print(f"Error: Required data file not found at '{path}'.", file=sys.stderr)
        print("Please run 'python download_lol_data.py' first.", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing data from '{path}': {e}", file=sys.stderr)
        sys.exit(1)

DATA_DIR = Path("data")
CHAMPION_METADATA_PATH = DATA_DIR / "champions" / "champion_metadata.json"
ITEM_METADATA_PATH = DATA_DIR / "items" / "item_metadata.json"

print("Loading League of Legends data...")
champion_metadata = load_json_data(CHAMPION_METADATA_PATH)
item_metadata = load_json_data(ITEM_METADATA_PATH)
champion_data = champion_metadata.get('data', {})
item_data = item_metadata.get('data', {})
print("Data loaded successfully.")

# --- Tool Definitions ---
@tool(
    name="get_champion_info",
    description="Gets the title and blurb for a given League of Legends champion by their name or ID (e.g., 'Aatrox', 'MissFortune').",
)
def get_champion_info(champion_name: str) -> str:
    """
    Gets the title and a brief summary (blurb) for a given League of Legends champion.
    """
    champion_name_lower = champion_name.lower()
    for champ_details in champion_data.values():
        if champ_details['name'].lower() == champion_name_lower or champ_details['id'].lower() == champion_name_lower:
            return f"""Champion: {champ_details['name']}
Title: {champ_details['title']}
Blurb: {champ_details['blurb']}"""
    return f"Champion '{champion_name}' not found."

@tool(
    name="get_item_info",
    description="Gets the plaintext description for a given League of Legends item by its name (e.g., 'Blade of The Ruined King').",
)
def get_item_info(item_name: str) -> str:
    """
    Gets the plaintext description for a given League of Legends item.
    """
    item_name_lower = item_name.lower()
    for item_details in item_data.values():
        if item_details['name'].lower() == item_name_lower:
            # Use .get() for safer access to 'plaintext' and 'description'
            description = item_details.get('plaintext')
            if not description:
                # Fallback to the full description if plaintext is missing
                description = item_details.get('description', 'No description available.')
            return f"""Item: {item_details['name']}
Description: {description}"""
    return f"Item '{item_name}' not found."

@tool(
    name="list_all_champions",
    description="Lists the names of all available League of Legends champions.",
)
def list_all_champions() -> list[str]:
    """Lists the names of all available League of Legends champions."""
    if not champion_data:
        return ["Champion data is not loaded or is empty."]
    return sorted([champ['name'] for champ in champion_data.values()])

@tool(
    name="list_all_items",
    description="Lists the names of all available League of Legends items.",
)
def list_all_items() -> list[str]:
    """Lists the names of all available League of Legends items."""
    if not item_data:
        return ["Item data is not loaded or is empty."]
    # Filter out items that don't have a name
    return sorted([item['name'] for item in item_data.values() if 'name' in item])

# --- Server Configuration ---
server = MCPServer("LoL_Data_Server")
server.collect(get_champion_info, get_item_info, list_all_champions, list_all_items)

if __name__ == "__main__":
    print("Starting Dedalus MCP server...")
    print("Access the API at http://127.0.0.1:8000")
    print("API documentation (Swagger UI) is available at http://127.0.0.1:8000/docs")
    asyncio.run(server.serve())
