import requests
import pandas as pd

def fetch_data():
    url = "https://disease.sh/v3/covid-19/all"
    response = requests.get(url)
    return response.json()

def fetch_historical_data(days=60):
    url = f"https://disease.sh/v3/covid-19/historical/all?lastdays={days}"
    response = requests.get(url)
    return response.json()

def fetch_country_data(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(url)
    return response.json()

def prepare_data(historical_data):
    df = pd.DataFrame({
        'Date': list(historical_data['cases'].keys()),
        'Cases': list(historical_data['cases'].values()),
        'Deaths': list(historical_data['deaths'].values()),
        'Recovered': list(historical_data['recovered'].values())
    })
    df['Date'] = pd.to_datetime(df['Date'])
    df['Daily Cases'] = df['Cases'].diff().fillna(0)
    df['Daily Deaths'] = df['Deaths'].diff().fillna(0)
    df['Daily Recovered'] = df['Recovered'].diff().fillna(0)
    return df
