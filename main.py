#!/usr/bin/env python3
"""
AI-Driven Productivity Demo
=============================
Shows BEFORE vs AFTER: manual report process vs automated AI pipeline.

Usage:
    python main.py
    ANTHROPIC_API_KEY=sk-ant-... python main.py
"""

import os
import sys
import time

sys.path.insert(0, ".")

from workflows.manual   import run_manual
from workflows.data_gen import get_two_months
from ai.pipeline        import clean, compute_kpis, generate_report, save

BANNER = """
╔════════════════════════════════════════════════════╗
║       AI-Driven Productivity Demo  v1.0           ║
║  Manual Process  →  Automated AI Pipeline         ║
╚════════════════════════════════════════════════════╝
"""

def fmt_time(minutes: float) -> str:
    if minutes >= 60:
        return f"{minutes/60:.1f} hrs"
    return f"{minutes:.1f} min"

def main():
    print(BANNER)
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("  ⚠️  Demo mode (no ANTHROPIC_API_KEY) — AI narrative is simulated.\n")

    # ── BEFORE ────────────────────────────────────────────────────────────────
    print("━" * 56)
    print("  BEFORE: Manual Analyst Workflow")
    print("━" * 56)
    manual_result = run_manual()
    manual_minutes = manual_result["total_minutes"]

    # ── AFTER ─────────────────────────────────────────────────────────────────
    print("\n" + "━" * 56)
    print("  AFTER: Automated AI Pipeline")
    print("━" * 56 + "\n")

    t0 = time.time()

    print("  [1/4] Ingesting Oracle data export...")
    current_raw, previous_raw = get_two_months()
    t1 = time.time()
    print(f"        {len(current_raw)} rows loaded in {(t1-t0)*1000:.0f}ms")

    print("  [2/4] Auto-cleaning data...")
    current_clean, quality = clean(current_raw)
    previous_clean, _      = clean(previous_raw)
    t2 = time.time()
    print(f"        Removed {quality['nulls_removed']} nulls, "
          f"{quality['dupes_removed']} dupes, fixed {quality['casing_fixed']} casing errors "
          f"({(t2-t1)*1000:.0f}ms)")

    print("  [3/4] Computing KPIs...")
    kpis = compute_kpis(current_clean, previous_clean)
    t3 = time.time()
    print(f"        Revenue ${kpis['current_revenue']:,.0f} | "
          f"MoM {kpis['mom_growth_pct']:+.1f}% | "
          f"Win rate {kpis['win_rate_pct']}% ({(t3-t2)*1000:.0f}ms)")

    print("  [4/4] Generating AI report...")
    report = generate_report(kpis, quality, api_key)
    t4 = time.time()
    print(f"        Report ready ({(t4-t3)*1000:.0f}ms)")

    report_path = save(report, path="reports")
    total_seconds = t4 - t0
    ai_minutes = total_seconds / 60

    # ── Comparison ────────────────────────────────────────────────────────────
    reduction = round((1 - ai_minutes / manual_minutes) * 100)
    speedup   = round(manual_minutes / ai_minutes)

    print(f"\n{'━'*56}")
    print("  📊 BEFORE vs AFTER")
    print(f"{'━'*56}")
    print(f"  Manual process   : {fmt_time(manual_minutes)}")
    print(f"  AI pipeline      : {total_seconds:.1f} seconds")
    print(f"  Time saved       : {fmt_time(manual_minutes - ai_minutes)} ({reduction}% reduction)")
    print(f"  Speed multiplier : {speedup}x faster")
    print(f"  Human errors     : {quality['nulls_removed'] + quality['dupes_removed']} issues auto-fixed")
    print(f"{'━'*56}")
    print(f"\n  ✅  Report saved → {report_path}\n")

    print("=" * 56)
    print(report[:1200] + ("\n  ...[truncated — see file for full report]" if len(report) > 1200 else ""))
    print("=" * 56 + "\n")

if __name__ == "__main__":
    main()
