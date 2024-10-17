import pandas as pd
import requests
from datetime import datetime, timedelta
import os

# Fetch real market prices from API
url = "https://sfl.world/api/v1/prices"
response = requests.get(url)

if response.status_code == 200:
    prices = response.json()
else:
    raise Exception(f"Failed to retrieve data: {response.status_code}")

# Extract data from the response
p2p_prices = prices['data'].get('p2p', {})

# Create a dataframe with resources and their prices from all three categories
df_resources = pd.DataFrame({
    'Resource': list(p2p_prices.keys()),  # All resources
    'P2P (SFL)': list(p2p_prices.values()),
})

# Function to round time to the nearest 15 minutes
def round_time(dt=None, round_to=15):
    if dt is None:
        dt = datetime.now()
    seconds = (dt - dt.min).seconds
    rounding = (seconds + round_to * 60 / 2) // (round_to * 60) * (round_to * 60)
    return dt + timedelta(0, rounding - seconds, -dt.microsecond)

# Get the current rounded time
current_time = round_time(datetime.now(), round_to=15)
date_str = current_time.strftime('%Y-%m-%d %H:%M')

# Add timestamp column to dataframe
df_resources['Date'] = date_str

# Define the folder path for storing files by month
folder_path = 'price_tracking'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Get the current year and month for the file naming convention
year_month_str = current_time.strftime('%Y_%m')

# Save the file with the format YYYY_MM.csv
csv_file = os.path.join(folder_path, f'resource_prices_{year_month_str}.csv')

# Save the data, avoiding duplicates
try:
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)

        # Drop rows that are duplicates based on 'Resource' and 'Date'
        df_resources = df_resources[~df_resources[['Resource', 'Date']].apply(tuple, 1).isin(df_existing[['Resource', 'Date']].apply(tuple, 1))]

    if not df_resources.empty:
        df_resources.to_csv(csv_file, mode='a', index=False, header=not os.path.exists(csv_file))
        print(f"Data successfully saved to {csv_file}")
    else:
        print("No new data to save, all records are duplicates.")
except Exception as e:
    print(f"Error saving data: {e}")