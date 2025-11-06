from sqlalchemy import create_engine, Column, Integer, String, Float, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./audit.db")
Base = declarative_base()
class Audit(Base):
    __tablename__ = "audit"
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String, index=True)
    timestamp = Column(Float)
    action = Column(String)
    score = Column(Float)
    rationale = Column(Text)
    details = Column(JSON)
if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    print("Initialized database at", DATABASE_URL)
