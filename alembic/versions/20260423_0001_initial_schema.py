"""initial schema

Revision ID: 20260423_0001
Revises:
Create Date: 2026-04-23 00:00:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260423_0001"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=100), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("location_scope", sa.String(length=255), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=False)
    op.create_index(op.f("ix_users_role"), "users", ["role"], unique=False)

    op.create_table(
        "rule_configs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("rule_key", sa.String(length=64), nullable=False),
        sa.Column("rule_value", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("updated_by", sa.String(length=64), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rule_key"),
    )
    op.create_index(op.f("ix_rule_configs_id"), "rule_configs", ["id"], unique=False)
    op.create_index(op.f("ix_rule_configs_rule_key"), "rule_configs", ["rule_key"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("target_type", sa.String(length=64), nullable=False),
        sa.Column("target_id", sa.String(length=64), nullable=True),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("ip", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)
    op.create_index(op.f("ix_audit_logs_username"), "audit_logs", ["username"], unique=False)
    op.create_index(op.f("ix_audit_logs_action"), "audit_logs", ["action"], unique=False)
    op.create_index(op.f("ix_audit_logs_created_at"), "audit_logs", ["created_at"], unique=False)

    op.create_table(
        "auth_refresh_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("token", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("revoked", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("token"),
    )
    op.create_index(op.f("ix_auth_refresh_tokens_id"), "auth_refresh_tokens", ["id"], unique=False)
    op.create_index(op.f("ix_auth_refresh_tokens_user_id"), "auth_refresh_tokens", ["user_id"], unique=False)
    op.create_index(op.f("ix_auth_refresh_tokens_token"), "auth_refresh_tokens", ["token"], unique=False)
    op.create_index(
        op.f("ix_auth_refresh_tokens_expires_at"),
        "auth_refresh_tokens",
        ["expires_at"],
        unique=False,
    )
    op.create_index(op.f("ix_auth_refresh_tokens_revoked"), "auth_refresh_tokens", ["revoked"], unique=False)

    op.create_table(
        "auth_revoked_tokens",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("jti", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("jti"),
    )
    op.create_index(op.f("ix_auth_revoked_tokens_id"), "auth_revoked_tokens", ["id"], unique=False)
    op.create_index(op.f("ix_auth_revoked_tokens_jti"), "auth_revoked_tokens", ["jti"], unique=False)
    op.create_index(
        op.f("ix_auth_revoked_tokens_expires_at"),
        "auth_revoked_tokens",
        ["expires_at"],
        unique=False,
    )

    op.add_column("alerts", sa.Column("first_response_at", sa.DateTime(), nullable=True))
    op.add_column("alerts", sa.Column("resolved_at", sa.DateTime(), nullable=True))
    op.add_column("alerts", sa.Column("sla_due_at", sa.DateTime(), nullable=True))
    op.add_column("alerts", sa.Column("escalated_at", sa.DateTime(), nullable=True))
    op.create_index(op.f("ix_alerts_sla_due_at"), "alerts", ["sla_due_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_alerts_sla_due_at"), table_name="alerts")
    op.drop_column("alerts", "escalated_at")
    op.drop_column("alerts", "sla_due_at")
    op.drop_column("alerts", "resolved_at")
    op.drop_column("alerts", "first_response_at")

    op.drop_index(op.f("ix_auth_revoked_tokens_expires_at"), table_name="auth_revoked_tokens")
    op.drop_index(op.f("ix_auth_revoked_tokens_jti"), table_name="auth_revoked_tokens")
    op.drop_index(op.f("ix_auth_revoked_tokens_id"), table_name="auth_revoked_tokens")
    op.drop_table("auth_revoked_tokens")

    op.drop_index(op.f("ix_auth_refresh_tokens_revoked"), table_name="auth_refresh_tokens")
    op.drop_index(op.f("ix_auth_refresh_tokens_expires_at"), table_name="auth_refresh_tokens")
    op.drop_index(op.f("ix_auth_refresh_tokens_token"), table_name="auth_refresh_tokens")
    op.drop_index(op.f("ix_auth_refresh_tokens_user_id"), table_name="auth_refresh_tokens")
    op.drop_index(op.f("ix_auth_refresh_tokens_id"), table_name="auth_refresh_tokens")
    op.drop_table("auth_refresh_tokens")

    op.drop_index(op.f("ix_audit_logs_created_at"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_action"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_username"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index(op.f("ix_rule_configs_rule_key"), table_name="rule_configs")
    op.drop_index(op.f("ix_rule_configs_id"), table_name="rule_configs")
    op.drop_table("rule_configs")

    op.drop_index(op.f("ix_users_role"), table_name="users")
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_table("users")
