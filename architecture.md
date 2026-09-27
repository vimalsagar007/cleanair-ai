# CLEANAIR AI — Architecture Specification

CLEANAIR AI is a production-grade multi-agent environmental intelligence and safety platform built on Google Gemini, LangGraph, Model Context Protocol (MCP), Agent-to-Agent (A2A) task delegation, RAG, and Google Cloud infrastructure.

```mermaid
graph TD
    User([User / Web UI]) <--> API[FastAPI Gateway]
    
    subgraph Multi-Agent LangGraph Workflow
        API --> Supervisor[Supervisor Agent]
        Supervisor --> Location[Location Agent]
        Supervisor --> AQIAgent[Air Quality Agent]
        Supervisor --> WeatherAgent[Weather Agent]
        Supervisor --> TrendAgent[Pollution Trend Agent]
        
        AQIAgent <--> MCP[Pollution MCP Server]
        WeatherAgent <--> MCP
        TrendAgent <--> MCP
        
        Supervisor --> HealthAgent[Health & Safety RAG Agent]
        HealthAgent <--> RAG[RAG Vector Store & FAISS]
        RAG <--> PDFs[Authoritative Health PDFs]
        
        Supervisor --> AlertAgent[Alert Evaluation Agent]
        AlertAgent --> PubSub[Google Cloud Pub/Sub]
        PubSub --> AlertProc[Alert Processor Engine]
        AlertProc --> Notifier[Multi-Channel Notification Service]
        
        Supervisor --> Grounding[Evidence & Grounding Agent]
        Grounding --> FinalResponse[Final Response Agent]
    end

    FinalResponse --> API
    API --> BigQuery[(Google Cloud BigQuery)]
```

## System Guarantees
1. **Zero Measurement Fabrication**: Measured AQI, pollutant levels, weather, and timestamps originate strictly from verified station data tools via MCP.
2. **Authoritative RAG Safety Guidance**: Health and safety advice is grounded in 9 WHO/EPA compliant PDF guidelines with footnote citations.
3. **Grounding Validation Loop**: Output is validated before response assembly; fails safely if evidence is missing or corrupted.
4. **Prompt Injection Guardrails**: Neutralizes adversarial prompts attempting instruction overrides.
