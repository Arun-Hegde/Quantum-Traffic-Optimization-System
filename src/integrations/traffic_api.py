"""
Real-time traffic & weather API clients.

Real API mode: set GOOGLE_MAPS_API_KEY / OPENWEATHER_API_KEY in environment.
Mock mode (default): realistic time-of-day traffic simulation with congestion
hotspots, rush-hour patterns, and weather impact — no API keys needed.
"""
import os
import math
import random
import requests
from datetime import datetime
from typing import Optional, Dict


# ── Time-of-day traffic multipliers (24h) ────────────────────────────────────
# Models: night low → morning rush → midday moderate → evening rush → night low
_HOUR_MULTIPLIER = [
    0.3, 0.25, 0.2, 0.2, 0.25, 0.4,   # 00–05: night
    0.7, 1.0,  1.3, 1.2, 0.9, 0.8,    # 06–11: morning rush peaks at 08
    0.75, 0.7, 0.7, 0.8, 1.0, 1.4,    # 12–17: midday + evening rush peaks at 17
    1.3, 1.0,  0.8, 0.6, 0.5, 0.4,    # 18–23: evening taper
]

# City-specific congestion hotspot edges (node pairs that get extra traffic)
# Keyed by city name (lowercase). Each entry: list of (node_a, node_b, extra_traffic)
_CITY_HOTSPOTS = {
    "hyderabad": [(0, 2, 8), (2, 4, 10), (3, 5, 7)],
    "bangalore": [(1, 2, 9), (2, 4, 11), (0, 3, 6)],
    "mumbai":    [(0, 3, 10), (3, 4, 12), (3, 5, 8)],
    "new york":  [(0, 2, 11), (2, 3, 9), (0, 3, 7)],
    "london":    [(0, 3, 8), (2, 4, 10), (3, 5, 9)],
    "tokyo":     [(0, 1, 7), (1, 3, 11), (2, 5, 9)],
}


def _time_multiplier() -> float:
    """Return traffic multiplier for the current hour."""
    hour = datetime.now().hour
    return _HOUR_MULTIPLIER[hour]


def _apply_mock_real_traffic(G, city_name: str = "") -> bool:
    """
    Simulate real-time traffic with:
    - Time-of-day multiplier applied to all edges
    - City-specific congestion hotspots
    - Small random jitter (±2) to simulate sensor noise
    """
    mult   = _time_multiplier()
    city_k = city_name.lower()
    hotspots = {(min(a, b), max(a, b)): extra
                for a, b, extra in _CITY_HOTSPOTS.get(city_k, [])}

    for u, v in G.edges():
        base    = G[u][v].get("traffic", random.randint(5, 20))
        scaled  = base * mult
        jitter  = random.uniform(-2, 2)
        key     = (min(u, v), max(u, v))
        hotspot = hotspots.get(key, 0)
        G[u][v]["traffic"] = int(min(25, max(1, scaled + jitter + hotspot)))

    return True


