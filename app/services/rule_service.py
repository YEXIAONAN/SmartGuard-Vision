from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.rule_config import RuleConfig

DEFAULT_RULES = {
    "alert_sla_minutes": (str(settings.default_alert_sla_minutes), "告警处置SLA时长（分钟）"),
    "sensor_temp_threshold": (str(settings.default_sensor_temp_threshold), "温度阈值（摄氏度）"),
    "sensor_smoke_threshold": (str(settings.default_sensor_smoke_threshold), "烟雾阈值（ppm）"),
}


def seed_default_rules(db: Session):
    existing = {
        item.rule_key: item
        for item in db.scalars(select(RuleConfig).where(RuleConfig.rule_key.in_(DEFAULT_RULES.keys()))).all()
    }
    for rule_key, (rule_value, description) in DEFAULT_RULES.items():
        if rule_key not in existing:
            db.add(
                RuleConfig(
                    rule_key=rule_key,
                    rule_value=rule_value,
                    description=description,
                    updated_by="system",
                ),
            )
    db.commit()


def list_rules(db: Session):
    return db.scalars(select(RuleConfig).order_by(RuleConfig.rule_key.asc())).all()


def set_rule(db: Session, rule_key: str, rule_value: str, updated_by: str, description: str | None = None):
    rule = db.scalar(select(RuleConfig).where(RuleConfig.rule_key == rule_key))
    if rule is None:
        rule = RuleConfig(
            rule_key=rule_key,
            rule_value=rule_value,
            description=description,
            updated_by=updated_by,
        )
        db.add(rule)
    else:
        rule.rule_value = rule_value
        rule.updated_by = updated_by
        if description is not None:
            rule.description = description
    db.commit()
    db.refresh(rule)
    return rule


def get_rule_value(db: Session, rule_key: str, fallback: str) -> str:
    rule = db.scalar(select(RuleConfig).where(RuleConfig.rule_key == rule_key))
    if rule is None or rule.rule_value is None:
        return fallback
    return rule.rule_value


def get_rule_int(db: Session, rule_key: str, fallback: int) -> int:
    value = get_rule_value(db, rule_key, str(fallback))
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return fallback


def get_rule_float(db: Session, rule_key: str, fallback: float) -> float:
    value = get_rule_value(db, rule_key, str(fallback))
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback
