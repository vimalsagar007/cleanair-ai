from typing import Dict, Any, List
from rag.citations import CitationBuilder

class FinalResponseAgent:
    """Assembles final response without exposing chain-of-thought, embedding verified citations."""

    @staticmethod
    def assemble_response(
        query: str,
        city: str,
        aqi_data: Dict[str, Any],
        weather_data: Dict[str, Any],
        trend_data: Dict[str, Any],
        health_contexts: List[Any],
        alert_info: Dict[str, Any],
        grounding_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        
        if not grounding_result.get("is_valid", False):
            return {
                "answer": "Insufficient verified information to provide a reliable recommendation.",
                "grounding_status": "FAILED",
                "citations": [],
                "data_summary": {}
            }

        aqi_val = aqi_data.get("aqi", "N/A")
        category = aqi_data.get("category", "Moderate")
        primary_pollutant = aqi_data.get("primary_pollutant", "PM2.5")
        station_name = aqi_data.get("station_name", f"{city} Air Station")
        timestamp = aqi_data.get("timestamp", "")
        
        temp = weather_data.get("temperature_c", "N/A")
        wind_speed = weather_data.get("wind_speed_kmh", "N/A")
        wind_dir = weather_data.get("wind_direction_cardinal", "")

        trend = trend_data.get("trend", "STABLE")
        delta = trend_data.get("delta_24h", 0)

        # Build response text
        body = f"### Current Air Quality Overview for {city}\n\n"
        body += f"* **AQI Level:** **{aqi_val}** ({category})\n"
        body += f"* **Primary Pollutant:** {primary_pollutant}\n"
        body += f"* **Monitoring Station:** {station_name}\n"
        body += f"* **Data Timestamp:** {timestamp}\n"
        body += f"* **Weather Conditions:** {temp}°C | Wind: {wind_speed} km/h {wind_dir}\n"
        body += f"* **24-Hour Trend:** {trend.capitalize()} ({delta:+d} AQI points in past 24h)\n\n"

        body += "### Recommended Safety Precautions\n"
        for idx, ctx in enumerate(health_contexts, 1):
            body += f"- {ctx.content[:200]}... **[{idx}]**\n"

        if alert_info.get("alert_triggered"):
            event = alert_info.get("event", {})
            body += f"\n> **⚠️ Active Air Quality Alert:** {event.get('trigger_reason', 'Threshold exceeded')}\n"

        citation_out = CitationBuilder.format_citations(health_contexts)
        body += citation_out["formatted_markdown"]

        return {
            "answer": body,
            "grounding_status": "PASSED",
            "citations": citation_out["citations"],
            "data_summary": {
                "city": city,
                "aqi": aqi_val,
                "category": category,
                "primary_pollutant": primary_pollutant,
                "station": station_name,
                "timestamp": timestamp,
                "weather": f"{temp}°C, Wind {wind_speed} km/h",
                "trend": trend
            }
        }
