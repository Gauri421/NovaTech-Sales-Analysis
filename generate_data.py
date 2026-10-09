import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

products = {
    'Gaming Laptop': {'category': 'Computers', 'price': 85000, 'cost': 65000},
    'Business Laptop': {'category': 'Computers', 'price': 55000, 'cost': 42000},
    'Wireless Headphones': {
        'category': 'Accessories',
        'price': 3500,
        'cost': 1800,
    },
    'Mechanical Keyboard': {
        'category': 'Accessories',
        'price': 4500,
        'cost': 2200,
    },
    'Smart Watch': {'category': 'Wearables', 'price': 8000, 'cost': 4500},
    '4K Monitor': {'category': 'Displays', 'price': 28000, 'cost': 19000},
    'Smartphone Pro': {'category': 'Mobiles', 'price': 65000, 'cost': 50000},
    'USB-C Hub': {'category': 'Accessories', 'price': 1500, 'cost': 600},
}

regions_states = {
    'North': ['Delhi', 'Punjab', 'Uttar Pradesh'],
    'South': ['Karnataka', 'Tamil Nadu', 'Telangana'],
    'East': ['West Bengal', 'Odisha'],
    'West': ['Maharashtra', 'Gujarat'],
}

channels = ['Online Website', 'Retail Store', 'Corporate Direct']
customer_types = ['Consumer', 'Corporate', 'Small Business']

data = []
start_date = datetime(2025, 1, 1)

for i in range(1, 101):
  order_id = f'NTE-2025-{1000 + i}'
  date = start_date + timedelta(days=random.randint(0, 364))

  prod_name = random.choice(list(products.keys()))
  prod_info = products[prod_name]

  region = random.choice(list(regions_states.keys()))
  state = random.choice(regions_states[region])

  qty = random.choices([1, 2, 3, 5, 10], weights=[50, 25, 15, 7, 3])[0]
  unit_price = prod_info['price']
  unit_cost = prod_info['cost']
  discount_pct = random.choice([0.0, 0.05, 0.10, 0.15, 0.20])

  data.append({
      'Order_ID': order_id,
      'Order_Date': date.strftime('%Y-%m-%d'),
      'Product_Name': prod_name,
      'Category': prod_info['category'],
      'Quantity': qty,
      'Unit_Price_INR': unit_price,
      'Unit_Cost_INR': unit_cost,
      'Discount_Pct': discount_pct,
      'Region': region,
      'State': state,
      'Sales_Channel': random.choice(channels),
      'Customer_Type': random.choice(customer_types),
  })

df = pd.DataFrame(data)

# Inject dirty sample entries for cleaning demonstration
df.loc[12, 'Discount_Pct'] = np.nan
df.loc[25, 'Region'] = 'north'
df.loc[45, 'Product_Name'] = 'Smart Watch '

os.makedirs('data', exist_ok=True)
df.to_csv('data/sales_data.csv', index=False)
print('Successfully generated: data/sales_data.csv')