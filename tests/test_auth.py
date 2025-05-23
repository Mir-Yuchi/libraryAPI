from fastapi.testclient import TestClient


def test_auth_flow(client: TestClient):
    # Register
    creds = {"email": "admin@example.com", "password": "secret"}
    resp = client.post("/auth/register", json=creds)
    assert resp.status_code == 201

    # Login
    login_data = {"username": creds["email"], "password": creds["password"]}
    token_resp = client.post("/auth/login", data=login_data)
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]

    # Access protected without a token
    assert client.get("/books/").status_code == 401

    # With token
    headers = {"Authorization": f"Bearer {token}"}
    assert client.get("/books/", headers=headers).status_code == 200
