import os
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

DATA_FOLDER = "app/scraped_data"
VECTOR_STORE_FOLDER = "app/vector_store"

def load_documents():
    print("📄 Memuat dokumen...")
    documents = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            path = os.path.join(DATA_FOLDER, filename)
            loader = TextLoader(path, encoding="utf-8")
            documents.extend(loader.load())
    return documents

def main():
    docs = load_documents()
    print(f"✂️ Memotong {len(docs)} dokumen menjadi chunk...")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )

    print("🧠 Membuat embeddings & menyimpan ke Chroma...")
    db = Chroma.from_documents(split_docs, embeddings, persist_directory=VECTOR_STORE_FOLDER)

    db.persist()
    print(f"✅ Vector store berhasil disimpan di: {VECTOR_STORE_FOLDER}")

if __name__ == "__main__":
    main()
