-- Script to reset tables to zero data
TRUNCATE TABLE
  raw_overpass_query,
  raw_acs_zip,
  stg_osm_poi,
  stg_poi_zcta,
  stg_acs_zip,
  mart_competitors,
  mart_demand
RESTART IDENTITY;
