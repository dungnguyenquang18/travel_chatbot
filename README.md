# Chatbot Tư vấn Tour Du lịch

## Mô tả

Chatbot multiagent tư vấn tour du lịch, sử dụng LangGraph, LangChain, Groq API, SQLite DB, và Wikipedia API.

## Cấu trúc thư mục

```
travel_chatbot/
├── crawl_data/                   # Thư mục crawl data
│   └── crawl.py          # File crawl data rồi chuyển sang mongodb.
├── main.py               # File chính: Xây dựng graph LangGraph, kết nối agents/tools, chạy chatbot.
├── agents.py             # Định nghĩa 3 agents: supervisor, sql_agent, search_agent.
├── tools.py              # Định nghĩa tools: sql_query_tool (truy vấn DB), location_search_tool (tìm info địa danh).
├── prompts.py            # Chứa prompt templates cho từng agent.
├── config.py             # Lưu cấu hình: API key Groq, DB path, v.v.
├── requirements.txt      # Danh sách dependencies.
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
