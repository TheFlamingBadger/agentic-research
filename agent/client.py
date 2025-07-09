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
    prompt_path = None
    config_path = "agent/mcp_configs/config.json"

    if len(sys.argv) > 1:
        config_path = f"agent/mcp_configs/{sys.argv[1]}.json"

    if len(sys.argv) > 2:
        prompt_path = f"agent/prompts/{sys.argv[2]}.md"
    
    print(config_path, prompt_path)

    try:
        host = Agent(
            config_path=config_path,
            prompt_path=prompt_path,
            logging=True,
        )
    except Exception as e:
        print(f"Failed to load config: {e}")
        return

    await chat_loop(host)


if __name__ == "__main__":
    asyncio.run(main())
