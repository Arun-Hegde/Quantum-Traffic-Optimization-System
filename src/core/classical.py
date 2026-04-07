"""
Classical Dijkstra routing.
"""
import networkx as nx
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config.settings import SOURCE_NODE, TARGET_NODE, INTERSECTIONS


def classical_shortest_path(G: nx.Graph, source: int = SOURCE_NODE, target: int = TARGET_NODE):
    path = nx.shortest_path(G, source=source, target=target, weight="traffic")
    cost = compute_path_cost(path, G)
    return path, cost


def compute_path_cost(path, G: nx.Graph, alpha=1.0, beta=1.0, gamma=1.0):
    """Composite cost: alpha*traffic + beta*fuel + gamma*emissions + congestion interaction"""
    if not path or isinstance(path, str):
        return None
    
    traffic = sum(G[path[i]][path[i+1]]["traffic"] for i in range(len(path)-1))
    fuel = sum(G[path[i]][path[i+1]].get("fuel", 0) for i in range(len(path)-1))
    emissions = sum(G[path[i]][path[i+1]].get("emissions", 0) for i in range(len(path)-1))
    
    interaction = sum(
        G[path[i]][path[i+1]]["traffic"] * G[path[i+1]][path[i+2]]["traffic"] * 1.5 / 100.0
        for i in range(len(path)-2)
        if G.has_edge(path[i], path[i+1]) and G.has_edge(path[i+1], path[i+2])
    )
    return round(alpha*traffic + beta*fuel + gamma*emissions + interaction, 2)


def path_to_names(path, intersections=None):
    src = intersections or INTERSECTIONS
    return [src[n]["name"] for n in path]
