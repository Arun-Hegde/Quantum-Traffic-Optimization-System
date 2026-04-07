"""
Multi-city road network definitions with real GPS coordinates.
"""

CITIES = {
    "hyderabad": {
        "name": "Hyderabad", "country": "India",
        "center": (17.4065, 78.4772), "timezone": "Asia/Kolkata",
        "intersections": {
            0: {"name": "HITEC City",    "lat": 17.4435, "lon": 78.3772, "color": "#22d3ee"},
            1: {"name": "Gachibowli",    "lat": 17.4401, "lon": 78.3489, "color": "#a78bfa"},
            2: {"name": "Jubilee Hills", "lat": 17.4316, "lon": 78.4119, "color": "#fb923c"},
            3: {"name": "Banjara Hills", "lat": 17.4156, "lon": 78.4385, "color": "#34d399"},
            4: {"name": "Ameerpet",      "lat": 17.4374, "lon": 78.4487, "color": "#f472b6"},
            5: {"name": "Secunderabad",  "lat": 17.4399, "lon": 78.4983, "color": "#fbbf24"},
        },
        "roads": [(0,1),(0,2),(1,2),(1,3),(2,3),(2,4),(3,4),(3,5),(4,5)],
    },
    "bangalore": {
        "name": "Bangalore", "country": "India",
        "center": (12.9716, 77.5946), "timezone": "Asia/Kolkata",
        "intersections": {
            0: {"name": "Electronic City", "lat": 12.8456, "lon": 77.6603, "color": "#22d3ee"},
            1: {"name": "Koramangala",     "lat": 12.9352, "lon": 77.6245, "color": "#a78bfa"},
            2: {"name": "Indiranagar",     "lat": 12.9784, "lon": 77.6408, "color": "#fb923c"},
            3: {"name": "MG Road",         "lat": 12.9759, "lon": 77.6061, "color": "#34d399"},
            4: {"name": "Whitefield",      "lat": 12.9698, "lon": 77.7499, "color": "#f472b6"},
            5: {"name": "Hebbal",          "lat": 13.0358, "lon": 77.5970, "color": "#fbbf24"},
        },
        "roads": [(0,1),(1,2),(1,3),(2,3),(2,4),(3,5),(4,5),(0,3)],
    },
    "mumbai": {
        "name": "Mumbai", "country": "India",
        "center": (19.0760, 72.8777), "timezone": "Asia/Kolkata",
        "intersections": {
            0: {"name": "Bandra",   "lat": 19.0596, "lon": 72.8295, "color": "#22d3ee"},
            1: {"name": "Andheri",  "lat": 19.1136, "lon": 72.8697, "color": "#a78bfa"},
            2: {"name": "Powai",    "lat": 19.1176, "lon": 72.9060, "color": "#fb923c"},
            3: {"name": "Dadar",    "lat": 19.0178, "lon": 72.8478, "color": "#34d399"},
            4: {"name": "Worli",    "lat": 19.0176, "lon": 72.8170, "color": "#f472b6"},
            5: {"name": "Colaba",   "lat": 18.9067, "lon": 72.8147, "color": "#fbbf24"},
        },
        "roads": [(0,1),(0,3),(0,4),(1,2),(2,3),(3,4),(3,5),(4,5)],
    },
    "newyork": {
        "name": "New York", "country": "USA",
        "center": (40.7128, -74.0060), "timezone": "America/New_York",
        "intersections": {
            0: {"name": "Times Square",   "lat": 40.7580, "lon": -73.9855, "color": "#22d3ee"},
            1: {"name": "Central Park",   "lat": 40.7829, "lon": -73.9654, "color": "#a78bfa"},
            2: {"name": "Brooklyn Bridge","lat": 40.7061, "lon": -73.9969, "color": "#fb923c"},
            3: {"name": "Wall Street",    "lat": 40.7074, "lon": -74.0113, "color": "#34d399"},
            4: {"name": "JFK Airport",    "lat": 40.6413, "lon": -73.7781, "color": "#f472b6"},
            5: {"name": "LaGuardia",      "lat": 40.7769, "lon": -73.8740, "color": "#fbbf24"},
        },
        "roads": [(0,1),(0,2),(0,3),(1,5),(2,3),(2,4),(3,4),(4,5)],
    },
    "london": {
        "name": "London", "country": "UK",
        "center": (51.5074, -0.1278), "timezone": "Europe/London",
        "intersections": {
            0: {"name": "Piccadilly Circus","lat": 51.5100, "lon": -0.1347, "color": "#22d3ee"},
            1: {"name": "Oxford Street",    "lat": 51.5154, "lon": -0.1419, "color": "#a78bfa"},
            2: {"name": "Tower Bridge",     "lat": 51.5055, "lon": -0.0754, "color": "#fb923c"},
            3: {"name": "Westminster",      "lat": 51.4995, "lon": -0.1248, "color": "#34d399"},
            4: {"name": "Canary Wharf",     "lat": 51.5054, "lon": -0.0235, "color": "#f472b6"},
            5: {"name": "Heathrow",         "lat": 51.4700, "lon": -0.4543, "color": "#fbbf24"},
        },
        "roads": [(0,1),(0,2),(0,3),(1,5),(2,3),(2,4),(3,5),(4,5)],
    },
    "tokyo": {
        "name": "Tokyo", "country": "Japan",
        "center": (35.6762, 139.6503), "timezone": "Asia/Tokyo",
        "intersections": {
            0: {"name": "Shibuya",       "lat": 35.6595, "lon": 139.7004, "color": "#22d3ee"},
            1: {"name": "Shinjuku",      "lat": 35.6938, "lon": 139.7034, "color": "#a78bfa"},
            2: {"name": "Ginza",         "lat": 35.6717, "lon": 139.7650, "color": "#fb923c"},
            3: {"name": "Tokyo Station", "lat": 35.6812, "lon": 139.7671, "color": "#34d399"},
            4: {"name": "Roppongi",      "lat": 35.6627, "lon": 139.7298, "color": "#f472b6"},
            5: {"name": "Narita Airport","lat": 35.7720, "lon": 140.3929, "color": "#fbbf24"},
        },
        "roads": [(0,1),(0,4),(1,2),(1,3),(2,3),(2,5),(3,5),(4,5)],
    },
    "quantum_metropolis": {
        "name": "Quantum Metropolis", "country": "Future",
        "center": (17.4, 78.4), "timezone": "UTC",
        "intersections": {
            0: {"name": "Nexus Hub", "lat": 17.45, "lon": 78.35, "color": "#22d3ee"},
            1: {"name": "Cyber Node", "lat": 17.46, "lon": 78.40, "color": "#a78bfa"},
            2: {"name": "Data Center Alpha", "lat": 17.45, "lon": 78.45, "color": "#fb923c"},
            3: {"name": "Holo District", "lat": 17.40, "lon": 78.34, "color": "#34d399"},
            4: {"name": "Core Router", "lat": 17.40, "lon": 78.40, "color": "#f472b6"},
            5: {"name": "Qubit Square", "lat": 17.40, "lon": 78.46, "color": "#fbbf24"},
            6: {"name": "Aero Port", "lat": 17.35, "lon": 78.35, "color": "#22d3ee"},
            7: {"name": "Tech Park", "lat": 17.34, "lon": 78.40, "color": "#a78bfa"},
            8: {"name": "Neo Downtown", "lat": 17.35, "lon": 78.45, "color": "#fb923c"},
            9: {"name": "Silicon Way", "lat": 17.43, "lon": 78.37, "color": "#34d399"},
            10: {"name": "Energy Grid", "lat": 17.43, "lon": 78.43, "color": "#f472b6"},
            11: {"name": "Factory Zone", "lat": 17.37, "lon": 78.37, "color": "#fbbf24"},
            12: {"name": "Residential Ring", "lat": 17.37, "lon": 78.43, "color": "#22d3ee"},
            13: {"name": "Cloud Tower", "lat": 17.48, "lon": 78.40, "color": "#a78bfa"},
            14: {"name": "Deep Core", "lat": 17.32, "lon": 78.40, "color": "#fb923c"},
        },
        "roads": [
            (0,1),(0,3),(0,9),(1,2),(1,4),(1,13),(2,5),(2,10),(3,4),(3,6),(3,9),
            (4,5),(4,7),(4,9),(4,10),(4,11),(4,12),(5,8),(5,10),(6,7),(6,11),
            (7,8),(7,11),(7,12),(7,14),(8,12),(9,11),(10,12)
        ],
    },
}


def get_city_config(city_id: str):
    return CITIES.get(city_id.lower())


def list_available_cities():
    return [
        {"id": k, "name": v["name"], "country": v["country"], "center": v["center"]}
        for k, v in CITIES.items()
    ]
