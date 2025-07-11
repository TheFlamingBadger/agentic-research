from .base import APIPlatform
from google import genai
from google.genai import types
from mcp.types import Tool
import time

class Gemini(APIPlatform):
    """Gemini AI platform for generating text responses.

    Args:
        APIPlatform (Class): Base schema for AI platforms.
    """
    def __init__(self, api_key: str, system_prompt: str = None):
        super().__init__()
        self.api_key = api_key
        self.system_prompt = system_prompt
        self.last_prompt_time = 0

    def chat(self, messages: list[types.Content], toolsObj: list[Tool]) -> types.Content:
        # Sleep until 1 second has elapsed since last chat
        time.sleep(max(0, 1 - (time.time() - self.last_prompt_time)))

        if self.system_prompt:
            messages.insert(0, types.Content(
                role="user",
                parts=[
                    types.Part(text=self.system_prompt)],
            ))

        client = genai.Client()
        config = genai.types.GenerateContentConfig(tools=toolsObj)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )

        self.last_prompt_time = time.time()
        return response.candidates[0].content
