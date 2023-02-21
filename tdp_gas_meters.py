import pandas as pd

# Load data
meters_df = pd.read_csv('gorilla_test_data.csv')
forecast_df = pd.read_csv('rate_table.csv')

aq_band = forecast_df.groupby('exit_zone').apply(
    lambda x: pd.IntervalIndex.from_arrays(x['aq_min_kwh'], x['aq_max_kwh'], closed='left')
)

aq_band.name = 'aq_band'

# Merge forecast and meter data
merged_df = pd.merge(meters_df, forecast_df, on='exit_zone')
merged_df = pd.merge(merged_df, aq_band, on='exit_zone')

# Calculate daily transportation distribution charge
merged_df['daily_charge'] = merged_df.apply(
    lambda row: row['rate_p_per_kwh'] * row['aq_kwh'] if row['aq_band'].contains(row['aq_kwh'])[0] else 0,
    axis=1
)

# Calculate total cost per meter and total consumption per meter
meter_summary = merged_df.groupby('meter_id').agg(
    total_cost=('daily_charge', 'sum'),
    total_consumption=('aq_kwh', 'sum')
)

# Convert total cost to pounds
meter_summary['total_cost'] = meter_summary['total_cost'] * 0.01

# Calculate cost per day for each meter
daily_summary = merged_df.groupby(['meter_id', 'date']).agg(
    cost_per_day=('aq_kwh', 'first'),
    rate_per_kwh=('rate_p_per_kwh', 'first')
)
daily_summary['cost_per_day'] = daily_summary['cost_per_day'] * daily_summary['rate_per_kwh'] * 0.01

# Aggregate daily summary to meter summary
daily_summary_agg = daily_summary.groupby('meter_id').agg(
    total_estimated_consumption=('cost_per_day', 'count'),
    total_cost=('cost_per_day', 'sum')
)

# Round all numerical values to 2 decimals
meter_summary = meter_summary.round(2)
daily_summary_agg = daily_summary_agg.round(2)

# Rename columns and index
meter_summary = meter_summary.rename(columns={'total_cost': 'Total Cost (£)', 'total_consumption': 'Total Estimated Consumption(kWh)'})
daily_summary_agg = daily_summary_agg.rename(columns={'total_estimated_consumption': 'Total Estimated Consumption(kWh)', 'total_cost': 'Total Cost (£)'})
daily_summary_agg.index.names = ['Meter ID']

# Print results
print('Meter Summary:')
print(meter_summary)
print('\n')
print('Daily Summary:')
print(daily_summary_agg)
