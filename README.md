# Dedalus MCP Server

This repository contains the Python-based Dedalus MCP (Multi-Client Protocol) server.
It is designed to manage and facilitate communication between multiple clients using the Dedalus protocol.

## Setup

(Further setup instructions will go here.)

## Usage

(Further usage instructions will go here.)

## Test the MCP Server

Once the server is running (using `python server.py`), you can test it using `curl` commands in a new terminal.

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