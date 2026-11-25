"""python3 run.py YYYY-MM-DD: print what etl/daily_totals.sql returns for that day."""

import os
import sqlite3
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
day = sys.argv[1] if len(sys.argv) > 1 else "2026-11-10"
db = sqlite3.connect(":memory:")
with open(os.path.join(ROOT, "data", "seed.sql"), encoding="utf-8") as f:
    db.executescript(f.read())
with open(os.path.join(ROOT, "etl", "daily_totals.sql"), encoding="utf-8") as f:
    query = f.read().strip().rstrip(";")
cur = db.execute(query, {"day": day})
print(" | ".join(c[0] for c in cur.description))
for row in cur.fetchall():
    print(" | ".join(str(v) for v in row))
