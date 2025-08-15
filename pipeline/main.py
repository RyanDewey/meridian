from extract.fetch_census import get_population_data, get_demographic_data
from extract.fetch_yelp import get_business_data
from transform.clean_data import clean_population_data, clean_business_data, clean_demographic_data

# Zip codes for San Clemente
zip_codes = [
    90620, 90621, 90622, 90623, 90624, 90630, 90631, 90632, 90633, 90638, 90639, 90650, 90651, 90652, 90660, 90670, 90720, 90721, 90740, 90742, 90743, 92602, 92603, 92604, 92605, 92606, 92607, 92609, 92610, 92612, 92614, 92615, 92616, 92617, 92618, 92619, 92620, 92623, 92624, 92625, 92626, 92627, 92628, 92629, 92630, 92637, 92646, 92647, 92648, 92649, 92650, 92651, 92652, 92653, 92654, 92655, 92656, 92657, 92658, 92659, 92660, 92661, 92662, 92663, 92672, 92673, 92674, 92675, 92676, 92677, 92678, 92679, 92683, 92684, 92685, 92688, 92690, 92691, 92692, 92693, 92694, 92697, 92698, 92701, 92702, 92703, 92704, 92705, 92706, 92707, 92708, 92709, 92710, 92711, 92712, 92725, 92728, 92735, 92780, 92781, 92782, 92799, 92801, 92802, 92803, 92804, 92805, 92806, 92807, 92808, 92809, 92811, 92812, 92814, 92815, 92816, 92817, 92821, 92822, 92823, 92825, 92831, 92832, 92833, 92834, 92835, 92836, 92837, 92838, 92840, 92841, 92842, 92843, 92844, 92845, 92846, 92850, 92856, 92857, 92859, 92861, 92862, 92863, 92864, 92865, 92866, 92867, 92868, 92869, 92870, 92871, 92885, 92886, 92887, 92899
]

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
