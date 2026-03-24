from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

base_url = os.getenv("BASE_URL")
api_key = os.getenv("GROQ_API_KEY")

# llm = ChatOllama(
#     model="llama3.2:latest",
#     temperature=0.7,
#     base_url=base_url,
# )

llm = ChatGroq(
    api_key=os.getenv(api_key),
    temperature=0.5,
    model="llama-3.3-70b-versatile"
)

response = llm.invoke([
    HumanMessage(content="Explain transformers in simple terms")
])

print(response.content)

