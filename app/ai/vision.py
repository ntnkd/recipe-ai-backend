# app/ai/vision.py


import google.generativeai as genai
from app.ai.model_loader import get_genai_model
from PIL import Image
import io
import re
import json


def extract_ingredients_from_image(image_bytes: bytes) -> list[str]:
    genai, model_name = get_genai_model()

    model = genai.GenerativeModel(model_name)

    # Convert sang JPEG
    try:
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != "RGB":
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=98, optimize=True, subsampling=0)
        image_bytes = buf.getvalue()
    except Exception as e:
        print("Lỗi convert ảnh:", e)
        return []
    
    # Prompt nhận diện nguyên liệu từ ảnh
    prompt = """
    Bạn là chuyên gia nhận diện nguyên liệu nấu ăn Việt Nam từ ảnh thực tế (tủ lạnh, chợ, bàn bếp, siêu thị...).

    Nhiệm vụ: Phân tích kỹ ảnh và liệt kê TẤT CẢ nguyên liệu thực phẩm bạn thấy.

    QUY TẮC BẮT BUỘC:
    - Chỉ liệt kê khi chắc chắn ≥80%
    - Tên nguyên liệu bằng tiếng Việt phổ thông, ngắn gọn nhất có thể
    - Không thêm số lượng, không thêm mô tả
    - Không lặp lại (dù nguyên liệu xuất hiện nhiều lần)
    - Đọc được nhãn chai, bao bì (nếu rõ chữ)
    - Phân biệt chính xác: cà chua ≠ cà rốt, thịt heo ≠ thịt bò, hành lá ≠ hành tây, v.v.

    ĐỊNH DẠNG TRẢ VỀ DUY NHẤT:
    Chỉ trả về 1 mảng JSON, không giải thích, không text thừa.

    Ví dụ:
    ["gà", "trứng", "cà rốt", "hành tây", "tỏi", "giá đỗ", "nước mắm", "đường", "ớt", "hành lá", "lá chanh"]

    Bắt đầu phân tích ảnh ngay:
    """

    try:
        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        raw_text = response.text.strip()

        
        ingredients = []

        # Lấy nguyên liệu từ phản hồi bằng regex + JSON parse
        matches = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw_text)
        if matches:
            ingredients = [item.strip().lower() for item in matches if item.strip()]
        else:
            array_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
            if array_match:
                try:
                    cleaned = array_match.group(0)
                    cleaned = cleaned.replace(r'\"', '"').replace(r"\'", "'")
                    temp = json.loads(cleaned)
                    ingredients = [str(x).strip().lower() for x in temp if x]
                except:
                    pass

        # Làm sạch & chuẩn hóa tên nguyên liệu
        clean_list = []
        for item in ingredients:
            item = item.strip().lower()
            # Chuẩn hóa một số tên hay bị sai
            item = item.replace("thịt gà", "gà").replace("thịt heo", "heo").replace("thịt bò", "bò")
            item = item.replace("hành lá", "hành lá").replace("hành tím", "hành tím")
            item = item.replace("cà chua", "cà chua").replace("cà rốt", "cà rốt")
            if item and len(item) <= 25:  # lọc nhiễu
                clean_list.append(item)

        # Xóa trùng
        final_ingredients = sorted(list(dict.fromkeys(clean_list)))

        return final_ingredients

    except Exception as e:
        print("Lỗi xử lý ảnh với Gemini:", repr(e))
        return []