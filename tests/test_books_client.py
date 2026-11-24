from api.main import app
from fastapi.testclient import TestClient

BOOK_ID = 1
CATEGORY_ID = 1


# Guided test (R-02: Existing book lookup)
def test_get_existing_book_client():
  with TestClient(app) as client:
    response = client.get(f"/books/{BOOK_ID}")
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == BOOK_ID
    assert data["title"] == "Dune"


# R-01 Scenario 1: Available collection with records
def test_get_books_collection_client():
  with TestClient(app) as client:
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4


# R-01 Scenario 2: Response structure matches the API contract
def test_get_books_contract_client():
  with TestClient(app) as client:
    response = client.get("/books")
    assert response.status_code == 200
    first_book = response.json()[0]
    expected_keys = {"book_id", "title", "isbn", "publication_year"}
    assert expected_keys.issubset(first_book.keys())


# R-01 Scenario 3: Returned records match known seed data
def test_get_books_known_data_client():
  with TestClient(app) as client:
    response = client.get("/books")
    assert response.status_code == 200
    titles = [book["title"] for book in response.json()]
    assert "Dune" in titles
    assert "Good Omens" in titles


# R-03 Scenario 1: Existing category containing books
def test_get_category_books_existing_client():
  with TestClient(app) as client:
    response = client.get(f"/categories/{CATEGORY_ID}/books")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(book["category"] == "Science Fiction" for book in data)


# R-03 Scenario 2: Category ID that does not exist
def test_get_category_books_nonexistent_client():
  with TestClient(app) as client:
    response = client.get("/categories/999/books")
    assert response.status_code == 200
    assert response.json() == []


# R-03 Scenario 3: Invalid non-numeric category identifier
def test_get_category_books_invalid_id_client():
  with TestClient(app) as client:
    response = client.get("/categories/xyz/books")
    assert response.status_code == 422
    