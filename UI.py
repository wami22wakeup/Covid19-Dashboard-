import streamlit as st
import plotly.express as px

def display_metrics(data):
    st.header("Current COVID-19 Statistics")
    st.metric("Total Cases", data['cases'])
    st.metric("Total Deaths", data['deaths'])
    st.metric("Total Recovered", data['recovered'])

def display_charts(df):
    st.header("COVID-19 Cases Over Time")
    
    fig = px.line(df, x='Date', y='Cases', title='Total Cases Over Time')
    st.plotly_chart(fig)

    fig = px.line(df, x='Date', y='Deaths', title='Total Deaths Over Time')
    st.plotly_chart(fig)

    fig = px.line(df, x='Date', y='Recovered', title='Total Recovered Over Time')
    st.plotly_chart(fig)

    st.header("Daily Changes")

    fig = px.bar(df, x='Date', y='Daily Cases', title='Daily New Cases')
    st.plotly_chart(fig)

    fig = px.bar(df, x='Date', y='Daily Deaths', title='Daily New Deaths')
    st.plotly_chart(fig)

    fig = px.bar(df, x='Date', y='Daily Recovered', title='Daily New Recovered')
    st.plotly_chart(fig)

def select_country(countries):
    country = st.selectbox("Select a country", countries)
    return country
