from extract.fetch_acs import run as extract_acs
from extract.fetch_overpass import run_example_san_clemente_bbox as extract_overpass
from transform.transform_acs import transform_latest_acs
from transform.transform_overpass import transform_overpass_to_staging
from transform.run_sql import run_sql_dir


# Main function to call all other functions
def run_pipeline():

    # Define constant arguments
    ACS_YEAR = 2023
    ZIPS = [92672, 92673, 92624, 92675, 92629]

    SQL_DIR = "transform/sql"
    SQL_STEPS = [
        "03_make_poi_geom.sql",
        "04_spatial_join_poi_to_zcta.sql",
        "05_compute_competitors.sql",
        "06_compute_demand.sql",
    ]

    # Extract raw data
    extract_acs(ACS_YEAR, ZIPS)
    extract_overpass()

    # Transform raw data to normalized version
    transform_latest_acs()
    transform_overpass_to_staging(query_name="chinese_restaurants_san_clemente_bbox",
        only_latest_per_query=False)

    sql_steps = [
        "03_make_poi_geom.sql",
        "04_spatial_join_poi_to_zcta.sql",
        "05_compute_competitors.sql",
        "06_compute_demand.sql",
    ]

    run_sql_dir(SQL_DIR, SQL_STEPS)

    print("\n✅ Pipeline completed successfully\n")


if __name__ == "__main__":
    run_pipeline()
