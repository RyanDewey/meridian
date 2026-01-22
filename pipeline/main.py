from extract.fetch_acs import fetch_acs_zcta
from pipeline.run_sql import run_sql_dir


# Main function to call all other functions
def run_pipeline():
    pass


    

    sql_steps = [
        "03_make_poi_geom.sql",
        "04_spatial_join_poi_to_zcta.sql",
        "05_compute_competitors.sql",
        "06_compute_demand.sql",
    ]

    run_sql_dir("sql", sql_steps)


if __name__ == "__main__":
    run_pipeline()
