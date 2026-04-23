from fastapi import APIRouter

from app.api.routes.alerts import router as alerts_router
from app.api.routes.audit import router as audit_router
from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.devices import router as devices_router
from app.api.routes.health import router as health_router
from app.api.routes.rules import router as rules_router
from app.api.routes.sensors import router as sensors_router
from app.api.routes.vision import router as vision_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router, prefix="/api/auth", tags=["auth"])
api_router.include_router(audit_router, prefix="/api/audit", tags=["audit"])
api_router.include_router(dashboard_router, prefix="/api/dashboard", tags=["dashboard"])
api_router.include_router(alerts_router, prefix="/api/alerts", tags=["alerts"])
api_router.include_router(devices_router, prefix="/api/devices", tags=["devices"])
api_router.include_router(rules_router, prefix="/api/rules", tags=["rules"])
api_router.include_router(vision_router, prefix="/api/vision", tags=["vision"])
api_router.include_router(sensors_router, prefix="/api/sensors", tags=["sensors"])
