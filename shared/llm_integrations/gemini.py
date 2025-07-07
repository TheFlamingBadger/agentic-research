from .base import APIPlatform
from google import genai
from google.genai.types import Content
from mcp.types import Tool

class Gemini(APIPlatform):
    """Gemini AI platform for generating text responses.

    Args:
        APIPlatform (Class): Base schema for AI platforms.
    """
    def __init__(self, api_key: str, system_prompt: str = None):
        super().__init__()
        self.api_key = api_key
        self.system_prompt = system_prompt

    def chat(self, messages: list[Content], toolsObj: list[Tool]) -> Content:
        # if self.system_prompt:
        #     prompt = f"{self.system_prompt}\n{prompt}"

        client = genai.Client()
        config = genai.types.GenerateContentConfig(tools=toolsObj)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )

        return response.candidates[0].content
        # return [part.content for part in response.candidates[0].content.parts]
