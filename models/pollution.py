from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

class AQICategory(str, Enum):
    GOOD = "Good"                       # 0-50 (Green)
    MODERATE = "Moderate"               # 51-100 (Yellow)
    UNHEALTHY_SENSITIVE = "Unhealthy for Sensitive Groups" # 101-150 (Orange)
    UNHEALTHY = "Unhealthy"             # 151-200 (Red)
    VERY_UNHEALTHY = "Very Unhealthy"   # 201-300 (Purple)
    HAZARDOUS = "Hazardous"             # 301+ (Maroon)

class PollutantType(str, Enum):
    PM25 = "PM2.5"
    PM10 = "PM10"
    NO2 = "NO2"
    O3 = "O3"
    SO2 = "SO2"
    CO = "CO"

class PollutantReading(BaseModel):
    pollutant: PollutantType
    value: float = Field(..., description="Measured concentration value")
    unit: str = Field(..., description="Measurement unit e.g. ug/m3 or ppm")
    sub_index: int = Field(..., ge=0, description="Individual pollutant AQI sub-index")
    quality_status: str = Field(default="VERIFIED", description="Data quality check status e.g. VERIFIED, PROVISIONAL")

class LocationInfo(BaseModel):
    city: str
    state: Optional[str] = None
    country: str = "USA"
    latitude: float
    longitude: float
    neighborhood: Optional[str] = None

class AQIMeasurement(BaseModel):
    measurement_id: str
    station_id: str
    station_name: str
    location: LocationInfo
    timestamp: str
    aqi: int = Field(..., ge=0, le=500)
    primary_pollutant: PollutantType
    category: AQICategory
    pollutants: List[PollutantReading]
    source: str = Field(default="Official Monitoring Station Network")
    data_quality: str = Field(default="VERIFIED")

class WeatherConditions(BaseModel):
    station_id: str
    timestamp: str
    temperature_c: float
    temperature_f: float
    humidity_percent: float
    wind_speed_kmh: float
    wind_direction_deg: float
    wind_direction_cardinal: str
    pressure_hpa: float
    condition: str
    visibility_km: float

class PollutionForecast(BaseModel):
    location: LocationInfo
    generated_at: str
    forecast_hours: List[Dict[str, Any]] = Field(default_factory=list)
    dominant_pollutant: PollutantType
    trend_summary: str

class MonitoringStation(BaseModel):
    station_id: str
    name: str
    operator: str
    location: LocationInfo
    is_active: bool = True
    last_updated: str
    distance_km: Optional[float] = None
    supported_pollutants: List[PollutantType]
