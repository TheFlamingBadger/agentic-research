import os
from dotenv import load_dotenv, find_dotenv
from shared.llm_integrations.gemini import Gemini

load_dotenv(find_dotenv())

# AI agent config
def load_system_prompt():
    try:
        with open("src/prompts/system_prompt.md", "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

system_prompt = load_system_prompt()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

def GetGemini():
    return Gemini(api_key=gemini_api_key, system_prompt=system_prompt)