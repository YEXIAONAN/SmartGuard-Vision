from datetime import datetime, timedelta

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.alert import Alert
from app.models.device import Device
from app.models.sensor_record import SensorRecord
from app.models.vision_record import VisionRecord


def seed_initial_data():
    with SessionLocal() as db:
        device_exists = db.scalar(select(Device.id).limit(1))
        if device_exists:
            return

        now = datetime.now()
        devices = [
            Device(
                device_code="CAM-001",
                device_name="东侧车棚视频监测设备",
                device_type="camera",
                location="教学楼东侧集中停放区",
                status="normal",
                is_online=True,
                last_seen_at=now,
            ),
            Device(
                device_code="SEN-001",
                device_name="宿舍区烟温传感器",
                device_type="sensor",
                location="学生宿舍北侧充电棚",
                status="warning",
                is_online=True,
                last_seen_at=now - timedelta(minutes=1),
            ),
            Device(
                device_code="CHG-001",
                device_name="后勤区充电终端",
                device_type="charger",
                location="后勤服务区",
                status="normal",
                is_online=True,
                last_seen_at=now - timedelta(minutes=2),
            ),
            Device(
                device_code="CAM-002",
                device_name="地下停放点视频监测设备",
                device_type="camera",
                location="地下停放点 02",
                status="offline",
                is_online=False,
                last_seen_at=now - timedelta(hours=1),
            ),
        ]
        db.add_all(devices)
        db.flush()

        vision_records = [
            VisionRecord(
                device_id=devices[0].id,
                device_code=devices[0].device_code,
                location=devices[0].location,
                event_type="飞线充电",
                risk_level="high",
                confidence=0.96,
                detected_count=1,
                payload={"boxes": 2, "remark": "异常接线"},
                reported_at=now - timedelta(minutes=8),
            ),
            VisionRecord(
                device_id=devices[3].id,
                device_code=devices[3].device_code,
                location=devices[3].location,
                event_type="越线停放",
                risk_level="medium",
                confidence=0.89,
                detected_count=2,
                payload={"boxes": 2, "remark": "占用通道边界"},
                reported_at=now - timedelta(hours=2),
            ),
        ]

        sensor_records = [
            SensorRecord(
                device_id=devices[1].id,
                device_code=devices[1].device_code,
                sensor_type="smoke_temperature",
                location=devices[1].location,
                temperature=58.5,
                humidity=62.0,
                smoke_ppm=14.0,
                risk_level="high",
                payload={"temp_threshold": 50},
                reported_at=now - timedelta(minutes=5),
            ),
            SensorRecord(
                device_id=devices[2].id,
                device_code=devices[2].device_code,
                sensor_type="temperature",
                location=devices[2].location,
                temperature=34.2,
                humidity=51.0,
                smoke_ppm=3.1,
                risk_level="low",
                payload={"power_state": "charging"},
                reported_at=now - timedelta(hours=3),
            ),
        ]

        alerts = [
            Alert(
                alert_code="ALT-20260416-0001",
                alert_type="飞线充电",
                alert_level="high",
                source_type="vision",
                location=devices[0].location,
                description="检测到飞线充电行为，建议立即现场复核。",
                status="pending",
                device_id=devices[0].id,
                occurred_at=now - timedelta(minutes=8),
            ),
            Alert(
                alert_code="ALT-20260416-0002",
                alert_type="温升异常",
                alert_level="high",
                source_type="sensor",
                location=devices[1].location,
                description="温度与烟雾指标持续偏高，存在热风险。",
                status="processing",
                handled_by="值班员-王敏",
                handling_note="已通知现场巡查人员赶赴宿舍区充电棚复核。",
                device_id=devices[1].id,
                occurred_at=now - timedelta(minutes=5),
            ),
            Alert(
                alert_code="ALT-20260415-0003",
                alert_type="越线停放",
                alert_level="medium",
                source_type="vision",
                location=devices[3].location,
                description="车辆停放越线，占用消防通道边界。",
                status="resolved",
                handled_by="管理员-李强",
                handling_note="现场完成移车，消防通道恢复畅通。",
                handled_at=now - timedelta(days=1, hours=1, minutes=30),
                device_id=devices[3].id,
                occurred_at=now - timedelta(days=1, hours=2),
            ),
        ]

        db.add_all(vision_records)
        db.add_all(sensor_records)
        db.add_all(alerts)
        db.commit()
