import json
import random
import math
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List

CITIES_50 = [
    ("San Francisco", 37.7749, -122.4194, "USA"),
    ("Los Angeles", 34.0522, -118.2437, "USA"),
    ("New York", 40.7128, -74.0060, "USA"),
    ("Seattle", 47.6062, -122.3321, "USA"),
    ("Chicago", 41.8781, -87.6298, "USA"),
    ("Houston", 29.7604, -95.3698, "USA"),
    ("Phoenix", 33.4484, -112.0740, "USA"),
    ("Denver", 39.7392, -104.9903, "USA"),
    ("Boston", 42.3601, -71.0589, "USA"),
    ("Atlanta", 33.7490, -84.3880, "USA"),
    ("Miami", 25.7617, -80.1918, "USA"),
    ("Dallas", 32.7767, -96.7970, "USA"),
    ("San Diego", 32.7157, -117.1611, "USA"),
    ("Portland", 45.5152, -122.6784, "USA"),
    ("Las Vegas", 36.1699, -115.1398, "USA"),
    ("London", 51.5074, -0.1278, "UK"),
    ("Paris", 48.8566, 2.3522, "France"),
    ("Berlin", 52.5200, 13.4050, "Germany"),
    ("Tokyo", 35.6762, 139.6503, "Japan"),
    ("Beijing", 39.9042, 116.4074, "China"),
    ("Delhi", 28.6139, 77.2090, "India"),
    ("Mumbai", 19.0760, 72.8777, "India"),
    ("Sydney", -33.8688, 151.2093, "Australia"),
    ("Toronto", 43.6532, -79.3832, "Canada"),
    ("Vancouver", 49.2827, -123.1207, "Canada"),
    ("Mexico City", 19.4326, -99.1332, "Mexico"),
    ("Sao Paulo", -23.5505, -46.6333, "Brazil"),
    ("Buenos Aires", -34.6037, -58.3816, "Argentina"),
    ("Cairo", 30.0444, 31.2357, "Egypt"),
    ("Johannesburg", -26.2041, 28.0473, "South Africa"),
    ("Seoul", 37.5665, 126.9780, "South Korea"),
    ("Bangkok", 13.7563, 100.5018, "Thailand"),
    ("Singapore", 1.3521, 103.8198, "Singapore"),
    ("Jakarta", -6.2088, 106.8456, "Indonesia"),
    ("Istanbul", 41.0082, 28.9784, "Turkey"),
    ("Rome", 41.9028, 12.4964, "Italy"),
    ("Madrid", 40.4168, -3.7038, "Spain"),
    ("Amsterdam", 52.3676, 4.9041, "Netherlands"),
    ("Vienna", 48.2082, 16.3738, "Austria"),
    ("Zurich", 47.3769, 8.5417, "Switzerland"),
    ("Dubai", 25.2048, 55.2708, "UAE"),
    ("Riyadh", 24.7136, 46.6753, "Saudi Arabia"),
    ("Warsaw", 52.2297, 21.0122, "Poland"),
    ("Prague", 50.0755, 14.4378, "Czech Republic"),
    ("Stockholm", 59.3293, 18.0686, "Sweden"),
    ("Oslo", 59.9139, 10.7522, "Norway"),
    ("Copenhagen", 55.6761, 12.5683, "Denmark"),
    ("Helsinki", 60.1699, 24.9384, "Finland"),
    ("Auckland", -36.8485, 174.7633, "New Zealand"),
    ("Dublin", 53.3498, -6.2603, "Ireland"),
]

