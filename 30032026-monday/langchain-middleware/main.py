import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mongodb import MongoDBChatMessageHistory
from langchain_ollama import ChatOllama

load_dotenv()

ollama_model = os.getenv("OLLAMA_MODEL")
mongo_uri = os.getenv("MONGODB_CONNECTION_STRING")

llm = ChatOllama(
    model=ollama_model,
    temperature=0.3
)

session_id = "user_session_1"
mongo_memory = MongoDBChatMessageHistory(
    connection_string=mongo_uri,
    session_id=session_id,
    database_name="chat_middleware_memory",
    collection_name="history"
)

system_prompt = """
You are a professional AI assistant that keeps track of the conversation. 
Guidelines:
1. Maintain context using short-term memory (last 4 exchanges fully visible).
2. Retrieve older messages from long-term memory (MongoDB) when needed.
3. Answer clearly and naturally, human-like.
4. Recall previous questions and answers accurately. For example:
   User: What is 2+2?
   AI: 2+2 equals 4.
   User: What was my first question?
   AI: Your first question was "What is 2+2?", and the answer was "4".
5. If an answer is not found in any memory, respond politely indicating lack of information.
"""

agent = create_agent(
    model=llm,
    checkpointer=None,
    system_prompt=system_prompt,
    middleware=[
        SummarizationMiddleware(
            model=llm,
            trigger=("messages",4),
            keep=("messages",4)
        )
    ]
)

def update_long_term(message):
    if len(message) > 8:
        old_message = message[:-8]
        for msg in old_message:
            mongo_memory.add_message(msg)

        return message[-8:]
    return message

def search_long_term(query):
    for msg in reversed(mongo_memory.messages):
        if query.lower() in msg.content.lower():
            return msg
    return None

def chat():
    thread_id = "thread_1"
    local_message = []

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "quit":
            print("Conversation ended")
            break

        prompt_message = HumanMessage(content=user_input)
        retrieved_msg = search_long_term(user_input)

        if retrieved_msg:
            prompt_message.content += f"\nRelevant old memory: {retrieved_msg.content}"

        result = agent.invoke(
            {"messages": local_message + [prompt_message]},
            config={"configurable": {"thread_id": thread_id}}
        )

        response = result["messages"][-1].content
        print(f"\nAI : {response}")

        local_message.append(HumanMessage(content=user_input))
        local_message.append(AIMessage(content=response))

        local_message = update_long_term(local_message)

if __name__ == "__main__":
    chat()



