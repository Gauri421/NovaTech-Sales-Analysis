import os
import pandas as pd

if not os.path.exists('data/sales_data.csv'):
  import generate_data

df = pd.read_csv('data/sales_data.csv')

# Data Cleaning
df['Product_Name'] = df['Product_Name'].str.strip()
df['Region'] = df['Region'].str.title()
df['Discount_Pct'] = df['Discount_Pct'].fillna(0.0)

# Financial Metrics
df['Gross_Sales'] = df['Quantity'] * df['Unit_Price_INR']
df['Discount_Amount'] = df['Gross_Sales'] * df['Discount_Pct']
df['Net_Sales'] = df['Gross_Sales'] - df['Discount_Amount']
df['Total_Cost'] = df['Quantity'] * df['Unit_Cost_INR']
df['Profit'] = df['Net_Sales'] - df['Total_Cost']
df['Profit_Margin_Pct'] = (df['Profit'] / df['Net_Sales']) * 100

os.makedirs('data', exist_ok=True)
df.to_csv('data/cleaned_sales_data.csv', index=False)
print('Successfully generated: data/cleaned_sales_data.csv')