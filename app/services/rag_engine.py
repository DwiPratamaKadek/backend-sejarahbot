import os
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def build_qa():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    vectordb = Chroma(
        persist_directory="app/vector_store",
        embedding_function=embeddings
    )

    retriever = vectordb.as_retriever()

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain

def generate_enriched_prompt(user_query: str) -> str:
    qa_chain = build_qa()
    result = qa_chain.invoke({"query": user_query})
    context = "\n".join([doc.page_content for doc in result["source_documents"]])
    enriched_prompt = f"""
    Based on the following context, generate an image that illustrates the concept.

    Context:
    {context}

    User Prompt:
    {user_query}
    """
    return enriched_prompt.strip()
