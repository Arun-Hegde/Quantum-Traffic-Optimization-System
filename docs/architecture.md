# Architecture Overview — Quantum Traffic Optimization System v3.0

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          CLIENT LAYER                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  Web Browser  │  Mobile App  │  API Clients  │  Monitoring Tools        │
└────────┬──────────────┬──────────────┬──────────────┬────────────────────┘
         │              │              │              │
         ▼              ▼              ▼              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       APPLICATION LAYER                                  │
├──────────────────────────────┬──────────────────────────────────────────┤
│   Streamlit Frontend         │   FastAPI Backend                        │
│   - Interactive Dashboard    │   - REST API Endpoints                   │
│   - Real-time Visualization  │   - Request Validation                   │
│   - Multi-tab Interface      │   - Authentication & CORS                │
│   - Chart Rendering          │   - Rate Limiting                        │
└──────────────┬───────────────┴──────────────┬───────────────────────────┘
               │                              │
               ▼                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         BUSINESS LOGIC LAYER                             │
├──────────────────┬──────────────────┬───────────────────────────────────┤
│  Core Algorithms │  Integrations    │  Utilities                        │
│  - Classical     │  - Traffic APIs  │  - Logging                        │
│  - Quantum QAOA  │  - Weather APIs  │  - Caching                        │
│  - GenAI         │  - Real-time Data│  - Metrics                        │
│  - Simulation    │                  │  - Monitoring                     │
└──────────┬───────┴──────────┬───────┴──────────┬────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                          DATA LAYER                                      │
├──────────────────┬──────────────────┬───────────────────────────────────┤
│  PostgreSQL      │  Redis Cache     │  External APIs                    │
│  - Optimization  │  - Query Cache   │  - Google Maps                    │
│  - History       │  - Session Store │  - TomTom Traffic                 │
│  - Analytics     │  - Rate Limiting │  - OpenWeather                    │
│  - Metrics       │                  │  - IBM Quantum                    │
└──────────────────┴──────────────────┴───────────────────────────────────┘
           │                  │                  │
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      INFRASTRUCTURE LAYER                                │
├──────────────────┬──────────────────┬───────────────────────────────────┤
│  Docker          │  Monitoring      │  Cloud Services                   │
│  - Containers    │  - Prometheus    │  - AWS/GCP/Azure                  │
│  - Compose       │  - Grafana       │  - Load Balancer                  │
│  - Networking    │  - Alerting      │  - CDN                            │
└──────────────────┴──────────────────┴───────────────────────────────────┘
```

---

## Request Flow

### Optimization Request Flow

```
User → Frontend → API Gateway → FastAPI
                                   │
                                   ├─→ Cache Check (Redis)
                                   │   └─→ Return if cached
                                   │
                                   ├─→ Load City Config
                                   │
                                   ├─→ Build Traffic Graph
                                   │   ├─→ Get Real-time Traffic (optional)
                                   │   └─→ Apply Weather Impact (optional)
                                   │
                                   ├─→ Classical Optimization (Dijkstra)
                                   │   └─→ Path + Cost
                                   │
                                   ├─→ Quantum Optimization (QAOA)
                                   │   ├─→ Build QUBO
                                   │   ├─→ Solve with Qiskit
                                   │   ├─→ Decode Solution
                                   │   └─→ Extract Path + Cost
                                   │
                                   ├─→ Generate AI Explanation
                                   │
                                   ├─→ Create Visualization
                                   │   └─→ Save Folium Map
                                   │
                                   ├─→ Save to Database
                                   │   ├─→ Optimization Run
                                   │   └─→ Update City Metrics
                                   │
                                   ├─→ Record Metrics (Prometheus)
                                   │
                                   └─→ Return Response
                                       └─→ Cache Result (Redis)
