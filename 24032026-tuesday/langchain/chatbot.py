import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from tavily import TavilyClient
from langchain_core.messages import ToolMessage
import streamlit as st

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

st.title("Chatbot")
st.write("Make search on web")

tavily_client = TavilyClient(api_key = TAVILY_API_KEY)

@tool("Search", description = "Search the queries on web")
def search(user_query: str):
    return tavily_client.search(user_query)

llm = ChatGroq(
    api_key = GROQ_API_KEY,
    model = GROQ_MODEL,
    temperature = 0.3
)

model = llm.bind_tools([search])

query = st.text_input("Enter your query")

if query:
    messages = [HumanMessage(content=query)]

    result = model.invoke(messages)
    messages.append(result)

    if result.tool_calls:
        for tool_call in result.tool_calls:
            search_results = search.invoke(tool_call["args"])

            messages.append(ToolMessage(
                content=str(search_results),
                tool_call_id=tool_call["id"]
            ))

        final_response = model.invoke(messages)
        st.success(final_response.content)
    else:
        st.success(result.content)