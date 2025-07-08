# Agentic Research

A proof of concept and research inquiry into the state and usefulness of agentic systems.

## System Structure

<img width=80% alt="System Diagram" src="https://github.com/user-attachments/assets/e3b20155-4316-4ce7-9cac-31efbe6b564b" />

## Repository Structure

```
.
├── agent/ 
│   ├── llm_integrations/
│   │   ├── base.py             # Defines LLM base class
│   │   ├── gemini_client.py    # Establishes Gemini client
│   │   ├── gemini.py           # Implements base LLM class virtual functions
│   │   └── models.py           # Defines Pydantic LLM input-output objects
│   ├── logger/
│   │   └── config.py           # Configured logger behaviour
│   ├── mcp_configs/            # MCP configuration files (Claude structure)
│   ├── prompts/                # System prompts for agents
│   ├── agent.py                # Defines agent class
│   └── client.py               # Instantiates agent client
│
├── server/
│   ├── mongodb/
│   │   └── mongo_client.py     # Establishes MongoDB client
│   └── server.py               # Runs MCP server and defines tools and resources
│
├── .env                        # Environment variables (manually created)
├── .gitignore                  # Files and directories to ignore
├── LICENSE                     # Open source license (MIT)
├── README.md                   # Project overview and setup instructions
└── requirements.txt            # Python dependencies
```

## Instructions

### Setup Project

1. Clone repository into Python virtual environment
2. Activate virtual environment with `source bin/activate` on Unix or `.\Scripts\activate` on Windows
3. Install dependencies with `pip install -r requirements.txt`
4. Create the file `.../agent/mcp_configs/config.json` populate with completed template:
    ```json
    {
        "mcpServers": {
            "local_server": {
                "command": "uv",
                "args": [
                    "--directory",
                    "C:\\Users\\[username]\\[path]\\[to]\\[venv]\\[repo]\\server",
                    "run",
                    "server.py"
                ]
            }
        }
    }
    ```
5. Create and populate `.env` and define `MONGODB_USER`, `MONGODB_PWD`, `MONGODB_CLUSTER`, `GEMINI_API_KEY`

### Running Project

Run MCP server with `mcp dev .../server/server.py`

Run MCP client with `uv run .../agent/client.py`

- **Note:** you may need to add current directory to Python path with `export PYTHONPATH=.` on Unix or `$env:PYTHONPATH="."` on Windows

## Resources

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
