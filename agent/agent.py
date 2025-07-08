from llm_integrations.gemini_client import GetGemini
from llm_integrations.base import APIPlatform
from mcp.types import ListToolsResult
from google.genai import types
from fastmcp import Client
import logger.config
import structlog
import asyncio
import json
import sys

# Workaround for asyncio hanging on event loop close on Windows
COINIT_MULTITHREADED = 0x0
sys.coinit_flags = COINIT_MULTITHREADED

class MCPHost:

    def __init__(self, config_path = "config.json", logging=False):
        try:
            with open(config_path) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise RuntimeError("Config file not found.")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON config file: {e}")
        except OSError as e:
            raise RuntimeError(f"Could not open config file: {e}")

        self.llm: APIPlatform = GetGemini()
        self.client = Client(self.config)
        self.log = structlog.get_logger()
        self.log.info("MCP host initialised")

    
    def log_response(self, response):
        
        if not self.log:
            return

        llm_response = []

        for part in response.parts:
            llm_response.append({
                "text": part.text,
                "function_call": part.function_call.model_dump_json() if part.function_call else None,
            })

        self.log.info(
            "llm_call",
            call_count=self.call_count,
            llm_response=llm_response,
        )

        self.call_count += 1

    
    def count_function_calls(self, response: types.Content):
        count = 0

        for part in response.parts:
            if part.function_call:
                count += 1

        return count


    async def process_query(self, query: str) -> str:
        """Process a query using an LLM and available tools"""

        self.call_count = 0

        output: list[str] = []
        messages: list[types.Content] = [
            types.Content(
                role="user",
                parts=[
                    types.Part(text=query)],
            )
        ]

        async with self.client:
            tools: ListToolsResult = await self.client.list_tools()        

        # Initial LLM call (tool selection call)
        response: types.Content = self.llm.chat(messages, tools)
        self.log_response(response)
        messages.append(response)

        # Finish condition: No function calls
        while(self.count_function_calls(response) != 0):
            for part in response.parts:
                if part.text:
                    output.append(part.text)

                elif part.function_call:
                    tool_call = part.function_call
                    tool_result = None

                    output.append(f"[Calling tool {tool_call.name} with args {tool_call.args}]")

                    async with self.client:
                        tool_result = await self.client.call_tool(
                            tool_call.name,
                            tool_call.args,
                        )

                    # Append the function response
                    function_result = types.Part.from_function_response(
                        name=tool_call.name,
                        response={"result": tool_result},
                    )
                    messages.append(types.Content(role="user", parts=[function_result]))

            # Secondary LLM call (process tool result)
            response: types.Content = self.llm.chat(messages, tools)
            self.log_response(response)
            messages.append(response)

        for part in response.parts:
            if part.text:
                output.append(part.text)

        return "\n\n".join(output)


    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                elif query != "":
                    response = await self.process_query(query)
                    print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")


async def main():
    host = None

    try:
        host = MCPHost("agent/mcp_configs/config.json", logging=True)
    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    await host.chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
