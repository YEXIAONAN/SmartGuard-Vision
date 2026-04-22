from datetime import datetime

from pydantic import BaseModel

from app.schemas.alert import AlertRead


class DashboardStats(BaseModel):
    device_count: int
    online_device_count: int
    offline_device_count: int
    alert_count: int
    today_alert_count: int
    high_risk_alert_count: int
    vision_record_count: int
    sensor_record_count: int
    charging_device_count: int
    abnormal_charging_event_count: int
    over_temperature_event_count: int


class DashboardTrendItem(BaseModel):
    date: str
    total_alerts: int
    high_risk_alerts: int


class DashboardRiskDistributionItem(BaseModel):
    level: str
    count: int


class DashboardCountItem(BaseModel):
    name: str
    count: int


class DashboardDeviceStatusItem(BaseModel):
    name: str
    online: int
    total: int


class DashboardMonitorItem(BaseModel):
    label: str
    value: str


class DashboardMonitorSnapshot(BaseModel):
    title: str
    channel: str
    point_code: str
    capture_status: str
    screen_label: str
    tags: list[str]
    recognition_items: list[DashboardMonitorItem]


class DashboardOverview(BaseModel):
    project_name: str
    generated_at: datetime
    stats: DashboardStats
    risk_distribution: list[DashboardRiskDistributionItem]
    seven_day_alert_trend: list[DashboardTrendItem]
    event_distribution: list[DashboardCountItem]
    area_risk_ranking: list[DashboardCountItem]
    device_status_summary: list[DashboardDeviceStatusItem]
    monitor_snapshot: DashboardMonitorSnapshot
    recent_alerts: list[AlertRead]
