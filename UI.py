import streamlit as st
import plotly.express as px
import pandas as pd

# Apply custom CSS
def apply_custom_css():
    css_file = 'style.css'
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_metrics(data):
    st.header("📊 Current COVID-19 Statistics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", f"{data['cases']:,}")
    col2.metric("Total Deaths", f"{data['deaths']:,}")
    col3.metric("Total Recovered", f"{data['recovered']:,}")

def display_charts(df):
    st.header("📈 COVID-19 Cases Over Time")
    
    # Line charts for cases, deaths, recovered, and active cases
    col1, col2 = st.columns(2)
    
    with col1:
        fig_cases = px.line(df, x='Date', y='Cases', title='Total Cases Over Time', template='plotly_dark')
        fig_cases.update_traces(line=dict(color='royalblue'))
        st.plotly_chart(fig_cases)

        fig_recovered = px.line(df, x='Date', y='Recovered', title='Total Recovered Over Time', template='plotly_dark')
        fig_recovered.update_traces(line=dict(color='green'))
        st.plotly_chart(fig_recovered)
    
    with col2:
        fig_deaths = px.line(df, x='Date', y='Deaths', title='Total Deaths Over Time', template='plotly_dark')
        fig_deaths.update_traces(line=dict(color='firebrick'))
        st.plotly_chart(fig_deaths)
        
        df['Active Cases'] = df['Cases'] - df['Deaths'] - df['Recovered']
        fig_active = px.line(df, x='Date', y='Active Cases', title='Active Cases Over Time', template='plotly_dark')
        fig_active.update_traces(line=dict(color='orange'))
        st.plotly_chart(fig_active)

    st.header("📉 Daily Changes")
    
    # Bar charts for daily changes
    col3, col4, col5 = st.columns(3)
    
    with col3:
        fig_daily_cases = px.bar(df, x='Date', y='Daily Cases', title='Daily New Cases', template='plotly_dark')
        fig_daily_cases.update_traces(marker_color='royalblue')
        st.plotly_chart(fig_daily_cases)

    with col4:
        fig_daily_deaths = px.bar(df, x='Date', y='Daily Deaths', title='Daily New Deaths', template='plotly_dark')
        fig_daily_deaths.update_traces(marker_color='firebrick')
        st.plotly_chart(fig_daily_deaths)

    with col5:
        fig_daily_recovered = px.bar(df, x='Date', y='Daily Recovered', title='Daily New Recovered', template='plotly_dark')
        fig_daily_recovered.update_traces(marker_color='green')
        st.plotly_chart(fig_daily_recovered)

def select_country(countries):
    country = st.sidebar.selectbox("Select a country", countries, index=0)
    return country

def main():
    st.title("COVID-19 Dashboard")
    st.markdown("""
        This application provides up-to-date statistics and visualizations of COVID-19 cases globally and for specific countries.
        Select a country from the sidebar to see detailed metrics and charts.
    """)
    
    apply_custom_css()

    # Sample data for illustration purposes
    countries = ["USA", "India", "Brazil", "Russia", "UK"]
    country_data = {
        "USA": {"cases": 34000000, "deaths": 600000, "recovered": 29000000},
        "India": {"cases": 31000000, "deaths": 410000, "recovered": 30000000},
        "Brazil": {"cases": 20000000, "deaths": 560000, "recovered": 18000000},
        "Russia": {"cases": 6000000, "deaths": 150000, "recovered": 5500000},
        "UK": {"cases": 5000000, "deaths": 128000, "recovered": 4300000},
    }

    selected_country = select_country(countries)
    data = country_data[selected_country]

    if data:
        display_metrics(data)

        # Example dataframe for demonstration
        df = pd.DataFrame({
            "Date": pd.date_range(start="2021-01-01", periods=100, freq="D"),
            "Cases": (pd.Series(range(100)) * 1000).cumsum(),
            "Deaths": (pd.Series(range(100)) * 50).cumsum(),
            "Recovered": (pd.Series(range(100)) * 800).cumsum(),
            "Daily Cases": pd.Series(range(100)) * 1000,
            "Daily Deaths": pd.Series(range(100)) * 50,
            "Daily Recovered": pd.Series(range(100)) * 800,
        })
        display_charts(df)
    else:
        st.error("Data not available for the selected country.")

if __name__ == "__main__":
    main()
