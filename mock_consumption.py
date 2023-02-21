import pandas as pd
import numpy as np
from random_meters import generate_random_meters
import random

def generate_consumption_data(meters, start_date, duration, exit_zones_list):
    # Generate a list of dates for the forecast period
    dates = pd.date_range(start_date, periods=duration, freq='D')

    # Initialize an empty DataFrame to store the consumption data
    consumption_data = pd.DataFrame(columns=['meter_id', 'date', 'rate_p_per_kwh', 'exit_zone', 'aq_min_kwh', 'aq_max_kwh'])

    # Loop through each meter and generate random consumption data for each day
    for meter_id in meters['meter_id']:
        meter = meters[meters['meter_id'] == meter_id].iloc[0]

        # Generate random consumption data for each day
        consumption = np.random.randint(10, 100, size=duration) * .005
        a=1
        aq_max_kwh_rnd = np.random.randint(10, 2500, size=duration)
        a=1
        rand_exit_zones = [exit_zones_list[np.random.randint(0, len(exit_zones_list))] for _ in range(duration)]
        a=1
        # Add the consumption data to the DataFrame
        meter_data = pd.DataFrame({
            'meter_id': [meter_id] * duration,
            'date': dates,
            'rate_p_per_kwh': consumption,
            'exit_zone': rand_exit_zones,
            'aq_min_kwh': 0,
            'aq_max_kwh': aq_max_kwh_rnd
        })

        # Append the meter data to the consumption data DataFrame
        consumption_data = pd.concat([consumption_data, meter_data], ignore_index=True)

    return consumption_data


# Generate a list of 100 random meters
exit_zones = ['EA1', 'EA2', 'EA3', 'EA4']
meters = generate_random_meters(10, exit_zones)

# Generate consumption data for the meters over a 30-day period starting on January 1, 2022
start_date = pd.to_datetime('2022-01-01')
duration = 100
consumption_data = generate_consumption_data(meters, start_date, duration, exit_zones)

# Print the first few rows of the consumption data DataFrame
print("\n************* MOCK CONSUMPTION DATA *************")
print(consumption_data.head())
