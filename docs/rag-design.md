# RAG Architecture & Citation System

The Enterprise RAG system ingests 9 synthetic authoritative PDF guidelines in `knowledge/`:

* `air_quality_guidelines.pdf`
* `pollution_precautions.pdf`
* `outdoor_activity_guidance.pdf`
* `indoor_air_quality.pdf`
* `children_air_quality_guidance.pdf`
* `elderly_air_quality_guidance.pdf`
* `outdoor_worker_guidance.pdf`
* `pollution_health_information.pdf`
* `emergency_guidance.pdf`

## RAG Pipeline Architecture
1. **Ingestion & Metadata Extraction**: Extracts `Document ID`, `Source`, `Topic`, `Region`, and `Effective Date`.
2. **Semantic Chunking**: Chunks text by logical sections and paragraph boundaries.
3. **Dense Vector Indexing**: Generates normalized 384-dimensional embeddings and indexes in an in-memory cosine vector store.
4. **Hybrid Retrieval & Reranking**: Combines term relevance and dense similarity with topic-based metadata filtering.
5. **Footnote Citations**: Every health recommendation references its source context with clickable footnote citations `[1]`, `[2]`.
