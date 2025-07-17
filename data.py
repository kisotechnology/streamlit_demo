import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range(start='2025-07-01', periods=52, freq='W')
products = [f'Product {i}' for i in range(1, 11)]

all_data = []
for product in products:
    base_demand = np.random.uniform(100, 1000)
    demand = np.maximum(0, np.random.normal(base_demand, base_demand*0.2, len(dates)))
    forecast = np.maximum(0, np.random.normal(base_demand, base_demand*0.15, len(dates)))
    
    product_data = pd.DataFrame({
        'date': dates,
        'product_name': product,
        'forecast': forecast,
        'demand': demand
    })
    all_data.append(product_data)

df = pd.concat(all_data, ignore_index=True).sort_values(['product_name', 'date'])
df['forecast_error'] = np.abs(df['demand'] - df['forecast'])
df['relative_error'] = df['forecast_error'] / df['demand'].replace(0, 1)
