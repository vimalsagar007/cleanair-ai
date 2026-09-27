import math
import random
from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from .pollution import (
    AQIMeasurement, AQICategory, PollutantType, PollutantReading,
    WeatherConditions, MonitoringStation, PollutionForecast, LocationInfo
)
from .provider_interface import PollutionDataProvider

CITIES_DATABASE: Dict[str, Dict[str, Any]] = {
    "san francisco": {"lat": 37.7749, "lon": -122.4194, "state": "CA", "base_aqi": 38, "country": "USA"},
    "los angeles": {"lat": 34.0522, "lon": -118.2437, "state": "CA", "base_aqi": 115, "country": "USA"},
    "new york": {"lat": 40.7128, "lon": -74.0060, "state": "NY", "base_aqi": 52, "country": "USA"},
    "seattle": {"lat": 47.6062, "lon": -122.3321, "state": "WA", "base_aqi": 32, "country": "USA"},
    "chicago": {"lat": 41.8781, "lon": -87.6298, "state": "IL", "base_aqi": 68, "country": "USA"},
    "houston": {"lat": 29.7604, "lon": -95.3698, "state": "TX", "base_aqi": 82, "country": "USA"},
    "phoenix": {"lat": 33.4484, "lon": -112.0740, "state": "AZ", "base_aqi": 95, "country": "USA"},
    "denver": {"lat": 39.7392, "lon": -104.9903, "state": "CO", "base_aqi": 61, "country": "USA"},
    "london": {"lat": 51.5074, "lon": -0.1278, "state": "England", "base_aqi": 45, "country": "UK"},
    "beijing": {"lat": 39.9042, "lon": 116.4074, "state": "Beijing", "base_aqi": 165, "country": "China"},
    "delhi": {"lat": 28.6139, "lon": 77.2090, "state": "Delhi", "base_aqi": 285, "country": "India"},
    "tokyo": {"lat": 35.6762, "lon": 139.6503, "state": "Tokyo", "base_aqi": 28, "country": "Japan"},
    "sydney": {"lat": -33.8688, "lon": 151.2093, "state": "NSW", "base_aqi": 25, "country": "Australia"},
    "paris": {"lat": 48.8566, "lon": 2.3522, "state": "IDF", "base_aqi": 58, "country": "France"},
}

def resolve_aqi_category(aqi: int) -> AQICategory:
    if aqi <= 50:
        return AQICategory.GOOD
    elif aqi <= 100:
        return AQICategory.MODERATE
    elif aqi <= 150:
        return AQICategory.UNHEALTHY_SENSITIVE
    elif aqi <= 200:
        return AQICategory.UNHEALTHY
    elif aqi <= 300:
        return AQICategory.VERY_UNHEALTHY
    else:
        return AQICategory.HAZARDOUS

