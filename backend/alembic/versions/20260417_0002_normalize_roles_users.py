"""normalize roles and users

Revision ID: 20260417_0002
Revises: 20260417_0001
Create Date: 2026-04-17 00:30:00

"""

from alembic import op
import sqlalchemy as sa


revision = "20260417_0002"
down_revision = "20260417_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_roles_name"), "roles", ["name"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=128), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)
    op.create_index(op.f("ix_users_role_id"), "users", ["role_id"], unique=False)

    op.bulk_insert(
        sa.table(
            "roles",
            sa.column("id", sa.Integer()),
            sa.column("name", sa.String()),
            sa.column("description", sa.String()),
            sa.column("is_active", sa.Boolean()),
        ),
        [
            {"id": 1, "name": "admin", "description": "Full platform administrator", "is_active": True},
            {"id": 2, "name": "sensor", "description": "Telemetry producer / ingestion client", "is_active": True},
            {"id": 3, "name": "soc", "description": "Security operations analyst", "is_active": True},
        ],
    )

    op.bulk_insert(
        sa.table(
            "users",
            sa.column("id", sa.Integer()),
            sa.column("username", sa.String()),
            sa.column("full_name", sa.String()),
            sa.column("email", sa.String()),
            sa.column("hashed_password", sa.String()),
            sa.column("role_id", sa.Integer()),
            sa.column("is_active", sa.Boolean()),
        ),
        [
            {"id": 1, "username": "abdul", "full_name": "Abdul Sammed Shaik", "email": "abdul@example.com", "hashed_password": "MIGRATE_LATER", "role_id": 1, "is_active": True},
            {"id": 2, "username": "sensor", "full_name": "Portal Sensor Agent", "email": "sensor@example.com", "hashed_password": "MIGRATE_LATER", "role_id": 2, "is_active": True},
            {"id": 3, "username": "soc", "full_name": "SOC Analyst", "email": "soc@example.com", "hashed_password": "MIGRATE_LATER", "role_id": 3, "is_active": True},
        ],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_users_role_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_table("users")

    op.drop_index(op.f("ix_roles_name"), table_name="roles")
    op.drop_table("roles")
