from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_transactions():
    r = client.get("/transactions")
    assert isinstance(r.json(), list)
    assert len(r.json()) > 0

def test_categories():
    r = client.get("/transactions/categories")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert all("total" in v and "count" in v for v in data.values())

def test_category_filter():
    #Pick a category
    r = client.get("/transactions/Groceries")
    if r.status_code == 200:
        for t in r.json():
            assert "description" in t
    else:
        assert r.status_code == 404