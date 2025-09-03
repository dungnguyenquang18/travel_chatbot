from langchain_groq import ChatGroq
from langchain.agents import create_react_agent
from prompts import SUPERVISOR_PROMPT, SQL_AGENT_PROMPT, SEARCH_AGENT_PROMPT
from tools import sql_query_tool, location_search_tool
from config import GROQ_API_KEY

llm = ChatGroq(api_key=GROQ_API_KEY )

# Supervisor Agent: Router
def create_supervisor_agent():
    return create_react_agent(llm, tools=[], prompt=SUPERVISOR_PROMPT)

# SQL Agent: Xử lý DB
def create_sql_agent():
    return create_react_agent(llm, tools=[sql_query_tool], prompt=SQL_AGENT_PROMPT)

# Search Agent: Tìm info địa danh
def create_search_agent():
    return create_react_agent(llm, tools=[location_search_tool], prompt=SEARCH_AGENT_PROMPT)
