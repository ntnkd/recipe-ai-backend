# app/routes/vision_routes.py

import io
import os
import re
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# Cấu hình Gemini một lần
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # 1.5-flash cực chuẩn cho nhận diện đồ ăn VN


@router.post("/vision-test")
async def vision_test(file: UploadFile = File(...)):
    try:
        # Đọc và convert ảnh sang JPEG chất lượng cao (rất quan trọng!)
        image_bytes = await file.read()
        if not image_bytes:
            raise HTTPException(400, "File ảnh rỗng")

        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=95, optimize=True)
        image_bytes = buf.getvalue()

        # Model
        model = genai.GenerativeModel(MODEL_NAME)

        # Prompt siêu chặt chẽ + bắt buộc trả JSON
        prompt = """
Bạn là chuyên gia nhận diện nguyên liệu nấu ăn từ ảnh chụp thực tế (tủ lạnh, chợ, bàn bếp...).

Nhiệm vụ: Liệt kê CHÍNH XÁC tất cả nguyên liệu thực phẩm có trong ảnh.

YÊU CẦU BẮT BUỘC:
- Chỉ trả về đúng 1 mảng JSON (không giải thích, không đánh số, không xuống dòng thừa).
- Tên nguyên liệu bằng tiếng Việt phổ thông, ngắn gọn.
- Không lặp lại nguyên liệu.
- Chỉ liệt kê khi chắc chắn ≥ 90%.
- Nếu không có nguyên liệu hoặc ảnh không rõ → trả về []

Ví dụ đúng định dạng (không thêm gì khác):
["gà", "cà rốt", "hành tây", "tỏi", "giá đỗ", "nước mắm", "đường"]

Bây giờ phân tích ảnh và trả về kết quả ngay:
        """

        # Gửi ảnh + prompt
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        raw_text = response.text.strip()

        # === PHẦN SIÊU CHẮC CHẮN: LẤY MẢNG DÙ GEMINI TRẢ KIỂU GÌ CŨNG ĐƯỢC ===
        ingredients = []

        # Cách 1: Lấy bằng regex (rất mạnh)
        matches = re.findall(r'"([^"]*)"', raw_text)
        if matches:
            ingredients = [item.strip() for item in matches if item.strip() and len(item.strip()) <= 30]

        # Cách 2: Nếu cách 1 không được thì thử tìm khối [...]
        if not ingredients:
            array_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
            if array_match:
                try:
                    json_str = array_match.group(0)
                    json_str = json_str.replace(r'\"', '"').replace(r"\'", "'")
                    ingredients = json.loads(json_str)
                    ingredients = [str(x).strip() for x in ingredients if x]
                except:
                    pass

        # Làm sạch lần cuối
        ingredients = list(dict.fromkeys(ingredients))  # xóa trùng (nếu có)

        return {
            "status": "ok",
            "nguyen_lieu": ingredients,           # ← Đây là kết quả bạn muốn
            "so_luong": len(ingredients),
            "gemini_raw": raw_text                 # để debug khi cần
        }

    except Exception as e:
        print("LỖI /vision-test:", repr(e))
        raise HTTPException(500, f"Lỗi xử lý ảnh: {str(e)}")