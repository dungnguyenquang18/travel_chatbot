from langchain_groq import ChatGroq
from langchain.agents import create_react_agent
from prompts import SUPERVISOR_PROMPT, SQL_AGENT_PROMPT, SEARCH_AGENT_PROMPT
from tools import sql_query_tool, location_search_tool
from config import GROQ_API_KEY_1, GROQ_API_KEY_2, GROQ_API_KEY_3

superivsor_llm = ChatGroq(api_key=GROQ_API_KEY_1 , model='openai/gpt-oss-120b')
sql_llm = ChatGroq(api_key=GROQ_API_KEY_2 , model='openai/gpt-oss-20b')
search_llm = ChatGroq(api_key=GROQ_API_KEY_3 , model='openai/gpt-oss-20b')
# Supervisor Agent: Router
def create_supervisor_agent():
    return create_react_agent(superivsor_llm, tools=[], prompt=SUPERVISOR_PROMPT)

# SQL Agent: Xử lý DB
def create_sql_agent():
    return create_react_agent(sql_llm, tools=[sql_query_tool], prompt=SQL_AGENT_PROMPT)

# Search Agent: Tìm info địa danh
def create_search_agent():
    return create_react_agent(search_llm, tools=[location_search_tool], prompt=SEARCH_AGENT_PROMPT)
