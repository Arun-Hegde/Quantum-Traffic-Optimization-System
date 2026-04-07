"""
Plotly chart visualizations.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import networkx as nx
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config.settings import INTERSECTIONS
from src.simulation.traffic_simulation import get_traffic_color

_DARK = "#0f172a"
_CARD = "#1e293b"
_TEXT = "white"


def cost_comparison_chart(classical_cost: int, quantum_cost) -> go.Figure:
    labels = ["Classical (Dijkstra)", "Quantum (QAOA)"]
    values = [classical_cost, quantum_cost if quantum_cost is not None else 0]
    colors = ["#3b82f6", "#a855f7"]
    valid  = [True, quantum_cost is not None]

    fig = go.Figure()
    for label, val, color, ok in zip(labels, values, colors, valid):
        fig.add_trace(go.Bar(
            name=label, x=[label], y=[val],
            marker_color=color, opacity=0.9 if ok else 0.3,
            text=[str(val) if ok else "N/A"], textposition="outside",
            textfont=dict(size=16, color=_TEXT),
        ))

    winner = "Quantum 🏆" if (quantum_cost and quantum_cost < classical_cost) else "Classical 🏆"
    fig.update_layout(
        title=dict(text=f"<b>Route Cost Comparison</b> — Winner: {winner}",
                   x=0.5, font=dict(size=17, color=_TEXT)),
        paper_bgcolor=_DARK, plot_bgcolor=_CARD,
        font=dict(color=_TEXT, family="Inter, Arial"),
        barmode="group", showlegend=False,
        xaxis=dict(gridcolor="#334155"), yaxis=dict(gridcolor="#334155"),
        margin=dict(t=60, b=40),
    )
    return fig


def edge_traffic_heatmap(G: nx.Graph, intersections=None) -> go.Figure:
    src = intersections or INTERSECTIONS
    rows = []
    for u, v, d in G.edges(data=True):
        rows.append({
            "Road": f"{src.get(u,{}).get('name',u)} → {src.get(v,{}).get('name',v)}",
            "Traffic": d.get("traffic", 0),
            "Status": "Free" if d.get("traffic",0) <= 8 else ("Moderate" if d.get("traffic",0) <= 17 else "Congested"),
        })
    df = pd.DataFrame(rows).sort_values("Traffic", ascending=False)

    fig = px.bar(df, x="Traffic", y="Road", orientation="h",
                 color="Traffic", color_continuous_scale=["#22c55e","#f97316","#ef4444"],
                 text="Traffic")
    fig.update_layout(
        title=dict(text="<b>Edge Traffic Heatmap</b>", x=0.5, font=dict(size=17, color=_TEXT)),
        paper_bgcolor=_DARK, plot_bgcolor=_CARD,
        font=dict(color=_TEXT), coloraxis_showscale=False,
        margin=dict(t=60, l=180, b=40),
    )
    fig.update_traces(textposition="outside", textfont_color=_TEXT)
    return fig


def path_breakdown_chart(G: nx.Graph, classical_path, quantum_path, intersections=None) -> go.Figure:
    src = intersections or INTERSECTIONS
    fig = go.Figure()

    def add_path(path, color, name):
        if not path or isinstance(path, str):
            return
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            if G.has_edge(u, v):
                t = G[u][v]["traffic"]
                label = f"{src.get(u,{}).get('name',u)} → {src.get(v,{}).get('name',v)}"
                fig.add_trace(go.Bar(name=f"{name}: {label}", x=[label], y=[t],
                                     marker_color=color, opacity=0.85,
                                     text=[str(t)], textposition="outside",
                                     textfont=dict(color=_TEXT)))

    add_path(classical_path, "#3b82f6", "Classical")
    add_path(quantum_path,   "#a855f7", "Quantum")

    fig.update_layout(
        title=dict(text="<b>Path Edge Traffic Breakdown</b>", x=0.5, font=dict(size=17, color=_TEXT)),
        paper_bgcolor=_DARK, plot_bgcolor=_CARD,
        font=dict(color=_TEXT), barmode="group",
        xaxis=dict(gridcolor="#334155"), yaxis=dict(gridcolor="#334155"),
        margin=dict(t=60, b=80),
    )
    return fig


def quantum_win_rate_chart(history: list) -> go.Figure:
    """Pie chart of quantum vs classical wins from history."""
    q_wins = sum(1 for r in history if r.get("quantum_advantage"))
    c_wins = len(history) - q_wins
    fig = go.Figure(go.Pie(
        labels=["Quantum Wins", "Classical Wins"],
        values=[q_wins, c_wins],
        marker_colors=["#a855f7", "#3b82f6"],
        hole=0.45,
        textinfo="label+percent",
        textfont=dict(size=14, color=_TEXT),
    ))
    fig.update_layout(
        title=dict(text="<b>Quantum vs Classical Win Rate</b>", x=0.5, font=dict(size=17, color=_TEXT)),
        paper_bgcolor=_DARK, font=dict(color=_TEXT),
        showlegend=False, margin=dict(t=60),
    )
    return fig


def runtime_trend_chart(history: list) -> go.Figure:
    """Line chart of optimization runtime over time."""
    if not history:
        return go.Figure()
    times   = [r.get("timestamp", "")[:19] for r in history]
    runtimes= [r.get("runtime_seconds", 0) for r in history]
    fig = go.Figure(go.Scatter(
        x=times, y=runtimes, mode="lines+markers",
        line=dict(color="#22d3ee", width=2),
        marker=dict(size=7, color="#22d3ee"),
    ))
    fig.update_layout(
        title=dict(text="<b>Optimization Runtime Trend</b>", x=0.5, font=dict(size=17, color=_TEXT)),
        paper_bgcolor=_DARK, plot_bgcolor=_CARD,
        font=dict(color=_TEXT),
        xaxis=dict(gridcolor="#334155", title="Time"),
        yaxis=dict(gridcolor="#334155", title="Seconds"),
        margin=dict(t=60),
    )
    return fig
