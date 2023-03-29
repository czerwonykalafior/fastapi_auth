from starlette.testclient import TestClient

from main import app

api_client = TestClient(app)


def test_login():
    resp = api_client.post(
        "/token", data={"grant_type": "password", "scope": "me", "username": "johndoe", "password": "secret"}
    )
    assert "access_token" in resp.json()
    assert "token_type" in resp.json()


def test_access_denied():
    resp = api_client.get("/users/me/")
    assert resp.status_code == 401
