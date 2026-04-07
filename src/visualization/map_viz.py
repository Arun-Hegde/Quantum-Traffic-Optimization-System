"""
Real-world interactive Folium map with OpenStreetMap tiles.
"""
import folium
from folium.plugins import MiniMap, Fullscreen, MousePosition
import os, sys
from typing import Optional, Dict
import networkx as nx

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config.settings import INTERSECTIONS, CITY_CENTER, MAP_OUTPUT_FILE, ASSETS_DIR, CITY_NAME
from src.simulation.traffic_simulation import get_traffic_color, get_traffic_label


def build_map(G: nx.Graph,
              classical_path=None,
              quantum_path=None,
              city_config: Optional[Dict] = None) -> folium.Map:

    intersections = city_config["intersections"] if city_config else INTERSECTIONS
    center        = city_config["center"]        if city_config else CITY_CENTER
    city_name     = city_config["name"]          if city_config else CITY_NAME

    source_node = min(intersections.keys())
    target_node = max(intersections.keys())

    fmap = folium.Map(location=center, zoom_start=13, tiles="OpenStreetMap")

    # ── Plugins ──────────────────────────────────────────────────────────────
    Fullscreen(position="topright").add_to(fmap)
    MiniMap(toggle_display=True).add_to(fmap)
    MousePosition().add_to(fmap)

    # ── All road edges coloured by traffic ───────────────────────────────────
    for u, v, data in G.edges(data=True):
        traffic   = data.get("traffic", 1)
        color     = get_traffic_color(traffic)
        label     = get_traffic_label(traffic)
        road_name = data.get("road_name", f"Road {u}–{v}")
        lat1, lon1 = intersections[u]["lat"], intersections[u]["lon"]
        lat2, lon2 = intersections[v]["lat"], intersections[v]["lon"]

        folium.PolyLine(
            [(lat1, lon1), (lat2, lon2)],
            color=color, weight=6, opacity=0.8,
            tooltip=f"🛣️ {road_name} | Traffic: {traffic} | {label}",
        ).add_to(fmap)

    # ── Classical path (blue dashed) ─────────────────────────────────────────
    if classical_path and not isinstance(classical_path, str) and len(classical_path) > 1:
        coords = [(intersections[n]["lat"], intersections[n]["lon"]) for n in classical_path]
        folium.PolyLine(coords, color="#3b82f6", weight=9, opacity=0.95,
                        dash_array="12", tooltip="🔵 Classical (Dijkstra) Path").add_to(fmap)

    # ── Quantum path (red solid) ─────────────────────────────────────────────
    if quantum_path and not isinstance(quantum_path, str) and len(quantum_path) > 1:
        coords = [(intersections[n]["lat"], intersections[n]["lon"]) for n in quantum_path]
        folium.PolyLine(coords, color="#ef4444", weight=9, opacity=0.95,
                        tooltip="🔴 Quantum (QAOA) Path").add_to(fmap)

    # ── Intersection markers ─────────────────────────────────────────────────
    for nid, meta in intersections.items():
        nbrs = [G[nid][nb]["traffic"] for nb in G.neighbors(nid) if G.has_edge(nid, nb)]
        avg  = round(sum(nbrs) / len(nbrs), 1) if nbrs else 0
        lbl  = get_traffic_label(int(avg))

        if nid == source_node:
            icon_color, icon_icon = "green", "play"
        elif nid == target_node:
            icon_color, icon_icon = "red", "stop"
        else:
            icon_color, icon_icon = "blue", "info-sign"

        popup_html = f"""
        <div style="font-family:Arial;min-width:190px;padding:4px">
          <h4 style="margin:4px 0;color:#1e293b">📍 {meta['name']}</h4>
          <hr style="margin:4px 0"/>
          <b>Node ID:</b> {nid}<br/>
          <b>GPS:</b> {meta['lat']:.4f}, {meta['lon']:.4f}<br/>
          <b>Avg Traffic:</b> {avg} — {lbl}<br/>
          {'<b style="color:green">🚦 SOURCE</b>' if nid == source_node else ''}
          {'<b style="color:red">🏁 DESTINATION</b>' if nid == target_node else ''}
        </div>"""

        folium.Marker(
            location=(meta["lat"], meta["lon"]),
            popup=folium.Popup(popup_html, max_width=230),
            tooltip=meta["name"],
            icon=folium.Icon(color=icon_color, icon=icon_icon, prefix="glyphicon"),
        ).add_to(fmap)

    # ── Legend ───────────────────────────────────────────────────────────────
    legend = """
    <div style="position:fixed;bottom:30px;left:30px;z-index:9999;
                background:rgba(15,23,42,0.93);color:#f1f5f9;
                padding:14px 18px;border-radius:12px;font-family:Arial;
                border:1px solid #334155;font-size:13px;line-height:1.8">
      <b style="font-size:14px">🗺️ Legend</b><br/>
      <span style="color:#22c55e">━━</span> Free Flow 🟢<br/>
      <span style="color:#f97316">━━</span> Moderate 🟡<br/>
      <span style="color:#ef4444">━━</span> Congested 🔴<br/>
      <span style="color:#3b82f6">╌╌</span> Classical (Dijkstra)<br/>
      <span style="color:#ef4444">━━</span> Quantum (QAOA)
    </div>"""
    fmap.get_root().html.add_child(folium.Element(legend))

    # ── Title overlay ────────────────────────────────────────────────────────
    title = f"""
    <div style="position:fixed;top:12px;left:50%;transform:translateX(-50%);
                z-index:9999;background:rgba(15,23,42,0.93);color:#f1f5f9;
                padding:10px 28px;border-radius:30px;font-family:Arial;
                border:1px solid #334155;font-size:15px;font-weight:bold;">
      🚦 {city_name} — Quantum Traffic Optimization
    </div>"""
    fmap.get_root().html.add_child(folium.Element(title))

    return fmap


def save_map(fmap: folium.Map, output_path: str = MAP_OUTPUT_FILE) -> str:
    os.makedirs(ASSETS_DIR, exist_ok=True)
    fmap.save(output_path)
    return output_path
