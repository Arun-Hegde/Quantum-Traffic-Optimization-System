"""
Streamlit frontend — Quantum Traffic Optimization System v3.0
Tabs: Dashboard | Real-World Map | Charts | AI Insights | History & Analytics
"""
import streamlit as st
import requests
import streamlit.components.v1 as components
import os, sys, time

ROOT = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, ROOT)

from config.settings import APP_TITLE, APP_SUBTITLE, INTERSECTIONS, MAP_OUTPUT_FILE, SOURCE_NODE, TARGET_NODE
from config.cities import list_available_cities, get_city_config

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Quantum Traffic Optimizer",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
html,body,[class*="css"]{font-family:'Inter',sans-serif;background:#0f172a;color:#f1f5f9}
.hero{background:linear-gradient(135deg,#0f172a 0%,#1a1040 50%,#0d1a2e 100%);
      border:1px solid #334155;border-radius:20px;padding:28px 40px;text-align:center;margin-bottom:20px}
.hero h1{font-size:2.2rem;font-weight:900;margin:0;
         background:linear-gradient(90deg,#38bdf8,#a78bfa,#f472b6);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:#94a3b8;font-size:1rem;margin:6px 0 0}
.metric-card{background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;
             border-radius:14px;padding:18px 22px;text-align:center;transition:transform .2s}
.metric-card:hover{transform:translateY(-3px);box-shadow:0 10px 30px rgba(139,92,246,.2)}
.metric-card .label{color:#94a3b8;font-size:.78rem;text-transform:uppercase;letter-spacing:1px}
.metric-card .value{color:#f1f5f9;font-size:1.9rem;font-weight:800;margin:6px 0 3px}
.metric-card .sub{color:#64748b;font-size:.75rem}
.path-pill{display:inline-block;background:rgba(56,189,248,.12);border:1px solid #38bdf8;
           border-radius:999px;padding:3px 12px;margin:3px;font-size:.8rem;color:#38bdf8}
.path-pill-q{background:rgba(244,63,94,.12);border-color:#f43f5e;color:#f43f5e}
.section-title{font-size:1.05rem;font-weight:700;color:#a78bfa;
               border-left:4px solid #a78bfa;padding-left:10px;margin:18px 0 10px}
.ai-report{background:#0f172a;border:1px solid #334155;border-radius:10px;padding:18px;
           font-family:'Courier New',monospace;font-size:.8rem;color:#94a3b8;
           white-space:pre-wrap;line-height:1.6;overflow-x:auto}
.status-box{padding:14px 22px;background:linear-gradient(135deg,#1e293b,#0f172a);
            border:1px solid #334155;border-radius:12px;text-align:center;margin-top:16px}
div[data-testid="stButton"]>button{
  background:linear-gradient(135deg,#7c3aed,#2563eb)!important;color:white!important;
  border:none!important;border-radius:10px!important;font-size:1rem!important;
  font-weight:700!important;padding:10px 36px!important;
  box-shadow:0 4px 18px rgba(124,58,237,.4)!important}
div[data-baseweb="tab-list"]{background:#1e293b;border-radius:10px;padding:3px}
div[data-baseweb="tab"]{border-radius:7px!important;color:#94a3b8!important}
div[aria-selected="true"][data-baseweb="tab"]{
  background:linear-gradient(135deg,#7c3aed,#2563eb)!important;color:white!important}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    # City selector
    cities = list_available_cities()
    city_names = {c["name"]: c["id"] for c in cities}
    selected_city_name = st.selectbox("🌍 Select City", list(city_names.keys()), index=0)
    selected_city_id   = city_names[selected_city_name]
    city_cfg = get_city_config(selected_city_id)

    intersections = city_cfg["intersections"]
    node_names = {v["name"]: k for k, v in intersections.items()}

    st.markdown("---")
    st.markdown("**🚦 Route Configuration**")
    src_name = st.selectbox("Source", list(node_names.keys()), index=0)
    tgt_name = st.selectbox("Destination", list(node_names.keys()), index=len(node_names)-1)
    src_node = node_names[src_name]
    tgt_node = node_names[tgt_name]

    st.markdown("---")
    st.markdown("**🔧 Options**")
    use_real_traffic = st.toggle("📡 Real-Time Traffic", value=False,
                                  help="Uses time-of-day mock traffic by default. "
                                       "Set GOOGLE_MAPS_API_KEY + OPENWEATHER_API_KEY for live data.")
    forecast_traffic_ui = st.toggle("🔮 1-Hour Forecast", value=False, help="Predict traffic conditions 1 hour into the future.")
    api_url = st.text_input("API URL", value="http://127.0.0.1:8000")

    st.markdown("---")
    st.markdown("**📍 Intersections**")
    for nid, meta in intersections.items():
        badge = " 🚦" if nid == src_node else (" 🏁" if nid == tgt_node else "")
        st.markdown(
            f"<span style='color:{meta['color']};font-size:.8rem'>● </span>"
            f"<span style='font-size:.8rem'>{meta['name']}{badge}</span>",
            unsafe_allow_html=True,
        )
    st.markdown("---")
    st.caption("Quantum Traffic Optimizer v3.0")

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>{APP_TITLE}</h1>
  <p>{APP_SUBTITLE}</p>
  <p style="color:#475569;font-size:.8rem;margin-top:8px">
    {selected_city_name} &nbsp;|&nbsp;
    {src_name} &nbsp;→&nbsp; {tgt_name}
  </p>
</div>
""", unsafe_allow_html=True)

# ── Run button ────────────────────────────────────────────────────────────────
col_btn, _ = st.columns([1, 4])
with col_btn:
    run = st.button("⚛️ Run Optimization", use_container_width=True)

# ── Main logic ────────────────────────────────────────────────────────────────
if run:
    if src_node == tgt_node:
        st.error("Source and destination must be different nodes.")
        st.stop()

    with st.spinner("⚛️ Running QAOA quantum optimization… (~10–20 seconds)"):
        try:
            resp = requests.get(
                f"{api_url}/run",
                params={
                    "city": selected_city_id,
                    "source": src_node,
                    "target": tgt_node,
                    "use_real_traffic": str(use_real_traffic).lower(),
                    "forecast": str(forecast_traffic_ui).lower(),
                },
                timeout=180,
            )
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.ConnectionError:
            st.error(
                "❌ Cannot connect to the FastAPI server.\n\n"
                "Run in a separate terminal:\n"
                "```\nuvicorn api.main:app --reload\n```"
            )
            st.stop()
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API Error {resp.status_code}: {resp.text}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            st.stop()

    st.success(f"✅ Optimization complete in **{data.get('runtime_seconds','?')}s** "
               f"| Run #{data.get('optimization_id','?')}")

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dashboard", "🗺️ Real-World Map", "📈 Charts", "🤖 AI Insights", "📜 History"
    ])

    # ════════════════════ TAB 1 — DASHBOARD ══════════════════════════════════
    with tab1:
        c_cost = data["classical_cost"]
        q_cost = data.get("quantum_cost")
        delta  = (c_cost - q_cost) if q_cost is not None else None

        m1, m2, m3, m4 = st.columns(4)
        def metric_card(col, label, value, sub, color):
            col.markdown(f"""<div class="metric-card">
              <div class="label">{label}</div>
              <div class="value" style="color:{color}">{value}</div>
              <div class="sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

        metric_card(m1, "Classical Cost", c_cost, "Dijkstra Algorithm", "#38bdf8")
        metric_card(m2, "Quantum Cost",
                    q_cost if q_cost is not None else "N/A", "QAOA Algorithm", "#a78bfa")
        d_str   = f"{delta:+.2f}" if delta is not None else "N/A"
        d_color = "#22c55e" if (delta and delta > 0) else "#f59e0b"
        metric_card(m3, "Cost Delta", d_str, "Classical − Quantum", d_color)
        metric_card(m4, "Runtime", f"{data.get('runtime_seconds','?')}s",
                    "Total Simulation", "#fb923c")
                    
        m5, m6, m7, m8 = st.columns(4)
        metric_card(m5, "Fuel Usage", f"{data.get('fuel_cost', 0.0)} L", "Liters (Q Path)", "#34d399")
        metric_card(m6, "Emissions", f"{data.get('emissions', 0.0)} kg", "kg CO₂ (Q Path)", "#f43f5e")
        metric_card(m7, "Hardware", f"{data.get('hardware_used', 'Unknown')}", "QPU / Simulator", "#a78bfa")
        metric_card(m8, "Network Size", f"{len(intersections)} Nodes", "Graph Scale", "#22d3ee")

        st.markdown(f"""<div class="status-box">
          <span style="font-size:1.2rem;font-weight:700">{data['status']}</span>
        </div>""", unsafe_allow_html=True)

        # Weather info
        if data.get("weather"):
            w = data["weather"]
            src_label = w.get("source", "")
            src_badge = (
                "🟢 Live" if "OpenWeather" in src_label
                else "🟡 Mock (enable OPENWEATHER_API_KEY for live)"
            )
            st.info(
                f"🌤️ **{w.get('condition')}** — {w.get('description')} | "
                f"🌡️ {w.get('temperature')}°C | 💨 {w.get('wind_speed')} m/s | "
                f"💧 {w.get('humidity')}% humidity | {src_badge}"
            )

        # Paths
        st.markdown("<div class='section-title'>🔵 Classical Route (Dijkstra)</div>",
                    unsafe_allow_html=True)
        c_names = data.get("classical_path_names", data["classical_path"])
        pills = " → ".join(f"<span class='path-pill'>{n}</span>" for n in c_names)
        st.markdown(f"<div style='margin:8px 0'>{pills}</div>", unsafe_allow_html=True)

        st.markdown("<div class='section-title'>🔴 Quantum Route (QAOA)</div>",
                    unsafe_allow_html=True)
        q_names = data.get("quantum_path_names", data["quantum_path"])
        if isinstance(q_names, list):
            q_pills = " → ".join(f"<span class='path-pill path-pill-q'>{n}</span>" for n in q_names)
            st.markdown(f"<div style='margin:8px 0'>{q_pills}</div>", unsafe_allow_html=True)
        else:
            st.warning(f"Quantum path: {q_names}")

        # NetworkX graph
        st.markdown("<div class='section-title'>🕸️ Traffic Network Graph</div>",
                    unsafe_allow_html=True)
        try:
            from src.simulation.traffic_simulation import create_traffic_graph, simulate_congestion
            from src.visualization.graph_viz import draw_traffic_graph, fig_to_bytes
            G_vis = simulate_congestion(create_traffic_graph(city_cfg))
            fig = draw_traffic_graph(
                G_vis,
                classical_path=data.get("classical_path"),
                quantum_path=data.get("quantum_path") if not isinstance(data.get("quantum_path"), str) else None,
                intersections=intersections,
                title=f"{selected_city_name} Traffic Network",
            )
            st.image(fig_to_bytes(fig), use_column_width=True)
        except Exception as e:
            import traceback
            st.warning(f"Graph unavailable: {e}")
            st.error(traceback.format_exc())

    # ════════════════════ TAB 2 — REAL-WORLD MAP ══════════════════════════════
    with tab2:
        st.markdown("""
        <div style="color:#94a3b8;font-size:.9rem;margin-bottom:10px">
        🗺️ Real-world OpenStreetMap with traffic-colored roads.<br/>
        <span style="color:#3b82f6">━━</span> Classical (Dijkstra) &nbsp;|&nbsp;
        <span style="color:#ef4444">━━</span> Quantum (QAOA) &nbsp;|&nbsp;
        Click markers for intersection details.
        </div>""", unsafe_allow_html=True)

        map_path = os.path.join(ROOT, MAP_OUTPUT_FILE)
        if os.path.exists(map_path):
            with open(map_path, "r", encoding="utf-8") as f:
                map_html = f.read()
            components.html(map_html, height=620, scrolling=False)
        else:
            # Generate map on the fly if not saved
            try:
                from src.simulation.traffic_simulation import create_traffic_graph, simulate_congestion
                from src.visualization.map_viz import build_map, save_map
                G_map = simulate_congestion(create_traffic_graph(city_cfg))
                fmap  = build_map(
                    G_map,
                    classical_path=data.get("classical_path"),
                    quantum_path=data.get("quantum_path") if not isinstance(data.get("quantum_path"), str) else None,
                    city_config=city_cfg,
                )
                save_map(fmap, MAP_OUTPUT_FILE)
                with open(MAP_OUTPUT_FILE, "r", encoding="utf-8") as f:
                    components.html(f.read(), height=620, scrolling=False)
            except Exception as e:
                st.error(f"Map generation failed: {e}")

    # ════════════════════ TAB 3 — CHARTS ══════════════════════════════════════
    with tab3:
        try:
            from src.simulation.traffic_simulation import create_traffic_graph, simulate_congestion
            from src.visualization.chart_viz import (
                cost_comparison_chart, edge_traffic_heatmap, path_breakdown_chart
            )
            G_ch = simulate_congestion(create_traffic_graph(city_cfg))

            col_a, col_b = st.columns(2)
            with col_a:
                st.plotly_chart(
                    cost_comparison_chart(data["classical_cost"], data.get("quantum_cost")),
                    use_container_width=True,
                )
            with col_b:
                st.plotly_chart(
                    edge_traffic_heatmap(G_ch, intersections),
                    use_container_width=True,
                )

            q_path_raw = data.get("quantum_path")
            if not isinstance(q_path_raw, str):
                st.plotly_chart(
                    path_breakdown_chart(G_ch, data["classical_path"], q_path_raw, intersections),
                    use_container_width=True,
                )
        except Exception as e:
            st.error(f"Charts error: {e}")

    # ════════════════════ TAB 4 — AI INSIGHTS ═════════════════════════════════
    with tab4:
        st.markdown("""
        <div style="color:#94a3b8;font-size:.9rem;margin-bottom:10px">
        🤖 AI-generated analysis comparing quantum vs classical routing performance.
        </div>""", unsafe_allow_html=True)
        st.markdown(f"<div class='ai-report'>{data['explanation']}</div>",
                    unsafe_allow_html=True)
        with st.expander("📦 Raw API Response"):
            st.json(data)

    # ════════════════════ TAB 5 — HISTORY & ANALYTICS ═════════════════════════
    with tab5:
        st.markdown("<div class='section-title'>📜 Recent Optimization Runs</div>",
                    unsafe_allow_html=True)
        try:
            hist_resp = requests.get(f"{api_url}/history",
                                     params={"city": selected_city_id, "limit": 20},
                                     timeout=10)
            hist_data = hist_resp.json()
            runs = hist_data.get("runs", [])

            if runs:
                import pandas as pd
                df = pd.DataFrame(runs)
                df["quantum_advantage"] = df["quantum_advantage"].map(
                    {True: "✅ Quantum", False: "⚠️ Classical", None: "—"}
                )
                st.dataframe(
                    df[["id","city","timestamp","classical_cost","quantum_cost",
                        "quantum_advantage","runtime_seconds"]],
                    use_container_width=True,
                )

                # Win rate chart
                from src.visualization.chart_viz import quantum_win_rate_chart, runtime_trend_chart
                col_c, col_d = st.columns(2)
                with col_c:
                    st.plotly_chart(quantum_win_rate_chart(hist_data["runs"]),
                                    use_container_width=True)
                with col_d:
                    st.plotly_chart(runtime_trend_chart(hist_data["runs"]),
                                    use_container_width=True)
            else:
                st.info("No history yet — run an optimization first.")
        except Exception as e:
            st.warning(f"History unavailable: {e}")

        # City analytics
        st.markdown("<div class='section-title'>📊 City Analytics</div>",
                    unsafe_allow_html=True)
        try:
            an_resp = requests.get(f"{api_url}/analytics/city/{selected_city_id}", timeout=10)
            an = an_resp.json()
            a1, a2, a3, a4 = st.columns(4)
            metric_card(a1, "Total Runs",    an.get("total_optimizations", 0), selected_city_name, "#38bdf8")
            metric_card(a2, "Quantum Wins",  an.get("quantum_wins", 0),        "QAOA victories",   "#a78bfa")
            metric_card(a3, "Classical Wins",an.get("classical_wins", 0),      "Dijkstra victories","#3b82f6")
            metric_card(a4, "Q Win Rate",    f"{an.get('quantum_win_rate',0)}%","Quantum advantage","#22c55e")
        except Exception as e:
            st.warning(f"Analytics unavailable: {e}")

# ── Welcome screen ────────────────────────────────────────────────────────────
else:
    st.markdown("""
    <div style="text-align:center;padding:60px 20px;color:#475569">
      <div style="font-size:4rem">⚛️</div>
      <h3 style="color:#64748b;font-weight:600;margin:12px 0 8px">
        Press <span style="color:#a78bfa">⚛️ Run Optimization</span> to begin
      </h3>
      <p style="font-size:.9rem">
        QAOA will optimize the selected city's traffic network in real time.
      </p>
      <p style="font-size:.8rem;margin-top:8px;color:#334155">
        Make sure the FastAPI server is running:<br/>
        <code style="background:#1e293b;padding:2px 10px;border-radius:6px;color:#38bdf8">
          uvicorn api.main:app --reload
        </code>
      </p>
    </div>

    <div style="display:flex;gap:16px;flex-wrap:wrap;justify-content:center;margin-top:20px">
      <div class="metric-card" style="min-width:160px">
        <div class="label">Cities</div>
        <div class="value" style="color:#38bdf8">6</div>
        <div class="sub">Global coverage</div>
      </div>
      <div class="metric-card" style="min-width:160px">
        <div class="label">Algorithm</div>
        <div class="value" style="color:#a78bfa">QAOA</div>
        <div class="sub">Quantum optimizer</div>
      </div>
      <div class="metric-card" style="min-width:160px">
        <div class="label">Map</div>
        <div class="value" style="color:#fb923c">OSM</div>
        <div class="sub">Real-world tiles</div>
      </div>
      <div class="metric-card" style="min-width:160px">
        <div class="label">Database</div>
        <div class="value" style="color:#22c55e">SQLite</div>
        <div class="sub">History tracking</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
