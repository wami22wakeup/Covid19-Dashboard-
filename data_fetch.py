import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd

# Retry setup
retry_strategy = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)

def fetch_data():
    url = "https://api.covid19api.com/summary"
    response = http.get(url)
    response.raise_for_status()
    return response.json()

def fetch_country_data(country):
    url = f"https://api.covid19api.com/dayone/country/{country}"
    response = http.get(url)
    response.raise_for_status()
    return response.json()

def fetch_historical_data():
    url = "https://api.covid19api.com/all"
    response = http.get(url)
    response.raise_for_status()
    return response.json()

def prepare_data(country_data):
    df = pd.DataFrame(country_data)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Daily Cases'] = df['Confirmed'].diff().fillna(0)
    df['Daily Deaths'] = df['Deaths'].diff().fillna(0)
    df['Daily Recovered'] = df['Recovered'].diff().fillna(0)
    df.rename(columns={'Confirmed': 'Cases'}, inplace=True)
    return df
