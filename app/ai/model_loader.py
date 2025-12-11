# AI_recipe_generator/app/ai/model_loader.py

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()



def get_genai_model():
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-live")

    genai.configure(api_key=api_key)

    return genai, model_name