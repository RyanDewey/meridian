import requests
import os
from utils.db import get_conn
import json
from dotenv import load_dotenv

ACS_BASE_URL = 'https://api.census.gov/data'
load_dotenv()

# Returns raw data from acs
def fetch_acs_zcta(year: int, zcta: str, variables: list[str]) -> dict:
    # Build api url
    url = f"{ACS_BASE_URL}/{year}/acs/acs5"
    key = os.environ["CENSUS_API_KEY"]
    params = {
        "get": ",".join(variables),
        "for": f"zip code tabulation area:{zcta}",
    }
    # Add api key
    if key:
        params["key"] = key
    
    try:
        # Get population data from census api for ALL zip codes
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("The Census API timed out.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    try:
        # Turn into json format
        data = response.json()
    except Exception as e:
        print(f"Error turning raw data to json: {e}")

    # Return raw data
    return {"raw": data, "url": response.url}


# Saves raw data to the database
def save_raw_acs(zip_code: str, year: int, variables: list[str], payload: dict):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            insert into raw_acs_zip (zip, year, variables, payload)
            values (%s, %s, %s, %s::jsonb)
            """,
            (zip_code, year, variables, json.dumps(payload)),
        )

def run(year: int, zips: list[str]):
    variables = ["B01003_001E", "B19013_001E"]
    for z in zips:
        payload = fetch_acs_zcta(year, z, variables)
        save_raw_acs(z, year, variables, payload)
        print(f"✅ ACS saved raw for {z} ({year})")

if __name__ == "__main__":
    run(2023, [ 92672, 92673, 92624, 92675, 92629 ])