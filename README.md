# Chatbot Tư vấn Tour Du lịch

## Mô tả

Chatbot multiagent tư vấn tour du lịch, sử dụng LangGraph, LangChain, Groq API, SQLite DB, và Wikipedia API.

## Cấu trúc thư mục

```
travel_chatbot/
├── main.py
├── agents.py
├── tools.py
├── prompts.py
├── config.py
├── db/
│   └── tours.db
├── requirements.txt
└── README.md
```

## Hướng dẫn triển khai

1. Cài đặt dependencies: `pip install -r requirements.txt`
2. Tạo database: Tạo file `db/tours.db` với schema phù hợp.
3. Lấy Groq API key tại [https://x.ai/api](https://x.ai/api), thêm vào `config.py`.
4. Chạy project: `python main.py`

## Gợi ý schema DB

Table `tours`: `id`, `name`, `location`, `price`, `description`.

## Mở rộng

- Thêm logging, error handling.
- Dùng API search mạnh hơn.
- Tối ưu prompt cho từng agent.
