# Agentic Research

<img width="888" alt="Screenshot 2025-07-03 at 4 47 48 pm" src="https://github.com/user-attachments/assets/ea132ab1-884f-4fd7-b7d6-45dcdfb153e3" />

# Links

- [MCP Architecture](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [MCP Schema](https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/schema/2025-06-18/schema.ts)
- [Public MCP Servers & Clients](https://www.pulsemcp.com/)
- [Gemini Function Calling](https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#python_4)
- [Gemini Tool Use](https://ai.google.dev/gemini-api/docs/live-tools?hl=en)

### Specifications

- [MCP Spec](https://modelcontextprotocol.io/specification/2025-06-18/)
- [JSON-RPC Spec](https://www.jsonrpc.org/specification)

### Frameworks

- [FastMCP Framework](https://gofastmcp.com/)

### Mukti-Agent SDKs

- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/)
- [Microsoft Autogen](https://github.com/microsoft/autogen)
- [LangGraph](https://www.langchain.com/langgraph)

# Instructions

## Setup Project

1. Clone repository into Python virtual environment
2. Activate virtual environment with `source bin/activate` on Unix or `.\Scripts\activate` on Windows
3. Install dependencies with `pip install -r requirements.txt`
4. Create the file `.../research_agent/mcp_client/config.json` populate with completed template:
    ```json
    {
        "mcpServers": {
            "local_server": {
                "command": "uv",
                "args": [
                    "--directory",
                    "C:\\Users\\[username]\\[path]\\[to]\\[venv]\\[repo]\\research_agent\\mcp_server",
                    "run",
                    "server.py"
                ]
            }
        }
    }
    ```
5. Create and populate `.env` and define `MONGODB_USER`, `MONGODB_PWD`, `MONGODB_CLUSTER`, `GEMINI_API_KEY`

## Running Project

Run MCP server with `mcp dev .../research_agent/mcp_server/server.py`

Run MCP client with `uv run .../research/agent/mcp_client/host.py`

- **Note:** you may need to add current directory to Python path with `export PYTHONPATH=.` on Unix or `$env:PYTHONPATH="."` on Windows
