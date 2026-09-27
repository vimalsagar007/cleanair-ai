# Troubleshooting & Diagnostic Guide

## Common Issues & Solutions

### 1. `ModuleNotFoundError: No module named 'models'`
**Cause**: Missing `PYTHONPATH` when running scripts directly.
**Fix**: Execute commands with `PYTHONPATH=. python3 script_name.py`.

### 2. MCP Tool Timeout / Unavailable
**Cause**: Local MCP server process not initialized or port blocked.
**Fix**: The FastAPI server embeds local MCP tools in-process, falling back smoothly to `MockPollutionProvider`.

### 3. Missing RAG Contexts
**Cause**: Knowledge PDFs not generated.
**Fix**: Run `python3 knowledge/generate_pdfs.py` to regenerate PDFs in `knowledge/`.

### 4. Grounding Validation Rejection
**Cause**: Draft text generated numbers inconsistent with MCP tool values.
**Fix**: Check `EvidenceAgent` logs in the Developer Agent Trace panel.
