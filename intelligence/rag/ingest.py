from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

KNOWLEDGE_BASE_PATH = ("intelligence/rag/knowledge_base")
CHROMA_DB_PATH = ("intelligence/rag/chroma_db")

def main():
    """
    Build the BlackTrace cybersecurity vector database
    """

    loader = DirectoryLoader(str(KNOWLEDGE_BASE_PATH), glob="**/*.md")

    documents = loader.load()

    print(f"Loaded {len(documents)} documents.")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Generated {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_PATH)
    )

    print(f"Persisted at: {CHROMA_DB_PATH}")

if __name__ == "__main__":
    main()
