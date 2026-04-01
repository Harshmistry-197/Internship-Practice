import os
from langchain.agents import create_agent
from langchain.agents.middleware import before_model, after_model, AgentState
from langchain.messages import AIMessage
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime

load_dotenv()

ollama_model = os.getenv("OLLAMA_MODEL")

@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime):
    print("Message count :", len(state["messages"]))
    if len(state["messages"]) >= 4:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None

@after_model
def log_response(state: AgentState, runtime: Runtime):
    print(f"Model returned: {state['messages'][-1].content}")
    return None

model = ChatOllama(
    model=ollama_model,
    temperature=0.3
)

agent = create_agent(
    model,
    middleware=[check_message_limit, log_response],
    checkpointer=InMemorySaver()
)

config = {"configurable": {"thread_id": "thread_1"}}

while True:
    user_input = input("\nEnter your message: ")
    if user_input.lower() == "exit":
        print("Conversation Ended")
        break
    inputs = {"messages": [HumanMessage(content=user_input)]}
    result = agent.invoke(inputs,config = config)

    print(f"\nFinal Agent Response: {result['messages'][-1].content}")
