import logging
from types import SimpleNamespace

import intelligence.rag.retriever as rag_retriever


def test_retriever_initializes_lazily_and_reuses_resources(monkeypatch):
    created = []

    class FakeRetriever:
        def invoke(self, query):
            return [SimpleNamespace(page_content=f"Context for {query}")]

    def create_retriever():
        created.append(True)
        return FakeRetriever()

    monkeypatch.setattr(rag_retriever, "_retriever", None)
    monkeypatch.setattr(rag_retriever, "_create_retriever", create_retriever)

    assert rag_retriever._retriever is None
    assert rag_retriever.retrieve_context("first query") == [
        "Context for first query"
    ]
    assert rag_retriever.retrieve_context("second query") == [
        "Context for second query"
    ]
    assert len(created) == 1


def test_retriever_initialization_failure_returns_empty_context(monkeypatch, caplog):
    def fail_to_create_retriever():
        raise RuntimeError("model initialization failed")

    monkeypatch.setattr(rag_retriever, "_retriever", None)
    monkeypatch.setattr(
        rag_retriever,
        "_create_retriever",
        fail_to_create_retriever
    )

    with caplog.at_level(logging.ERROR):
        assert rag_retriever.retrieve_context("query") == []

    assert "RAG retrieval failed" in caplog.text