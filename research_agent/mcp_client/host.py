import asyncio
import json
from fastmcp import Client
from shared.llm_integrations.gemini_client import GetGemini
from shared.llm_integrations.base import APIPlatform

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

        async with self.client:
            tools = await self.client.list_tools()

        print(tools)
        return

        # Initial LLM call (tool selection call)
        response = self.llm.chat(query, tools)
        return

        # Process response and handle tool calls
        tool_results = []
        final_text = []

        for content in response.content:
            if content.type == 'text':
                final_text.append(content.text)

            elif content.type == 'tool_use':
                tool_name = content.name
                tool_args = content.input
                
                # TODO: Find which client has tool (handle no tool)
                client = self.clients[0]

                # Execute tool call
                result = await client.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                final_text.append(f"[Calling tool {tool_name} with args {tool_args}]")

                # Continue conversation with tool results
                if hasattr(content, 'text') and content.text:
                    messages.append({
                      "role": "assistant",
                      "content": content.text
                    })
                messages.append({
                    "role": "user", 
                    "content": result.content
                })

                # Secondary LLM call (tool result processing call)
                response = self.llm.chat(
                    messages=messages,
                )

                final_text.append(response.content[0].text)

        return "\n".join(final_text)
    

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
