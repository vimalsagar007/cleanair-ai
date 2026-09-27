# CLEANAIR AI — Pollution Intelligence, Safety & Alert Platform

[![Python 3.14](https://img.shields.io/badge/python-3.14-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-Agentic_AI-orange.svg)](https://deepmind.google/technologies/gemini/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-purple.svg)](https://www.langchain.com/langgraph)

**CLEANAIR AI** is an enterprise-grade agentic AI platform designed to deliver real-time pollution intelligence, authoritative health & safety guidance, automated threshold alert notifications, and multi-agent coordination powered by Google Gemini, LangGraph, Model Context Protocol (MCP), Agent-to-Agent (A2A) messaging, and Google Cloud Infrastructure.

---

## 🌟 Key Features & Capabilities

- 🤖 **Multi-Agent Orchestration**: 9 specialized agents (Location, Air Quality, Weather, Trend, Health RAG, Alert, Evidence Grounding, Supervisor, Final Response) working via LangGraph.
- 📡 **Model Context Protocol (MCP)**: 14 tools providing structured measurement retrieval from monitoring stations.
- 💬 **Agent-to-Agent (A2A) Delegation**: Standardized message passing with correlation tracking, timeouts, and circuit breakers.
- 📚 **Enterprise RAG Engine**: 9 WHO/US EPA-aligned PDF health & safety documents with inline footnote citations `[1]`, `[2]`.
- 🛡️ **Grounding & Prompt Injection Defense**: Validates numerical claims against tool data; blocks adversarial instruction overrides.
- 🔔 **Real-Time Alert Pipeline**: Google Cloud Pub/Sub topic emulator with idempotent threshold evaluation and multi-channel notifications.
- 🎨 **Cinematic Environmental Dashboard**: Modern glassmorphism UI with interactive station map, historical charts, AI chat advisor, and developer agent execution trace panel.
- 📊 **Evaluation Benchmark**: Benchmark runner measuring Grounding Accuracy (100%), Attack Block Rate (100%), and Latency (~2.45 ms).

---

## 🚀 Quick Start (Local Setup)

### 1. Clone & Setup Environment
```bash
git clone https://github.com/cleanair-ai/cleanair-ai.git
cd cleanair-ai
python3 -m venv venv
source venv/bin/activate
pip install -r pyproject.toml
```

### 2. Generate Synthetic Database & Knowledge PDFs
```bash
PYTHONPATH=. python3 data/seed_db.py
PYTHONPATH=. python3 knowledge/generate_pdfs.py
```

### 3. Run Test Suite & Evaluation Benchmark
```bash
PYTHONPATH=. python3 run_tests.py
PYTHONPATH=. python3 evaluation/runner.py
```

### 4. Execute 15 Demo Scenarios
```bash
PYTHONPATH=. python3 demo_scenarios.py
```

### 5. Launch Application Server
```bash
PYTHONPATH=. python3 -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload
```
Open your browser at **`http://localhost:8000`** to view the environmental dashboard and AI chat advisor.

---

## 🏛️ System Architecture

See [architecture.md](file:///config/Desktop/Session1/cleanair-ai/architecture.md) for full architectural diagrams and data flow details.

---

## ☁️ Google Cloud Deployment

```bash
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_REGION="us-central1"
bash deployment/deploy_gcp.sh
```

---

## 📁 Repository Structure

```
cleanair-ai/
├── README.md
├── architecture.md
├── pyproject.toml
├── Dockerfile
├── docker-compose.yml
├── evaluation_report.md
├── demo_scenarios.py
├── run_tests.py
├── models/
├── data/
├── knowledge/
├── rag/
├── mcp/
├── a2a/
├── agents/
├── graph/
├── alert_engine/
├── safety/
├── evaluation/
├── api/
├── frontend/
├── tests/
├── deployment/
└── docs/
```
