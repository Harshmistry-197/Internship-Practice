import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyMuPDFLoader
from prompt import load_prompt

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL")

llm = ChatGroq(
    api_key=groq_api_key,
    model=groq_model,
    temperature=0.3
)

def extract_pdf(file_path):
    loader = PyMuPDFLoader(file_path)
    docs = loader.load()
    text = "\n".join([doc.page_content for doc in docs])

    return text


req_prompt = PromptTemplate.from_template(load_prompt("requirement"))
us_prompt = PromptTemplate.from_template(load_prompt("user_story"))
task_prompt = PromptTemplate.from_template(load_prompt("generate_task"))

requirement_chain = req_prompt | llm
user_stories_chain = us_prompt | llm
tasks_chain = task_prompt | llm


@tool("generate_requirement", description="Analyzes raw text or document content to identify and categorize specific"
                                 " Functional and Non-Functional software requirements")
def generate_requirements(text: str):
    """Generate software requirements from raw text"""
    try:
        return requirement_chain.invoke({"text": text}).content
    except Exception as e:
        print(e)

@tool("generate_user_stories", description="Converts a list of software requirements into structured user stories using "
                                 "the 'As a, I want, So that' format.")
def generate_user_stories(requirement: str):
    """Convert Requirements into user stories"""
    try:
        return user_stories_chain.invoke({"requirements": requirement}).content
    except Exception as e:
        print(e)

@tool("generate_task", description="Generates a structured list of actionable development tasks based on "
                                   "provided user stories.")
def generate_task(user_stories: str):
    """Generate development tasks from user stories"""
    try:
       return tasks_chain.invoke({"user_stories": user_stories}).content
    except Exception as e:
        print(e)


tools = [
    generate_requirements,
    generate_user_stories,
    generate_task
]

agent_prompt = load_prompt("agent_prompt")

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=agent_prompt
)


if __name__ == "__main__":
    pdf_path = "SRS.pdf"

    print(f"Extracting PDF")
    text = extract_pdf(pdf_path)

    print(f"Agent Execution")
    task = agent.invoke({
        "input": f"Process this system and generate requirements, user stories and tasks:\n{text[:1500]}"
    })

    print(task["messages"][-1].content)