def generate_synthetic_dataset() -> Dict[str, Any]:
    """Generate 50 locations, 100 monitoring stations, 10,000 pollution observations,
    5,000 weather observations, 1,000 alert events, 100 user alert configs."""
    random.seed(42)
    now = datetime.now(timezone.utc)

    # 1. Locations (50)
    locations = []
    for idx, (city, lat, lon, country) in enumerate(CITIES_50, 1):
        locations.append({
            "location_id": f"loc_{idx:03d}",
            "city": city,
            "latitude": lat,
            "longitude": lon,
            "country": country
        })

    # 2. Monitoring Stations (100 - 2 per location)
    stations = []
    for loc in locations:
        c_title = loc["city"]
        stations.append({
            "station_id": f"stn_{loc['location_id']}_a",
            "name": f"{c_title} Central Urban Station",
            "operator": "National Air Quality Agency",
            "city": c_title,
            "latitude": loc["latitude"],
            "longitude": loc["longitude"],
            "is_active": True
        })
        stations.append({
            "station_id": f"stn_{loc['location_id']}_b",
            "name": f"{c_title} Industrial Suburb Station",
            "operator": "Regional Environmental Council",
            "city": c_title,
            "latitude": loc["latitude"] + 0.02,
            "longitude": loc["longitude"] + 0.03,
            "is_active": True
        })

    # 3. Pollution Observations (10,000 - 100 stations x 100 hourly steps)
    pollution_observations = []
    for stn in stations:
        base_aqi = random.randint(30, 140)
        for step in range(100):
            t = now - timedelta(hours=step)
            aqi_val = max(10, min(450, int(base_aqi + math.sin(step / 4.0) * 25.0 + random.randint(-8, 8))))
            pollution_observations.append({
                "observation_id": f"obs_{stn['station_id']}_{step}",
                "station_id": stn["station_id"],
                "city": stn["city"],
                "timestamp": t.isoformat(),
                "aqi": aqi_val,
                "pm25": round(aqi_val * 0.28, 1),
                "pm10": round(aqi_val * 0.55, 1),
                "no2": round(aqi_val * 0.18, 1),
                "o3": round(aqi_val * 0.22, 1),
                "so2": round(aqi_val * 0.05, 1),
                "co": round(aqi_val * 0.01, 2),
                "primary_pollutant": "PM2.5"
            })

    # 4. Weather Observations (5,000 - 50 locations x 100 hourly steps)
    weather_observations = []
    for loc in locations:
        for step in range(100):
            t = now - timedelta(hours=step)
            weather_observations.append({
                "weather_id": f"wth_{loc['location_id']}_{step}",
                "city": loc["city"],
                "timestamp": t.isoformat(),
                "temp_c": round(20.0 + math.sin(step / 6.0) * 5.0, 1),
                "humidity": round(60.0 + math.cos(step / 6.0) * 15.0, 1),
                "wind_speed_kmh": round(10.0 + random.uniform(0, 12), 1),
                "condition": "Clear" if step % 2 == 0 else "Partly Cloudy"
            })

    # 5. User Alert Configurations (100)
    user_alert_configs = []
    for i in range(1, 101):
        loc = random.choice(locations)
        user_alert_configs.append({
            "config_id": f"cfg_{i:03d}",
            "user_id": f"usr_{i:03d}",
            "city": loc["city"],
            "aqi_threshold": random.choice([75, 100, 120, 150]),
            "pm25_threshold": 35.4,
            "notify_rapid_deterioration": True,
            "is_active": True
        })

    # 6. Alert Events (1,000)
    alert_events = []
    for i in range(1, 1001):
        cfg = random.choice(user_alert_configs)
        t = now - timedelta(hours=random.randint(1, 200))
        measured = cfg["aqi_threshold"] + random.randint(5, 50)
        alert_events.append({
            "alert_id": f"alt_{i:04d}",
            "config_id": cfg["config_id"],
            "user_id": cfg["user_id"],
            "city": cfg["city"],
            "severity": "WARNING" if measured < 150 else "HIGH",
            "trigger_reason": f"AQI reached {measured}, crossing user threshold of {cfg['aqi_threshold']}.",
            "metric_name": "AQI",
            "measured_value": float(measured),
            "threshold_value": float(cfg["aqi_threshold"]),
            "timestamp": t.isoformat(),
            "recommended_action": "Reduce heavy outdoor exertion and close windows if sensitive."
        })

    return {
        "locations": locations,
        "stations": stations,
        "pollution_observations": pollution_observations,
        "weather_observations": weather_observations,
        "user_alert_configs": user_alert_configs,
        "alert_events": alert_events
    }
