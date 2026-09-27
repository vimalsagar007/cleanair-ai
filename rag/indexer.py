import numpy as np
from typing import List, Dict, Any, Optional
from .ingestion import DocumentChunk
from .embeddings import EmbeddingModel

class VectorIndexer:
    """In-memory vector store indexer with metadata filtering."""

    def __init__(self, embedding_model: EmbeddingModel):
        self.embedding_model = embedding_model
        self.chunks: List[DocumentChunk] = []
        self.vectors: Optional[np.ndarray] = None

    def add_chunks(self, chunks: List[DocumentChunk]):
        if not chunks:
            return
        self.chunks.extend(chunks)
        embeddings = [self.embedding_model.embed_text(c.content) for c in chunks]
        matrix = np.vstack(embeddings)
        if self.vectors is None:
            self.vectors = matrix
        else:
            self.vectors = np.vstack([self.vectors, matrix])

    def search(self, query: str, top_k: int = 5, topic_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        if not self.chunks or self.vectors is None:
            return []

        query_vec = self.embedding_model.embed_text(query)
        # Cosine similarity
        scores = np.dot(self.vectors, query_vec)

        results = []
        for idx, score in enumerate(scores):
            chunk = self.chunks[idx]
            if topic_filter and topic_filter.lower() not in chunk.topic.lower():
                continue
            results.append({
                "chunk": chunk,
                "score": float(score)
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
