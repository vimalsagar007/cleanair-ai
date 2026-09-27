from typing import Optional
from fastapi import APIRouter, Query
from models.mock_provider import MockPollutionProvider

router = APIRouter(prefix="/monitoring-stations", tags=["Monitoring Stations"])
provider = MockPollutionProvider()

@router.get("")
async def get_stations(city: Optional[str] = Query(default=None)):
    stations = await provider.get_monitoring_stations(city)
    return {
        "city": city or "All",
        "count": len(stations),
        "stations": [s.model_dump() for s in stations]
    }

@router.get("/nearby")
async def get_nearby_stations(lat: float = 37.7749, lon: float = -122.4194):
    stations = await provider.get_nearby_stations(lat, lon)
    return {
        "latitude": lat,
        "longitude": lon,
        "count": len(stations),
        "stations": [s.model_dump() for s in stations]
    }
