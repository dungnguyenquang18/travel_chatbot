
from langchain.tools import tool
from pymongo import MongoClient

@tool
def sql_query_tool(query: dict) -> str:
    """Thực thi truy vấn MongoDB trên collection 'tours'.
    Query là một dict MongoDB filter, ví dụ: {'location': 'Đà Lạt'} hoặc {'price': {'$lt': 5000000}}.
    """
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['tour']
        collection = db['tour_db']
        results = list(collection.find(query))
        if not results:
            return "Không tìm thấy kết quả phù hợp."
        # Chuyển kết quả sang dạng dễ đọc
        output = []
        for doc in results:
            doc.pop('_id', None)
            output.append(str(doc))
        return '\n'.join(output)
    except Exception as e:
        return f"Lỗi: {e}"
    finally:
        client.close()

@tool
def location_search_tool(location: str) -> str:
    """Tìm thông tin về địa danh du lịch."""
    import requests
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={location}"
    response = requests.get(url)
    data = response.json()
    page = next(iter(data['query']['pages'].values()))
    return page.get('extract', 'Không tìm thấy info.')
