from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.7,
    base_url=base_url,
)

response = llm.invoke([
    HumanMessage(content="Explain transformers in simple terms")
])

print(response.content)

