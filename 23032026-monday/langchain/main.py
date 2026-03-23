from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0.7,
    base_url="http://ai:11434",
)

response = llm.invoke([
    HumanMessage(content="Explain transformers in simple terms")
])

print(response.content)

