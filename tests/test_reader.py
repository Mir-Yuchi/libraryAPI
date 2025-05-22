from fastapi.testclient import TestClient


def test_create_and_get_reader(client: TestClient):
    # Create a new reader
    reader_data = {"name": "Alice", "email": "alice@example.com"}
    resp = client.post("/readers/", json=reader_data)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] == 1
    assert created["name"] == reader_data["name"]
    assert created["email"] == reader_data["email"]

    resp2 = client.get(f"/readers/{created['id']}")
    assert resp2.status_code == 200
    assert resp2.json() == created


def test_read_readers_list(client: TestClient):
    # Ensure list endpoint returns a list
    resp = client.get("/readers/?skip=0&limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_update_and_delete_reader(client: TestClient):
    # Create a reader to update
    reader_data = {"name": "Bob", "email": "bob@example.com"}
    resp = client.post("/readers/", json=reader_data)
    reader_id = resp.json()["id"]

    # Update the reader name
    update_data = {"name": "Robert"}
    resp2 = client.put(f"/readers/{reader_id}", json=update_data)
    assert resp2.status_code == 200
    assert resp2.json()["name"] == "Robert"

    # Delete the reader
    resp3 = client.delete(f"/readers/{reader_id}")
    assert resp3.status_code == 204

    # Confirm deletion
    resp4 = client.get(f"/readers/{reader_id}")
    assert resp4.status_code == 404
