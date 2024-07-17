import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from UI import apply_custom_css, display_metrics, display_charts, select_country

# Page configuration
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide",
)

# Apply custom CSS for better UI
apply_custom_css()

# Title and description
st.title("🌍 Interactive COVID-19 Dashboard")
st.markdown("""
This dashboard provides real-time updates and historical data on COVID-19.
Use the selectors below to filter data by country and date range.
""")

try:
    # Fetch summary data
    summary_url = "https://disease.sh/v3/covid-19/all"
    summary_data = requests.get(summary_url).json()
    st.write("Summary Data:", summary_data)  # Debug print

    # Display global metrics
    display_metrics(summary_data)

    # Select country
    countries = requests.get("https://disease.sh/v3/covid-19/countries").json()
    selected_country = select_country([country['country'] for country in countries])

    # Fetch historical data
    historical_url = f"https://disease.sh/v3/covid-19/historical/{selected_country}?lastdays=30"
    historical_data = requests.get(historical_url).json()

    # Extract timeline data and create a DataFrame
    if 'timeline' in historical_data:
        timeline = historical_data['timeline']
        df = pd.DataFrame({
            'Date': pd.to_datetime(list(timeline['cases'].keys())).date,
            'Cases': list(timeline['cases'].values()),
            'Deaths': list(timeline['deaths'].values()),
            'Recovered': list(timeline['recovered'].values())
        })

        # Calculate daily changes
        df['Daily Cases'] = df['Cases'].diff().fillna(0)
        df['Daily Deaths'] = df['Deaths'].diff().fillna(0)
        df['Daily Recovered'] = df['Recovered'].diff().fillna(0)

        # Display charts
        display_charts(df)
    else:
        st.error("Historical data not found for the selected country.")

except requests.ConnectionError:
    st.error("Network error: Unable to connect to the COVID-19 API.")
except requests.HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
except Exception as err:
    st.error(f"An error occurred: {err}")

# Additional information
st.markdown("""
### Data Source
Data is sourced from [disease.sh](https://disease.sh).
""")
