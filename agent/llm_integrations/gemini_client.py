import os
from dotenv import load_dotenv, find_dotenv
from llm_integrations.gemini import Gemini

load_dotenv(find_dotenv())

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

def GetGemini(prompt_path = None):
    system_prompt = None

    try:
        system_prompt = open(prompt_path, "r", encoding="utf-8").read()
        print("System prompt successfully loaded:\n", system_prompt)
    except Exception as e:
        print("System prompt load failed. Error:", e)

    return Gemini(api_key=gemini_api_key, system_prompt=system_prompt)