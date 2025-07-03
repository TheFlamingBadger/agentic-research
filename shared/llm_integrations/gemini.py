from .base import APIPlatform
import google.generativeai as genai

class Gemini(APIPlatform):
    """Gemini AI platform for generating text responses.

    Args:
        APIPlatform (Class): Base schema for AI platforms.
    """
    def __init__(self, api_key: str, system_prompt: str = None):
        super().__init__()
        self.api_key = api_key
        self.system_prompt = system_prompt
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
    
    def chat(self, prompt: str) -> str:
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n{prompt}"
        
        chat = self.model.start_chat()
        response = chat.send_message(prompt)
        print(f"Response: {response}")
        
        return response.text