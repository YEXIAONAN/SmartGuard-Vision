from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


engine_kwargs = {"pool_pre_ping": True}
if settings.sqlalchemy_database_uri.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.sqlalchemy_database_uri, **engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db():
    from app.models import (  # noqa: F401
        Alert,
        AlertActionLog,
        AuditLog,
        AuthRefreshToken,
        AuthRevokedToken,
        Device,
        RuleConfig,
        SensorRecord,
        User,
        VisionRecord,
    )

    Base.metadata.create_all(bind=engine)
    ensure_schema_compatibility()


def ensure_schema_compatibility():
    inspector = inspect(engine)
    table_names = set(inspector.get_table_names())
    if "alerts" not in table_names:
        return

    existing_columns = {column["name"] for column in inspector.get_columns("alerts")}
    alter_statements = []

    if "handled_by" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN handled_by VARCHAR(64)")
    if "handling_note" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN handling_note TEXT")
    if "handled_at" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN handled_at DATETIME")
    if "first_response_at" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN first_response_at DATETIME")
    if "resolved_at" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN resolved_at DATETIME")
    if "sla_due_at" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN sla_due_at DATETIME")
    if "escalated_at" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN escalated_at DATETIME")

    if "users" in table_names:
        user_columns = {column["name"] for column in inspector.get_columns("users")}
        if "location_scope" not in user_columns:
            alter_statements.append("ALTER TABLE users ADD COLUMN location_scope VARCHAR(255)")

    if not alter_statements:
        return

    with engine.begin() as connection:
        for statement in alter_statements:
            connection.execute(text(statement))
