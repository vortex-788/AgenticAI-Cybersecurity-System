from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import Dict,Any
from app.agent_logic import mock_enrich, compute_score, EnrichedAlert, decide_action, execute_action
from init_db import Audit, Base, DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import time, os
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./audit.db')
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
app = FastAPI(title='AgenticAI Cybersecurity MVP')
class AlertIn(BaseModel):
    id: str | None = None
    source: str = 'unknown'
    timestamp: float | None = None
    observables: Dict[str,Any]
@app.post('/ingest')
async def ingest(alert: AlertIn, background_tasks: BackgroundTasks):
    payload = alert.dict()
    payload['id'] = payload.get('id') or f"a-{int(time.time()*1000)}"
    payload['timestamp'] = payload.get('timestamp') or time.time()
    background_tasks.add_task(process_alert, payload)
    return {'status':'accepted','event_id': payload['id']}
@app.get('/audit')
def get_audit(limit: int = 50):
    db = SessionLocal()
    rows = db.query(Audit).order_by(Audit.id.desc()).limit(limit).all()
    result = []
    for r in rows:
        result.append({'id': r.id, 'event_id': r.event_id, 'timestamp': r.timestamp, 'action': r.action, 'score': r.score, 'rationale': r.rationale, 'details': r.details})
    db.close()
    return {'count': len(result), 'items': result}
def process_alert(alert: Dict[str,Any]):
    enrichment = mock_enrich(alert)
    score = compute_score(enrichment, alert)
    enriched = EnrichedAlert(alert=alert, whois=enrichment.get('whois'), passive_dns=enrichment.get('passive_dns'), host_info=enrichment.get('host_info'), mitre=enrichment.get('mitre'), score=score, rationale='auto')
    decision = decide_action(enriched)
    execution = execute_action(decision, enriched)
    db = SessionLocal()
    aud = Audit(event_id=execution.get('event_id'), timestamp=execution.get('timestamp'), action=execution.get('action'), score=execution.get('score'), rationale=execution.get('rationale'), details=execution)
    db.add(aud)
    db.commit()
    db.close()
