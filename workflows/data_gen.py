"""
Mock Sales Data Generator
===========================
Produces realistic monthly sales data simulating an Oracle export.
Includes intentional data quality issues (nulls, dupes, mixed formats)
to demonstrate the AI cleaning step.
"""

import random
from datetime import datetime, timedelta

REGIONS    = ["APAC", "EMEA", "AMER", "LATAM"]
PRODUCTS   = ["Enterprise Suite", "DataBridge Pro", "SecureAI Gateway", "Analytics Hub"]
REPS       = ["Sarah K.", "James T.", "Mei L.", "Carlos R.", "Anna P.", "Tom W."]
STATUSES   = ["Closed Won", "Closed Won", "Closed Won", "Closed Lost", "Pending"]  # weighted

def _rand_date(month_offset=0):
    base = datetime.now().replace(day=1) - timedelta(days=30 * month_offset)
    return (base + timedelta(days=random.randint(0, 27))).strftime("%Y-%m-%d")

def _make_row(i: int, month_offset: int = 0) -> dict:
    return {
        "deal_id":   f"D{10000 + i}",
        "rep":       random.choice(REPS),
        "region":    random.choice(REGIONS),
        "product":   random.choice(PRODUCTS),
        "amount":    round(random.uniform(5_000, 150_000), 2),
        "status":    random.choice(STATUSES),
        "close_date": _rand_date(month_offset),
        "currency":  random.choice(["USD", "USD", "USD", "EUR", "GBP"]),  # mostly USD
    }

def generate(n: int = 120, month_offset: int = 0, dirty: bool = True) -> list[dict]:
    rows = [_make_row(i, month_offset) for i in range(n)]

    if dirty:
        # Inject data quality issues (realistic Oracle export problems)
        for i in random.sample(range(n), k=8):
            rows[i]["amount"] = None          # null amounts
        for i in random.sample(range(n), k=5):
            rows[i]["region"] = rows[i]["region"].lower()  # casing mismatch
        for i in random.sample(range(n), k=4):
            rows.append(rows[i].copy())       # duplicate rows
        for i in random.sample(range(n), k=3):
            rows[i]["currency"] = "eur"       # lowercase currency

    random.shuffle(rows)
    return rows

def get_two_months() -> tuple[list[dict], list[dict]]:
    """Return current month and previous month data."""
    current  = generate(n=120, month_offset=0, dirty=True)
    previous = generate(n=105, month_offset=1, dirty=False)
    return current, previous
