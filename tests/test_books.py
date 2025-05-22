import pytest
from fastapi.testclient import TestClient


def test_create_and_get_book(client: TestClient):
    # Create a new book
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "year": 1949,
        "isbn": "1234567890",
        "copies_available": 5,
    }
    resp = client.post("/books/", json=book_data)
    assert resp.status_code == 201
    created = resp.json()
    assert created["id"] == 1
    for key, value in book_data.items():
        assert created[key] == value

    # Retrieve the same book
    resp2 = client.get(f"/books/{created['id']}")
    assert resp2.status_code == 200
    assert resp2.json() == created


def test_read_books_list(client: TestClient):
    # Ensure list endpoint returns a list
    resp = client.get("/books/?skip=0&limit=10")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)


def test_update_and_delete_book(client: TestClient):
    # Create a book to update
    book_data = {"title": "Old Title", "author": "Auth", "copies_available": 1}
    resp = client.post("/books/", json=book_data)
    book_id = resp.json()["id"]

    # Update the book title
    update_data = {"title": "New Title"}
    resp2 = client.put(f"/books/{book_id}", json=update_data)
    assert resp2.status_code == 200
    assert resp2.json()["title"] == "New Title"

    # Delete the book
    resp3 = client.delete(f"/books/{book_id}")
    assert resp3.status_code == 204

    # Confirm deletion
    resp4 = client.get(f"/books/{book_id}")
    assert resp4.status_code == 404
