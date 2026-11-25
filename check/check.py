"""`python3 check/check.py`: one line per task, for the interviewer. Do not edit anything in check/ or data/.
Standard library only (SQLite comes with Python)."""

import hashlib
import os
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D1, D2 = "2026-11-10", "2026-11-11"
EXPECTED_D1 = {"ana": (5000, 2), "ben": (4000, 1), "caro": (3000, 1), "dan": (1500, 1),
               "eve": (3500, 1), "frank": (1200, 1)}


def read(path):
    try:
        with open(os.path.join(ROOT, path), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def statements(sql):
    return [s for s in (part.strip() for part in sql.split(";")) if s and not all(
        l.strip().startswith("--") or not l.strip() for l in s.splitlines())]


def new_db():
    db = sqlite3.connect(":memory:")
    db.executescript(read("data/seed.sql"))
    return db


def extract(db, day):
    query = read("etl/daily_totals.sql").strip().rstrip(";")
    return {r[0]: (r[1], r[2]) for r in db.execute(query, {"day": day}).fetchall()}


def run_job(db, day):
    query = read("etl/daily_totals.sql").strip().rstrip(";")
    db.execute("DROP TABLE IF EXISTS temp.staging")
    db.execute(f"CREATE TEMP TABLE staging AS SELECT user_id, total_cents, payment_count FROM ({query})", {"day": day})
    for s in statements(read("etl/load.sql")):
        db.execute(s, {"day": day})
    db.commit()


errors = []
got = {}
try:
    got = extract(new_db(), D1)
except Exception as e:  # noqa: BLE001
    errors.append(f"extract: {e}")

ok = lambda u: got.get(u) == EXPECTED_D1[u]
t1a = ok("ana")                      # duplicate 'settled' event counted once
t1b = ok("dan")                      # completed but not settled yet: does not count
t2a = ok("ben")                      # refunded payment excluded
t2b = ok("caro") and ok("eve") and "gus" not in got   # only payments created that day
t1 = t1a and t1b                     # both, so dropping the 'settled' rule does not pass
t2 = t2a + t2b

t3a = t3b = False
try:
    db = new_db()
    for s in statements(read("etl/target.sql")):
        db.execute(s)
    one = new_db()
    one_d1, one_d2 = extract(one, D1), extract(one, D2)
    run_job(db, D1)
    run_job(db, D2)
    run_job(db, D1)
    rows = db.execute("SELECT day, user_id, total_cents, payment_count FROM daily_totals").fetchall()
    rows_d1 = sorted(r[1:] for r in rows if r[0] == D1)
    rows_d2 = sorted(r[1:] for r in rows if r[0] == D2)
    t3a = bool(one_d1) and rows_d1 == sorted((u, *v) for u, v in one_d1.items())
    t3b = bool(one_d2) and rows_d2 == sorted((u, *v) for u, v in one_d2.items())
except Exception as e:  # noqa: BLE001
    errors.append(f"job: {e}")

h = hashlib.sha256()
for rel in ["data/seed.sql"] + sorted("check/" + f for f in os.listdir(os.path.join(ROOT, "check")) if f.endswith(".py")):
    h.update(rel.encode())
    with open(os.path.join(ROOT, rel), "rb") as fh:
        h.update(fh.read())


def line(label, text):
    print(label.ljust(24, ".") + " " + text)


mark = lambda b: "✓" if b else "✗"
print("\nDaily payments ETL — check\n")
line("T1 Counted once", f"{int(t1)}/1  duplicate event counted once {mark(t1a)}  still only settled payments {mark(t1b)}")
line("T2 Payments and day", f"{t2}/2  refunds excluded {mark(t2a)}  only that day {mark(t2b)}")
line("T3 Safe to run again", f"{int(t3a and t3b)}/1  retry leaves the day the same {mark(t3a)}  other days kept {mark(t3b)}")
for e in errors:
    line("SQL error", e)
line("Check files", h.hexdigest()[:8])
print("")
