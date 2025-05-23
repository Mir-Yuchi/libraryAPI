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


def test_create_and_get_book(client: TestClient):
    headers = get_auth_header(client)
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "isbn": "1234567890",
        "copies_available": 5,
    }
    resp = client.post("/books/", json=book_data, headers=headers)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] == 1
    for key, value in book_data.items():
        assert created[key] == value

    resp2 = client.get(f"/books/{created['id']}", headers=headers)
    assert resp2.status_code == 200
    assert resp2.json() == created


def test_read_books_list(client: TestClient):
    headers = get_auth_header(client)
    resp = client.get("/books/?skip=0&limit=10", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_update_and_delete_book(client: TestClient):
    headers = get_auth_header(client)
    book_data = {
        "title": "Old Title",
        "author": "Auth",
        "copies_available": 1,
    }
    resp = client.post("/books/", json=book_data, headers=headers)
    book_id = resp.json()["id"]

    # Update
    update_data = {"title": "New Title"}
    resp2 = client.put(f"/books/{book_id}", json=update_data, headers=headers)
    assert resp2.status_code == 200
    assert resp2.json()["title"] == "New Title"

    # Delete
    resp3 = client.delete(f"/books/{book_id}", headers=headers)
    assert resp3.status_code == 204

    # Confirm deletion
    resp4 = client.get(f"/books/{book_id}", headers=headers)
    assert resp4.status_code == 404
