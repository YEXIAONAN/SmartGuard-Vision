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
    from app.models import Alert, Device, SensorRecord, VisionRecord  # noqa: F401

    Base.metadata.create_all(bind=engine)
    ensure_alert_columns()


def ensure_alert_columns():
    inspector = inspect(engine)
    if "alerts" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("alerts")}
    alter_statements = []

    if "handled_by" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN handled_by VARCHAR(64)")
    if "handling_note" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN handling_note TEXT")
    if "handled_at" not in existing_columns:
        alter_statements.append("ALTER TABLE alerts ADD COLUMN handled_at DATETIME")

    if not alter_statements:
        return

    with engine.begin() as connection:
        for statement in alter_statements:
            connection.execute(text(statement))
