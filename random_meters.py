import numpy as np
import pandas as pd


def generate_random_meters(meter_count, exit_zones):
    # Create a random list of exit zones for the meters
    exit_zone_list = np.random.choice(exit_zones, size=meter_count)

    # Create a DataFrame with the exit zones and random annual quantities
    meter_df = pd.DataFrame({
        'exit_zone': exit_zone_list,
        'aq_kwh': np.random.randint(low=1000, high=50000, size=meter_count)
    })

    # Generate unique meter IDs
    meter_df['meter_id'] = 'meter_' + pd.Series(range(1, meter_count + 1)).astype(str)

    # Reorder the columns to match the desired order
    meter_df = meter_df[['meter_id', 'aq_kwh', 'exit_zone']]

    return meter_df



exit_zones = ['EA1', 'EA2', 'EA3', 'EA4', 'EA5', 'EA6']
meter_count = 10

random_meters = generate_random_meters(meter_count, exit_zones)
print("\n************* RANDOM METERS *************" )
print(random_meters)
