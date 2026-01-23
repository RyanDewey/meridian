# pipeline/transform_overpass.py
import json
from typing import Any, Dict, Optional, Tuple, List
from dotenv import load_dotenv

from db import get_conn

load_dotenv()

def _get_lat_lon(element: Dict[str, Any]) -> Tuple[Optional[float], Optional[float]]:
    """
    Overpass elements:
      - nodes: have 'lat' and 'lon'
      - ways/relations: may have 'center': {'lat':..,'lon':..} when using 'out center'
    """
    if "lat" in element and "lon" in element:
        return element.get("lat"), element.get("lon")
    center = element.get("center") or {}
    return center.get("lat"), center.get("lon")

def _safe_json(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False)

def transform_overpass_to_staging(
    query_name: Optional[str] = None,
    only_latest_per_query: bool = True,
) -> int:
    """
    Reads raw_overpass_query rows, extracts POIs from payload->elements, and upserts into stg_osm_poi.

    Args:
      query_name: if provided, only transform rows for this query_name
      only_latest_per_query: if True, transforms only the latest successful raw row per query_name
                             (good for MVP). If False, transforms all successful rows.

    Returns:
      count of elements processed (attempted upserts)
    """
    with get_conn() as conn, conn.cursor() as cur:
        # 1) Choose which raw rows to transform
        if only_latest_per_query:
            # latest success per query_name (or for a specific query_name)
            if query_name:
                cur.execute(
                    """
                    select id, query_name, pulled_at, payload
                    from raw_overpass_query
                    where query_name = %s
                      and status_code = 200
                      and payload is not null
                    order by pulled_at desc
                    limit 1
                    """,
                    (query_name,),
                )
            else:
                cur.execute(
                    """
                    select distinct on (query_name)
                      id, query_name, pulled_at, payload
                    from raw_overpass_query
                    where status_code = 200
                      and payload is not null
                    order by query_name, pulled_at desc
                    """
                )
        else:
            # all successful rows (careful: can be a lot)
            if query_name:
                cur.execute(
                    """
                    select id, query_name, pulled_at, payload
                    from raw_overpass_query
                    where query_name = %s
                      and status_code = 200
                      and payload is not null
                    order by pulled_at desc
                    """,
                    (query_name,),
                )
            else:
                cur.execute(
                    """
                    select id, query_name, pulled_at, payload
                    from raw_overpass_query
                    where status_code = 200
                      and payload is not null
                    order by pulled_at desc
                    """
                )

        raw_rows = cur.fetchall()
        if not raw_rows:
            print("No successful raw Overpass rows found to transform.")
            return 0

        processed = 0

        # 2) Transform each raw row's elements
        for raw_id, qname, pulled_at, payload in raw_rows:
            # psycopg2 may return jsonb as dict or as str depending on settings
            if isinstance(payload, str):
                payload = json.loads(payload)

            elements = (payload or {}).get("elements", [])
            for el in elements:
                osm_type = el.get("type")
                osm_id = el.get("id")
                if not osm_type or osm_id is None:
                    continue

                tags = el.get("tags") or {}
                name = tags.get("name")
                amenity = tags.get("amenity")
                cuisine = tags.get("cuisine")

                lat, lon = _get_lat_lon(el)

                # Skip entries without a location (rare, but happens)
                # (You can keep them if you want, but they won’t map cleanly to ZIPs later.)
                if lat is None or lon is None:
                    continue

                cur.execute(
                    """
                    insert into stg_osm_poi (
                      osm_type, osm_id, name, amenity, cuisine, lat, lon,
                      query_name, pulled_at, tags, raw
                    )
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s::jsonb,%s::jsonb)
                    on conflict (osm_type, osm_id) do update
                    set name = excluded.name,
                        amenity = excluded.amenity,
                        cuisine = excluded.cuisine,
                        lat = excluded.lat,
                        lon = excluded.lon,
                        query_name = excluded.query_name,
                        pulled_at = excluded.pulled_at,
                        tags = excluded.tags,
                        raw = excluded.raw
                    """,
                    (
                        osm_type,
                        int(osm_id),
                        name,
                        amenity,
                        cuisine,
                        float(lat),
                        float(lon),
                        qname,
                        pulled_at,
                        _safe_json(tags),
                        _safe_json(el),
                    ),
                )
                processed += 1

        print(f"✅ Transformed Overpass → stg_osm_poi. raw_rows={len(raw_rows)} elements_upserted={processed}")
        return processed

if __name__ == "__main__":
    # Example: transform only your San Clemente Chinese query
    transform_overpass_to_staging(query_name="chinese_restaurants_san_clemente_bbox", only_latest_per_query=True)
