# AI_recipe_generator/app/schemas/recipe_schema.py

from pydantic import BaseModel
from typing import List

class RecipeRequest(BaseModel):
    ingredients: List[str] | None = None
    description: str | None = None