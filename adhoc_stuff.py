# Use the UNICEF API to return the Youth Literacy dataset
youth_literacy = get_unicef_data('https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,EDUCATION,1.0/.ED_15-24_LR._T._T._T._T.PCNT?format=sdmx-csv&labels=id')

# Clean and format the data
youth_literacy = clean_unicef_data(youth_literacy, 'youth_literacy')

# Add the dataset to the main DataFrame
complete_dataset = pd.merge(left=complete_dataset,
                       right=youth_literacy,
                       left_on=['iso3_code'],
                       right_on=['iso3_code'],
                       how='inner')
complete_dataset

#########################

# Use the UNICEF API to return the Education Expenditure dataset
education_exp = get_unicef_data('https://sdmx.data.unicef.org/ws/public/sdmxapi/rest/data/UNICEF,ECONOMIC,1.0/.ECON_GVT_EDU_EXP_PTGDP?format=sdmx-csv&labels=id')

# Clean and format the data
education_exp = clean_unicef_data(education_exp, 'education_exp')

# Add the dataset to the main DataFrame
complete_dataset = pd.merge(left=complete_dataset,
                       right=education_exp,
                       left_on=['iso3_code'],
                       right_on=['iso3_code'],
                       how='inner')
complete_dataset

############################

def get_unicef_data(url: str) -> pd.DataFrame:
    response = requests.get(url)
    dataset = StringIO(response.text)
    df = pd.read_csv(dataset)
    return df

#############################

def clean_unicef_data(df: pd.DataFrame, value_name: str) -> pd.DataFrame:
    # Remove unneeded columns
    df = df[['REF_AREA', 'OBS_VALUE']]

    # Remove Nans and null values from the dataset
    df = df.dropna(subset=['OBS_VALUE'])

    # Rename columns
    df = df.rename(columns={'REF_AREA': 'iso3_code', 'OBS_VALUE': value_name})

    return df