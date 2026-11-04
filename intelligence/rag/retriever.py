import logging
from pathlib import Path
from threading import Lock


CHROMA_DB_PATH = Path("intelligence/rag/chroma_db")
logger = logging.getLogger(__name__)

_retriever = None
_retriever_lock = Lock()


def _create_retriever():
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_chroma import Chroma

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    vector_store = Chroma(
        persist_directory=str(CHROMA_DB_PATH),
        embedding_function=embeddings
    )
    return vector_store.as_retriever(search_kwargs={"k": 4})


def _get_retriever():
    global _retriever

    if _retriever is None:
        with _retriever_lock:
            if _retriever is None:
                _retriever = _create_retriever()

    return _retriever


def warm_up_retriever() -> None:
    """Initialize RAG resources explicitly when startup warm-up is desired."""
    _get_retriever()


def retrieve_context(query: str):
    """
    Retrieves relevant cybersecurity intelligence
    from the BlackTrace vector database.
    """

    try:
        results = _get_retriever().invoke(query)
    except Exception:
        logger.exception("RAG retrieval failed; returning empty context.")
        return []

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
