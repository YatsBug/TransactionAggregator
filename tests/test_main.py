from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert "message" in r.json()

def test_transactions_list():
    r = client.get("/transactions")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1 

def test_customer_endpoint():
    r = client.get("/transactions/customer/101")
    if r.status_code == 200:
        data = r.json()
        assert isinstance(data, list)
        assert all(t["customer_id"] == 101 for t in data)
    else:
        assert r.status_code == 404

def test_summary_all_and_customer():
    r_all = client.get("/transactions/summary")
    assert r_all.status_code == 200
    assert isinstance(r_all.json(), dict)

    r_cust = client.get("/transactions/summary?customer_id=101")
    assert r_cust.status_code in (200, 404)
    if r_cust.status_code == 200:
        assert isinstance(r_cust.json(), dict)

def test_category_filter():
    r = client.get("/transactions/category/Groceries")
    assert r.status_code in (200, 404)
    if r.status_code == 200:
        for t in r.json():
            assert "description" in t
            assert "category" in t
