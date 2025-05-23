from fastapi.testclient import TestClient


def get_auth_header(client: TestClient) -> dict:
    creds = {"email": "admin@example.com", "password": "secret123"}
    client.post("/auth/register", json=creds)
    login_resp = client.post(
        "/auth/login",
        data={"username": creds["email"], "password": creds["password"]},
    )
    token = login_resp.json().get("access_token")
    return {"Authorization": f"Bearer {token}"}


def test_create_and_get_user(client: TestClient):
    headers = get_auth_header(client)

    # 1) Create a new user
    resp = client.post(
        "/users/",
        json={"email": "alice@example.com", "password": "secret123"},
        headers=headers,
    )
    assert resp.status_code == 201
    created = resp.json()
    assert isinstance(created["id"], int) and created["id"] > 0
    assert created["email"] == "alice@example.com"
    assert created["is_active"] is True

    # 2) Retrieve the same user
    resp2 = client.get(f"/users/{created['id']}", headers=headers)
    assert resp2.status_code == 200
    assert resp2.json() == created
