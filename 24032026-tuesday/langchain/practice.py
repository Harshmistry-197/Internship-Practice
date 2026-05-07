from langchain_classic.chains.conversation.base import ConversationChain
from langchain_classic.memory import ConversationBufferMemory
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

API_KEY = os.getenv("GROQ_API_KEY")

def llm_model():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=API_KEY,
        temperature=0.5
    )
    return llm

def generate_text(llm, user_input):

    if user_input.lower() == "exit":
        print("Conversation Ended")
        return
    response = llm.invoke(user_input)
    print(f"Bot : {response.content}\n\n")

def memory():

    memories = ConversationBufferMemory()
    return memories

def coversation_chain():
    conversation_chain = ConversationChain(
        llm=llm_model(),
        memory=memory(),
    )
    return conversation_chain


def main():
    while True:
        user_input = input("You : ")
        if user_input.lower() == "exit":
            print("Conversation Ended")
            break
        chain = coversation_chain()
        ch = chain.run(user_input)
        print("Bot : ", ch)


if __name__ == "__main__":
    main()