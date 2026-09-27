import re
from typing import Dict, Any

class LocationAgent:
    """Agent responsible for identifying and resolving location from user prompt."""

    def __init__(self, default_city: str = "San Francisco"):
        self.default_city = default_city

    async def resolve_location(self, user_query: str, current_location: str = None) -> Dict[str, Any]:
        query_lower = user_query.lower()
        
        # Match cities
        known_cities = [
            "san francisco", "los angeles", "new york", "seattle", "chicago",
            "houston", "phoenix", "denver", "boston", "atlanta", "miami",
            "london", "beijing", "delhi", "tokyo", "sydney", "paris"
        ]
        
        resolved_city = None
        for c in known_cities:
            if c in query_lower:
                resolved_city = c.title()
                break

        if not resolved_city:
            resolved_city = current_location if current_location else self.default_city

        return {
            "city": resolved_city,
            "resolved_via": "NLP_PATTERN_MATCH" if resolved_city != self.default_city else "DEFAULT_FALLBACK"
        }
