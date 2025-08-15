import requests
import pandas as pd

api_key = 'f01cca6a59e13e855ac681716055ca2ad72ef2c6'
population_base_url = 'https://api.census.gov/data/2023/acs/acs5?get=B01001_001E&for=zip%20code%20tabulation%20area:'
demographic_base_url = ''

# Returns dataframe with population data
def get_population_data(zip_codes):
    # Build zip code list to insert in Census query 
    zip_codes_list = f"{zip_codes[0]}"
    for zip_code in zip_codes[1:]:
        zip_codes_list += f",{zip_code}"


    # Get population data from census api
    response = requests.get(f"{population_base_url}{zip_codes_list}&key={api_key}")
    
    # Turn into json format
    data = response.json()

    # Store in dataframe
    df = pd.DataFrame(data[1:], columns=['population_total', 'zip_code'])

    # Reorder columns to put zip_code first
    df = df[['zip_code', 'population_total']]

    # Print dataframe for debugging
    print(df)

    # Return dataframe
    return df

# Returns dataframe with demographic data
def get_demographic_data(zip_codes):
    # Get demographic data from census API
    response = requests.get(f"{demographic_base_url}")

    # Store in dataframe
    df = pd.DataFrame(response)

    # Return dataframe
    return df

    