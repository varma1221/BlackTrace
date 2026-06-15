from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


CHROMA_DB_PATH = Path("intelligence/rag/chroma_db")


embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


vector_store = Chroma(persist_directory=str(CHROMA_DB_PATH), embedding_function=embeddings)


retriever = vector_store.as_retriever(search_kwargs={"k": 4})


def retrieve_context(query: str):
    """
    Retrieves relevant cybersecurity intelligence
    from the BlackTrace vector database.
    """

    results = retriever.invoke(query)

    return [
        document.page_content
        for document in results
    ]


if __name__ == "__main__":
    query = "FTP brute force attack behavior"
    contexts = retrieve_context(query)

    print("\nRetrieved Context:\n")

    for index, context in enumerate(contexts, start=1):
        print(f"\nContext {index}\n")
        print(context)
