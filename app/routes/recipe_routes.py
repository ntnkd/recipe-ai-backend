# AI_recipe_generator/app/routes/recipe_routes.py

from fastapi import APIRouter, HTTPException
from app.schemas.recipe_schema import RecipeRequest
from app.ai.generator import generate_recipe, generate_recipe_from_description

router = APIRouter()

@router.post("/generate-recipe")
def generate_recipe_api(request: RecipeRequest):
    try:
        if request.ingredients:
            return {
                "mode": "ingredients",
                "recipe": generate_recipe(request.ingredients)
            }

        if request.description:
            return {
                "mode": "description",
                "recipe": generate_recipe_from_description(request.description)
            }

        raise HTTPException(400, "Bạn phải gửi 'ingredients' hoặc 'description'")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))