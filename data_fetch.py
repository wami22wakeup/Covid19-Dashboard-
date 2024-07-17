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
    url = "https://disease.sh/v3/covid-19/all"  # Fetch global data
    response = http.get(url)
    response.raise_for_status()
    return response.json()

def fetch_country_data(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"  # Fetch country-specific data
    response = http.get(url)
    response.raise_for_status()
    return response.json()

def fetch_historical_data(country):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=all"  # Fetch historical data
    response = http.get(url)
    response.raise_for_status()
    return response.json()

def prepare_data(country_data):
    # Depending on the response structure, you may need to adjust this
    df = pd.DataFrame(country_data['timeline']).T.reset_index()
    df.columns = ['Date', 'Cases', 'Deaths', 'Recovered']  # Adjust based on the response structure
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Daily Cases'] = df['Cases'].diff().fillna(0)
    df['Daily Deaths'] = df['Deaths'].diff().fillna(0)
    df['Daily Recovered'] = df['Recovered'].diff().fillna(0)
    return df
