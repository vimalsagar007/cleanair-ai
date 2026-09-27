# Google Cloud Production Deployment Guide

CLEANAIR AI is packaged for cloud-native deployment on Google Cloud Platform:

## Cloud Services Used
* **Cloud Run**: Serverless container hosting for the FastAPI web server & MCP tools.
* **BigQuery**: Historical pollution analytics, weather trends, and alert event logs.
* **Cloud Storage**: Persistent storage for RAG PDF knowledge documents.
* **Pub/Sub**: Event-driven alert pipeline (`pollution-updates`, `pollution-alerts`, `agent-events`).
* **Secret Manager**: Secure API key management.

## Deployment Script Execution
```bash
export GCP_PROJECT_ID="your-gcp-project-id"
export GCP_REGION="us-central1"
bash deployment/deploy_gcp.sh
```
