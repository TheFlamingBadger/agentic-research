from .base import APIPlatform
from google import genai
from google.genai import types
import mcp.types

class Gemini(APIPlatform):
    """Gemini AI platform for generating text responses.

    Args:
        APIPlatform (Class): Base schema for AI platforms.
    """
    def __init__(self, api_key: str, system_prompt: str = None):
        super().__init__()
        self.api_key = api_key
        self.system_prompt = system_prompt

    def formatTools(self, tools: list[mcp.types.Tool]) -> types.Tool:
        
        formatted_tools = [{ 
            "name": tool.name,
            "description": tool.description,
            "parameters": {
                "type": "object",
                "properties": {
                    param: {
                        "type": details["type"],
                        "description": details["title"]
                 } for param, details in tool.inputSchema["properties"].items()
                },
                "required": tool.inputSchema["required"],
            },
        } for tool in tools]

        try:
            return genai.types.Tool(function_declarations=formatted_tools)
        except Exception as e:
            print(f"Failed to convert into Gemini tool object: {e}")
    
    def chat(self, prompt: str, toolsObj: list[mcp.types.Tool]) -> str:
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n{prompt}"

        client = genai.Client()
        config = genai.types.GenerateContentConfig(tools=self.formatTools(toolsObj))

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=config,
        )
        
        print(response)
        return response