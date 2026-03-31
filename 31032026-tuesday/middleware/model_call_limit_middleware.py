import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain.agents.middleware import ModelCallLimitMiddleware

load_dotenv()

ollama_model = os.getenv("OLLAMA_MODEL")

system_prompt = """
You MUST process one Cricketer at a time.
Call the tool separately in different steps.
Do NOT combine tool calls.
"""

llm = ChatOllama(
    model = ollama_model,
    temperature = 0
)

@tool
def get_pm_details(name):
    """Get achievements for a specific Cricketer."""
    return f"Details for {name}: Achievements and awards achieved in indian cricket team."

agent = create_agent(
    model=llm,
    tools=[get_pm_details],
    system_prompt=system_prompt,
    middleware=[
        ModelCallLimitMiddleware(
            run_limit=1,
            exit_behavior="error"
        ),
    ]
)

try:
    query = "Get me details for Rohit Sharma and Virat Kohli"
    response = agent.invoke({"messages": [HumanMessage(content = query)]})
    print(response["messages"][-1].content)
except Exception as e:
    print(e)