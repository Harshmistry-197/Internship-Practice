import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

groq_model = os.getenv("GROQ_MODEL")
groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=groq_api_key,
    model=groq_model,
    temperature=0.3
)

@tool("Addition", description="This tool gives the addition of all the numbers")
def addition(numbers: list[float]):
    """This tool gives the addition of all the numbers"""

    return sum(numbers)

agent = create_agent(
    model=llm,
    tools=[addition],
    system_prompt="""
    You are an intelligent calculator agent.
    - Always use tools for mathematical calculations.
    - Break complex problems into steps.
    - Return clean and precise answers.
    """
)

query = {
    "messages": [HumanMessage(
        content=f"Provide the result of 9-5-3"
    )]
}

response = agent.invoke(query)

print(response["messages"][-1].content)
