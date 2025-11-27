# AI_recipe_generator/app/utils/formatters.py


#Loại bỏ Markdown (```json ... ```) nếu có
def clean_json_text(text: str) -> str:
    
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        cleaned = cleaned.split("json", 1)[-1].strip()
        cleaned = cleaned.strip().lstrip("\n").rstrip("`").strip()
    return cleaned
