from agent import Agent
import asyncio
import sys

# Workaround for asyncio hanging on event loop close on Windows
COINIT_MULTITHREADED = 0x0
sys.coinit_flags = COINIT_MULTITHREADED


async def chat_loop(host):
    print("\nMCP Client Started!")
    print("Type your queries or 'quit' to exit.")
    
    while True:
        try:
            query = input("\nQuery: ").strip()
            
            if query.lower() == 'quit':
                break
            elif query != "":
                response = await host.process_query(query)
                print("\n" + response)
                
        except Exception as e:
            print(f"\nError: {str(e)}")


async def main():
    host = None

    try:
        host = Agent("agent/mcp_configs/config.json", logging=True)
    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    await chat_loop(host)


if __name__ == "__main__":
    asyncio.run(main())
