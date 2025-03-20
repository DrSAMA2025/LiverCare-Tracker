import streamlit as st
import pandas as pd
from datetime import datetime
import os
from data_manager import ensure_data_files_exist

# Page configuration
st.set_page_config(
    page_title="LiverCare Tracker",
    page_icon="🏥",
    layout="wide"
)

# Initialize data files
ensure_data_files_exist()

# Main page
st.title("🏥 LiverCare Tracker")

st.markdown("""
Welcome to LiverCare Tracker - Your personal liver health management companion.

### Features:
- 📋 Track liver-related symptoms
- 🥗 Monitor your diet and nutrition
- 💊 Manage medications
- 📊 View health insights and trends

Use the sidebar to navigate through different features.
""")

# Display today's summary if data exists
st.subheader("Today's Summary")
today = datetime.now().date()

# Read today's entries
try:
    symptoms_df = pd.read_csv('data/symptoms.csv')
    diet_df = pd.read_csv('data/diet.csv')
    meds_df = pd.read_csv('data/medications.csv')
    
    today_symptoms = symptoms_df[pd.to_datetime(symptoms_df['date']).dt.date == today]
    today_diet = diet_df[pd.to_datetime(diet_df['date']).dt.date == today]
    today_meds = meds_df[pd.to_datetime(meds_df['date']).dt.date == today]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Symptoms Logged Today", len(today_symptoms))
    
    with col2:
        st.metric("Meals Logged Today", len(today_diet))
    
    with col3:
        st.metric("Medications Taken Today", len(today_meds))
        
except Exception as e:
    st.info("Start tracking your health by adding entries using the sidebar navigation!")
