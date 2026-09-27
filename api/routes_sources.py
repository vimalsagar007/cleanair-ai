from fastapi import APIRouter
import os

router = APIRouter(prefix="/sources", tags=["Knowledge Base Sources"])

@router.get("")
async def get_knowledge_sources():
    knowledge_dir = "knowledge"
    sources = []
    if os.path.exists(knowledge_dir):
        files = [f for f in os.listdir(knowledge_dir) if f.endswith(".pdf")]
        for f in files:
            sources.append({
                "document_name": f,
                "title": f.replace("_", " ").replace(".pdf", "").title(),
                "type": "Authoritative Guidelines PDF",
                "authority": "WHO / US EPA / Environmental Health Council",
                "effective_date": "2024-01-01"
            })
    return {
        "count": len(sources),
        "sources": sources
    }
