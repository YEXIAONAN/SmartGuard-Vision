from collections import Counter, defaultdict
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.device import Device
from app.models.sensor_record import SensorRecord
from app.models.vision_record import VisionRecord
from app.schemas.dashboard import (
    DashboardCountItem,
    DashboardDeviceStatusItem,
    DashboardMonitorItem,
    DashboardMonitorSnapshot,
    DashboardOverview,
    DashboardRiskDistributionItem,
    DashboardStats,
    DashboardTrendItem,
)
from app.services.alert_service import list_alerts

HIGH_RISK_LEVELS = {"high", "高风险"}
MEDIUM_RISK_LEVELS = {"medium", "中风险"}
DEVICE_TYPE_LABELS = {
    "camera": "视频监测设备",
    "sensor": "传感设备",
    "charger": "充电终端",
}


def normalize_risk_level(value: str | None) -> str:
    level = str(value or "").strip().lower()
    if level in HIGH_RISK_LEVELS or "高" in level:
        return "high"
    if level in MEDIUM_RISK_LEVELS or "中" in level:
        return "medium"
    if level == "low" or "低" in level:
        return "low"
    return "other"


def risk_level_label(value: str | None) -> str:
    risk_level = normalize_risk_level(value)
    if risk_level == "high":
        return "高风险"
    if risk_level == "medium":
        return "中风险"
    if risk_level == "low":
        return "低风险"
    return str(value or "未知")


def alert_status_label(value: str | None) -> str:
    status = str(value or "").strip().lower()
    if status == "pending":
        return "待处理"
    if status == "processing":
        return "处理中"
    if status == "resolved":
        return "已处理"
    return str(value or "未知")


def device_type_label(value: str | None) -> str:
    return DEVICE_TYPE_LABELS.get(str(value or "").strip().lower(), str(value or "其他设备"))


