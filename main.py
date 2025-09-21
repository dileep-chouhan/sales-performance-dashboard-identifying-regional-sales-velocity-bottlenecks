import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# --- 1. Synthetic Data Generation ---
np.random.seed(42) # for reproducibility
num_regions = 4
num_weeks = 52
regions = ['North', 'South', 'East', 'West']
data = {
    'Region': np.random.choice(regions, size=num_weeks * num_regions),
    'Week': np.tile(np.arange(1, num_weeks + 1), num_regions),
    'Sales': np.random.randint(500, 2000, size=num_weeks * num_regions),
    'Leads': np.random.randint(100, 500, size=num_weeks * num_regions),
    'Conversion_Rate': np.random.rand(num_weeks * num_regions) * 0.3 + 0.1 # Between 10% and 40%
}
df = pd.DataFrame(data)
#Adding some noise to simulate bottlenecks
df.loc[df['Region'] == 'North', 'Sales'] -= np.random.randint(0, 500, size=len(df[df['Region'] == 'North']))
df.loc[df['Region'] == 'South', 'Leads'] -= np.random.randint(0, 200, size=len(df[df['Region'] == 'South']))
# --- 2. Data Cleaning and Analysis ---
#Ensure no negative values after adding noise
df['Sales'] = df['Sales'].clip(lower=0)
df['Leads'] = df['Leads'].clip(lower=0)
df['Conversion_Rate'] = df['Conversion_Rate'].clip(lower=0, upper=1)
# Calculate weekly average sales per region
weekly_sales = df.groupby(['Region', 'Week'])['Sales'].mean().unstack()
# Calculate total sales per region
total_sales_by_region = df.groupby('Region')['Sales'].sum()
# Calculate average conversion rate per region
avg_conversion_rate = df.groupby('Region')['Conversion_Rate'].mean()
# --- 3. Visualization ---
# Weekly Sales Trend by Region
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x='Week', y='Sales', hue='Region')
plt.title('Weekly Sales Trend by Region')
plt.xlabel('Week')
plt.ylabel('Average Weekly Sales')
plt.grid(True)
plt.tight_layout()
plt.savefig('weekly_sales_trend.png')
print("Plot saved to weekly_sales_trend.png")
# Total Sales by Region
plt.figure(figsize=(8, 6))
sns.barplot(x=total_sales_by_region.index, y=total_sales_by_region.values)
plt.title('Total Sales by Region')
plt.xlabel('Region')
plt.ylabel('Total Sales')
plt.grid(True)
plt.tight_layout()
plt.savefig('total_sales_by_region.png')
print("Plot saved to total_sales_by_region.png")
# Average Conversion Rate by Region
plt.figure(figsize=(8, 6))
sns.barplot(x=avg_conversion_rate.index, y=avg_conversion_rate.values)
plt.title('Average Conversion Rate by Region')
plt.xlabel('Region')
plt.ylabel('Average Conversion Rate')
plt.grid(True)
plt.tight_layout()
plt.savefig('conversion_rate_by_region.png')
print("Plot saved to conversion_rate_by_region.png")
#Further analysis could involve correlation analysis between leads and sales, or time series decomposition to identify seasonality.