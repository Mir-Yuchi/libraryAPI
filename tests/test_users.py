def test_create_and_get_user(client):
    # 1) Create
    resp = client.post(
        "/users/", json={"email": "alice@example.com", "password": "secret123"}
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert data["is_active"] is True
    assert isinstance(data["id"], int)
    assert "created_at" in data

    # 2) Retrieve
    user_id = data["id"]
    resp2 = client.get(f"/users/{user_id}")
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "alice@example.com"


def test_duplicate_email_conflict(client):
    # First succeeds
    resp1 = client.post("/users/", json={"email": "bob@example.com", "password": "pw"})
    assert resp1.status_code == 201

    # Second with same email fails
    resp2 = client.post("/users/", json={"email": "bob@example.com", "password": "pw2"})
    assert resp2.status_code == 409
    assert resp2.json() == {"detail": "Email already registered"}


def test_update_and_delete_user(client):
    # Create
    resp = client.post(
        "/users/", json={"email": "carol@example.com", "password": "oldpw"}
    )
    uid = resp.json()["id"]

    # Update email
    resp2 = client.put(f"/users/{uid}", json={"email": "carol2@example.com"})
    assert resp2.status_code == 200
    assert resp2.json()["email"] == "carol2@example.com"

    # Delete
    resp3 = client.delete(f"/users/{uid}")
    assert resp3.status_code == 204

    # Now 404 on get
    resp4 = client.get(f"/users/{uid}")
    assert resp4.status_code == 404