class MockPollutionProvider(PollutionDataProvider):
    """Realistic physics-aware synthetic pollution provider."""

    def __init__(self, seed: int = 42):
        self.seed = seed
        random.seed(seed)

    def _get_city_meta(self, city_name: str) -> Dict[str, Any]:
        key = city_name.strip().lower()
        if key in CITIES_DATABASE:
            return CITIES_DATABASE[key]
        
        # Default dynamic generation for unknown cities
        return {
            "lat": 37.7749,
            "lon": -122.4194,
            "state": "State",
            "base_aqi": 65,
            "country": "USA"
        }

    async def get_current_aqi(self, city_or_lat: str, lon: Optional[float] = None) -> AQIMeasurement:
        meta = self._get_city_meta(city_or_lat)
        city_title = city_or_lat.title()
        now = datetime.now(timezone.utc)
        
        # Diurnal fluctuation simulation: peak during 8 AM and 6 PM rush hours
        hour = now.hour
        rush_hour_factor = math.sin((hour - 8) * math.pi / 6) * 15 + math.sin((hour - 18) * math.pi / 6) * 20
        aqi_val = max(12, int(meta["base_aqi"] + rush_hour_factor + random.randint(-5, 5)))
        category = resolve_aqi_category(aqi_val)

        pm25_val = round(aqi_val * 0.28 + random.uniform(-1.5, 1.5), 1)
        pm10_val = round(aqi_val * 0.55 + random.uniform(-2.0, 2.0), 1)
        no2_val = round(aqi_val * 0.18 + random.uniform(-1.0, 1.0), 1)
        o3_val = round(aqi_val * 0.22 + random.uniform(-1.0, 1.0), 1)
        so2_val = round(aqi_val * 0.05 + random.uniform(-0.5, 0.5), 1)
        co_val = round(aqi_val * 0.01 + random.uniform(-0.1, 0.1), 2)

        readings = [
            PollutantReading(pollutant=PollutantType.PM25, value=pm25_val, unit="ug/m3", sub_index=aqi_val),
            PollutantReading(pollutant=PollutantType.PM10, value=pm10_val, unit="ug/m3", sub_index=max(10, int(aqi_val * 0.7))),
            PollutantReading(pollutant=PollutantType.NO2, value=no2_val, unit="ppb", sub_index=max(5, int(aqi_val * 0.4))),
            PollutantReading(pollutant=PollutantType.O3, value=o3_val, unit="ppb", sub_index=max(8, int(aqi_val * 0.5))),
            PollutantReading(pollutant=PollutantType.SO2, value=so2_val, unit="ppb", sub_index=max(2, int(aqi_val * 0.2))),
            PollutantReading(pollutant=PollutantType.CO, value=co_val, unit="ppm", sub_index=max(1, int(aqi_val * 0.1))),
        ]

        loc = LocationInfo(
            city=city_title,
            state=meta.get("state"),
            country=meta.get("country", "USA"),
            latitude=meta["lat"],
            longitude=meta["lon"],
            neighborhood="Central District"
        )

        return AQIMeasurement(
            measurement_id=f"meas_{city_title.lower()}_{now.strftime('%Y%m%d%H%M')}",
            station_id=f"stn_{city_title.lower()}_01",
            station_name=f"{city_title} Central Environmental Monitor",
            location=loc,
            timestamp=now.isoformat(),
            aqi=aqi_val,
            primary_pollutant=PollutantType.PM25,
            category=category,
            pollutants=readings,
            source="EPA / AirNow Verified Station Network",
            data_quality="VERIFIED"
        )

    async def get_aqi_history(self, city_or_lat: str, hours: int = 24) -> List[AQIMeasurement]:
        meta = self._get_city_meta(city_or_lat)
        city_title = city_or_lat.title()
        now = datetime.now(timezone.utc)
        history = []

        for h in range(hours, -1, -1):
            t = now - timedelta(hours=h)
            hour = t.hour
            rush_factor = math.sin((hour - 8) * math.pi / 6) * 15 + math.sin((hour - 18) * math.pi / 6) * 20
            aqi_val = max(10, int(meta["base_aqi"] + rush_factor + math.sin(h/3)*8))
            category = resolve_aqi_category(aqi_val)

            loc = LocationInfo(
                city=city_title,
                state=meta.get("state"),
                country=meta.get("country", "USA"),
                latitude=meta["lat"],
                longitude=meta["lon"]
            )

            readings = [
                PollutantReading(pollutant=PollutantType.PM25, value=round(aqi_val * 0.28, 1), unit="ug/m3", sub_index=aqi_val),
                PollutantReading(pollutant=PollutantType.PM10, value=round(aqi_val * 0.55, 1), unit="ug/m3", sub_index=max(10, int(aqi_val * 0.7))),
            ]

            history.append(
                AQIMeasurement(
                    measurement_id=f"meas_hist_{h}_{t.strftime('%H%M')}",
                    station_id=f"stn_{city_title.lower()}_01",
                    station_name=f"{city_title} Central Environmental Monitor",
                    location=loc,
                    timestamp=t.isoformat(),
                    aqi=aqi_val,
                    primary_pollutant=PollutantType.PM25,
                    category=category,
                    pollutants=readings,
                    source="EPA / AirNow Network",
                    data_quality="VERIFIED"
                )
            )
        return history

    async def get_weather(self, city_or_lat: str, lon: Optional[float] = None) -> WeatherConditions:
        meta = self._get_city_meta(city_or_lat)
        city_title = city_or_lat.title()
        now = datetime.now(timezone.utc)

        temp_c = round(21.5 + math.sin(now.hour / 4.0) * 4.0, 1)
        temp_f = round(temp_c * 9/5 + 32, 1)
        humidity = round(55.0 + math.cos(now.hour / 4.0) * 15.0, 1)
        wind_speed = round(12.4 + math.sin(now.hour) * 5.0, 1)

        return WeatherConditions(
            station_id=f"wth_{city_title.lower()}_01",
            timestamp=now.isoformat(),
            temperature_c=temp_c,
            temperature_f=temp_f,
            humidity_percent=humidity,
            wind_speed_kmh=wind_speed,
            wind_direction_deg=290.0,
            wind_direction_cardinal="WNW",
            pressure_hpa=1014.2,
            condition="Partly Cloudy",
            visibility_km=10.0
        )

    async def get_forecast(self, city_or_lat: str, hours: int = 24) -> PollutionForecast:
        meta = self._get_city_meta(city_or_lat)
        city_title = city_or_lat.title()
        now = datetime.now(timezone.utc)
        
        forecast_items = []
        for h in range(1, hours + 1):
            t = now + timedelta(hours=h)
            expected_aqi = max(15, int(meta["base_aqi"] + math.sin(h / 3.0) * 12.0))
            forecast_items.append({
                "timestamp": t.isoformat(),
                "predicted_aqi": expected_aqi,
                "category": resolve_aqi_category(expected_aqi).value,
                "confidence": "HIGH" if h <= 12 else "MEDIUM"
            })

        loc = LocationInfo(
            city=city_title,
            state=meta.get("state"),
            country=meta.get("country", "USA"),
            latitude=meta["lat"],
            longitude=meta["lon"]
        )

        return PollutionForecast(
            location=loc,
            generated_at=now.isoformat(),
            forecast_hours=forecast_items,
            dominant_pollutant=PollutantType.PM25,
            trend_summary="Pollution levels expected to stay moderate with slight evening peak during traffic rush."
        )

    async def get_monitoring_stations(self, city: Optional[str] = None) -> List[MonitoringStation]:
        city_name = city or "San Francisco"
        meta = self._get_city_meta(city_name)
        city_title = city_name.title()
        now = datetime.now(timezone.utc)

        stations = [
            MonitoringStation(
                station_id=f"stn_{city_title.lower()}_01",
                name=f"{city_title} Civic Center Station",
                operator="State Air Resources Board",
                location=LocationInfo(city=city_title, latitude=meta["lat"], longitude=meta["lon"], country="USA"),
                is_active=True,
                last_updated=now.isoformat(),
                distance_km=0.8,
                supported_pollutants=[PollutantType.PM25, PollutantType.PM10, PollutantType.NO2, PollutantType.O3]
            ),
            MonitoringStation(
                station_id=f"stn_{city_title.lower()}_02",
                name=f"{city_title} Industrial Park Monitor",
                operator="EPA Regional Office",
                location=LocationInfo(city=city_title, latitude=meta["lat"] + 0.02, longitude=meta["lon"] + 0.03, country="USA"),
                is_active=True,
                last_updated=now.isoformat(),
                distance_km=3.4,
                supported_pollutants=[PollutantType.PM25, PollutantType.SO2, PollutantType.CO]
            ),
            MonitoringStation(
                station_id=f"stn_{city_title.lower()}_03",
                name=f"{city_title} Coastal Air Sensor",
                operator="Coastal Environment Group",
                location=LocationInfo(city=city_title, latitude=meta["lat"] - 0.03, longitude=meta["lon"] - 0.02, country="USA"),
                is_active=True,
                last_updated=now.isoformat(),
                distance_km=5.1,
                supported_pollutants=[PollutantType.O3, PollutantType.PM25]
            ),
        ]
        return stations

    async def get_nearby_stations(self, lat: float, lon: float, radius_km: float = 25.0) -> List[MonitoringStation]:
        return await self.get_monitoring_stations("San Francisco")
