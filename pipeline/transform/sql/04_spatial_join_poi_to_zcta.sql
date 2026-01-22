CREATE TABLE IF NOT EXISTS stg_poi_zcta (
  osm_type text not null,
  osm_id bigint not null,
  zcta5 text not null,
  primary key (osm_type, osm_id)
);

INSERT INTO stg_poi_zcta (osm_type, osm_id, zcta5)
SELECT
  p.osm_type,
  p.osm_id,
  z.zcta5ce20
FROM stg_osm_poi p
JOIN dim_zcta z
  ON ST_Intersects(z.geom_4326, p.geom_4326)
WHERE p.geom_4326 IS NOT NULL
ON CONFLICT (osm_type, osm_id) DO UPDATE
SET zcta5 = EXCLUDED.zcta5;
