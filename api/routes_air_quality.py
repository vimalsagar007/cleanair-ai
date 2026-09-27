from fastapi import APIRouter, Query
from typing import Optional
from models.mock_provider import MockPollutionProvider

router = APIRouter(prefix="/air-quality", tags=["Air Quality"])
provider = MockPollutionProvider()

@router.get("")
async def get_air_quality(city: str = Query(default="San Francisco", description="City name")):
    meas = await provider.get_current_aqi(city)
    return meas.model_dump()

@router.get("/history")
async def get_air_quality_history(city: str = Query(default="San Francisco"), hours: int = Query(default=24, ge=1, le=168)):
    history = await provider.get_aqi_history(city, hours)
    return {
        "city": city,
        "hours": hours,
        "history": [h.model_dump() for h in history]
    }

@router.get("/trend")
async def get_air_quality_trend(city: str = Query(default="San Francisco")):
    history = await provider.get_aqi_history(city, 24)
    current_aqi = history[0].aqi
    past_aqi = history[-1].aqi
    delta = current_aqi - past_aqi
    trend = "DETERIORATING" if delta > 15 else ("IMPROVING" if delta < -15 else "STABLE")
    return {
        "city": city,
        "current_aqi": current_aqi,
        "past_24h_aqi": past_aqi,
        "delta_24h": delta,
        "trend": trend
    }
