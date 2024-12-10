import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("X_DUNE_API_KEY")

# Read addresses from CSV
addresses_df = pd.read_csv('addresses.csv')
addresses = addresses_df['address'].tolist()

# Prepare the output data
output_data = []

# Iterate over each address and make API request
for address in addresses:
    url = f"https://api.dune.com/api/echo/v1/balances/evm/{address}"
    headers = {"X-Dune-Api-Key": api_key}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'balances' in data and data['balances']:
            balance_info = data['balances'][0]
            output_data.append({
                "address": balance_info.get("address"),
                "symbol": balance_info.get("symbol"),
                 "chain": balance_info.get("chain"),
                "amount": balance_info.get("amount"),
                "decimals": balance_info.get("decimals"),
                "price_usd": balance_info.get("price_usd"),
                "value_usd": balance_info.get("value_usd")
            })
    else:
        print(f"Failed to fetch data for address {address}")

# Write the output data to a new CSV file
output_df = pd.DataFrame(output_data)
output_df.to_csv('output_balances.csv', index=False)