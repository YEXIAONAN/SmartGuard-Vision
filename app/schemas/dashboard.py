from datetime import datetime

from pydantic import BaseModel

from app.schemas.alert import AlertRead


class DashboardStats(BaseModel):
    device_count: int
    online_device_count: int
    alert_count: int
    today_alert_count: int
    high_risk_alert_count: int
    vision_record_count: int
    sensor_record_count: int


class DashboardTrendItem(BaseModel):
    date: str
    total_alerts: int
    high_risk_alerts: int


class DashboardRiskDistributionItem(BaseModel):
    level: str
    count: int


class DashboardOverview(BaseModel):
    project_name: str
    generated_at: datetime
    stats: DashboardStats
    risk_distribution: list[DashboardRiskDistributionItem]
    seven_day_alert_trend: list[DashboardTrendItem]
    recent_alerts: list[AlertRead]
