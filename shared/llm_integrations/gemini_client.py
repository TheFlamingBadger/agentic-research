import os
from dotenv import load_dotenv, find_dotenv
from shared.llm_integrations.gemini import Gemini
from shared.prompts.agent_prompt import prompt

load_dotenv(find_dotenv())

# system_prompt = prompt
system_prompt = None
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

def GetGemini():
    return Gemini(api_key=gemini_api_key, system_prompt=system_prompt)