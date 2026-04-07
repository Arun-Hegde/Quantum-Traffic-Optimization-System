"""
NetworkX graph visualization (headless Matplotlib).
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import io, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config.settings import INTERSECTIONS
from src.simulation.traffic_simulation import get_traffic_color


def draw_traffic_graph(G: nx.Graph,
                       classical_path=None,
                       quantum_path=None,
                       intersections=None,
                       title: str = "Traffic Network") -> plt.Figure:
    src = intersections or INTERSECTIONS
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#1e293b")

    # Support both string and int keys if JSON conversion happened
    def get_meta(nid):
        if nid in src: return src[nid]
        if str(nid) in src: return src[str(nid)]
        try:
            int_nid = int(nid)
            if int_nid in src: return src[int_nid]
        except: pass
        return {}

    pos = {n: (get_meta(n).get("lon", 0), get_meta(n).get("lat", 0)) for n in G.nodes() if get_meta(n)}

    # Edge colours by traffic
    edge_colors = [get_traffic_color(G[u][v].get("traffic", 1)) for u, v in G.edges()]
    edge_widths = [2 + G[u][v].get("traffic", 1) / 8 for u, v in G.edges()]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths,
                           alpha=0.8, ax=ax)

    # Classical path
    if classical_path and not isinstance(classical_path, str) and len(classical_path) > 1:
        c_edges = list(zip(classical_path, classical_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=c_edges,
                               edge_color="#3b82f6", width=5, style="dashed",
                               alpha=0.95, ax=ax)

    # Quantum path
    if quantum_path and not isinstance(quantum_path, str) and len(quantum_path) > 1:
        q_edges = list(zip(quantum_path, quantum_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=q_edges,
                               edge_color="#ef4444", width=5, alpha=0.95, ax=ax)

    # Nodes
    node_colors = [get_meta(n).get("color", "#64748b") for n in G.nodes()]
    
    # Robust node sizing
    valid_keys = []
    for k in src.keys():
        try: valid_keys.append(int(k))
        except: pass
    min_k = min(valid_keys) if valid_keys else -1
    max_k = max(valid_keys) if valid_keys else -1
    
    node_sizes = []
    for n in G.nodes():
        try:
            node_sizes.append(900 if int(n) in (min_k, max_k) else 600)
        except:
            node_sizes.append(600)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                           alpha=0.95, ax=ax)

    # Labels
    labels = {n: get_meta(n).get("name", str(n)) for n in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels,
                            font_size=8, font_color="white", font_weight="bold", ax=ax)

    # Edge traffic labels
    edge_labels = {(u, v): G[u][v].get("traffic", "") for u, v in G.edges()}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels,
                                 font_size=7, font_color="#94a3b8", ax=ax)

    # Legend
    patches = [
        mpatches.Patch(color="#22c55e", label="Free Flow"),
        mpatches.Patch(color="#f97316", label="Moderate"),
        mpatches.Patch(color="#ef4444", label="Congested"),
        mpatches.Patch(color="#3b82f6", label="Classical Path"),
        mpatches.Patch(color="#ef4444", label="Quantum Path"),
    ]
    ax.legend(handles=patches, loc="lower right", facecolor="#1e293b",
              edgecolor="#334155", labelcolor="white", fontsize=8)

    ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=12)
    ax.axis("off")
    plt.tight_layout()
    return fig


def fig_to_bytes(fig: plt.Figure) -> bytes:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=120, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return buf.read()
