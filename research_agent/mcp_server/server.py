from fastmcp import FastMCP

# Create a server instance
mcp = FastMCP(name="MyAssistantServer")

@mcp.tool
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}"

if __name__ == "__main__":
    mcp.run()