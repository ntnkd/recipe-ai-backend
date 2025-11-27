# app/routes/vision_routes.py   

import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
from app.ai.vision import extract_ingredients_from_image
from app.ai.generator import generate_recipe   

router = APIRouter()


@router.post("/recipe-from-image")
async def recipe_from_image(file: UploadFile = File(...)):
    
    try:
        # Kiểm tra file ảnh
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(400, "Chỉ chấp nhận file ảnh (jpg, png, webp...)")

        image_bytes = await file.read()
        if len(image_bytes) == 0:
            raise HTTPException(400, "File ảnh rỗng")

        # Tối ưu ảnh trước khi gửi Gemini
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=95, optimize=True)
            optimized_bytes = buf.getvalue()
        except Exception as e:
            raise HTTPException(400, f"Không đọc được ảnh: {e}")

        # Nhận diện nguyên liệu 
        ingredients = extract_ingredients_from_image(optimized_bytes)

        if not ingredients:
            return {
                "status": "no_ingredients",
                "message": "Không tìm thấy nguyên liệu nào trong ảnh. Vui lòng chụp rõ hơn!",
                "ingredients_detected": [],
                "recipe": None
            }



        # Tạo công thức từ nguyên liệu nhận diện được
        recipe = generate_recipe(ingredients)

        # Nếu generator lỗi 
        if isinstance(recipe, dict) and recipe.get("error"):
            return {
                "status": "partial_success",
                "message": "Nhận diện nguyên liệu thành công nhưng tạo công thức thất bại",
                "ingredients_detected": ingredients,
                "recipe": None,
                "generator_error": recipe.get("error")
            }

        # Thành công hoàn hảo!
        return {
            "status": "success",
            "message": f"Tạo công thức thành công từ {len(ingredients)} nguyên liệu!",
            "ingredients_detected": ingredients,
            "recipe": recipe
        }

    except HTTPException:
        raise
    except Exception as e:
        print("Lỗi không mong muốn /recipe-from-image:", repr(e))
        raise HTTPException(500, "Lỗi hệ thống khi xử lý ảnh")