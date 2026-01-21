-- Initialize schema script
-- RAW: store unmodified responses
create table if not exists raw_acs_zip (
  id bigserial primary key,
  zip text not null,
  year int not null,
  variables text[] not null,
  pulled_at timestamptz not null default now(),
  payload jsonb not null
);

-- STAGING: cleaned, typed, consistent columns
create table if not exists stg_acs_zip (
  zip text not null,
  year int not null,
  population int,
  median_household_income int,
  primary key (zip, year)
);

create table if not exists raw_overpass_query (
  id bigserial primary key,
  source text not null default 'overpass',
  query_name text not null,                 -- e.g. "chinese_restaurants_san_clemente_bbox"
  query_text text not null,                 -- the actual Overpass QL
  query_params jsonb not null default '{}'::jsonb,  -- bbox, tags, etc.
  query_hash text not null,                 -- sha256(query_text + params)
  status_code int,
  pulled_at timestamptz not null default now(),
  duration_ms int,
  response_bytes int,
  payload jsonb                              -- raw Overpass JSON (nullable if failed)
);

create index if not exists idx_raw_overpass_query_hash
  on raw_overpass_query (query_hash);

create index if not exists idx_raw_overpass_query_pulled_at
  on raw_overpass_query (pulled_at desc);


create table if not exists stg_osm_poi (
  osm_type text not null,                 -- node | way | relation
  osm_id bigint not null,
  name text,
  amenity text,
  cuisine text,
  lat double precision,
  lon double precision,
  query_name text not null,
  pulled_at timestamptz not null,
  tags jsonb,
  raw jsonb,
  primary key (osm_type, osm_id)
);

create index if not exists idx_stg_osm_poi_query
  on stg_osm_poi (query_name, pulled_at desc);


-- MART: demand output
create table if not exists mart_demand (
  zip text not null,
  year int not null,
  term text not null,
  population int,
  median_household_income int,
  competitor_count int,
  demand_score numeric,
  computed_at timestamptz not null default now(),
  primary key (zip, year, term)
);
