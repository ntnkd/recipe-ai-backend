# AI_recipe_generator/app/ai/generator.py

import json
from app.utils.formatters import clean_json_text
from app.ai.model_loader import get_genai_model

#Sinh công thức nấu ăn từ danh sách nguyên liệu
def generate_recipe(ingredients: list[str]) -> dict:
    
    genai, model_name = get_genai_model()

    prompt = f"""
    Bạn là một đầu bếp chuyên nghiệp AI, giàu kinh nghiệm với các món ăn sáng tạo, lành mạnh và đa dạng văn hóa. 
    Nhiệm vụ của bạn là tạo ra một công thức nấu ăn độc đáo, hấp dẫn, sử dụng chính xác các nguyên liệu đã cho: {', '.join(ingredients)}. 
    Bạn phải đảm bảo công thức:
    - Sáng tạo: Kết hợp các nguyên liệu theo cách mới mẻ, không theo lối mòn, ví dụ như fusion giữa các nền ẩm thực khác nhau (Á Đông, Địa Trung Hải, hiện đại...).
    - Cân bằng dinh dưỡng: Ưu tiên sự hài hòa giữa protein, carbs, chất béo, vitamin và khoáng chất từ các nguyên liệu có sẵn.
    - Dễ thực hiện: Phù hợp cho người nấu ăn tại nhà, với các bước rõ ràng, an toàn và không yêu cầu dụng cụ chuyên dụng.
    - Phần ăn: Dành cho 2-4 người, trừ khi nguyên liệu gợi ý khác.
    - Sử dụng hết hoặc tối ưu hóa các nguyên liệu: Không thêm nguyên liệu mới trừ khi cần thiết cho gia vị cơ bản (muối, tiêu, dầu ăn, nếu không được chỉ định).

    Trả lời BẮT BUỘC dưới dạng JSON hợp lệ, không có bất kỳ văn bản nào khác. Cấu trúc JSON phải bao gồm chính xác các trường sau:
    - "name": Tên công thức (bằng tiếng Việt, ngắn gọn, hấp dẫn, ví dụ: "Salad Gà Xào Rau Củ Thơm Lừng").
    - "ingredients": Danh sách các nguyên liệu dưới dạng mảng JSON, mỗi phần tử là một đối tượng với hai trường con: "name" (tên nguyên liệu) và "quantity" (số lượng cụ thể, ví dụ: "200g" hoặc "2 quả"). Liệt kê theo thứ tự sử dụng trong công thức, và chỉ sử dụng các nguyên liệu từ danh sách đã cho (có thể điều chỉnh số lượng).
    - "instructions": Danh sách các bước thực hiện dưới dạng mảng JSON các chuỗi, mỗi bước được đánh số tự động (bắt đầu từ 1.), chi tiết từng hành động cụ thể (bao gồm lượng gia vị chính xác nếu áp dụng, ví dụ: "nêm 1/2 muỗng cà phê muối và 1/4 muỗng cà phê tiêu đen"), thời gian ước tính cho bước đó nếu cần, và mẹo nhỏ để thành công (ví dụ: "1. Rửa sạch rau củ dưới vòi nước lạnh để giữ độ giòn, tránh ngâm lâu làm mất vitamin. Tránh dùng cụm từ chung chung như 'nêm gia vị vừa miệng'; hãy chỉ định lượng cụ thể để dễ theo dõi và lặp lại.").
    - "estimated_time": Thời gian nấu ước tính tổng cộng (số nguyên, đơn vị phút, ví dụ: 45, bao gồm chuẩn bị và nấu).
    - "calories": Ước tính tổng calo cho toàn bộ công thức (số nguyên, dựa trên kiến thức dinh dưỡng chuẩn, ví dụ: 800, cho toàn bộ phần ăn).

    Ví dụ định dạng đầu ra JSON (giả sử nguyên liệu là ['gà', 'cà rốt', 'hành tây'] cho món "Gà Xào Rau Củ"):
    {{
        "name": "Gà Xào Rau Củ Thơm Mật Ong",
        "ingredients": [
            {{"name": "thịt gà", "quantity": "300g"}},
            {{"name": "cà rốt", "quantity": "2 củ"}},
            {{"name": "hành tây", "quantity": "1 củ"}}
        ],
        "instructions": [
            "1. Rửa sạch thịt gà, cắt miếng vừa ăn và ướp với 1/2 muỗng cà phê muối, 1/4 muỗng cà phê tiêu đen trong 10 phút để ngấm gia vị.",
            "2. Gọt vỏ cà rốt và hành tây, cắt lát mỏng để giữ độ giòn khi xào (dày khoảng 0.5cm).",
            "3. Đun nóng chảo với 1 thìa dầu ăn (khoảng 15ml), xào thịt gà đến khi săn lại (khoảng 5 phút), sau đó cho rau củ vào đảo đều ở lửa trung bình.",
            "4. Nêm thêm 1 thìa cà phê mật ong, 1/4 muỗng cà phê bột nghệ để tạo vị ngọt tự nhiên và màu sắc đẹp, xào thêm 3-5 phút nữa cho rau chín tới nhưng vẫn giòn."
        ],
        "estimated_time": 30,
        "calories": 650
    }}

    Đảm bảo JSON không có lỗi cú pháp, và nội dung phải logic, hấp dẫn để người dùng dễ theo dõi.
    """

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    text = clean_json_text(response.text)

    try:
        return json.loads(text)
    except Exception as e:
        return {"error": str(e), "raw_text": response.text}
    
#Sinh công thức nấu ăn từ mô tả món ăn
def generate_recipe_from_description(description: str) -> dict:


    genai, model_name = get_genai_model()

    prompt = f"""
Bạn là đầu bếp AI 3 sao Michelin, chuyên sáng tạo món ăn từ mô tả tự do.

Dựa chính xác vào mô tả sau, hãy tạo một công thức hoàn chỉnh, hấp dẫn, khả thi tại nhà:

"{description}"

Yêu cầu bắt buộc:
- Phân tích đúng phong cách ẩm thực (Ý, Nhật, Việt, fusion, healthy, v.v.)
- Đảm bảo món ăn phù hợp với mô tả về vị giác (béo, cay, chua ngọt, thanh mát, đậm đà...)
- Chọn nguyên liệu hợp lý, dễ tìm, phù hợp với người Việt
- Phần ăn: 2 người (trừ khi mô tả yêu cầu khác)
- Có thể thêm gia vị cơ bản (muối, tiêu, đường, dầu ăn, tỏi, hành) nếu cần thiết để món ngon hơn

TRẢ VỀ DUY NHẤT MỘT ĐOẠN JSON HỢP LỆ, KHÔNG CÓ BẤT KỲ VĂN BẢN NÀO KHÁC (kể cả ```json hay giải thích).

Cấu trúc JSON chính xác:
{{
  "name": "Tên món ăn",
  "ingredients": [
    {{"name": "tên nguyên liệu", "quantity": "số lượng cụ thể"}},
    {{"name": "mì Ý", "quantity": "200g"}},
    ...
  ],
  "instructions": [
    "1. Luộc mì với nước sôi có chút muối trong 8 phút, vớt ra để ráo.",
    "2. Phi thơm tỏi băm với bơ, cho kem tươi vào đun sôi nhẹ.",
    ...
  ],
  "estimated_time": 25,
  "calories": 720
}}

Bây giờ hãy tạo công thức ngay từ mô tả trên.
"""

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    text = clean_json_text(response.text)

    try:
        return json.loads(text)
    except Exception as e:
        return {
            "error": str(e),
            "raw_text": response.text
        }
