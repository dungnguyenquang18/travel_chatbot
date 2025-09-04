from langgraph.graph import StateGraph, END
from agents import create_supervisor_agent, create_sql_agent, create_search_agent
from typing import TypedDict, List, Tuple, Any

# Define state schema
class State(TypedDict):
    query: str
    result: str
    intermediate_steps: List[Tuple[str, str]]
    supervisor_output: str

# Xây dựng graph
graph = StateGraph(State)

supervisor_chain = create_supervisor_agent()
sql_agent = create_sql_agent()
search_agent = create_search_agent()

# Wrapper function for supervisor
def supervisor_node(state):
    print(f"\n🎯 [SUPERVISOR] Nhận query: {state['query']}")
    result = supervisor_chain.run(query=state["query"])
    print(f"🎯 [SUPERVISOR] Quyết định route đến: {result}")
    return {"supervisor_output": result}

# Wrapper functions for agents
def sql_agent_node(state):
    print(f"\n💾 [SQL AGENT] Bắt đầu xử lý query: {state['query']}")
    result = sql_agent.invoke(state)
    print(f"💾 [SQL AGENT] Hoàn thành xử lý")
    return result

def search_agent_node(state):
    print(f"\n🌍 [SEARCH AGENT] Bắt đầu xử lý query: {state['query']}")
    result = search_agent.invoke(state)
    print(f"🌍 [SEARCH AGENT] Hoàn thành xử lý")
    return result

graph.add_node("supervisor", supervisor_node)
graph.add_node("sql_agent", sql_agent_node)
graph.add_node("search_agent", search_agent_node)

# Conditional routing function
def route_after_supervisor(state):
    # Đọc output từ supervisor
    supervisor_output = state.get("supervisor_output", "")
    print(f"🔄 [ROUTER] Supervisor output: {supervisor_output}")
    
    # Route dựa trên output của supervisor
    if "sql_agent" in supervisor_output.lower():
        print(f"🔄 [ROUTER] Route đến: sql_agent")
        return "sql_agent"
    elif "search_agent" in supervisor_output.lower():
        print(f"🔄 [ROUTER] Route đến: search_agent")
        return "search_agent"
    else:
        # Fallback: route dựa trên query
        if "tour" in state["query"].lower():
            print(f"🔄 [ROUTER] Fallback route đến: sql_agent")
            return "sql_agent"
        else:
            print(f"🔄 [ROUTER] Fallback route đến: search_agent")
            return "search_agent"

# Edges: Supervisor route đến các node
graph.add_conditional_edges("supervisor", route_after_supervisor)
graph.add_edge("sql_agent", END)
graph.add_edge("search_agent", END)

graph.set_entry_point("supervisor")

# Compile graph
app = graph.compile()

# Chạy chatbot
if __name__ == "__main__":
    while True:
        query = input("Nhập query tư vấn tour: ")
        if query.lower() == "exit":
            break
        result = app.invoke({"query": query, "intermediate_steps": [], "supervisor_output": ""})
        
        print("Debug - Toàn bộ result:", result)
        print("Debug - Supervisor output:", result.get("supervisor_output", ""))
        print("Debug - Final result:", result.get("result", "Không có"))
        
        # Lấy kết quả từ agent cuối cùng
        if "sql_agent" in result.get("supervisor_output", ""):
            print("Kết quả từ SQL Agent:", result.get("result", "Không có kết quả"))
        elif "search_agent" in result.get("supervisor_output", ""):
            print("Kết quả từ Search Agent:", result.get("result", "Không có kết quả"))
        else:
            print("Kết quả:", result)
