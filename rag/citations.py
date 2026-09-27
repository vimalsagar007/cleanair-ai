from typing import List, Dict, Any
from .retriever import RetrievedContext

class CitationBuilder:
    """Formats retrieved contexts into structured footnote citations."""

    @staticmethod
    def format_citations(contexts: List[RetrievedContext]) -> Dict[str, Any]:
        citations = []
        for ctx in contexts:
            citations.append({
                "citation_id": ctx.citation_id,
                "document": ctx.document_name,
                "title": ctx.title,
                "source": ctx.source,
                "section": ctx.section,
                "score": ctx.relevance_score,
                "snippet": ctx.content[:150] + "..." if len(ctx.content) > 150 else ctx.content
            })
        
        formatted_text = "\n\n### References & Authoritative Sources\n"
        for c in citations:
            formatted_text += f"* **{c['citation_id']}** [{c['title']}] - *{c['source']}* (Section: {c['section']})\n"

        return {
            "citations": citations,
            "formatted_markdown": formatted_text
        }
