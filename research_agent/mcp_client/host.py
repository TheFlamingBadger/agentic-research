import asyncio
import json
from fastmcp import Client
from shared.llm_integrations.gemini_client import GetGemini
from shared.llm_integrations.base import APIPlatform
from mcp.types import ListToolsResult, PromptMessage
from google.genai import types

class MCPHost:

    def __init__(self, config_path = "config.json"):
        self.llm: APIPlatform = GetGemini()

        try:
            with open(config_path) as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise RuntimeError("Config file not found.")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON config file: {e}")
        except OSError as e:
            raise RuntimeError(f"Could not open config file: {e}")

        self.client = Client(self.config)


    async def process_query(self, query: str) -> str:
        """Process a query using an LLM and available tools"""

        output = []
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
        messages.append(response) # Append the content from the model's response.

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

        # If there's a function result to process, make secondary LLM call
        response: types.Content = self.llm.chat(messages, tools)

        if response.parts[0].text:
            output.append(response.parts[0].text)
        
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
                    
                response = await self.process_query(query)
                print("\n" + response)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")


async def main():
    host = None

    try:
        host = MCPHost("research_agent/mcp_client/config.json")
    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    await host.chat_loop()


if __name__ == "__main__":
    asyncio.run(main())
