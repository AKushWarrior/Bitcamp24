import pandas as pd

counties = pd.read_csv('input/countycodes.csv')

for year in [2020, 2040]:
    for rcp in ['rcp45', 'rcp85']:
        county_year_rcp = counties.where(counties['fips'] % 1000 != 0).dropna()
        ii = 'input/Impacts/'
        back = rcp + '-' + str(year) + "b.csv"
        agriculture = pd.read_csv(ii + 'Agriculture/county_20a/yields-total-' + back)[['region', 'q0.5']]
        property_crime = pd.read_csv(ii + 'Crime/county_20a/crime-property-' + back)[['region', 'q0.5']]
        violent_crime = pd.read_csv(ii + 'Crime/county_20a/crime-violent-' + back)[['region', 'q0.5']]
        labor = pd.read_csv(ii + 'Labor/county_20a/labor-total-productivity-' + back)[['region', 'q0.5']]
        mortality = pd.read_csv(ii + 'Mortality/county_20a/health-mortality-' + back)[['region', 'q0.5']]

        county_year_rcp = pd.merge(county_year_rcp, agriculture, how='left', left_on='fips', right_on='region').rename(columns={'q0.5': 'agriculture'})
        county_year_rcp.drop('region', axis=1, inplace=True)
        county_year_rcp = pd.merge(county_year_rcp, property_crime, how='left', left_on='fips', right_on='region').rename(columns={'q0.5': 'prop_crime'})
        county_year_rcp.drop('region', axis=1, inplace=True)
        county_year_rcp = pd.merge(county_year_rcp, violent_crime, how='left', left_on='fips', right_on='region').rename(columns={'q0.5':'violent_crime'})
        county_year_rcp.drop('region', axis=1, inplace=True)
        county_year_rcp = pd.merge(county_year_rcp, labor, how='left', left_on='fips', right_on='region').rename(columns={'q0.5':'labor'})
        county_year_rcp.drop('region', axis=1, inplace=True)
        county_year_rcp = pd.merge(county_year_rcp, mortality, how='left', left_on='fips', right_on='region').rename(columns={'q0.5':'mortality'})
        county_year_rcp.drop('region', axis=1, inplace=True)
        county_year_rcp.rename(columns={'fips': 'county'}, inplace=True)
        county_year_rcp.fillna(0, inplace=True)

        county_year_rcp['total'] = (county_year_rcp['agriculture'] + county_year_rcp['prop_crime'] +
                                    county_year_rcp['violent_crime'] + county_year_rcp['labor'] +
                                    county_year_rcp['mortality'])

        total = county_year_rcp['total']
        county_year_rcp['safety'] = 100 - (total - total.min()) * 100 / (total.max() - total.min())

        print("Min GDP Change:       " + rcp + "  " + str(year) + "  " + str(county_year_rcp['total'].min()))
        print("Max GDP Change:       " + rcp + "  " + str(year) + "  " + str(county_year_rcp['total'].max()))
        print("Average Safety Score: " + rcp + "  " + str(year) + "  " + str(county_year_rcp['safety'].mean()) + "\n")

        county_year_rcp.to_csv("output/" + str(year + 10) + "-" + rcp + ".csv", index=False)

