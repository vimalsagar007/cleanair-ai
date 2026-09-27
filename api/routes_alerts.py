from fastapi import APIRouter, HTTPException
from typing import Optional
from api.schemas import AlertCreateRequest
from models.alert_models import AlertConfig
from api.routes_chat import alert_processor, notifier

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.post("")
async def create_alert_config(req: AlertCreateRequest):
    cfg = AlertConfig(
        user_id=req.user_id,
        config_id=f"cfg_{req.city.lower()}",
        city=req.city,
        aqi_threshold=req.aqi_threshold,
        channels=req.channels,
        is_active=True
    )
    alert_processor.register_config(cfg)
    return {"status": "SUCCESS", "config": cfg.model_dump()}

@router.get("")
async def get_active_alerts(user_id: str = "default_user"):
    notifications = notifier.get_user_notifications(user_id)
    return {
        "user_id": user_id,
        "count": len(notifications),
        "notifications": [n.model_dump() for n in notifications]
    }

@router.delete("/{alert_id}")
async def delete_alert(alert_id: str):
    return {"status": "DELETED", "alert_id": alert_id}
