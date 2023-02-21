import pandas as pd


def calculate_transportation_cost(meter_df, consumption_data):
    # Merge meter and consumption data based on meter_id
    merged_df = pd.merge(meter_df, consumption_data, on='exit_zone')

    # Calculate AQ bands
    aq_band = merged_df.groupby('exit_zone').apply(
        lambda x: pd.IntervalIndex.from_arrays(x['aq_min_kwh'], x['aq_max_kwh'], closed='left')
    )

    # Map each meter to its corresponding AQ band
    merged_df['aq_band'] = merged_df['exit_zone'].map(aq_band)

    # Calculate daily charge for each meter based on the consumption data
    merged_df['daily_charge'] = merged_df.apply(
        lambda row: row['rate_p_per_kwh'] * row['aq_kwh'] if row['aq_band'].contains(row['aq_kwh'])[0] else 0,
        axis=1
    )

    # Calculate total cost per meter for the entire forecast period
    total_cost = merged_df.groupby('meter_id')['daily_charge'].sum() * 0.01

    # Calculate total consumption per meter for the entire forecast period
    total_consumption = merged_df.groupby('meter_id')['aq_kwh'].sum()

    # Combine the results into a single DataFrame
    result_df = pd.DataFrame({
        'Meter ID': total_cost.index,
        'Total Estimated Consumption(kWh)': total_consumption.values,
        'Total Cost (£)': total_cost.values
    })
    a=1
    return result_df


# Read meter data from file
meter_df = pd.read_csv('gorilla_test_data.csv')

# Read forecast data from file
forecast_df = pd.read_csv('rate_table.csv')

result = calculate_transportation_cost(meter_df, forecast_df)
print(result)
