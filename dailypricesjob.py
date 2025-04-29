from google.cloud import datastore
import yfinance as yf
import shortuuid
from datetime import datetime
import pytz  # Import timezone handling
import sys
import os

print("Python path:", sys.executable)
print("PYTHONPATH:", os.environ.get("PYTHONPATH"))
print("PATH:", os.environ.get("PATH"))

GOOGLE_CLOUD_CLIENT_ID = "sentiment-analysis-379200"
GOOGLE_CLOUD_DAILYPRICES_KEY = "Dailyprices"

# Authenticate to datastore
client = datastore.Client(GOOGLE_CLOUD_CLIENT_ID)

# Use a uuid for unique id for database
company_info_query = client.query(kind="Company_Info")
company_info_results = list(company_info_query.fetch())
company_info_tickers = [result['Yahoo_Ticker'].split(" ")[0] for result in company_info_results]

print(company_info_tickers)

# Set Eastern Timezone with automatic DST adjustment
eastern = pytz.timezone('America/New_York')

def update_datastore(symbol):
    key = client.key(GOOGLE_CLOUD_DAILYPRICES_KEY, str(shortuuid.ShortUUID().random(length=7)))

    stock = yf.Ticker(symbol)
    data = stock.history(period='1d')  # Get only today's price

    if data.empty:
        print(f"No trading data found for {symbol}. Skipping...")
        return  # Skip if no data is available

    latest_price = round(data['Close'].iloc[-1], 2)  # Get today's closing price

    # Convert timestamp to Eastern Time (ET) with automatic EST/EDT adjustment
    et_now = datetime.now(pytz.utc).astimezone(eastern)

    task = datastore.Entity(key)
    task.update({
        'Date': et_now,  # Store with correct Eastern Time (EST or EDT)
        'price': latest_price,
        'ticker': symbol,
        'volume': int(stock.info.get("volume", 0))  # Default to 0 if volume is missing
    })
    client.put(task)
    print(f"Stored data for {symbol} at {et_now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

for company_info_ticker in company_info_tickers:
    update_datastore(company_info_ticker)

