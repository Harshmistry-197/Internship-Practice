from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
from langgraph.types import Command
import os

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

llm = ChatOllama(
    model = OLLAMA_MODEL,
    temperature = 0
)

@tool(
    "your_read_email_tool",
    description = "This function is used to read email messages using email id"
)
def your_read_email_tool(email_id: str) -> str:
    """function to read an email by its ID."""
    return f"Email content for ID: {email_id}"

@tool(
    "your_send_email_tool",
    description = "This function is used to send an email."
)
def your_send_email_tool(recipient: str, subject: str, body: str) -> str:
    """function to send an email."""
    return f"Email sent to {recipient} with subject '{subject}'"


agent = create_agent(
    model = llm,
    tools = [your_read_email_tool, your_send_email_tool],
    checkpointer = InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on = {
                "your_read_email_tool": {
                    "allowed_decisions": ["approve", "edit", "reject"],
                },
                "your_send_email_tool": False,
            }
        )
    ]
)

config = {"configurable":{"thread_id":"thread_1"}}

while True:
    user_query = input("\nEnter your query: ")
    if user_query.lower() == "exit":
        break
    final_query = {
        "messages": [
            HumanMessage(
            content = user_query,
            )
        ]
    }

    response = agent.invoke(
        final_query,
        config = config
    )

    state = agent.invoke(
        Command(
            resume = {
                "decisions": [
                    {
                        "type": "approve"
                    }
                ]
            }
        ),
        config = config
    )

    print(f"\nResponse: {state["messages"][-1].content}\n")