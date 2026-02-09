import asyncio
import os
from dedalus_labs import AsyncDedalus, DedalusRunner
from dedalus_mcp.auth import Connection, SecretKeys, SecretValues
from dotenv import load_dotenv

# Load environment variables from .env file (DEDALUS_API_KEY, DEDALUS_AS_URL, etc.)
load_dotenv()

# --- Connection Definition (Following the X/Twitter README example format) ---
# For our LoL MCP server, we are not connecting to an external API that requires
# credentials from the client's perspective.
# However, if this MCP server *itself* needed external credentials (e.g., to an external
# LoL API beyond DDragon), you would define them here.
# This section is included to follow the requested README format for client-side credentials,
# but `lol_mcp_secrets` will be empty as our tools don't require client-supplied secrets.

# Define a dummy connection for our MCP server if the runner expects one for marketplace entry
# The name should ideally match a connection name expected by the server or marketplace.
# Since our MCP doesn't expose external credentials, this is mostly for structure if needed.
# For now, we will omit actual secrets as our server doesn't require them from client.

# For direct use with runner.run, we provide the MCP server slug directly.
# The credentials passed to runner.run are typically for *external APIs* that the *MCP server itself*
# uses, or for credentials *required by the marketplace*.

async def main():
    # DEDALUS_API_KEY and DEDALUS_AS_URL should be set in your .env file or environment
    client = AsyncDedalus()
    runner = DedalusRunner(client)

    mcp_slug = "five/nextmetal-mcp" # From the marketplace URL provided by the user
    model_name = "anthropic/claude-sonnet-4-20250514" # Example model from user's sample README

    print(f"Connecting to live MCP server via DedalusRunner with slug: {mcp_slug}")
    print(f"Using model: {model_name}")

    try:
        # Test case 1: List champions
        print("\n--- Listing all League of Legends champions via runner ---")
        response_list_champions = await runner.run(
            input="List all League of Legends champions.",
            model=model_name,
            mcp_servers=[mcp_slug],
            # No `credentials` needed here as our LoL MCP server's tools
            # don't require client-supplied external API keys.
        )
        print(f"Runner Response (List Champions):\n{response_list_champions.final_output}\n")

        # Test case 2: Get Champion Information for Aatrox
        print("\n--- Getting Champion Information for Aatrox via runner ---")
        response_aatrox = await runner.run(
            input="Tell me about the League of Legends champion Aatrox.",
            model=model_name,
            mcp_servers=[mcp_slug],
        )
        print(f"Runner Response (Aatrox Info):\n{response_aatrox.final_output}\n")

        # Test case 3: Get Item Information for Blade of the Ruined King
        print("\n--- Getting Item Information for Blade of the Ruined King via runner ---")
        response_item = await runner.run(
            input="What is the item 'Blade of the Ruined King' in League of Legends?",
            model=model_name,
            mcp_servers=[mcp_slug],
        )
        print(f"Runner Response (Item Info):\n{response_item.final_output}\n")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())