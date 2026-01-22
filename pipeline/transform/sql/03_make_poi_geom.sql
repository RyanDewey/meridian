ALTER TABLE stg_osm_poi
ADD COLUMN IF NOT EXISTS geom_4326 geometry(Point, 4326);

UPDATE stg_osm_poi
SET geom_4326 = ST_SetSRID(ST_MakePoint(lon, lat), 4326)
WHERE geom_4326 IS NULL
  AND lon IS NOT NULL
  AND lat IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_stg_osm_poi_geom
ON stg_osm_poi USING GIST (geom_4326);

CREATE INDEX IF NOT EXISTS idx_dim_zcta_geom
ON dim_zcta USING GIST (geom_4326);
