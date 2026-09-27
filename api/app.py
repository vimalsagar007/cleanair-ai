import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from api.routes_air_quality import router as air_quality_router
from api.routes_chat import router as chat_router
from api.routes_alerts import router as alerts_router
from api.routes_stations import router as stations_router
from api.routes_investigations import router as investigations_router
from api.routes_sources import router as sources_router

app = FastAPI(
    title="CLEANAIR AI — Pollution Intelligence, Safety & Alert Platform",
    description="Enterprise Multi-Agent Air Quality Intelligence, RAG Safety Guidance, MCP Tools, and Event Alert Engine.",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(air_quality_router, prefix="/api/v1")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(alerts_router, prefix="/api/v1")
app.include_router(stations_router, prefix="/api/v1")
app.include_router(investigations_router, prefix="/api/v1")
app.include_router(sources_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "HEALTHY", "service": "CLEANAIR AI API", "version": "1.0.0"}

@app.get("/ready")
async def readiness_check():
    return {"status": "READY", "mcp_server": "CONNECTED", "vector_store": "INDEXED"}

# Mount frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