def get_dashboard_overview(db: Session) -> DashboardOverview:
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)

    device_count = db.scalar(select(func.count(Device.id))) or 0
    online_device_count = db.scalar(select(func.count(Device.id)).where(Device.is_online.is_(True))) or 0
    offline_device_count = device_count - online_device_count
    alert_count = db.scalar(select(func.count(Alert.id))) or 0
    today_alert_count = db.scalar(select(func.count(Alert.id)).where(Alert.occurred_at >= today_start)) or 0
    high_risk_alert_count = (
        db.scalar(select(func.count(Alert.id)).where(Alert.alert_level.in_(["high", "高风险"]))) or 0
    )
    vision_record_count = db.scalar(select(func.count(VisionRecord.id))) or 0
    sensor_record_count = db.scalar(select(func.count(SensorRecord.id))) or 0

    all_alerts = db.scalars(select(Alert).order_by(Alert.occurred_at.desc())).all()
    all_devices = db.scalars(select(Device).order_by(Device.last_seen_at.desc())).all()
    all_sensor_records = db.scalars(select(SensorRecord).order_by(SensorRecord.reported_at.desc())).all()
    all_vision_records = db.scalars(select(VisionRecord).order_by(VisionRecord.reported_at.desc())).all()

    charging_sensor_records = [
        record for record in all_sensor_records if isinstance(record.payload, dict) and record.payload.get("power_state") == "charging"
    ]
    charging_device_count = len({record.device_code for record in charging_sensor_records if record.device_code})
    abnormal_charging_event_count = sum(
        1
        for record in all_vision_records
        if "充电" in record.event_type and normalize_risk_level(record.risk_level) in {"high", "medium"}
    ) + sum(
        1
        for record in charging_sensor_records
        if (
            (record.temperature is not None and record.temperature >= 50)
            or (record.smoke_ppm is not None and record.smoke_ppm >= 10)
            or normalize_risk_level(record.risk_level) in {"high", "medium"}
        )
    )
    over_temperature_event_count = sum(
        1 for record in all_sensor_records if record.temperature is not None and record.temperature >= 50
    )

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
        if normalize_risk_level(alert.alert_level) == "high":
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

    event_distribution = [
        DashboardCountItem(name=name, count=count)
        for name, count in Counter(alert.alert_type for alert in all_alerts).most_common(6)
    ]
    area_risk_ranking = [
        DashboardCountItem(name=name, count=count)
        for name, count in Counter(alert.location for alert in all_alerts).most_common(6)
    ]

    device_status_summary = []
    for device_type, count in Counter(device.device_type for device in all_devices).most_common():
        online = sum(1 for device in all_devices if device.device_type == device_type and device.is_online)
        device_status_summary.append(
            DashboardDeviceStatusItem(
                name=device_type_label(device_type),
                online=online,
                total=count,
            )
        )

    latest_alert = all_alerts[0] if all_alerts else None
    latest_device = None
    if latest_alert and latest_alert.device_id is not None:
        latest_device = next((device for device in all_devices if device.id == latest_alert.device_id), None)
    if latest_device is None and all_devices:
        latest_device = all_devices[0]

    latest_sensor = all_sensor_records[0] if all_sensor_records else None
    latest_vision = all_vision_records[0] if all_vision_records else None
    monitor_tags = list(dict.fromkeys(alert.alert_type for alert in all_alerts[:4]))
    monitor_snapshot = DashboardMonitorSnapshot(
        title=f"{latest_alert.alert_type}联动画面" if latest_alert else "实时监测面板",
        channel=latest_device.device_name if latest_device else "等待设备接入",
        point_code=latest_device.device_code if latest_device else "--",
        capture_status="在线" if latest_device and latest_device.is_online else "离线",
        screen_label=latest_alert.alert_type if latest_alert else "暂无实时事件",
        tags=monitor_tags,
        recognition_items=[
            DashboardMonitorItem(
                label="监测点位",
                value=latest_alert.location if latest_alert else latest_device.location if latest_device else "--",
            ),
            DashboardMonitorItem(
                label="风险等级",
                value=risk_level_label(latest_alert.alert_level) if latest_alert else "正常",
            ),
            DashboardMonitorItem(
                label="处置状态",
                value=alert_status_label(latest_alert.status) if latest_alert else "--",
            ),
            DashboardMonitorItem(
                label="停放识别",
                value=latest_vision.event_type if latest_vision else "暂无视觉识别结果",
            ),
            DashboardMonitorItem(
                label="充电状态",
                value="充电中" if charging_sensor_records else "未监测到充电状态",
            ),
            DashboardMonitorItem(
                label="温度/烟雾",
                value=(
                    f"{latest_sensor.temperature or '--'}℃ / {latest_sensor.smoke_ppm or '--'}ppm"
                    if latest_sensor
                    else "-- / --"
                ),
            ),
            DashboardMonitorItem(
                label="最近上报",
                value=(
                    max(
                        [record.reported_at for record in [latest_sensor, latest_vision] if record is not None],
                        default=now,
                    ).strftime("%Y-%m-%d %H:%M:%S")
                ),
            ),
        ],
    )

    recent_alerts = list_alerts(db, limit=5)

    return DashboardOverview(
        project_name="智感护航——面向停充场景的多模态安全感知平台",
        generated_at=now,
        stats=DashboardStats(
            device_count=device_count,
            online_device_count=online_device_count,
            offline_device_count=offline_device_count,
            alert_count=alert_count,
            today_alert_count=today_alert_count,
            high_risk_alert_count=high_risk_alert_count,
            vision_record_count=vision_record_count,
            sensor_record_count=sensor_record_count,
            charging_device_count=charging_device_count,
            abnormal_charging_event_count=abnormal_charging_event_count,
            over_temperature_event_count=over_temperature_event_count,
        ),
        risk_distribution=risk_distribution,
        seven_day_alert_trend=seven_day_alert_trend,
        event_distribution=event_distribution,
        area_risk_ranking=area_risk_ranking,
        device_status_summary=device_status_summary,
        monitor_snapshot=monitor_snapshot,
        recent_alerts=recent_alerts,
    )
