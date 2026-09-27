from typing import List, Dict, Any

class EvaluationMetrics:
    """Calculates benchmark metrics for RAG, Multi-Agent routing, and Grounding."""

    @staticmethod
    def calculate_hit_rate(retrieved_docs: List[str], expected_doc: str) -> float:
        return 1.0 if any(expected_doc.lower() in d.lower() for d in retrieved_docs) else 0.0

    @staticmethod
    def calculate_mrr(retrieved_docs: List[str], expected_doc: str) -> float:
        for rank, doc in enumerate(retrieved_docs, 1):
            if expected_doc.lower() in doc.lower():
                return 1.0 / rank
        return 0.0

    @staticmethod
    def calculate_groundedness(response_text: str, verified_aqi: int) -> float:
        if str(verified_aqi) in response_text or "insufficient" in response_text.lower():
            return 1.0
        return 0.0

    @staticmethod
    def calculate_citation_coverage(response_text: str, citations: List[Any]) -> float:
        if not citations:
            return 0.0
        cited = sum(1 for c in citations if c.get("citation_id", "") in response_text)
        return cited / len(citations)
