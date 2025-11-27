# AI_recipe_generator/app/ai/model_loader.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# def get_genai_model():
    
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         raise ValueError("Missing GEMINI_API_KEY in .env")
    
#     genai.configure(api_key=api_key)
#     model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
#     return genai, model_name


def get_genai_model():
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    genai.configure(api_key=api_key)

    return genai, model_name