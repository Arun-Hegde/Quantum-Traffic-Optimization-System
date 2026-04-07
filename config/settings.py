"""
Global configuration for the Quantum Traffic Optimization System.
"""

SOURCE_NODE = 0
TARGET_NODE = 5
NUM_QAOA_REPS = 3
MAX_OPTIMIZER_ITER = 100

CITY_NAME   = "Hyderabad"
CITY_CENTER = (17.4065, 78.4772)

INTERSECTIONS = {
    0: {"name": "HITEC City",    "lat": 17.4435, "lon": 78.3772, "color": "#22d3ee"},
    1: {"name": "Gachibowli",    "lat": 17.4401, "lon": 78.3489, "color": "#a78bfa"},
    2: {"name": "Jubilee Hills", "lat": 17.4316, "lon": 78.4119, "color": "#fb923c"},
    3: {"name": "Banjara Hills", "lat": 17.4156, "lon": 78.4385, "color": "#34d399"},
    4: {"name": "Ameerpet",      "lat": 17.4374, "lon": 78.4487, "color": "#f472b6"},
    5: {"name": "Secunderabad",  "lat": 17.4399, "lon": 78.4983, "color": "#fbbf24"},
}

ROAD_EDGES = [
    (0, 1), (0, 2),
    (1, 2), (1, 3),
    (2, 3), (2, 4),
    (3, 4), (3, 5),
    (4, 5),
]

TRAFFIC_LOW    = 8
TRAFFIC_MEDIUM = 17

APP_TITLE       = "🚦 Quantum Traffic Optimization System"
APP_SUBTITLE    = "QAOA + GenAI | Hyderabad Smart City"
ASSETS_DIR      = "assets"
MAP_OUTPUT_FILE = "assets/traffic_map.html"
