import time
import logging
from typing import Dict, Any, List, Optional
from models.mock_provider import MockPollutionProvider
from mcp.schemas import MCPToolRequest, MCPToolResponse, MCPError

logger = logging.getLogger("PollutionMCPTools")
logger.setLevel(logging.INFO)

class PollutionMCPTools:
    """Enterprise MCP Tools registry for Pollution & Air Quality System."""

    def __init__(self, provider: Optional[MockPollutionProvider] = None):
        self.provider = provider or MockPollutionProvider()
        self.active_alerts_db: List[Dict[str, Any]] = []
        self.alert_prefs_db: Dict[str, Dict[str, Any]] = {}

    async def execute_tool(self, request: MCPToolRequest) -> MCPToolResponse:
        start_time = time.time()
        tool_name = request.tool_name
        args = request.arguments
        cid = request.correlation_id

        logger.info(f"[MCP Execution] Tool: {tool_name} | CorrelationID: {cid}")

        try:
            handler = getattr(self, f"tool_{tool_name}", None)
            if not handler:
                return MCPToolResponse(
                    tool_name=tool_name,
                    status="ERROR",
                    error=MCPError(code=404, message=f"Tool '{tool_name}' not found on Pollution MCP Server."),
                    correlation_id=cid,
                    execution_time_ms=round((time.time() - start_time) * 1000, 2)
                )

            res_data = await handler(args)
            return MCPToolResponse(
                tool_name=tool_name,
                status="SUCCESS",
                result=res_data,
                correlation_id=cid,
                execution_time_ms=round((time.time() - start_time) * 1000, 2)
            )
        except Exception as e:
            logger.error(f"[MCP Error] Tool: {tool_name} | Error: {str(e)}")
            return MCPToolResponse(
                tool_name=tool_name,
                status="ERROR",
                error=MCPError(code=500, message=f"Tool execution failed: {str(e)}"),
                correlation_id=cid,
                execution_time_ms=round((time.time() - start_time) * 1000, 2)
            )

    # Tool 1: get_current_aqi
    async def tool_get_current_aqi(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        meas = await self.provider.get_current_aqi(city)
        return meas.model_dump()

    # Tool 2: get_pollutants
    async def tool_get_pollutants(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        meas = await self.provider.get_current_aqi(city)
        return {
            "city": city,
            "timestamp": meas.timestamp,
            "pollutants": [p.model_dump() for p in meas.pollutants]
        }

    # Tool 3: get_aqi_history
    async def tool_get_aqi_history(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        hours = int(args.get("hours", 24))
        history = await self.provider.get_aqi_history(city, hours)
        return {
            "city": city,
            "hours": hours,
            "records_count": len(history),
            "history": [h.model_dump() for h in history]
        }

    # Tool 4: get_pollution_trend
    async def tool_get_pollution_trend(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        history = await self.provider.get_aqi_history(city, 24)
        if not history:
            return {"city": city, "trend": "STABLE", "delta_24h": 0}

        current_aqi = history[0].aqi
        past_aqi = history[-1].aqi
        delta = current_aqi - past_aqi
        
        if delta > 15:
            trend = "DETERIORATING"
        elif delta < -15:
            trend = "IMPROVING"
        else:
            trend = "STABLE"

        return {
            "city": city,
            "current_aqi": current_aqi,
            "aqi_24h_ago": past_aqi,
            "delta_24h": delta,
            "trend": trend,
            "analysis": f"Air quality in {city} is {trend.lower()} over the past 24 hours (change of {delta:+d} AQI points)."
        }

    # Tool 5: get_weather
    async def tool_get_weather(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        wth = await self.provider.get_weather(city)
        return wth.model_dump()

    # Tool 6: get_forecast
    async def tool_get_forecast(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        hours = int(args.get("hours", 24))
        fc = await self.provider.get_forecast(city, hours)
        return fc.model_dump()

    # Tool 7: get_monitoring_stations
    async def tool_get_monitoring_stations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city")
        stations = await self.provider.get_monitoring_stations(city)
        return {
            "city": city,
            "count": len(stations),
            "stations": [s.model_dump() for s in stations]
        }

    # Tool 8: get_nearby_monitoring_stations
    async def tool_get_nearby_monitoring_stations(self, args: Dict[str, Any]) -> Dict[str, Any]:
        lat = float(args.get("latitude", 37.7749))
        lon = float(args.get("longitude", -122.4194))
        stations = await self.provider.get_nearby_stations(lat, lon)
        return {
            "latitude": lat,
            "longitude": lon,
            "count": len(stations),
            "stations": [s.model_dump() for s in stations]
        }

    # Tool 9: get_location_information
    async def tool_get_location_information(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        meta = self.provider._get_city_meta(city)
        return {
            "city": city.title(),
            "state": meta.get("state"),
            "country": meta.get("country", "USA"),
            "latitude": meta["lat"],
            "longitude": meta["lon"],
            "base_aqi": meta.get("base_aqi", 50)
        }

    # Tool 10: get_pollution_sources
    async def tool_get_pollution_sources(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city_or_lat", "San Francisco")
        return {
            "city": city,
            "primary_sources": [
                {"source": "Vehicular Exhaust & Transportation", "contribution_percent": 42},
                {"source": "Industrial Emissions & Power", "contribution_percent": 28},
                {"source": "Residential Heating & Wood Smoke", "contribution_percent": 18},
                {"source": "Secondary Photochemical Formation (Ozone)", "contribution_percent": 12},
            ],
            "confidence": "HIGH",
            "source_inventory": "EPA National Emissions Inventory (NEI)"
        }

    # Tool 11: get_user_alert_preferences
    async def tool_get_user_alert_preferences(self, args: Dict[str, Any]) -> Dict[str, Any]:
        user_id = args.get("user_id", "default_user")
        pref = self.alert_prefs_db.get(user_id, {
            "user_id": user_id,
            "city": "San Francisco",
            "aqi_threshold": 100,
            "is_active": True
        })
        return pref

    # Tool 12: save_alert_preference
    async def tool_save_alert_preference(self, args: Dict[str, Any]) -> Dict[str, Any]:
        user_id = args.get("user_id", "default_user")
        city = args.get("city", "San Francisco")
        threshold = int(args.get("aqi_threshold", 100))
        pref = {
            "user_id": user_id,
            "city": city,
            "aqi_threshold": threshold,
            "channels": args.get("channels", ["in_app"]),
            "is_active": True
        }
        self.alert_prefs_db[user_id] = pref
        return {"status": "SAVED", "preference": pref}

    # Tool 13: create_alert
    async def tool_create_alert(self, args: Dict[str, Any]) -> Dict[str, Any]:
        alert_item = {
            "alert_id": f"alt_{len(self.active_alerts_db)+1:04d}",
            "city": args.get("city", "San Francisco"),
            "severity": args.get("severity", "WARNING"),
            "reason": args.get("reason", "AQI threshold exceeded"),
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "status": "ACTIVE"
        }
        self.active_alerts_db.append(alert_item)
        return {"status": "CREATED", "alert": alert_item}

    # Tool 14: get_active_alerts
    async def tool_get_active_alerts(self, args: Dict[str, Any]) -> Dict[str, Any]:
        city = args.get("city")
        if city:
            filtered = [a for a in self.active_alerts_db if a.get("city", "").lower() == city.lower()]
        else:
            filtered = self.active_alerts_db
        return {
            "count": len(filtered),
            "alerts": filtered
        }
