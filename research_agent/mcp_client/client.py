import asyncio
from fastmcp import Client
import sys
import os

# Add the parent directory to the path to import the server
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'mcp_server'))

# Use subprocess transport to run the server
client = Client([
    sys.executable, 
    os.path.join(os.path.dirname(__file__), '..', 'mcp_server', 'server.py')
])

async def call_greet(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)
        
async def call_db(var: str):
    async with client:
        result = await client.call_resource("getParam", {"var": var})
        print(result)

asyncio.run(call_greet("Ford"))
asyncio.run(call_db("users"))
