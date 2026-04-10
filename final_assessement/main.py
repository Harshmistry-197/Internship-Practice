from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_ollama import ChatOllama
from db import connect
from rag import create_retriever
import os
from dotenv import load_dotenv
load_dotenv()

MODEL = "mistral-nemo"
BASE_URL = os.getenv("BASE_URL")
memory=connect()

llm = ChatOllama(
    model=MODEL,
    temperature=0.3,
    base_url="http://172.16.1.224:11434"
)

summarization = SummarizationMiddleware(
    model = llm,
    max_tokens = 500,
    trigger=("messages", 6),
    keep= ("messages", 6)
)

retriever = create_retriever()
thread_id = "thread_1"
config={"configurable": {"thread_id": thread_id}}

prompt = "You are a helpful assistant. Use the provided context to answer questions."
agent = create_agent(
            model=llm,
            tools=[],
            middleware=[summarization],
            checkpointer=memory,
            system_prompt=prompt
        )

while True:
    try:
        user_input = input("user: ")
        if user_input.lower() == "exit":
            print("conversation ended")
            break

        data = retriever.invoke(user_input)
        context = "\n".join([d.page_content for d in data])

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config)

        response = result["messages"][-1].content

        print("Chatbot: ", response)

    except Exception as e:
        print(e)





