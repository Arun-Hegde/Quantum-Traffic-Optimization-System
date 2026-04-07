"""
Traffic simulation — builds real-world city road graphs with GPS coordinates.
"""
import random
import networkx as nx
from typing import Optional, Dict

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config.settings import INTERSECTIONS, ROAD_EDGES, TRAFFIC_LOW, TRAFFIC_MEDIUM


def create_traffic_graph(city_config: Optional[Dict] = None) -> nx.Graph:
    G = nx.Graph()
    intersections = city_config["intersections"] if city_config else INTERSECTIONS
    roads         = city_config["roads"]          if city_config else ROAD_EDGES

    for nid, meta in intersections.items():
        G.add_node(nid, name=meta["name"], lat=meta["lat"], lon=meta["lon"], color=meta["color"])

    for u, v in roads:
        lat_diff = abs(intersections[u]["lat"] - intersections[v]["lat"])
        lon_diff = abs(intersections[u]["lon"] - intersections[v]["lon"])
        dist_km  = round(((lat_diff**2 + lon_diff**2) ** 0.5) * 111, 2)
        fuel_cost = round(dist_km * random.uniform(0.5, 1.5), 2)
        emissions = round(dist_km * random.uniform(1.0, 3.0), 2)
        G.add_edge(u, v,
                   weight=dist_km,
                   fuel=fuel_cost,
                   emissions=emissions,
                   capacity=random.randint(800, 2000),
                   traffic=0,
                   road_name=f"{intersections[u]['name']} – {intersections[v]['name']}")
    return G


def simulate_congestion(G: nx.Graph, seed: Optional[int] = None) -> nx.Graph:
    if seed is not None:
        random.seed(seed)
    for u, v in G.edges():
        t = random.randint(1, 25)
        G[u][v]["traffic"] = t
        # Higher traffic slightly increases unit emissions due to idling
        G[u][v]["emissions"] = round(G[u][v]["emissions"] * (1 + t*0.02), 2)
    return G


def forecast_traffic(G: nx.Graph, hours_ahead: int = 1) -> nx.Graph:
    """Predicts future traffic by applying trend patterns + simulated peak hours."""
    from datetime import datetime
    current_hour = datetime.now().hour
    future_hour = (current_hour + hours_ahead) % 24
    
    # Simple peak-hour scaling logic (rush hour is 8-10 AM and 5-7 PM)
    peak_hours = [8, 9, 10, 17, 18, 19]
    is_now_peak = current_hour in peak_hours
    is_future_peak = future_hour in peak_hours
    
    multiplier = 1.0
    if not is_now_peak and is_future_peak:
        multiplier = 1.4  # Traffic building up
    elif is_now_peak and not is_future_peak:
        multiplier = 0.6  # Traffic dying down
    elif is_future_peak:
        multiplier = 1.1  # Still peak
    else:
        multiplier = 0.9  # Normal variance

    H = G.copy()
    for u, v in H.edges():
        t = H[u][v].get("traffic", 10)
        # Apply multiplier and add some random future variance
        t_future = int(min(25, max(1, (t * multiplier) + random.uniform(-2, 2))))
        H[u][v]["traffic"] = t_future
        H[u][v]["emissions"] = round(H[u][v].get("emissions", 1.0) * (1 + t_future*0.02), 2)
        
    return H


def get_traffic_color(traffic: int) -> str:
    if traffic <= TRAFFIC_LOW:    return "#22c55e"
    if traffic <= TRAFFIC_MEDIUM: return "#f97316"
    return "#ef4444"


def get_traffic_label(traffic: int) -> str:
    if traffic <= TRAFFIC_LOW:    return "Free Flow 🟢"
    if traffic <= TRAFFIC_MEDIUM: return "Moderate 🟡"
    return "Congested 🔴"
