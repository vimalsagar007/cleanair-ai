from rag.retriever import RAGRetriever

def test_rag_retrieval():
    retriever = RAGRetriever()
    retriever.initialize()
    contexts = retriever.retrieve_relevant_guidance("children recess school pollution precautions", top_k=3)
    assert len(contexts) > 0
    assert any("children" in c.document_name.lower() or "precautions" in c.document_name.lower() for c in contexts)
