AI_recipe_gennerator/
│
├── app/
│   ├── __init__.py
│   ├── main.py                # Khởi động server (Flask hoặc FastAPI)
│   ├── routes/
│   │   ├── __init__.py
│   │   └── recipe_routes.py   # Endpoint /getRecipes
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── generator.py       # File chính: xử lý AI sinh công thức
│   │   ├── retriever.py       # (tùy chọn) tìm kiếm từ dataset
│   │   └── model_loader.py    # Tải model hoặc API key
│   ├── data/
│   │   └── recipes.csv        # Dataset thực (nếu có)
│   ├── utils/
│   │   ├── __init__.py
│   │   └── formatters.py      # Format kết quả JSON 
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── recipe_schema.py   # Kiểm tra dữ liệu input/output
│   └── tests/
│       ├── __init__.py
│       └── test_api.py
│
├── requirements.txt
└── .env                       # API_KEY, cấu hình model
