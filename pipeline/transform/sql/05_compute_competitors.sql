CREATE TABLE IF NOT EXISTS mart_competitors (
  zcta5 text not null,
  business_type text not null,
  competitor_count int not null,
  computed_at timestamptz not null default now(),
  primary key (zcta5, business_type)
);

INSERT INTO mart_competitors (zcta5, business_type, competitor_count)
SELECT
  m.zcta5,
  'chinese' AS business_type,
  COUNT(*)::int AS competitor_count
FROM stg_osm_poi p
JOIN stg_poi_zcta m
  ON m.osm_type = p.osm_type AND m.osm_id = p.osm_id
WHERE p.cuisine ILIKE '%chinese%'
GROUP BY m.zcta5
ON CONFLICT (zcta5, business_type) DO UPDATE
SET competitor_count = EXCLUDED.competitor_count,
    computed_at = now();
