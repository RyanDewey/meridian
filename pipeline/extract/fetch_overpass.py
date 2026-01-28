import json
import time
import hashlib
from dataclasses import dataclass
from typing import Dict, Any, Optional, Tuple
import requests
from dotenv import load_dotenv

from utils.db import get_conn

load_dotenv()

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

@dataclass
class OverpassResult:
    status_code: int
    duration_ms: int
    response_bytes: int
    payload: Optional[Dict[str, Any]]
    error_text: Optional[str]

def sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def build_overpass_query_restaurants_cuisine_bbox(
    south: float, west: float, north: float, east: float,
    cuisine_regex: str = "chinese",
    include_fast_food: bool = True,
) -> str:
    """
    Returns Overpass QL to fetch restaurants (and optionally fast food) with cuisine matching regex,
    within a bounding box (south,west,north,east).
    """
    # Overpass uses (south,west,north,east)
    amenity_parts = ['"amenity"="restaurant"']
    if include_fast_food:
        amenity_parts.append('"amenity"="fast_food"')

    # We'll query nodes + ways + relations and output center points for areas.
    # "out center" adds center for ways/relations, nodes have lat/lon directly.
    # Note: cuisine tag may be multiple values like "chinese;noodles"
    query = f"""
    [out:json][timeout:25];
    (
      {";".join([f'node[{a}]["cuisine"~"{cuisine_regex}",i]({south},{west},{north},{east})' for a in amenity_parts])};
      {";".join([f'way[{a}]["cuisine"~"{cuisine_regex}",i]({south},{west},{north},{east})' for a in amenity_parts])};
      {";".join([f'relation[{a}]["cuisine"~"{cuisine_regex}",i]({south},{west},{north},{east})' for a in amenity_parts])};
    );
    out tags center;
    """
    return "\n".join(line.strip() for line in query.splitlines() if line.strip())

def call_overpass(query_text: str, max_retries: int = 5) -> OverpassResult:
    """
    Calls Overpass. Retries on 429/502/503/504 and timeouts with exponential backoff.
    """
    backoff = 2.0
    last_error = None

    for attempt in range(max_retries + 1):
        t0 = time.time()
        try:
            r = requests.post(
                OVERPASS_URL,
                data={"data": query_text},
                timeout=60,
                headers={"Accept": "application/json"},
            )
            duration_ms = int((time.time() - t0) * 1000)
            response_bytes = len(r.content or b"")

            if r.status_code == 200:
                try:
                    return OverpassResult(
                        status_code=200,
                        duration_ms=duration_ms,
                        response_bytes=response_bytes,
                        payload=r.json(),
                        error_text=None,
                    )
                except Exception as e:
                    # JSON parse error
                    return OverpassResult(
                        status_code=200,
                        duration_ms=duration_ms,
                        response_bytes=response_bytes,
                        payload=None,
                        error_text=f"JSON parse error: {e}",
                    )

            # Retryable statuses
            if r.status_code in (429, 502, 503, 504) and attempt < max_retries:
                last_error = f"HTTP {r.status_code}: {r.text[:300]}"
                time.sleep(backoff)
                backoff *= 2
                continue

            # Non-retryable or final attempt
            return OverpassResult(
                status_code=r.status_code,
                duration_ms=duration_ms,
                response_bytes=response_bytes,
                payload=None,
                error_text=r.text[:1000],
            )

        except (requests.Timeout, requests.ConnectionError) as e:
            duration_ms = int((time.time() - t0) * 1000)
            if attempt < max_retries:
                last_error = f"{type(e).__name__}: {e}"
                time.sleep(backoff)
                backoff *= 2
                continue
            return OverpassResult(
                status_code=0,
                duration_ms=duration_ms,
                response_bytes=0,
                payload=None,
                error_text=f"{type(e).__name__}: {e}",
            )

    # Shouldn't reach here, but just in case
    return OverpassResult(
        status_code=0,
        duration_ms=0,
        response_bytes=0,
        payload=None,
        error_text=last_error or "Unknown error",
    )

def save_raw_overpass(
    query_name: str,
    query_text: str,
    query_params: Dict[str, Any],
    result: OverpassResult,
) -> int:
    qhash = sha256_text(query_text + "\n" + json.dumps(query_params, sort_keys=True))

    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            insert into raw_overpass_query (
              query_name, query_text, query_params, query_hash,
              status_code, duration_ms, response_bytes, payload
            )
            values (%s, %s, %s::jsonb, %s, %s, %s, %s, %s::jsonb)
            returning id
            """,
            (
                query_name,
                query_text,
                json.dumps(query_params),
                qhash,
                result.status_code,
                result.duration_ms,
                result.response_bytes,
                json.dumps(result.payload) if result.payload is not None else None,
            ),
        )
        row_id = cur.fetchone()[0]
        return row_id

def run_example_san_clemente_bbox():
    # San Clemente-ish bounding box (rough MVP).
    # You can adjust later or derive bbox from ZIP polygons.
    south, west, north, east = 33.396754, -117.751671,33.650911, -117.576577

    query_name = "chinese_restaurants_san_clemente_bbox"
    query_params = {
        "bbox": {"south": south, "west": west, "north": north, "east": east},
        "cuisine_regex": "chinese",
        "include_fast_food": True,
    }

    query_text = build_overpass_query_restaurants_cuisine_bbox(
        south=south, west=west, north=north, east=east,
        cuisine_regex="chinese",
        include_fast_food=True,
    )

    result = call_overpass(query_text)
    row_id = save_raw_overpass(query_name, query_text, query_params, result)

    if result.status_code == 200 and result.payload:
        n = len(result.payload.get("elements", []))
        print(f"✅ Saved raw Overpass response row_id={row_id}, elements={n}, ms={result.duration_ms}")
    else:
        print(f"⚠️ Saved failure row_id={row_id}, status={result.status_code}, err={result.error_text}")

if __name__ == "__main__":
    run_example_san_clemente_bbox()

