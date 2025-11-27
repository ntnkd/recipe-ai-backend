# AI_recipe_generator/app/main.py

from fastapi import FastAPI
from app.routes.recipe_routes import router as recipe_router
from app.routes.vision_routes import router as vision_router
from app.routes.tet import router as tet_app

app = FastAPI(title="AI Recipe Generator API")


app.include_router(recipe_router, prefix="/api", tags=["recipes"])
app.include_router(vision_router, prefix="/api", tags=["vision"])
app.include_router(tet_app, prefix="/api", tags=["test"])

@app.get("/")
def root():
    return {"message": "Welcome to AI Recipe Generator API"}
