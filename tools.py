
from langchain.tools import tool
from pymongo import MongoClient

@tool
def sql_query_tool(query: dict) -> str:
    
    print(f"\n🔍 [SQL TOOL] Đang thực thi query: {query}")
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['tour']
        collection = db['tour_in4']
        print(f"📊 [SQL TOOL] Kết nối database thành công")
        
        results = list(collection.find(query))
        print(f"📈 [SQL TOOL] Tìm thấy {len(results)} kết quả")
        
        if not results:
            print("❌ [SQL TOOL] Không tìm thấy kết quả phù hợp")
            return "Không tìm thấy kết quả phù hợp."
        
        # Chuyển kết quả sang dạng dễ đọc
        output = []
        for i, doc in enumerate(results):
            doc.pop('_id', None)
            output.append(str(doc))
            print(f"📄 [SQL TOOL] Kết quả {i+1}: {str(doc)[:100]}...")
        
        final_result = '\n'.join(output)
        print(f"✅ [SQL TOOL] Trả về {len(output)} kết quả")
        return final_result
    except Exception as e:
        print(f"❌ [SQL TOOL] Lỗi: {e}")
        return f"Lỗi: {e}"
    finally:
        if 'client' in locals():
            client.close()
            print("🔌 [SQL TOOL] Đóng kết nối database")

@tool
def location_search_tool(location: str) -> str:
    """Tìm thông tin về địa danh du lịch."""
    print(f"\n🌍 [SEARCH TOOL] Đang tìm kiếm thông tin về: {location}")
    import requests
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&titles={location}"
    print(f"🔗 [SEARCH TOOL] URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"📡 [SEARCH TOOL] Response status: {response.status_code}")
        
        data = response.json()
        page = next(iter(data['query']['pages'].values()))
        result = page.get('extract', 'Không tìm thấy info.')
        
        print(f"📄 [SEARCH TOOL] Tìm thấy {len(result)} ký tự thông tin")
        print(f"✅ [SEARCH TOOL] Trả về thông tin về {location}")
        return result
    except Exception as e:
        print(f"❌ [SEARCH TOOL] Lỗi: {e}")
        return f"Lỗi khi tìm kiếm: {e}"
