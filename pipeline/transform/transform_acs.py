import json
from utils.db import get_conn
from dotenv import load_dotenv

load_dotenv()

def transform_latest_acs():
    """
    MVP: take the latest raw record per (zip, year) and upsert into stg_acs_zip
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            select distinct on (zip, year)
              zip, year, payload
            from raw_acs_zip
            order by zip, year, pulled_at desc
        """)
        rows = cur.fetchall()

        for zip_code, year, payload in rows:
            payload = payload  # already jsonb -> python dict in psycopg2? might be str depending config
            if isinstance(payload, str):
                payload = json.loads(payload)

            data = payload["raw"]
            headers = data[0]
            values = data[1]

            # Map header -> value
            m = dict(zip(headers, values))
            pop = int(m.get("B01003_001E")) if m.get("B01003_001E") not in (None, "") else None
            inc = int(m.get("B19013_001E")) if m.get("B19013_001E") not in (None, "") else None

            cur.execute("""
                insert into stg_acs_zip (zip, year, population, median_household_income)
                values (%s, %s, %s, %s)
                on conflict (zip, year) do update
                set population = excluded.population,
                    median_household_income = excluded.median_household_income
            """, (zip_code, year, pop, inc))

        print(f"✅ ACS transformed: {len(rows)} rows")

if __name__ == "__main__":
    transform_latest_acs()