class TrafficAPIClient:
    def __init__(self):
        self.google_key = os.getenv("GOOGLE_MAPS_API_KEY", "")
        self.tomtom_key = os.getenv("TOMTOM_API_KEY", "")

    def enrich_graph_with_real_traffic(self, G, intersections: Dict,
                                        city_name: str = "") -> bool:
        """
        Enrich graph edges with real-time traffic data.
        Uses Google Maps Distance Matrix API if key is set, otherwise
        falls back to realistic mock simulation.
        """
        if self.google_key:
            try:
                enriched = 0
                for u, v in G.edges():
                    origin = f"{intersections[u]['lat']},{intersections[u]['lon']}"
                    dest   = f"{intersections[v]['lat']},{intersections[v]['lon']}"
                    resp   = requests.get(
                        "https://maps.googleapis.com/maps/api/distancematrix/json",
                        params={
                            "origins":         origin,
                            "destinations":    dest,
                            "departure_time":  "now",
                            "traffic_model":   "best_guess",
                            "key":             self.google_key,
                        },
                        timeout=5,
                    )
                    data = resp.json()
                    el   = data["rows"][0]["elements"][0]
                    if el["status"] == "OK":
                        free_flow = el["duration"]["value"]
                        in_traffic = el.get("duration_in_traffic", el["duration"])["value"]
                        # Map delay ratio to 1-25 traffic scale
                        ratio = in_traffic / max(free_flow, 1)
                        G[u][v]["traffic"] = int(min(25, max(1, (ratio - 1) * 20 + 5)))
                        enriched += 1
                return enriched > 0
            except Exception as e:
                print(f"[TrafficAPI] Google Maps failed ({e})")
                
        # Fallback to TomTom if Google fails or isn't set
        if self.tomtom_key:
            try:
                enriched = 0
                for u, v in G.edges():
                    lat_o, lon_o = intersections[u]['lat'], intersections[u]['lon']
                    lat_d, lon_d = intersections[v]['lat'], intersections[v]['lon']
                    resp = requests.get(
                        f"https://api.tomtom.com/routing/1/calculateRoute/{lat_o},{lon_o}:{lat_d},{lon_d}/json",
                        params={"key": self.tomtom_key, "traffic": "true"},
                        timeout=5
                    )
                    data = resp.json()
                    if "routes" in data:
                        summary = data["routes"][0]["summary"]
                        travel_time = summary["travelTimeInSeconds"]
                        historic = summary.get("historicTravelTimeInSeconds", travel_time)
                        ratio = travel_time / max(historic, 1)
                        G[u][v]["traffic"] = int(min(25, max(1, (ratio - 1) * 20 + 5)))
                        enriched += 1
                return enriched > 0
            except Exception as e:
                print(f"[TrafficAPI] TomTom failed ({e}), using mock fallback")

        return _apply_mock_real_traffic(G, city_name)


class WeatherAPIClient:
    def __init__(self):
        self.key = os.getenv("OPENWEATHER_API_KEY", "")

    def get_weather(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Fetch current weather. Returns mock data if no API key is set.
        """
        if not self.key:
            return self._mock_weather(lat, lon)

        try:
            resp = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={"lat": lat, "lon": lon, "appid": self.key, "units": "metric"},
                timeout=5,
            )
            d = resp.json()
            return {
                "condition":   d["weather"][0]["main"],
                "description": d["weather"][0]["description"],
                "temperature": round(d["main"]["temp"], 1),
                "humidity":    d["main"]["humidity"],
                "wind_speed":  d["wind"]["speed"],
                "source":      "OpenWeatherMap",
            }
        except Exception as e:
            print(f"[WeatherAPI] OpenWeather failed ({e}), using mock")
            return self._mock_weather(lat, lon)

    def _mock_weather(self, lat: float, lon: float) -> Dict:
        """
        Deterministic mock weather based on lat/lon + current hour.
        Cycles through realistic conditions so the UI always shows something.
        """
        hour = datetime.now().hour
        # Vary condition by hour for demo realism
        conditions = [
            ("Clear",        "clear sky",          28.0, 45, 3.2),
            ("Clouds",       "scattered clouds",   25.0, 55, 4.1),
            ("Rain",         "light rain",         22.0, 78, 5.8),
            ("Clouds",       "broken clouds",      24.0, 60, 3.9),
            ("Clear",        "few clouds",         30.0, 40, 2.5),
            ("Thunderstorm", "thunderstorm",       19.0, 85, 8.2),
        ]
        idx = (int(abs(lat + lon)) + hour) % len(conditions)
        cond, desc, temp, hum, wind = conditions[idx]
        return {
            "condition":   cond,
            "description": desc,
            "temperature": temp,
            "humidity":    hum,
            "wind_speed":  wind,
            "source":      "Mock (set OPENWEATHER_API_KEY for live data)",
        }

    def get_traffic_impact_factor(self, weather: Optional[Dict]) -> float:
        """Return a traffic multiplier based on weather condition."""
        if not weather:
            return 1.0
        return {
            "Thunderstorm": 1.6,
            "Snow":         1.9,
            "Fog":          1.5,
            "Rain":         1.35,
            "Drizzle":      1.2,
            "Clouds":       1.1,
            "Clear":        1.0,
            "Haze":         1.15,
            "Mist":         1.2,
        }.get(weather.get("condition", ""), 1.0)
