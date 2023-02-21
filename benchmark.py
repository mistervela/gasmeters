import time
import datetime
import pandas as pd
from random_meters import generate_random_meters
from mock_consumption import generate_consumption_data
from transportation_cost import calculate_transportation_cost
from tabulate import tabulate

def benchmark_transportation_cost(meter_sizes, exit_zones, start_date, durations):
    costs = {}
    for meter_size in meter_sizes:
        # Generate random meters
        meters = generate_random_meters(meter_size, exit_zones)

        # Generate consumption data
        consumption_data = generate_consumption_data(meters, start_date, max(durations), exit_zones)

        for duration in durations:

            # Calculate transportation cost
            total_cost = calculate_transportation_cost(meters, consumption_data)['Total Cost (£)'].sum()

            # Record the transportation cost
            key = (meter_size, duration)
            costs[key] = total_cost

    return costs


meter_sizes = [100, 500]
exit_zones = ['EA1', 'EA2', 'EA3']
start_date = pd.to_datetime('2022-01-01')
durations = [30, 60, 90]

costs = benchmark_transportation_cost(meter_sizes, exit_zones, start_date, durations)

print('\n********************** BENCHMARK OF TRANSPORTATION COSTS FOR DIFFERENT METER SIZES ****************************\n')
print(tabulate(costs.items(), headers=['(meter_size, duration)', 'Total Cost (£)'], tablefmt='orgtbl'))