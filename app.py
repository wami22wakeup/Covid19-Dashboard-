import streamlit as st
import requests 
from data_fetch import fetch_data, fetch_country_data, prepare_data
from UI import display_metrics, display_charts, select_country, apply_custom_css

# Page configuration (must be the first Streamlit command)
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
    # Fetch and prepare data
    summary_data = fetch_data()
    st.write("Summary Data:", summary_data)  # Debug print

    # Display global metrics
    display_metrics(summary_data['Global'])

    # Select country
    selected_country = select_country([country['Country'] for country in summary_data['Countries']])

    # Fetch country-specific data
    country_data = fetch_country_data(selected_country)
    df_country = prepare_data(country_data)

    # Sidebar filters
    st.sidebar.header("Filters")
    date_range = st.sidebar.date_input("Select Date Range", [])
    if date_range:
        start_date, end_date = date_range
        df_country = df_country[(df_country['Date'] >= start_date) & (df_country['Date'] <= end_date)]

    # Display charts
    display_charts(df_country)

except requests.ConnectionError:
    st.error("Network error: Unable to connect to the COVID-19 API. Please check your internet connection or try again later.")
except requests.HTTPError as http_err:
    st.error(f"HTTP error occurred: {http_err}")
except Exception as err:
    st.error(f"An error occurred: {err}")

# Additional information
st.markdown("""
### Data Source
Data is sourced from the [COVID-19 API](https://covid19api.com/).
""")