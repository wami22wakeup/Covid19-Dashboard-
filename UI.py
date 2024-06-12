import streamlit as st
import plotly.express as px

# Apply custom CSS
def apply_custom_css():
    css_file = 'style.css'
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def display_metrics(data):
    st.header("📊 Current COVID-19 Statistics")
    st.metric("Total Cases", f"{data['cases']:,}")
    st.metric("Total Deaths", f"{data['deaths']:,}")
    st.metric("Total Recovered", f"{data['recovered']:,}")

def display_charts(df):
    st.header("📈 COVID-19 Cases Over Time")

    fig_cases = px.line(df, x='Date', y='Cases', title='Total Cases Over Time', template='plotly_dark')
    fig_cases.update_traces(line=dict(color='royalblue'))
    st.plotly_chart(fig_cases)

    fig_deaths = px.line(df, x='Date', y='Deaths', title='Total Deaths Over Time', template='plotly_dark')
    fig_deaths.update_traces(line=dict(color='firebrick'))
    st.plotly_chart(fig_deaths)

    fig_recovered = px.line(df, x='Date', y='Recovered', title='Total Recovered Over Time', template='plotly_dark')
    fig_recovered.update_traces(line=dict(color='green'))
    st.plotly_chart(fig_recovered)

    st.header("📉 Daily Changes")

    fig_daily_cases = px.bar(df, x='Date', y='Daily Cases', title='Daily New Cases', template='plotly_dark')
    fig_daily_cases.update_traces(marker_color='royalblue')
    st.plotly_chart(fig_daily_cases)

    fig_daily_deaths = px.bar(df, x='Date', y='Daily Deaths', title='Daily New Deaths', template='plotly_dark')
    fig_daily_deaths.update_traces(marker_color='firebrick')
    st.plotly_chart(fig_daily_deaths)

    fig_daily_recovered = px.bar(df, x='Date', y='Daily Recovered', title='Daily New Recovered', template='plotly_dark')
    fig_daily_recovered.update_traces(marker_color='green')
    st.plotly_chart(fig_daily_recovered)

def select_country(countries):
    country = st.sidebar.selectbox("Select a country", countries)
    return country
