from sqlalchemy import create_engine, Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.core.config import config

Base = declarative_base()

class IncidentJob(Base):
    __tablename__ = 'incident_jobs'
    
    id = Column(Integer, primary_key=True, index=True)
    correlation_id = Column(String, unique=True, index=True)
    source = Column(String) # e.g., 'jenkins', 'prometheus', 'github'
    status = Column(String, default="triage") # triage, research, debug, complete, failed
    failure_type = Column(String, nullable=True) # infrastructure, code, test_flake
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rca_report = Column(Text, nullable=True)
    suggested_fix = Column(Text, nullable=True)
    raw_logs = Column(JSON, nullable=True)

engine = create_engine(config.database.postgres_uri)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
