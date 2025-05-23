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


def test_borrow_and_return_flow(client: TestClient):
    headers = get_auth_header(client)
    reader = {"name": "Charlie", "email": "charlie@example.com"}
    resp_r = client.post("/readers/", json=reader, headers=headers)
    assert resp_r.status_code == 201
    reader_id = resp_r.json()["id"]

    book = {
        "title": "Dune",
        "author": "Frank Herbert",
        "year": 1965,
        "isbn": "1234567890123",
        "copies_available": 2,
    }
    resp_b = client.post("/books/", json=book, headers=headers)
    assert resp_b.status_code == 201
    book_id = resp_b.json()["id"]

    resp1 = client.post(
        "/borrow/", json={"book_id": book_id, "reader_id": reader_id}, headers=headers
    )
    assert resp1.status_code == 201
    borrow1 = resp1.json()
    assert borrow1["book_id"] == book_id
    assert borrow1["reader_id"] == reader_id

    resp_book = client.get(f"/books/{book_id}", headers=headers)
    assert resp_book.json()["copies_available"] == 1

    resp2 = client.post(
        "/borrow/", json={"book_id": book_id, "reader_id": reader_id}, headers=headers
    )
    assert resp2.status_code == 201

    resp3 = client.post(
        "/borrow/", json={"book_id": book_id, "reader_id": reader_id}, headers=headers
    )
    assert resp3.status_code == 400

    resp_ret = client.post(
        "/borrow/return",
        json={"book_id": book_id, "reader_id": reader_id},
        headers=headers,
    )
    assert resp_ret.status_code == 200
    ret = resp_ret.json()
    assert ret["return_date"] is not None

    resp_book2 = client.get(f"/books/{book_id}", headers=headers)
    assert resp_book2.json()["copies_available"] == 1

    resp4 = client.post(
        "/borrow/", json={"book_id": book_id, "reader_id": reader_id}, headers=headers
    )
    assert resp4.status_code == 201


def test_max_concurrent_borrows(client: TestClient):
    headers = get_auth_header(client)
    reader = {"name": "Dana", "email": "dana@example.com"}
    r = client.post("/readers/", json=reader, headers=headers).json()["id"]
    book_template = {"title": "1984", "author": "Orwell", "copies_available": 5}
    b = client.post("/books/", json=book_template, headers=headers).json()["id"]

    for _ in range(3):
        assert (
            client.post(
                "/borrow/", json={"book_id": b, "reader_id": r}, headers=headers
            ).status_code
            == 201
        )

    resp4 = client.post(
        "/borrow/", json={"book_id": b, "reader_id": r}, headers=headers
    )
    assert resp4.status_code == 400


def test_return_not_borrowed(client: TestClient):
    headers = get_auth_header(client)
    resp = client.post(
        "/borrow/return", json={"book_id": 999, "reader_id": 999}, headers=headers
    )
    assert resp.status_code == 404
