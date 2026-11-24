import requests

BASE_URL = "http://127.0.0.1:8000"
BOOK_ID = 1
CATEGORY_ID = 1

def test_get_existing_book_http():
    response = requests.get(f"{BASE_URL}/books/{BOOK_ID}", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == BOOK_ID
    assert data["title"] == "Dune"

def test_get_books_collection_http():
    response = requests.get(f"{BASE_URL}/books", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 4

def test_get_books_contract_http():
    response = requests.get(f"{BASE_URL}/books", timeout=5)
    assert response.status_code == 200
    first_book = response.json()[0]
    expected_keys = {"book_id", "title", "isbn", "publication_year"}
    assert expected_keys.issubset(first_book.keys())

def test_get_books_known_data_http():
    response = requests.get(f"{BASE_URL}/books", timeout=5)
    assert response.status_code == 200
    titles = [book["title"] for book in response.json()]
    assert "Dune" in titles
    assert "Good Omens" in titles

def test_get_category_books_existing_http():
    response = requests.get(f"{BASE_URL}/categories/{CATEGORY_ID}/books", timeout=5)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    assert all(book["category"] == "Science Fiction" for book in data)

def test_get_category_books_nonexistent_http():
    response = requests.get(f"{BASE_URL}/categories/999/books", timeout=5)
    assert response.status_code == 200
    assert response.json() == []

def test_get_category_books_invalid_id_http():
    response = requests.get(f"{BASE_URL}/categories/xyz/books", timeout=5)
    assert response.status_code == 422
