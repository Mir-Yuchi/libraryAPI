from fastapi.testclient import TestClient


def test_end_to_end_flow(client: TestClient):
    # 1) Register & 2) Login
    creds = {"email": "end2end@example.com", "password": "complexpw"}
    r1 = client.post("/auth/register", json=creds)
    assert r1.status_code == 201
    token_resp = client.post(
        "/auth/login",
        data={"username": creds["email"], "password": creds["password"]},
    )
    assert token_resp.status_code == 200
    token = token_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3) Create book
    book_payload = {
        "title": "E2E Book",
        "author": "Tester",
        "year": 2025,
        "isbn": "0001112223",
        "copies_available": 1,
    }
    b = client.post("/books/", json=book_payload, headers=headers)
    assert b.status_code == 201
    book_id = b.json()["id"]

    # 4) Create reader
    reader_payload = {"name": "Test Reader", "email": "reader@e2e.com"}
    r2 = client.post("/readers/", json=reader_payload, headers=headers)
    assert r2.status_code == 201
    reader_id = r2.json()["id"]

    # 5) Borrow
    borrow_resp = client.post(
        "/borrow/", json={"book_id": book_id, "reader_id": reader_id}, headers=headers
    )
    assert borrow_resp.status_code == 201
    assert borrow_resp.json()["book_id"] == book_id

    # 6) Return
    ret_resp = client.post(
        "/borrow/return",
        json={"book_id": book_id, "reader_id": reader_id},
        headers=headers,
    )
    assert ret_resp.status_code == 200
    assert ret_resp.json()["return_date"] is not None

    # 7) Final state: copies_available back to 1
    final_book = client.get(f"/books/{book_id}", headers=headers).json()
    assert final_book["copies_available"] == 1
