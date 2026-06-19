"""
Automated AI Pipeline
======================
The AFTER state — replaces all manual steps with an automated pipeline.

Steps:
  1. Ingest raw data (simulates Oracle export)
  2. Auto-clean: remove nulls, fix casing, deduplicate
  3. Compute KPIs
  4. Send to Claude AI for narrative + recommendations
  5. Save report
"""

import time
import json
import os
import re
import requests
from datetime import datetime

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"

# ── Step 1: Clean data ────────────────────────────────────────────────────────

def clean(rows: list[dict]) -> tuple[list[dict], dict]:
    """Remove nulls, fix casing, deduplicate. Returns (clean_rows, quality_report)."""
    original_count = len(rows)
    seen = set()
    clean_rows = []
    nulls_removed = 0
    casing_fixed = 0
    dupes_removed = 0

    for row in rows:
        # Drop nulls
        if row.get("amount") is None:
            nulls_removed += 1
            continue
        # Fix casing
        if row["region"] != row["region"].upper():
            row["region"] = row["region"].upper()
            casing_fixed += 1
        if row["currency"] != row["currency"].upper():
            row["currency"] = row["currency"].upper()
            casing_fixed += 1
        # Deduplicate
        key = (row["deal_id"], row["close_date"])
        if key in seen:
            dupes_removed += 1
            continue
        seen.add(key)
        clean_rows.append(row)

    return clean_rows, {
        "original_rows":  original_count,
        "clean_rows":     len(clean_rows),
        "nulls_removed":  nulls_removed,
        "dupes_removed":  dupes_removed,
        "casing_fixed":   casing_fixed,
    }

# ── Step 2: KPI computation ────────────────────────────────────────────────────

def compute_kpis(current: list[dict], previous: list[dict]) -> dict:
    def won(rows):
        return [r for r in rows if r["status"] == "Closed Won"]

    cur_won  = won(current)
    prev_won = won(previous)

    def revenue(rows):
        return sum(r["amount"] for r in rows)

    def by_region(rows):
        out = {}
        for r in rows:
            out[r["region"]] = out.get(r["region"], 0) + r["amount"]
        return {k: round(v, 2) for k, v in sorted(out.items(), key=lambda x: -x[1])}

    def by_rep(rows):
        out = {}
        for r in rows:
            out[r["rep"]] = out.get(r["rep"], 0) + r["amount"]
        return {k: round(v, 2) for k, v in sorted(out.items(), key=lambda x: -x[1])}

    cur_rev  = revenue(cur_won)
    prev_rev = revenue(prev_won)
    mom      = round((cur_rev - prev_rev) / prev_rev * 100, 1) if prev_rev else 0

    win_rate = round(len(cur_won) / len(current) * 100, 1) if current else 0

    return {
        "current_revenue":   round(cur_rev, 2),
        "previous_revenue":  round(prev_rev, 2),
        "mom_growth_pct":    mom,
        "total_deals":       len(current),
        "won_deals":         len(cur_won),
        "win_rate_pct":      win_rate,
        "revenue_by_region": by_region(cur_won),
        "revenue_by_rep":    by_rep(cur_won),
        "top_region":        next(iter(by_region(cur_won)), "N/A"),
        "top_rep":           next(iter(by_rep(cur_won)), "N/A"),
    }

# ── Step 3: AI narrative ──────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior sales analyst at an enterprise software company.
Write concise, confident, executive-ready reports. No filler. Numbers must match the data.
Format in Markdown. Use Traditional Chinese for the Chinese section."""

def generate_report(kpis: dict, quality: dict, api_key: str) -> str:
    prompt = f"""Generate a monthly sales performance report based on this data.

KPIs:
{json.dumps(kpis, indent=2)}

Data quality summary:
{json.dumps(quality, indent=2)}

Structure:
# Monthly Sales Report — {datetime.now().strftime("%B %Y")}

## Executive Summary (3 sentences, English)

## 執行摘要（繁體中文，3 句）

## KPI Dashboard
(Markdown table: metric / this month / last month / change)

## Regional Performance
(Table + 1 sentence insight per region)

## Top Performers
(List top 3 reps with revenue)

## Recommendations
(3 bullet points, specific and actionable)

## Data Quality
(1 sentence noting what was auto-cleaned)
"""
    if not api_key:
        return _demo_report(kpis, quality)

    resp = requests.post(
        ANTHROPIC_API_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": "claude-sonnet-4-6",
            "max_tokens": 1500,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]

def _demo_report(kpis: dict, quality: dict) -> str:
    mom = kpis["mom_growth_pct"]
    arrow = "↑" if mom >= 0 else "↓"
    return f"""# Monthly Sales Report — {datetime.now().strftime("%B %Y")}
*(Demo mode — set ANTHROPIC_API_KEY for live AI narrative)*

## Executive Summary
Revenue reached **${kpis['current_revenue']:,.0f}** this month, a **{arrow}{abs(mom)}% MoM change**.
Win rate stands at **{kpis['win_rate_pct']}%** across {kpis['total_deals']} total deals.
{kpis['top_region']} leads all regions; {kpis['top_rep']} is the top-performing rep.

## 執行摘要（繁體中文）
本月營收達 **${kpis['current_revenue']:,.0f}**，月環比變化 **{arrow}{abs(mom)}%**。
整體成交率為 **{kpis['win_rate_pct']}%**，共 {kpis['total_deals']} 筆商機。
{kpis['top_region']} 地區表現最佳，{kpis['top_rep']} 為本月業績冠軍。

## KPI Dashboard
| Metric | This Month | Last Month | Change |
|---|---|---|---|
| Revenue | ${kpis['current_revenue']:,.0f} | ${kpis['previous_revenue']:,.0f} | {arrow}{abs(mom)}% |
| Won Deals | {kpis['won_deals']} | — | — |
| Win Rate | {kpis['win_rate_pct']}% | — | — |
| Top Region | {kpis['top_region']} | — | — |

## Regional Performance
{chr(10).join(f"| {r} | ${v:,.0f} |" for r, v in kpis['revenue_by_region'].items())}

## Top Performers
{chr(10).join(f"{i+1}. {rep} — ${rev:,.0f}" for i, (rep, rev) in enumerate(list(kpis['revenue_by_rep'].items())[:3]))}

## Recommendations
- Replicate {kpis['top_region']} playbook across underperforming regions
- Schedule pipeline reviews for reps below average win rate
- Investigate currency mix for EUR/GBP deals — potential FX exposure

## Data Quality
Auto-pipeline removed {quality['nulls_removed']} null records, {quality['dupes_removed']} duplicates, and fixed {quality['casing_fixed']} casing errors before analysis.
"""

def save(report: str, path: str = "reports") -> str:
    os.makedirs(path, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fpath = f"{path}/report_{ts}.md"
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(report)
    return fpath
