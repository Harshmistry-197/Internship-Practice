import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.tools import tool
load_dotenv()

BASE_URL = os.getenv("BASE_URL")

def get_retriever():
    """ Loaded Documents and splitting into chunks and stored in vectorDb"""
    all_docs = []
    files = ["company_policies.pdf",
             "faq.pdf",
             "product_manual.pdf"
             ]
    for file in files:
        loader = PyPDFLoader(f"Database/{file}")
        docs = loader.load()
        all_docs.extend(docs)

    splitter = RecursiveCharacterTextSplitter(
               chunk_size=500,
               chunk_overlap=200
               )
    chunks = splitter.split_documents(all_docs)

    embeddings = OllamaEmbeddings(model="nomic-embed-text",base_url=BASE_URL)

    vector_store = Chroma.from_documents(
                    chunks,
                    embeddings,
                    persist_directory="chroma_Db"
                   )
    return vector_store.as_retriever(search_kwargs={"k":3})


get_retriever()


