-- Initialize schema script
-- RAW: ACS
CREATE TABLE IF NOT EXISTS raw_acs_zip (
  id bigserial PRIMARY KEY,
  zip text NOT NULL,
  year int NOT NULL,
  variables text[] NOT NULL,
  pulled_at timestamptz NOT NULL DEFAULT now(),
  payload jsonb NOT NULL
);

-- RAW: Overpass
CREATE TABLE IF NOT EXISTS raw_overpass_query (
  id bigserial PRIMARY KEY,
  source text NOT NULL DEFAULT 'overpass',
  query_name text NOT NULL,
  query_text text NOT NULL,
  query_params jsonb NOT NULL DEFAULT '{}'::jsonb,
  query_hash text NOT NULL,
  status_code int,
  pulled_at timestamptz NOT NULL DEFAULT now(),
  duration_ms int,
  response_bytes int,
  payload jsonb
);

CREATE INDEX IF NOT EXISTS idx_raw_overpass_query_hash
  ON raw_overpass_query (query_hash);

CREATE INDEX IF NOT EXISTS idx_raw_overpass_query_pulled_at
  ON raw_overpass_query (pulled_at desc);

-- STAGING: ACS
CREATE TABLE IF NOT EXISTS stg_acs_zip (
  zip text NOT NULL,
  year int NOT NULL,
  population int,
  median_household_income int,
  PRIMARY KEY (zip, year)
);

-- STAGING: OSM POIs
CREATE TABLE IF NOT EXISTS stg_osm_poi (
  osm_type text NOT NULL,
  osm_id bigint NOT NULL,
  name text,
  amenity text,
  cuisine text,
  lat double precision,
  lon double precision,
  query_name text NOT NULL,
  pulled_at timestamptz NOT NULL,
  tags jsonb,
  raw jsonb,
  PRIMARY KEY (osm_type, osm_id)
);

-- If you were adding geom before, keep it:
ALTER TABLE stg_osm_poi
ADD COLUMN IF NOT EXISTS geom geometry(Point, 4326);

-- POI -> ZCTA mapping
CREATE TABLE IF NOT EXISTS stg_poi_zcta (
  osm_type text NOT NULL,
  osm_id bigint NOT NULL,
  zcta5 text NOT NULL,
  PRIMARY KEY (osm_type, osm_id)
);

-- MART: competitors
CREATE TABLE IF NOT EXISTS mart_competitors (
  zcta5 text NOT NULL,
  business_type text NOT NULL,
  competitor_count int NOT NULL,
  computed_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (zcta5, business_type)
);

-- MART: demand
CREATE TABLE IF NOT EXISTS mart_demand (
  zcta5 text NOT NULL,
  year int NOT NULL,
  business_type text NOT NULL,
  population int,
  median_household_income int,
  competitor_count int,
  demand_score numeric,
  computed_at timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (zcta5, year, business_type)
);
