from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")  # ✅ .env variable
AGENT_MAP = {}

def generate_pdf_qa_agent(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(pages, embeddings)
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(),  # ✅ Correct usage
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    filename = os.path.basename(pdf_path)
    AGENT_MAP[filename] = qa

def chat_with_pdf_agent(filename, query):
    agent = AGENT_MAP.get(filename)
    if not agent:
        return "Agent not initialized. Please upload the PDF first."
    return agent.run(query)
