import requests

population_base_url = 'api.census.gov/data/2020/dec/sdhc'

def getPopulationData():
    response = requests.get(f"{population_base_url}")

    return response

    