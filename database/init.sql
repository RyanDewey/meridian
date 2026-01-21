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

create table if not exists raw_yelp_search (
  id bigserial primary key,
  zip text not null,
  term text not null,
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

create table if not exists stg_yelp_business (
  yelp_id text primary key,
  name text,
  zip text,
  term text,
  rating numeric,
  review_count int,
  lat double precision,
  lon double precision,
  is_closed boolean,
  pulled_at timestamptz not null default now(),
  raw jsonb
);

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
