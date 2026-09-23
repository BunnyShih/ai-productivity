# AI-Driven Productivity

> Replaces a 2-hour manual sales reporting process with a fully automated AI pipeline that runs in seconds — with better accuracy.

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Claude API](https://img.shields.io/badge/Claude-API-orange) ![Productivity](https://img.shields.io/badge/Time_Saved-99%25-brightgreen)

---

## The Problem

Every month, sales analysts spend 2+ hours on a repetitive reporting cycle:

| Step | Time |
|---|---|
| Export data from Oracle | ~15 min |
| Clean in Excel (nulls, dupes, casing) | ~25 min |
| Cross-reference prior month | ~20 min |
| Write regional narrative | ~25 min |
| Format in Word / PowerPoint | ~20 min |
| Email + handle follow-up corrections | ~15 min |
| **Total** | **~2 hours** |

Multiply by 12 months × number of teams. This is a solved problem.

---

## The Solution

A 4-step automated pipeline that produces the same output in under 5 seconds:

```
[1] Ingest Oracle export
        ↓
[2] Auto-clean: nulls → dropped, dupes → removed, casing → normalised
        ↓
[3] Compute KPIs: revenue, MoM growth, win rate, regional breakdown, top reps
        ↓
[4] Claude AI: generate bilingual executive report (English + Traditional Chinese)
        ↓
    📄 report_YYYYMMDD.md  — ready to send
```

---

## Results

```
  Manual process   : 1.9 hours
  AI pipeline      : 4.1 seconds
  Time saved       : 1.9 hours (99% reduction)
  Human errors     : 12 data issues auto-fixed
```

---

## Quick Start

```bash
git clone https://github.com/BunnyShih/ai-productivity
cd ai-productivity

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# Demo mode (no API key needed — AI narrative simulated)
python main.py

# Live mode with real Claude AI report
export ANTHROPIC_API_KEY=sk-ant-...
python main.py
```

---

## Sample Output

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  BEFORE: Manual Analyst Workflow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ⏳ Open Oracle / export CSV              12.6 min
  ⏳ Clean data in Excel                   24.6 min
  ⏳ Cross-reference last month            18.8 min
  ⏳ Write regional summary                21.6 min
  ⏳ Format report                         17.3 min
  ⏳ Email + corrections                   17.6 min
  Total: 112.5 minutes (1.9 hours)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AFTER: Automated AI Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [1/4] Ingesting Oracle export...   124 rows in 4ms
  [2/4] Auto-cleaning...             8 nulls, 4 dupes, 8 casing fixes
  [3/4] Computing KPIs...            $5.3M revenue | +14.8% MoM
  [4/4] Generating AI report...      done

  ✅ Report saved → reports/report_20260617.md
```

---

## Project Structure

```
ai-productivity/
├── workflows/
│   ├── manual.py       # Simulates manual process with realistic timing
│   └── data_gen.py     # Mock Oracle export with realistic data quality issues
├── ai/
│   └── pipeline.py     # Clean → KPIs → Claude API → save
├── reports/            # Generated reports (auto-created)
└── main.py             # BEFORE vs AFTER comparison runner
```

---

## Adapting to Your Stack

| Change | Where |
|---|---|
| Real Oracle data | Replace `data_gen.py` with `cx_Oracle` connector |
| Different data source | Swap ingest step — pipeline is source-agnostic |
| Slack/email delivery | Add step after `save()` in `main.py` |
| Scheduled runs | Wrap `main.py` in cron / Airflow / GitHub Actions |
| Different language output | Change `SYSTEM_PROMPT` in `pipeline.py` |

---

## Skills Demonstrated

| Skill | Implementation |
|---|---|
| **AI-Driven Productivity** | End-to-end automation with before/after measurement |
| **Legacy Data Integration** | Oracle export ingestion + auto data cleaning |
| **AI Report Generation** | Bilingual executive reports via Claude API |

---

## License

MIT