```

---

## Module Responsibilities

### API Layer (`api/`)
| Module | Responsibility |
|--------|---------------|
| `main.py` | FastAPI application, endpoints, middleware, request handling |

### Core Logic (`src/core/`)
| Module | Responsibility |
|--------|---------------|
| `classical.py` | Dijkstra shortest-path algorithm, path cost calculation |
| `quantum_qaoa.py` | QUBO formulation, QAOA solver, solution decoding |
| `genai.py` | AI-powered analysis report generation |

### Simulation (`src/simulation/`)
| Module | Responsibility |
|--------|---------------|
| `traffic_simulation.py` | Multi-city graph construction, traffic simulation |

### Visualization (`src/visualization/`)
| Module | Responsibility |
|--------|---------------|
| `map_viz.py` | Folium interactive maps with OpenStreetMap |
| `chart_viz.py` | Plotly charts (bar, heatmap, breakdown) |
| `graph_viz.py` | NetworkX graph visualization |

### Database (`src/database/`)
| Module | Responsibility |
|--------|---------------|
| `models.py` | SQLAlchemy ORM models (OptimizationRun, CityMetrics, etc.) |
| `database.py` | Database connection, session management, initialization |

### Integrations (`src/integrations/`)
| Module | Responsibility |
|--------|---------------|
| `traffic_api.py` | Real-time traffic data from Google Maps, TomTom |
| | Weather data from OpenWeather API |

### Utilities (`src/utils/`)
| Module | Responsibility |
|--------|---------------|
| `logger.py` | Centralized logging configuration |
| `cache.py` | Redis caching with fallback to in-memory |
| `metrics.py` | Prometheus metrics collection |

### Configuration (`config/`)
| Module | Responsibility |
|--------|---------------|
| `settings.py` | Global constants, default city configuration |
| `cities.py` | Multi-city definitions with GPS coordinates |

### Frontend (`frontend/`)
| Module | Responsibility |
|--------|---------------|
| `app.py` | Streamlit dashboard with 4 tabs (Dashboard, Map, Charts, AI) |

---

## Data Models

### OptimizationRun
Stores each optimization execution for historical analysis.

```python
{
    "id": int,
    "city": str,
    "source_node": int,
    "target_node": int,
    "classical_path": list,
    "classical_cost": int,
    "quantum_path": list,
    "quantum_cost": int,
    "quantum_advantage": bool,
    "runtime_seconds": float,
    "traffic_data": dict,
    "weather_conditions": dict,
    "timestamp": datetime
}
```

### CityMetrics
Aggregate statistics per city.

```python
{
    "city": str,
    "total_optimizations": int,
    "quantum_wins": int,
    "classical_wins": int,
    "average_improvement": float,
    "average_runtime": float,
    "last_updated": datetime
}
```

### TrafficSnapshot
Real-time traffic data snapshots.

```python
{
    "city": str,
    "timestamp": datetime,
    "edge_traffic": dict,
    "average_traffic": float,
    "congestion_level": str,
    "weather": str,
    "is_rush_hour": bool
}
```

---

## API Endpoints

### Core Endpoints
- `GET /` - API information and features
- `GET /health` - Health check with service status
- `GET /metrics` - Prometheus metrics
- `GET /docs` - Interactive API documentation (Swagger)

### Optimization
- `GET /run` - Run traffic optimization
  - Query params: `city`, `source`, `target`, `use_real_traffic`
  - Returns: Comparative results with paths, costs, and analysis

### Configuration
- `GET /cities` - List all available cities
- `GET /config?city={city_id}` - Get city configuration

### Analytics
- `GET /history?city={city}&limit={n}` - Historical optimization runs
- `GET /analytics/city/{city_id}` - City-specific analytics and metrics

### Admin
- `DELETE /cache/clear` - Clear Redis cache

---

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **SQLAlchemy** - ORM for database
- **Alembic** - Database migrations

### Quantum Computing
- **Qiskit** - IBM Quantum framework
- **Qiskit Algorithms** - QAOA implementation
- **Qiskit Optimization** - QUBO formulation

### Frontend
- **Streamlit** - Interactive dashboards
- **Plotly** - Interactive charts
- **Folium** - Interactive maps
- **Matplotlib** - Static visualizations

### Data & Caching
- **PostgreSQL** - Primary database
- **Redis** - Caching and session storage
- **NetworkX** - Graph algorithms

### Monitoring
- **Prometheus** - Metrics collection
- **Grafana** - Visualization dashboards
- **Sentry** - Error tracking (optional)

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Reverse proxy (production)

---

## Scalability Considerations

### Horizontal Scaling
- API can be scaled to multiple instances behind a load balancer
- Stateless design allows easy horizontal scaling
- Redis for shared session/cache across instances

### Vertical Scaling
- Quantum optimization benefits from more CPU cores
- Increase QAOA iterations for better results
- More RAM for larger city graphs

### Database Optimization
- Indexed queries on frequently accessed columns
- Connection pooling for better performance
- Read replicas for analytics queries

### Caching Strategy
- Redis for frequently accessed data
- TTL-based cache invalidation
- Cache warming for popular cities

---

## Security Architecture

### Authentication & Authorization
- API key authentication (optional)
- JWT tokens for user sessions
- Role-based access control (RBAC)

### Data Protection
- HTTPS/TLS encryption in transit
- Database encryption at rest
- Secure credential management (environment variables)

### API Security
- CORS configuration
- Rate limiting per IP/API key
- Input validation and sanitization
- SQL injection prevention (ORM)

### Monitoring & Auditing
- Request logging
- Error tracking
- Audit trail for sensitive operations

---

## Performance Metrics

### Target Performance
- **API Response Time**: < 100ms (cached), < 5s (optimization)
- **Optimization Time**: 2-15 seconds (depends on QAOA iterations)
- **Cache Hit Rate**: > 80% for repeated queries
- **Throughput**: 100+ requests/second (with caching)
- **Availability**: 99.9% uptime

### Optimization Benchmarks
| City Size | Classical Time | Quantum Time | Total Time |
|-----------|---------------|--------------|------------|
| 6 nodes   | < 1ms         | 2-5s         | 2-5s       |
| 10 nodes  | < 5ms         | 5-10s        | 5-10s      |
| 20 nodes  | < 20ms        | 10-30s       | 10-30s     |

---

## Deployment Patterns

### Development
- Local Python environment
- SQLite database
- In-memory cache
- Single process

### Staging
- Docker Compose
- PostgreSQL container
- Redis container
- Multiple API workers

### Production
- Kubernetes/ECS cluster
- Managed PostgreSQL (RDS/Cloud SQL)
- Managed Redis (ElastiCache/MemoryStore)
- Auto-scaling groups
- Load balancer
- CDN for static assets

---

## Future Enhancements

### Planned Features
1. **Machine Learning Integration**
   - Traffic prediction models
   - Demand forecasting
   - Pattern recognition

2. **Advanced Quantum Algorithms**
   - VQE (Variational Quantum Eigensolver)
   - QAOA with adaptive parameters
   - Quantum annealing support

3. **Real-time Updates**
   - WebSocket support
   - Live traffic updates
   - Push notifications

4. **Mobile Application**
   - Native iOS/Android apps
   - Offline mode
   - GPS integration

5. **Multi-modal Transportation**
   - Public transit integration
   - Walking/cycling routes
   - Ride-sharing optimization

6. **Advanced Analytics**
   - Predictive analytics
   - A/B testing framework
   - Custom reporting

---

## Maintenance & Operations

### Regular Tasks
- Database backups (daily)
- Log rotation (weekly)
- Security updates (monthly)
- Performance tuning (quarterly)

### Monitoring Alerts
- High error rate (> 5%)
- Slow response time (> 5s)
- Database connection issues
- Cache failures
- Disk space warnings

### Disaster Recovery
- Automated backups
- Multi-region deployment
- Failover procedures
- Data replication

---

## Contributing Guidelines

### Code Standards
- Follow PEP 8 style guide
- Type hints for all functions
- Comprehensive docstrings
- Unit tests for new features

### Git Workflow
1. Create feature branch
2. Implement changes
3. Write tests
4. Update documentation
5. Submit pull request
6. Code review
7. Merge to main

### Testing Requirements
- Unit tests (> 80% coverage)
- Integration tests
- API endpoint tests
- Performance tests

---

## References

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [QAOA Algorithm Paper](https://arxiv.org/abs/1411.4028)
- [NetworkX Documentation](https://networkx.org/documentation/)

---

**Last Updated**: 2024
**Version**: 3.0.0
**Maintainer**: Development Team
