from typing import List, Dict, Any
from rag.retriever import RAGRetriever, RetrievedContext

class HealthAgent:
    """Agent responsible for RAG retrieval of health guidelines & safety precautions."""

    def __init__(self, retriever: RAGRetriever):
        self.retriever = retriever

    async def retrieve_health_guidance(self, query: str, aqi_category: str) -> List[RetrievedContext]:
        # Formulate targeted retrieval query
        search_query = f"{query} {aqi_category} air quality precautions health safety"
        contexts = self.retriever.retrieve_relevant_guidance(search_query, top_k=4)
        return contexts
