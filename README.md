# Transaction Aggregation API

A simple **FastAPI** backend that reads transaction data from local JSON
files, categorizes it, and provides both detailed and summarized endpoints
for analysis.


## Features

- Load transaction data from `data/transactions.json`
- Automatically categorize transactions (e.g. Groceries, Transport, Income...)
- View all transactions
- View category summaries
- Ready to run with **Docker** (no setup needed)

# Folder Structure

```text
📁 TRANSACTIONAGGREGATOR/
├── 📂 app/
│   ├── 📄 __init__.py
│   └── 📄 main.py
├── 📂 data/
│   ├── 📄 customer_101.json
│   ├── 📄 customer_102.json
│   ├── 📄 customer_103.json
│   └── 📄 transactions.json
├── 📂 tests/
│   └── 📄 test_main.py
├── ⚙️ Dockerfile
├── 📘 README.md
└── 📄 requirements.txt
```

---

# How to Run the App

## Option 1: Run with Docker (Recommended)

### Note for Linux users:

> On **Linux**, you may need to use `sudo` before any docker command.

### Note for Windows users:

> If when you run `.venv\Scripts\activate` you see an Error, this is because
PowerShell blocks scripts by default for security reasons. You can safely fix
this **temporarily** by running:
- `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- `. .venv\Scripts\Activate.ps1`

### Step 1: Build the Docker image

#### Windows:
```bash
docker build -t transaction-aggregator:latest .
```

#### Linux:

```bash
sudo docker build -t transaction-aggregator:latest .
```

### Step 2: Run the container

#### Windows:
```bash
docker run -p 8000:8000 transaction-aggregator:latest
```

#### Linux:

```bash
sudo docker run -p 8000:8000 transaction-aggregator:latest
```

### Step 3: Verify it's running

Open your browser and visit:
- http://127.0.0.1:8000 {API Status}
- http://127.0.0.1:8000/transactions {All transactions}
- http://127.0.0.1:8000/transactions/summary {Aggregated summary}
- http://127.0.0.1:8000/docs {Swagger UI}

## Option 2: Run Locally (Without Docker)

### Step 1: Create and activate virtual environment

#### Windows:

```bash
python -m venv .venv
.venv/Scripts/activate
```

#### Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the app

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

# API Endpoints

| Endpoint                                 | Method | Description                                                          |
| -----------------------------------------| ------ | ---------------------------------------------------------------------|
| `/`                                      | GET    | Health Check                                                         |
| `/transactions`                          | GET    | Returns all transactions with categories                             |
| `/transactions/customer/{customer_id}`   | GET    | Transactions filtered by customer_id                                 |
| `/transactions/summary`                  | GET    | Aggregated totals by category optionally filtered by customer_id     |
| `/transactions/category/{category_name}` | GET    | Transactions filtered by category optionally filtered by customer_id |


# Example Output:

## /transactions

```json
{
  "0": {
    "id": 1,
    "customer_id": 101,
    "amount": 120.5,
    "description": "Pick n Pay",
    "date": "2025-10-08",
    "category": "Groceries"
  },
  "1": {
    "id": 2,
    "customer_id": 101,
    "amount": 45.0,
    "description": "Uber Trip",
    "date": "2025-10-03",
    "category": "Transport"
  },
  "2": {
    "id": 3,
    "customer_id": 101,
    "amount": 3000.0,
    "description": "Salary",
    "date": "2025-10-01",
    "category": "Income"
  },
  "3": {
    "id": 4,
    "customer_id": 101,
    "amount": 322.23,
    "description": "Woolworths Clothing",
    "date": "2025-10-05",
    "category": "Clothing"
  }
}
```

## transactions/customer/103

```json
{
  "0": {
    "id": 1,
    "customer_id": 103,
    "amount": 200.0,
    "description": "Woolworths Food",
    "date": "2025-10-11",
    "category": "Groceries"
  },
  "1": {
    "id": 2,
    "customer_id": 103,
    "amount": 75.0,
    "description": "Uber trip",
    "date": "2025-10-15",
    "category": "Transport"
  },
  "2": {
    "id": 3,
    "customer_id": 103,
    "amount": 329.99,
    "description": "Boxer",
    "date": "2025-10-17",
    "category": "Groceries"
  },
  "3": {
    "id": 4,
    "customer_id": 103,
    "amount": 24300.27,
    "description": "Salary",
    "date": "2025-10-01",
    "category": "Income"
  }
}
```

## transactions/summary

```json
{
  "Groceries": {
    "total": "770.99",
    "count": 4
  },
  "Transport": {
    "total": "165.0",
    "count": 3
  },
  "Income": {
    "total": "27300.27",
    "count": 2
  },
  "Clothing": {
    "total": "322.23",
    "count": 1
  },
  "Entertainment": {
    "total": "180.0",
    "count": 1
  }
}
```

## transactions/summary?customer_id=102

```json
{
  "Groceries": {
    "total": 120.5,
    "count": 1
  },
  "Transport": {
    "total": 45.0,
    "count": 1
  },
  "Entertainment": {
    "total": 180.0,
    "count": 1
  }
}
```

## /transactions/category/income

```json
{
  "0": {
    "id": 3,
    "customer_id": 101,
    "amount": 3000.0,
    "description": "Salary",
    "date": "2025-10-01",
    "category": "Income"
  },
  "1": {
    "id": 4,
    "customer_id": 103,
    "amount": 24300.27,
    "description": "Salary",
    "date": "2025-10-01",
    "category": "Income"
  }
}
```

## transactions/category/groceries?customer_id=103

```json
{
  "0": {
    "id": 1,
    "customer_id": 103,
    "amount": 200.0,
    "description": "Woolworths Food",
    "date": "2025-10-11",
    "category": "Groceries"
  },
  "1": {
    "id": 3,
    "customer_id": 103,
    "amount": 329.99,
    "description": "Boxer",
    "date": "2025-10-17",
    "category": "Groceries"
  }
}
```

# Tech Stack:

- **Python 3.13.9**
- **FastAPI**
- **Uvicorn**
- **Docker**

# License

This project was developed as part of a technical assessment and personal
learning project.
You are free to **resuse or modify the structure** for learning, portfolio,
or demonstration purposes.