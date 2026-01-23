CREATE TABLE IF NOT EXISTS mart_demand (
  zcta5 text not null,
  year int not null,
  business_type text not null,
  population int,
  median_household_income int,
  competitor_count int,
  demand_score numeric,
  computed_at timestamptz not null default now(),
  primary key (zcta5, year, business_type)
);

INSERT INTO mart_demand (
  zcta5, year, business_type,
  population, median_household_income, competitor_count,
  demand_score
)
SELECT
  a.zip AS zcta5,
  a.year,
  c.business_type,
  a.population,
  a.median_household_income,
  c.competitor_count,
  CASE
    WHEN a.population IS NULL OR a.median_household_income IS NULL THEN NULL
    ELSE (LN(1 + a.population::numeric) * LN(1 + a.median_household_income::numeric))
         / (c.competitor_count + 1)
  END AS demand_score
FROM stg_acs_zip a
JOIN mart_competitors c
  ON c.zcta5 = a.zip
WHERE a.year = 2023
ON CONFLICT (zcta5, year, business_type) DO UPDATE
SET population = EXCLUDED.population,
    median_household_income = EXCLUDED.median_household_income,
    competitor_count = EXCLUDED.competitor_count,
    demand_score = EXCLUDED.demand_score,
    computed_at = now();
