from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from .ingestion import DocumentChunk, RAGIngestionEngine
from .embeddings import EmbeddingModel
from .indexer import VectorIndexer

class RetrievedContext(BaseModel):
    chunk_id: str
    document_name: str
    title: str
    source: str
    topic: str
    content: str
    relevance_score: float
    citation_id: str
    section: str

class RAGRetriever:
    """Enterprise RAG Retriever with cross-score reranking and citations."""

    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = knowledge_dir
        self.embedding_model = EmbeddingModel(dimension=384)
        self.indexer = VectorIndexer(self.embedding_model)
        self._is_initialized = False

    def initialize(self):
        if self._is_initialized:
            return
        ingestion = RAGIngestionEngine()
        chunks = ingestion.ingest_directory(self.knowledge_dir)
        self.indexer.add_chunks(chunks)
        self._is_initialized = True

    def retrieve_relevant_guidance(self, query: str, top_k: int = 4, topic_filter: Optional[str] = None) -> List[RetrievedContext]:
        self.initialize()
        raw_results = self.indexer.search(query, top_k=top_k, topic_filter=topic_filter)
        
        contexts = []
        for idx, res in enumerate(raw_results, 1):
            c: DocumentChunk = res["chunk"]
            contexts.append(
                RetrievedContext(
                    chunk_id=c.chunk_id,
                    document_name=c.document_name,
                    title=c.title,
                    source=c.source,
                    topic=c.topic,
                    content=c.content,
                    relevance_score=round(res["score"], 4),
                    citation_id=f"[{idx}]",
                    section=c.section
                )
            )
        return contexts
