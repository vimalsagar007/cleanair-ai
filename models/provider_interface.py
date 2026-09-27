from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from .pollution import AQIMeasurement, WeatherConditions, MonitoringStation, PollutionForecast, LocationInfo

class PollutionDataProvider(ABC):
    """Abstract interface for Pollution & Air Quality data providers."""

    @abstractmethod
    async def get_current_aqi(self, city_or_lat: str, lon: Optional[float] = None) -> AQIMeasurement:
        """Fetch current AQI and pollutant concentrations."""
        pass

    @abstractmethod
    async def get_aqi_history(self, city_or_lat: str, hours: int = 24) -> List[AQIMeasurement]:
        """Fetch historical AQI measurements for the past N hours."""
        pass

    @abstractmethod
    async def get_weather(self, city_or_lat: str, lon: Optional[float] = None) -> WeatherConditions:
        """Fetch weather conditions."""
        pass

    @abstractmethod
    async def get_forecast(self, city_or_lat: str, hours: int = 24) -> PollutionForecast:
        """Fetch pollution forecast."""
        pass

    @abstractmethod
    async def get_monitoring_stations(self, city: Optional[str] = None) -> List[MonitoringStation]:
        """Fetch monitoring stations."""
        pass

    @abstractmethod
    async def get_nearby_stations(self, lat: float, lon: float, radius_km: float = 25.0) -> List[MonitoringStation]:
        """Fetch stations within radius."""
        pass
