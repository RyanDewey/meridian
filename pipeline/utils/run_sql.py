import os
from pathlib import Path
from db import get_conn

def run_sql_file(path: str) -> None:
    sql = Path(path).read_text(encoding="utf-8")
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)

def run_sql_dir(sql_dir: str, filenames: list[str]) -> None:
    for f in filenames:
        full = os.path.join(sql_dir, f)
        print(f"Running {full} ...")
        run_sql_file(full)
    print("✅ SQL transforms complete.")
