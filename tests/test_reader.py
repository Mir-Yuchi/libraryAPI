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


def test_create_and_get_reader(client: TestClient):
    headers = get_auth_header(client)
    # 1) Create
    reader_data = {"name": "Alice", "email": "alice@example.com"}
    resp = client.post("/readers/", json=reader_data, headers=headers)
    assert resp.status_code == 201
    created = resp.json()
    assert isinstance(created["id"], int) and created["id"] > 0
    assert created["name"] == reader_data["name"]
    assert created["email"] == reader_data["email"]

    # 2) Retrieve
    resp2 = client.get(f"/readers/{created['id']}", headers=headers)
    assert resp2.status_code == 200
    assert resp2.json() == created


def test_read_readers_list(client: TestClient):
    headers = get_auth_header(client)
    resp = client.get("/readers/?skip=0&limit=10", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_update_and_delete_reader(client: TestClient):
    headers = get_auth_header(client)
    # Create
    reader_data = {"name": "Bob", "email": "bob@example.com"}
    resp = client.post("/readers/", json=reader_data, headers=headers)
    reader_id = resp.json()["id"]

    # Update
    update_data = {"name": "Robert"}
    resp2 = client.put(f"/readers/{reader_id}", json=update_data, headers=headers)
    assert resp2.status_code == 200
    assert resp2.json()["name"] == "Robert"

    # Delete
    resp3 = client.delete(f"/readers/{reader_id}", headers=headers)
    assert resp3.status_code == 204

    # Confirm deletion
    resp4 = client.get(f"/readers/{reader_id}", headers=headers)
    assert resp4.status_code == 404
