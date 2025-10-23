from fastapi import FastAPI, HTTPException
import json
from pathlib import Path
from collections import defaultdict

app = FastAPI(title="Transaction Aggregation API")

# Load transactions from JSON file
DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "transactions.json"

def load_transactions():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Categorize transactions
def categorize(description: str) -> str:
    desc = description.lower()
    if "pick n pay" in desc or "checkers" in desc or "spar" in desc:
        return "Groceries"
    elif "uber" in desc or "bolt" in desc:
        return "Transport"
    elif "salary" in desc or "payroll" in desc:
        return "Income"
    else:
        return "Other"

@app.get("/")
def root():
    return {"message": "Transaction Aggregation API is running"}

@app.get("/transactions")
def get_all_transactions():
    transactions = load_transactions()
    for t in transactions:
        t["category"] = categorize(t["description"])
    return transactions

@app.get("/transactions/summary")
def get_summary():
    transactions = load_transactions()
    summary = defaultdict(lambda: {"total": 0.0, "count": 0})
    for t in transactions:
        category = categorize(t["description"])
        summary[category]["total"] += t["amount"]
        summary[category]["count"] += 1
    return summary

@app.get("/transactions/categories")
def get_totals_by_category():
    transactions = load_transactions()
    summary = defaultdict(lambda: {"total": 0.0, "count": 0})
    for t in transactions:
        category = categorize(t["description"])
        summary[category]["total"] += t["amount"]
        summary[category]["count"] += 1   
    return summary

@app.get("/transactions/{category}")
def get_transactions_by_category(category: str):
    transactions = load_transactions()
    filtered = []
    for t in transactions:
        if categorize(t["description"]).lower() == category.lower():
            filtered.append(t)
    if not filtered:
        raise HTTPException(status_code=404, detail="No transactions found for this category")
    return filtered
    
