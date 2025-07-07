import os
from dotenv import load_dotenv, find_dotenv
from shared.llm_integrations.gemini import Gemini
from shared.prompts.agent_prompt import prompt

load_dotenv(find_dotenv())

# # AI agent config
# def load_system_prompt():
#     try:
#         with open("../prompts/agent_prompt.md", "r") as f:
#             return f.read()
#     except FileNotFoundError:
#         print("you suck")

system_prompt = prompt
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

def GetGemini():
    return Gemini(api_key=gemini_api_key, system_prompt=system_prompt)