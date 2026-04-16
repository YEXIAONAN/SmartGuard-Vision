from collections import defaultdict
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.device import Device
from app.models.sensor_record import SensorRecord
from app.models.vision_record import VisionRecord
from app.schemas.dashboard import (
    DashboardOverview,
    DashboardRiskDistributionItem,
    DashboardStats,
    DashboardTrendItem,
)
from app.services.alert_service import list_alerts


def get_dashboard_overview(db: Session) -> DashboardOverview:
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)

    device_count = db.scalar(select(func.count(Device.id))) or 0
    online_device_count = db.scalar(select(func.count(Device.id)).where(Device.is_online.is_(True))) or 0
    alert_count = db.scalar(select(func.count(Alert.id))) or 0
    today_alert_count = db.scalar(select(func.count(Alert.id)).where(Alert.occurred_at >= today_start)) or 0
    high_risk_alert_count = (
        db.scalar(select(func.count(Alert.id)).where(Alert.alert_level.in_(["high", "高风险"]))) or 0
    )
    vision_record_count = db.scalar(select(func.count(VisionRecord.id))) or 0
    sensor_record_count = db.scalar(select(func.count(SensorRecord.id))) or 0

    risk_rows = db.execute(
        select(Alert.alert_level, func.count(Alert.id)).group_by(Alert.alert_level).order_by(func.count(Alert.id).desc())
    ).all()
    risk_distribution = [
        DashboardRiskDistributionItem(level=level, count=count) for level, count in risk_rows
    ]

    daily_totals = defaultdict(lambda: {"total": 0, "high": 0})
    start_day = today_start - timedelta(days=6)
    alert_rows = db.scalars(select(Alert).where(Alert.occurred_at >= start_day)).all()
    for alert in alert_rows:
        day_key = alert.occurred_at.strftime("%m-%d")
        daily_totals[day_key]["total"] += 1
        if alert.alert_level in {"high", "高风险"}:
            daily_totals[day_key]["high"] += 1

    seven_day_alert_trend = []
    for offset in range(7):
        current_day = start_day + timedelta(days=offset)
        key = current_day.strftime("%m-%d")
        counts = daily_totals[key]
        seven_day_alert_trend.append(
            DashboardTrendItem(
                date=key,
                total_alerts=counts["total"],
                high_risk_alerts=counts["high"],
            )
        )

    recent_alerts = list_alerts(db, limit=5)

    return DashboardOverview(
        project_name="智感护航——面向停充场景的多模态安全感知平台",
        generated_at=now,
        stats=DashboardStats(
            device_count=device_count,
            online_device_count=online_device_count,
            alert_count=alert_count,
            today_alert_count=today_alert_count,
            high_risk_alert_count=high_risk_alert_count,
            vision_record_count=vision_record_count,
            sensor_record_count=sensor_record_count,
        ),
        risk_distribution=risk_distribution,
        seven_day_alert_trend=seven_day_alert_trend,
        recent_alerts=recent_alerts,
    )
