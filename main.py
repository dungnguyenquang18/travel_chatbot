from langgraph.graph import Graph, END
from agents import create_supervisor_agent, create_sql_agent, create_search_agent

# Xây dựng graph
graph = Graph()

supervisor = create_supervisor_agent()
sql_agent = create_sql_agent()
search_agent = create_search_agent()

graph.add_node("supervisor", supervisor)
graph.add_node("sql_agent", sql_agent)
graph.add_node("search_agent", search_agent)

# Edges: Supervisor route đến các node
graph.add_edge("supervisor", "sql_agent")
graph.add_edge("supervisor", "search_agent")
graph.add_edge("sql_agent", "supervisor")
graph.add_edge("search_agent", "supervisor")
graph.add_edge("supervisor", END)

graph.set_entry_point("supervisor")

# Compile graph
app = graph.compile()

# Chạy chatbot
if __name__ == "__main__":
    while True:
        query = input("Nhập query tư vấn tour: ")
        if query.lower() == "exit":
            break
        result = app.invoke({"query": query})
        print("Kết quả:", result)
