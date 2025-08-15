from extract.fetch_census import get_population_data, get_demographic_data
from extract.fetch_yelp import get_business_data
from transform.clean_data import clean_population_data, clean_business_data, clean_demographic_data

# Zip codes for San Clemente
zip_codes = [92672, 92673]

# Main function to call all other functions
def run_pipeline():
    population_raw_df = get_population_data(zip_codes)
    # demographic_raw_df = get_demographic_data(zip_codes)
    # business_raw_df = get_business_data(zip_codes)

    # population_df = clean_population_data(population_raw_df)
    # demographic_df = clean_demographic_data(demographic_raw_df)
    # business_df = clean_business_data(business_raw_df)

if __name__ == "__main__":
    run_pipeline()
