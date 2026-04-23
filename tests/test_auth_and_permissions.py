from fastapi.testclient import TestClient

from app.main import app


def _login(username: str, password: str) -> dict:
    with TestClient(app) as client:
        response = client.post("/api/auth/login", json={"username": username, "password": password})
        assert response.status_code == 200
        return response.json()["data"]


def test_dashboard_requires_auth():
    with TestClient(app) as client:
        response = client.get("/api/dashboard/overview")
        assert response.status_code == 401


def test_admin_login_and_me():
    with TestClient(app) as client:
        login = client.post("/api/auth/login", json={"username": "admin", "password": "admin123"})
        assert login.status_code == 200
        token = login.json()["data"]["access_token"]

        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["data"]["role"] == "admin"


def test_viewer_cannot_update_alert_status():
    viewer = _login("viewer", "viewer123")
    token = viewer["access_token"]

    with TestClient(app) as client:
        alerts = client.get("/api/alerts", headers={"Authorization": f"Bearer {token}"})
        assert alerts.status_code == 200
        first_alert = alerts.json()["data"]["items"][0]
        patch = client.patch(
            f"/api/alerts/{first_alert['id']}/status",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "status": "processing",
                "handled_by": "viewer",
                "handling_note": "no permission",
            },
        )
        assert patch.status_code == 403


def test_refresh_and_logout():
    with TestClient(app) as client:
        login = client.post("/api/auth/login", json={"username": "operator", "password": "operator123"})
        assert login.status_code == 200
        data = login.json()["data"]
        access_token = data["access_token"]
        refresh_token = data["refresh_token"]

        refresh = client.post("/api/auth/refresh", json={"refresh_token": refresh_token})
        assert refresh.status_code == 200

        logout = client.post(
            "/api/auth/logout",
            headers={"Authorization": f"Bearer {access_token}"},
            json={"refresh_token": refresh_token},
        )
        assert logout.status_code == 200
