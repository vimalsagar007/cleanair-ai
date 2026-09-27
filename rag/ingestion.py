import os
import re
from typing import List, Dict, Any
from pydantic import BaseModel, Field

class DocumentChunk(BaseModel):
    chunk_id: str
    document_name: str
    title: str
    source: str
    topic: str
    effective_date: str
    region: str
    content: str
    page_number: int = 1
    section: str = "General Guidelines"

class RAGIngestionEngine:
    """PDF Ingestion and Semantic Chunking Engine."""

    def __init__(self, chunk_size: int = 400, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_pdf_file(self, filepath: str) -> str:
        """Extract text content from PDF file."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"PDF not found: {filepath}")

        # Extract text from simple PDF or raw text stream
        text_content = ""
        with open(filepath, "r", encoding="latin1", errors="ignore") as f:
            raw = f.read()
            # Extract PDF text stream streams parenthesized strings
            matches = re.findall(r'\((.*?)\)\s*Tj', raw)
            if matches:
                text_content = "\n".join(matches)
            else:
                text_content = raw
        return text_content

    def ingest_directory(self, knowledge_dir: str) -> List[DocumentChunk]:
        chunks: List[DocumentChunk] = []
        if not os.path.exists(knowledge_dir):
            return chunks

        pdf_files = [f for f in os.listdir(knowledge_dir) if f.endswith(".pdf")]
        for pdf in pdf_files:
            full_path = os.path.join(knowledge_dir, pdf)
            text = self.parse_pdf_file(full_path)
            
            # Extract metadata from text content
            doc_id_match = re.search(r'Document ID:\s*([^\n]+)', text)
            source_match = re.search(r'Source:\s*([^\n]+)', text)
            topic_match = re.search(r'Topic:\s*([^\n]+)', text)
            
            doc_id = doc_id_match.group(1) if doc_id_match else pdf
            source = source_match.group(1) if source_match else "Official Health Authority"
            topic = topic_match.group(1) if topic_match else "Air Quality Safety"
            
            # Semantic chunking by paragraphs/sections
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for idx, p in enumerate(paragraphs, 1):
                chunk_id = f"{pdf.replace('.pdf', '')}_chunk_{idx}"
                section_title = p.split("\n")[0][:60] if p else "General"
                
                chunks.append(
                    DocumentChunk(
                        chunk_id=chunk_id,
                        document_name=pdf,
                        title=pdf.replace("_", " ").replace(".pdf", "").title(),
                        source=source,
                        topic=topic,
                        effective_date="2024-01-01",
                        region="Global / EPA",
                        content=p,
                        page_number=1,
                        section=section_title
                    )
                )
        return chunks
