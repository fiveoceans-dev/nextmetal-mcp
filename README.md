# Dedalus MCP Server

This repository contains the Python-based Dedalus MCP (Multi-Client Protocol) server.
It is designed to manage and facilitate communication between multiple clients using the Dedalus protocol.

## Setup

(Further setup instructions will go here.)

## Usage

(Further usage instructions will go here.)

## Testing with Python Client (Recommended)

The Dedalus MCP server communicates using Server-Sent Events (SSE), especially when streaming capabilities are enabled. For a robust and programmatic way to interact with the server and parse its streamed responses, it is recommended to use the provided `client.py` script. This script utilizes the `dedalus_mcp.client` library, which is designed to handle SSE and abstract the underlying JSON-RPC details.

To use the client:

1.  **Ensure the MCP Server is running:**
    Open a terminal and start the server:
    ```bash
    python server.py
    ```
    Keep this terminal open as the server will continue to run.

2.  **Activate your Python virtual environment:**
    Open a *new* terminal and activate your virtual environment:
    ```bash
    source venv/bin/activate
    ```
    (Replace `venv/bin/activate` with `.\venv\Scripts\activate` on Windows)

3.  **Run the client script:**
    ```bash
    python client.py
    ```
    This script will connect to the server, list tools, and demonstrate calls to champion and item information tools.

## Testing with `curl` (Raw HTTP Interaction)

**Note:** The Dedalus MCP server primarily uses Server-Sent Events (SSE) for its responses. While the `curl` commands below are formatted to send correct JSON-RPC requests, piping their output to `json_pp` will result in "malformed JSON string" errors because `json_pp` cannot parse event streams. Use these commands to inspect raw server responses, or use `client.py` for parsed output.

### Access API Documentation

The API documentation (Swagger UI) is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### List all available tools

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

### Get Champion Information

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

### Get Item Information

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

### List All Champions

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

### List All Items

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