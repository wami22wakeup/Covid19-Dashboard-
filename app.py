import streamlit as st
from data_fetch import fetch_data, fetch_historical_data, fetch_country_data, prepare_data
from UI import display_metrics, display_charts, select_country

st.title("COVID-19 Dashboard")

# Fetch global data
global_data = fetch_data()
historical_data = fetch_historical_data()
df = prepare_data(historical_data)

# Display global metrics and charts
display_metrics(global_data)
display_charts(df)

# Fetch and display country-specific data
countries = ["USA", "India", "Brazil", "Russia", "UK"]  # You can add more countries
country = select_country(countries)

if country:
    country_data = fetch_country_data(country)
    country_historical_data = fetch_historical_data()
    country_df = prepare_data(country_historical_data)
    
    st.subheader(f"COVID-19 Statistics for {country}")
    display_metrics(country_data)
    display_charts(country_df)
