import os
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv
from prompts import PROMPT_JUNIOR_ENGINEER, PROMPT_HEAD_ENGINEER

# Load API keys from .env file
load_dotenv()

# --- Client Configuration ---

# 1. Standard OpenAI Client
openai_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# 2. DeepInfra Client (for Kimi) - It uses the OpenAI library structure
deepinfra_client = OpenAI(
    api_key=os.getenv("DEEPINFRA_API_KEY"),
    base_url="https://api.deepinfra.com/v1/openai", # This is the key change
)

# 3. Gemini Client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel('gemini-2.5-pro') #gemini-2.5-pro #gemini-1.5-pro-latest


# --- Agent Functions ---

def get_openai_report(report_data: str) -> str:
    """Generates an HVAC report using the OpenAI API."""
    try:
        prompt = PROMPT_JUNIOR_ENGINEER.format(report_data=report_data)
        response = openai_client.chat.completions.create(
            
            # model="gpt-3.5-turbo-0125",
            model="o3-2025-04-16",

            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {e}"

def get_kimi_report(report_data: str) -> str:
    """Generates an HVAC report using the Kimi model via DeepInfra."""
    try:
        prompt = PROMPT_JUNIOR_ENGINEER.format(report_data=report_data)
        response = deepinfra_client.chat.completions.create(
            # Specify the Kimi model name from DeepInfra
            
          
            # model="google/gemma-3-4b-it",
            model="moonshotai/Kimi-K2-Instruct",

            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling DeepInfra (Kimi) API: {e}"

def get_gemini_final_report(report_data: str, report_1: str, report_2: str) -> str:
    """Generates the final, verified report using the Gemini API."""
    try:
        prompt = PROMPT_HEAD_ENGINEER.format(
            report_data=report_data,
            report_1=report_1,
            report_2=report_2
        )
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error calling Gemini API: {e}"