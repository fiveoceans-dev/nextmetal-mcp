# Dedalus MCP Server

This repository contains the Python-based Dedalus MCP (Multi-Client Protocol) server.
It is designed to manage and facilitate communication between multiple clients using the Dedalus protocol.

## Setup

(Further setup instructions will go here.)

## Usage

(Further usage instructions will go here.)

---

## Testing

There are two primary ways to test and interact with the Dedalus MCP server: directly via a local Python client or through the Dedalus Marketplace using the `DedalusRunner`.

### 1. Testing with Local MCP Server (`client.py`)

This method is for interacting directly with a locally running instance of your MCP server.

**Requirements:**
*   Your local MCP server must be running (`python server.py`).

**How to use:**

1.  **Ensure the MCP Server is running:**
    Open a terminal and start your local server:
    ```bash
    python server.py
    ```
    Keep this terminal open as the server will continue to run.

2.  **Activate your Python virtual environment:**
    Open a *new* terminal and navigate to your project directory. Activate your virtual environment:
    ```bash
    source venv/bin/activate
    ```
    (Replace `venv/bin/activate` with `.\venv\Scripts\activate` on Windows)

3.  **Run the local client script:**
    ```bash
    python client.py
    ```
    This script (`client.py`) connects directly to your local server, lists tools, and demonstrates calls to champion and item information tools. It handles the Server-Sent Events (SSE) responses for clear output.

---

### 2. Testing with Live Dedalus Marketplace Server (`client-live.py`)

This method demonstrates how to interact with your MCP server once it's deployed to the Dedalus Marketplace. It uses the `dedalus_labs.AsyncDedalus` client and `DedalusRunner` for orchestrating interactions, following the best practices for marketplace integrations.

**Requirements:**
*   A Dedalus API Key.
*   The `DEDALUS_AS_URL` environment variable set.
*   Your MCP server must be deployed to the Dedalus Marketplace (e.g., at `https://www.dedaluslabs.ai/marketplace/five/nextmetal-mcp`).

**How to use:**

1.  **Claim your Dedalus API Key** from the Dedalus dashboard.

2.  **Set required environment variables:**
    Create a `.env` file in your project root or set these variables directly in your environment:
    ```
    DEDALUS_API_KEY="your_dedalus_api_key_here"
    DEDALUS_AS_URL="https://as.dedaluslabs.ai" # This is the default Agent Service URL
    ```
    Replace `"your_dedalus_api_key_here"` with your actual API key.

3.  **Activate your Python virtual environment** if you haven't already:
    ```bash
    source venv/bin/activate
    ```
    (On Windows, `.\venv\Scripts\activate`)

4.  **Run the live client script:**
    ```bash
    python client-live.py
    ```
    This script (`client-live.py`) will connect to the specified live marketplace MCP server and interact with its tools via the `DedalusRunner`, using prompts to trigger the tools.

---

### 3. Testing with `curl` (Raw HTTP Interaction)

**Note:** The Dedalus MCP server primarily uses Server-Sent Events (SSE) for its responses. While the `curl` commands below are formatted to send correct JSON-RPC requests, piping their output to `json_pp` will result in "malformed JSON string" errors because `json_pp` cannot parse event streams. Use these commands to inspect raw server responses (by omitting `| json_pp`), or use the Python clients for parsed output.

#### Access API Documentation

The API documentation (Swagger UI) is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

#### List all available tools

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mcp' \
  -H 'accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/list",
    "params": {}
  }' | json_pp
```

#### Get Champion Information

Replace `"Aatrox"` with any champion name (case-insensitive).

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mcp' \
  -H 'accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "get_champion_info",
      "input": {
        "champion_name": "Aatrox"
      }
    }
  }' | json_pp
```

#### Get Item Information

Replace `"Blade of the Ruined King"` with any item name (case-insensitive).

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mcp' \
  -H 'accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "get_item_info",
      "input": {
        "item_name": "Blade of the Ruined King"
      }
    }
  }' | json_pp
```

#### List All Champions

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mcp' \
  -H 'accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "list_all_champions",
      "input": {}
    }
  }' | json_pp
```

#### List All Items

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/mcp' \
  -H 'accept: application/json, text/event-stream' \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": "1",
    "method": "tools/call",
    "params": {
      "name": "list_all_items",
      "input": {}
    }
  }' | json_pp
```