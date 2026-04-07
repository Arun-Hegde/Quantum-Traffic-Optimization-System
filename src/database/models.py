from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime
from datetime import datetime
try:
    from sqlalchemy.orm import declarative_base
except ImportError:
    from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class OptimizationRun(Base):
    __tablename__ = "optimization_runs"
    id               = Column(Integer, primary_key=True, index=True)
    city             = Column(String, index=True)
    source_node      = Column(Integer)
    target_node      = Column(Integer)
    classical_path   = Column(JSON)
    classical_cost   = Column(Integer)
    quantum_path     = Column(JSON, nullable=True)
    quantum_cost     = Column(Integer, nullable=True)
    quantum_edges    = Column(JSON, nullable=True)
    runtime_seconds  = Column(Float)
    quantum_advantage= Column(Boolean)
    cost_improvement = Column(Float, nullable=True)
    timestamp        = Column(DateTime, default=datetime.utcnow)


class CityMetrics(Base):
    __tablename__ = "city_metrics"
    id                  = Column(Integer, primary_key=True, index=True)
    city                = Column(String, unique=True, index=True)
    total_optimizations = Column(Integer, default=0)
    quantum_wins        = Column(Integer, default=0)
    classical_wins      = Column(Integer, default=0)
    average_improvement = Column(Float, default=0.0)
    average_runtime     = Column(Float, default=0.0)
    last_updated        = Column(DateTime, default=datetime.utcnow)
