from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

embedding_model = os.getenv("EMBEDDING_MODEL")
base_url = os.getenv("BASE_URL")


def create_retriever():
    try:
        # data Load
        all_docs = []

        files = [
            "data/company_policies.pdf",
            "data/product_manual.pdf",
            "data/faq.pdf"
        ]

        for file in files:
            loader = PyMuPDFLoader(file)
            docs = loader.load()
            all_docs.extend(docs)

        # chunk
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunk = splitter.split_documents(all_docs)

        # embedding
        embedding = OllamaEmbeddings(model=embedding_model, base_url=base_url)


        # Vector Store
        vector_store = InMemoryVectorStore.from_documents(chunk, embedding)

        return vector_store.as_retriever()

    except Exception as e:
        print(e)

