"""
Manual Workflow Simulator
==========================
Simulates the BEFORE state — how a typical enterprise analyst
processes monthly sales reports manually.

Tracks time spent on each step to produce a realistic baseline.
"""

import time
import random

MANUAL_STEPS = [
    ("Open Oracle / export CSV",                  14.0),
    ("Clean data in Excel (remove dupes, fix nulls)", 22.0),
    ("Cross-reference with last month's sheet",   18.0),
    ("Write regional summary (copy-paste figures)", 25.0),
    ("Format report in Word / PowerPoint",        19.0),
    ("Email to stakeholders",                      4.0),
    ("Handle reply questions / corrections",      16.0),
]

def run_manual() -> dict:
    """
    Simulate a human analyst doing the monthly report.
    Returns timing breakdown and total.
    """
    print("\n  📋 MANUAL PROCESS (simulated)")
    print("  " + "─" * 48)

    steps = []
    total = 0.0

    for label, base_minutes in MANUAL_STEPS:
        # Add realistic variance ±20%
        actual = round(base_minutes * random.uniform(0.85, 1.20), 1)
        total += actual
        steps.append({"step": label, "minutes": actual})
        # Simulate elapsed time (compressed for demo)
        print(f"  ⏳ {label:<48} {actual:>5.1f} min")
        time.sleep(0.05)

    print(f"\n  Total time: {total:.1f} minutes ({total/60:.1f} hours)")
    return {"steps": steps, "total_minutes": round(total, 1)}
