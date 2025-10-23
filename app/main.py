from fastapi import FastAPI, HTTPException
import json
import logging
from pathlib import Path
from collections import defaultdict

app = FastAPI(title="Transaction Aggregation API")

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

logger = logging.getLogger("transaction_api")
logger.setLevel(logging.INFO)

def load_transactions():
    all_transactions = []
    if not DATA_DIR.exists():
        raise RuntimeError(f"Data directory {DATA_DIR} not found")

    for file in sorted(DATA_DIR.glob("*.json")):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    logger.warning("Skipping %s: expected a JSON array at root", file)
                    continue
                for t in data:
                    if not isinstance(t, dict):
                        logger.warning("Skipping item in %s: not an object", file)
                        continue
                    # require id, customer_id, amount, description
                    if "id" not in t or "customer_id" not in t or "amount" not in t or "description" not in t:
                        logger.warning("Skipping item in %s: missing required fields", file)
                        continue
                    all_transactions.append(t)
        except json.JSONDecodeError:
            logger.exception("Skipping %s: invalid JSON", file)
        except Exception:
            logger.exception("Error reading %s", file)

    return all_transactions

# Define keywords per category
CATEGORY_KEYWORDS = {
    "Groceries": ["pick n pay", "checkers", "spar", "woolworths food", "shoprite", "ok", "picknpay", "boxer", "food"],
    "Transport": ["uber", "bolt", "bus", "train", "taxi"],
    "Clothing": ["edgars", "woolworths clothing", "h&m", "cotton on", "pep", "ackermans", "clothing"],
    "Income": ["salary", "payroll", "bonus", "payment"],
    "Entertainment": ["cinema", "movie"],
    "Subscriptions": ["netflix", "disneyplus", "telkom", "dstv", "amazon prime", "spotify", "vodacom"],
    "Utilities": ["electricity", "water", "internet"]
}

def categorize(description: str) -> str:
    desc = (description or "").lower()
    # exact match or contains any keyword
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in desc for k in keywords):
            return category
    return "Other"

@app.get("/")
def root():
    return {"message": "Transaction Aggregation API is running"}

@app.get("/transactions")
def get_all_transactions():
    transactions = load_transactions()
    # annotate category for each transaction (non-mutating copy if you want)
    for t in transactions:
        t["category"] = categorize(t.get("description", ""))
    return transactions

@app.get("/transactions/customer/{customer_id}")
def get_transactions_for_customer(customer_id: int):
    transactions = load_transactions()
    filtered = [t for t in transactions if int(t.get("customer_id", -1)) == int(customer_id)]
    if not filtered:
        raise HTTPException(status_code=404, detail="No transactions found for this customer")
    for t in filtered:
        t["category"] = categorize(t.get("description", ""))
    return filtered

@app.get("/transactions/summary")
def get_summary(customer_id: int = None):
    transactions = load_transactions()
    if customer_id is not None:
        transactions = [t for t in transactions if int(t.get("customer_id", -1)) == int(customer_id)]

    summary = defaultdict(lambda: {"total": 0.0, "count": 0})
    for t in transactions:
        category = categorize(t.get("description", ""))
        # cast amount defensively
        try:
            amount = float(t.get("amount", 0.0))
        except Exception:
            amount = 0.0
        summary[category]["total"] += amount
        summary[category]["count"] += 1

    return summary

@app.get("/transactions/category/{category_name}")
def get_transactions_by_category(category_name: str, customer_id: int = None):
    transactions = load_transactions()
    if customer_id is not None:
        transactions = [t for t in transactions if int(t.get("customer_id", -1)) == int(customer_id)]

    filtered = [t for t in transactions if categorize(t.get("description", "")).lower() == category_name.lower()]
    if not filtered:
        raise HTTPException(status_code=404, detail="No transactions found for this category")
    for t in filtered:
        t["category"] = categorize(t.get("description", ""))
    return filtered

