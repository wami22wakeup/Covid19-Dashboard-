import streamlit as st
import plotly.express as px
import pandas as pd
from data_fetch import fetch_data, fetch_historical_data, fetch_country_data, prepare_data

# Page configuration
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide",
)

# Title and description
st.title("Interactive COVID-19 Dashboard")
st.markdown("""
This dashboard provides real-time updates and historical data on COVID-19.
Use the selectors below to filter data by country and date range.
""")

# Fetch and prepare data
summary_data = fetch_data()
historical_data = fetch_historical_data()
countries = [country['Country'] for country in summary_data['Countries']]
selected_country = st.sidebar.selectbox("Select Country", countries)

# Fetch country-specific data
country_data = fetch_country_data(selected_country)
df_country = prepare_data(country_data)

# Sidebar filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [])
if date_range:
    start_date, end_date = date_range
    df_country = df_country[(df_country['Date'] >= start_date) & (df_country['Date'] <= end_date)]

# Create Plotly figures
fig_summary = px.bar(
    df_country,
    x='Date',
    y='Cases',
    title=f'COVID-19 Cases in {selected_country}',
    labels={'Cases': 'Number of Cases', 'Date': 'Date'},
    template='plotly_dark'
)

# Adding more graphs
fig_deaths = px.line(
    df_country,
    x='Date',
    y='Deaths',
    title=f'COVID-19 Deaths in {selected_country}',
    labels={'Deaths': 'Number of Deaths', 'Date': 'Date'},
    template='plotly_dark',
    line_shape='spline'
)

fig_recovered = px.line(
    df_country,
    x='Date',
    y='Recovered',
    title=f'COVID-19 Recoveries in {selected_country}',
    labels={'Recovered': 'Number of Recoveries', 'Date': 'Date'},
    template='plotly_dark',
    line_shape='spline'
)

# Streamlit layout
col1, col2, col3 = st.columns(3)
col1.plotly_chart(fig_summary, use_container_width=True)
col2.plotly_chart(fig_deaths, use_container_width=True)
col3.plotly_chart(fig_recovered, use_container_width=True)

# Show data table
st.subheader(f"Data for {selected_country}")
st.dataframe(df_country)

# Additional information
st.markdown("""
### Data Source
Data is sourced from the [COVID-19 API](https://covid19api.com/).
""")
