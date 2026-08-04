from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, Text

from app.core.database import Base


class TelemetryEventORM(Base):
    __tablename__ = "telemetry_events"

    id = Column(String(32), primary_key=True, index=True)
    source = Column(String(80), nullable=False, index=True)
    event_type = Column(String(64), nullable=False, index=True)
    actor_id = Column(String(128), nullable=False, index=True)
    ip = Column(String(64), nullable=False)
    endpoint = Column(String(256), nullable=False)
    status = Column(String(32), nullable=False)
    payload = Column(JSON, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)


class AlertORM(Base):
    __tablename__ = "alerts"

    alert_id = Column(String(32), primary_key=True, index=True)
    event_id = Column(String(32), ForeignKey("telemetry_events.id"), nullable=True, index=True)
    title = Column(String(200), nullable=False)
    threat_type = Column(String(64), nullable=False, index=True)
    risk_score = Column(Integer, nullable=False, index=True)
    risk_level = Column(String(16), nullable=False, index=True)
    decision = Column(String(32), nullable=False, index=True)
    actions = Column(JSON, nullable=False)
    actor_id = Column(String(128), nullable=False, index=True)
    source = Column(String(80), nullable=False, index=True)
    status = Column(String(32), nullable=False, index=True)
    reasoning = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, index=True)


class TimelineORM(Base):
    __tablename__ = "timeline"

    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(DateTime(timezone=True), nullable=False, index=True)
    event = Column(String(32), nullable=False)
    message = Column(Text, nullable=False)
    risk_score = Column(Integer, nullable=False)
