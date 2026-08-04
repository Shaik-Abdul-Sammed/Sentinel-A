"""create telemetry tables

Revision ID: 20260417_0001
Revises: 
Create Date: 2026-04-17 00:00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20260417_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "telemetry_events",
        sa.Column("id", sa.String(length=32), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("ip", sa.String(length=64), nullable=False),
        sa.Column("endpoint", sa.String(length=256), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_telemetry_events_id"), "telemetry_events", ["id"], unique=False)
    op.create_index(op.f("ix_telemetry_events_source"), "telemetry_events", ["source"], unique=False)
    op.create_index(op.f("ix_telemetry_events_event_type"), "telemetry_events", ["event_type"], unique=False)
    op.create_index(op.f("ix_telemetry_events_actor_id"), "telemetry_events", ["actor_id"], unique=False)
    op.create_index(op.f("ix_telemetry_events_timestamp"), "telemetry_events", ["timestamp"], unique=False)

    op.create_table(
        "alerts",
        sa.Column("alert_id", sa.String(length=32), nullable=False),
        sa.Column("event_id", sa.String(length=32), nullable=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("threat_type", sa.String(length=64), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.Column("risk_level", sa.String(length=16), nullable=False),
        sa.Column("decision", sa.String(length=32), nullable=False),
        sa.Column("actions", sa.JSON(), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=False),
        sa.Column("source", sa.String(length=80), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("reasoning", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["event_id"], ["telemetry_events.id"]),
        sa.PrimaryKeyConstraint("alert_id"),
    )
    op.create_index(op.f("ix_alerts_alert_id"), "alerts", ["alert_id"], unique=False)
    op.create_index(op.f("ix_alerts_event_id"), "alerts", ["event_id"], unique=False)
    op.create_index(op.f("ix_alerts_threat_type"), "alerts", ["threat_type"], unique=False)
    op.create_index(op.f("ix_alerts_risk_score"), "alerts", ["risk_score"], unique=False)
    op.create_index(op.f("ix_alerts_risk_level"), "alerts", ["risk_level"], unique=False)
    op.create_index(op.f("ix_alerts_decision"), "alerts", ["decision"], unique=False)
    op.create_index(op.f("ix_alerts_actor_id"), "alerts", ["actor_id"], unique=False)
    op.create_index(op.f("ix_alerts_source"), "alerts", ["source"], unique=False)
    op.create_index(op.f("ix_alerts_status"), "alerts", ["status"], unique=False)
    op.create_index(op.f("ix_alerts_created_at"), "alerts", ["created_at"], unique=False)

    op.create_table(
        "timeline",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("time", sa.DateTime(timezone=True), nullable=False),
        sa.Column("event", sa.String(length=32), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("risk_score", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_timeline_time"), "timeline", ["time"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_timeline_time"), table_name="timeline")
    op.drop_table("timeline")

    op.drop_index(op.f("ix_alerts_created_at"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_status"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_source"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_actor_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_decision"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_risk_level"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_risk_score"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_threat_type"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_event_id"), table_name="alerts")
    op.drop_index(op.f("ix_alerts_alert_id"), table_name="alerts")
    op.drop_table("alerts")

    op.drop_index(op.f("ix_telemetry_events_timestamp"), table_name="telemetry_events")
    op.drop_index(op.f("ix_telemetry_events_actor_id"), table_name="telemetry_events")
    op.drop_index(op.f("ix_telemetry_events_event_type"), table_name="telemetry_events")
    op.drop_index(op.f("ix_telemetry_events_source"), table_name="telemetry_events")
    op.drop_index(op.f("ix_telemetry_events_id"), table_name="telemetry_events")
    op.drop_table("telemetry_events")
