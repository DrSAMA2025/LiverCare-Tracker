import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

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

    # Generate Health Insights
    st.header("📊 Health Analytics")

    # Symptom Trends
    st.subheader("Symptom Severity Trends")
    if not symptoms_df.empty:
        # Create interactive symptom trend chart
        fig = px.line(symptoms_df, x='date', y='severity', color='symptom',
                     title="Symptom Severity Over Time",
                     labels={'date': 'Date', 'severity': 'Severity Level', 'symptom': 'Symptom'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

        # Symptom frequency analysis
        symptom_counts = symptoms_df['symptom'].value_counts()
        fig_freq = px.bar(symptom_counts, 
                         title="Most Frequent Symptoms",
                         labels={'value': 'Frequency', 'index': 'Symptom'})
        st.plotly_chart(fig_freq, use_container_width=True)
    else:
        st.info("No symptom data available for the selected period.")

    # Diet Analysis
    st.subheader("Dietary Patterns")
    if not diet_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            sodium_dist = diet_df['sodium_level'].value_counts()
            fig_sodium = px.pie(values=sodium_dist.values, 
                              names=sodium_dist.index,
                              title="Sodium Level Distribution")
            st.plotly_chart(fig_sodium)

        with col2:
            protein_dist = diet_df['protein_level'].value_counts()
            fig_protein = px.pie(values=protein_dist.values, 
                               names=protein_dist.index,
                               title="Protein Level Distribution")
            st.plotly_chart(fig_protein)

        # Meal type distribution over time
        meal_dist = px.histogram(diet_df, x='date', color='meal_type',
                               title="Meal Distribution Over Time",
                               labels={'date': 'Date', 'count': 'Number of Meals'})
        st.plotly_chart(meal_dist)
    else:
        st.info("No diet data available for the selected period.")

    # Medication Analysis
    st.subheader("Medication Adherence Insights")
    if not meds_df.empty:
        # Calculate adherence rates
        med_adherence = meds_df.groupby('medication_name')['taken'].mean() * 100
        fig_meds = px.bar(med_adherence, 
                         title="Medication Adherence Rate (%)",
                         labels={'value': 'Adherence Rate (%)', 'index': 'Medication'})
        st.plotly_chart(fig_meds)

        # Medication timeline
        fig_timeline = px.scatter(meds_df, x='date', y='medication_name', 
                                color='taken',
                                title="Medication Timeline",
                                labels={'date': 'Date', 'medication_name': 'Medication'})
        st.plotly_chart(fig_timeline)
    else:
        st.info("No medication data available for the selected period.")

    # AI-Driven Insights
    st.header("🤖 Smart Health Insights")

    # Generate insights based on the data
    insights = []

    # Symptom Insights
    if not symptoms_df.empty:
        # Most severe symptoms
        severe_symptoms = symptoms_df[symptoms_df['severity'] >= 7]['symptom'].value_counts()
        if not severe_symptoms.empty:
            insights.append(f"⚠️ Your most severe symptoms are: {', '.join(severe_symptoms.index[:2])}")

        # Symptom patterns
        recent_symptoms = symptoms_df.sort_values('date').tail(5)
        if len(recent_symptoms) > 0:
            common_recent = recent_symptoms['symptom'].mode().iloc[0]
            insights.append(f"📈 Your most frequent recent symptom is: {common_recent}")

    # Diet Insights
    if not diet_df.empty:
        # Sodium level analysis
        high_sodium = diet_df['sodium_level'].value_counts().get('High', 0)
        total_meals = len(diet_df)
        if total_meals > 0 and (high_sodium / total_meals) > 0.3:
            insights.append("🧂 Consider reducing high-sodium meals as they appear frequently in your diet")

        # Protein level analysis
        low_protein = diet_df['protein_level'].value_counts().get('Low', 0)
        if total_meals > 0 and (low_protein / total_meals) > 0.3:
            insights.append("🥩 Your protein intake appears to be low. Consider adding more protein-rich foods to your diet")

    # Medication Insights
    if not meds_df.empty:
        # Adherence analysis
        low_adherence_meds = med_adherence[med_adherence < 80].index.tolist()
        if low_adherence_meds:
            insights.append(f"💊 Improvement needed in taking: {', '.join(low_adherence_meds)}")

    # Display insights
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("Add more health data to receive personalized insights!")

except Exception as e:
    st.error(f"Error generating insights: {str(e)}")