import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

st.title("Health Insights")

# Load all data
try:
    symptoms_df = pd.read_csv('data/symptoms.csv')
    diet_df = pd.read_csv('data/diet.csv')
    meds_df = pd.read_csv('data/medications.csv')
    
    # Convert dates
    symptoms_df['date'] = pd.to_datetime(symptoms_df['date'])
    diet_df['date'] = pd.to_datetime(diet_df['date'])
    meds_df['date'] = pd.to_datetime(meds_df['date'])
    
    # Time period selector
    time_period = st.selectbox(
        "Select Time Period",
        ["Last 7 days", "Last 30 days", "All time"]
    )
    
    # Filter data based on time period
    end_date = datetime.now()
    if time_period == "Last 7 days":
        start_date = end_date - timedelta(days=7)
    elif time_period == "Last 30 days":
        start_date = end_date - timedelta(days=30)
    else:
        start_date = symptoms_df['date'].min()
    
    # Filter dataframes
    symptoms_df = symptoms_df[symptoms_df['date'] >= start_date]
    diet_df = diet_df[diet_df['date'] >= start_date]
    meds_df = meds_df[meds_df['date'] >= start_date]
    
    # Symptom Trends
    st.subheader("Symptom Severity Trends")
    if not symptoms_df.empty:
        fig = px.line(symptoms_df, x='date', y='severity', color='symptom',
                     title="Symptom Severity Over Time")
        st.plotly_chart(fig)
    else:
        st.info("No symptom data available for the selected period.")
    
    # Diet Analysis
    st.subheader("Diet Analysis")
    if not diet_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            sodium_dist = diet_df['sodium_level'].value_counts()
            fig_sodium = px.pie(values=sodium_dist.values, names=sodium_dist.index,
                              title="Sodium Level Distribution")
            st.plotly_chart(fig_sodium)
        
        with col2:
            protein_dist = diet_df['protein_level'].value_counts()
            fig_protein = px.pie(values=protein_dist.values, names=protein_dist.index,
                               title="Protein Level Distribution")
            st.plotly_chart(fig_protein)
    else:
        st.info("No diet data available for the selected period.")
    
    # Medication Adherence
    st.subheader("Medication Adherence")
    if not meds_df.empty:
        med_adherence = meds_df.groupby('medication_name')['taken'].mean() * 100
        fig_meds = px.bar(med_adherence, title="Medication Adherence Rate (%)")
        st.plotly_chart(fig_meds)
    else:
        st.info("No medication data available for the selected period.")

except Exception as e:
    st.error(f"Error generating insights: {str(e)}")
