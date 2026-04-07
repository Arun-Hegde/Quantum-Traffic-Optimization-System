# 🚦 Quantum Traffic Optimization System with GenAI Smart Advisor

> **QAOA-powered smart city traffic routing** with real-time data integration, multi-city support, and GenAI-driven insights.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green.svg)](https://fastapi.tiangolo.com/)
[![Qiskit](https://img.shields.io/badge/Qiskit-1.0+-purple.svg)](https://qiskit.org/)

## 🌟 Features

### Core Capabilities
- ⚛️ **Quantum Optimization**: QAOA-based routing using Qiskit
- 🗺️ **Real-World Maps**: Interactive Folium maps with OpenStreetMap
- 🌍 **Multi-City Support**: 6 major cities (Hyderabad, Bangalore, Mumbai, New York, London, Tokyo)
- 📡 **Real-Time Traffic**: Integration with Google Maps & TomTom APIs
- 🌤️ **Weather-Aware**: Weather impact on traffic predictions
- 🤖 **GenAI Insights**: AI-powered route analysis and recommendations

### Professional Infrastructure
- 📚 **Documentation**: OpenAPI/Swagger auto-generated docs
- 📝 **Logging**: Structured logging with rotation

---

## 📁 Project Structure

```
quantum-traffic-optimization/
├── api/
│   └── main.py                      # FastAPI backend with all endpoints
├── config/
│   ├── settings.py                  # Global configuration
│   └── cities.py                    # Multi-city definitions
├── data/                            # Persistent SQLite storage
├── docs/
│   ├── architecture.md              # Architecture documentation
│   └── DEPLOYMENT.md                # Deployment documentation
├── frontend/
│   └── app.py                       # Streamlit dashboard
├── src/
│   ├── core/                        # Routing and optimization logic
│   ├── database/                    # SQLAlchemy models and connection
│   ├── integrations/                # External API clients
│   ├── simulation/                  # Traffic graph generation
│   ├── utils/                       # Shared utilities
│   └── visualization/               # Core visualization components
├── requirements.txt                 # Python dependencies
├── run.py                           # One-click launcher
└── streamlit_app.py                 # Streamlit Cloud entry point
```

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone <repository-url>
cd quantum-traffic-optimization

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Set environment variables for external APIs
# GOOGLE_MAPS_API_KEY, OPENWEATHER_API_KEY, TOMTOM_API_KEY

# 4. Start the application
python run.py

# Access:
# API:       http://localhost:8000
# Frontend:  http://localhost:8501
```

---

## 🌍 Supported Cities

| City | Country | Intersections | Features |
|------|---------|---------------|----------|
| 🇮🇳 Hyderabad | India | 6 | HITEC City, Gachibowli, Secunderabad |
| 🇮🇳 Bangalore | India | 6 | Electronic City, Koramangala, Whitefield |
| 🇮🇳 Mumbai | India | 6 | Bandra, Andheri, Colaba |
| 🇺🇸 New York | USA | 6 | Times Square, Central Park, Wall Street |
| 🇬🇧 London | UK | 6 | Piccadilly, Tower Bridge, Westminster |
| 🇯🇵 Tokyo | Japan | 6 | Shibuya, Shinjuku, Ginza |

---

## 📡 API Endpoints

### Core Endpoints
- `GET /` - API information
- `GET /health` - Health check with service status
- `GET /docs` - Interactive API documentation

### Optimization
- `GET /run` - Run traffic optimization
  - Query params: `city`, `source`, `target`, `use_real_traffic`
  - Returns: Classical vs Quantum comparison

### Configuration
- `GET /cities` - List all available cities
- `GET /config?city={city_id}` - Get city configuration

### Analytics
- `GET /history?city={city}&limit={n}` - Historical optimization runs
- `GET /analytics/city/{city_id}` - City-specific analytics

---

## 🔧 Configuration

### Environment Variables

```bash
# API
API_HOST=0.0.0.0
API_PORT=8000

# External APIs (optional — falls back to simulated data)
GOOGLE_MAPS_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
TOMTOM_API_KEY=your_key_here

# Quantum
QAOA_REPS=2
QAOA_MAX_ITER=50
```


---

## 🎨 Frontend Features

### Dashboard Tab
- KPI metrics (costs, runtime, improvement)
- Path visualization with pills
- NetworkX graph with highlighted routes
- Performance comparison

### Real-World Map Tab
- Interactive Folium map on OpenStreetMap
- Traffic-colored road segments
- Classical (blue dashed) vs Quantum (red) paths
- Clickable intersection markers

### Charts Tab
- Cost comparison bar chart
- Traffic heatmap
- Path breakdown analysis

### AI Insights Tab
- Structured GenAI analysis report
- Algorithm comparison
- Recommendations
- Raw API response viewer

---

## 🔬 Algorithm Details

### Quantum (QAOA)
- **Problem**: Formulated as QUBO (Quadratic Unconstrained Binary Optimization)
- **Solver**: Qiskit QAOA with COBYLA optimizer
- **Advantage**: Explores superposition of all routes simultaneously
- **Scaling**: Super-linear advantage with graph size (N nodes → 2^N states)

### Classical (Dijkstra)
- **Algorithm**: Standard shortest-path on weighted graph
- **Weight**: Real-time traffic load (1–25 units)
- **Complexity**: O(E + V log V) with Fibonacci heap

---

## 📖 Documentation

Detailed documentation is available in the `docs/` directory:
- [Architecture Overview](docs/architecture.md)
- [Deployment Guide](docs/DEPLOYMENT.md)

---

## 📈 Performance

- **Optimization Time**: 2–15 seconds (depends on QAOA iterations and graph size)
- **Supported Graph Sizes**: Up to 6 intersections per city (expandable)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 🙏 Acknowledgments

- **Qiskit** — IBM Quantum computing framework
- **FastAPI** — Modern Python web framework
- **Streamlit** — Interactive data apps
- **Folium** — Interactive maps
- **NetworkX** — Graph algorithms

---

**Built with ❤️ for Smart Cities**
