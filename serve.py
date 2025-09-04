from flask import Flask, request, jsonify
from agents import create_supervisor_agent, create_sql_agent, create_search_agent
from prompts import SUPERVISOR_PROMPT, SQL_AGENT_PROMPT, SEARCH_AGENT_PROMPT

app = Flask(__name__)

# Khởi tạo các agent
supervisor = create_supervisor_agent()
sql_agent = create_sql_agent()
search_agent = create_search_agent()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    query = data.get('query', '')
    context = data.get('context', '')
    # Supervisor quyết định agent
    supervisor_result = supervisor.invoke({"query": query, "context": context})
    # Đọc output từ supervisor
    if isinstance(supervisor_result, dict):
        agent_name = supervisor_result.get("supervisor_output", "END")
        reason = supervisor_result.get("reason", "")
    else:
        agent_name = supervisor_result
        reason = ""
    # Route đến agent phù hợp
    if agent_name == "sql_agent":
        result = sql_agent.invoke({"query": query, "schema": "..."})
    elif agent_name == "search_agent":
        result = search_agent.invoke({"location": query})
    else:
        result = {"result": "Kết thúc hoặc không xác định agent phù hợp."}
    return jsonify({
        "agent": agent_name,
        "reason": reason,
        "result": result
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
