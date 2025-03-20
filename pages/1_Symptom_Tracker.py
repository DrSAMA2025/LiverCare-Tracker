import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Symptom Tracker")

# Symptom tracking form
with st.form("symptom_form"):
    st.write("Log Your Symptoms")
    
    date = st.date_input("Date", value=datetime.now())
    
    symptom = st.selectbox(
        "Symptom",
        ["Fatigue", "Jaundice", "Abdominal Swelling", "Nausea", 
         "Loss of Appetite", "Itching", "Dark Urine", "Other"]
    )
    
    severity = st.slider("Severity", 1, 10, 5)
    
    notes = st.text_area("Additional Notes")
    
    submitted = st.form_submit_button("Log Symptom")
    
    if submitted:
        try:
            # Read existing data
            df = pd.read_csv('data/symptoms.csv')
            
            # Add new entry
            new_entry = pd.DataFrame([{
                'date': date,
                'symptom': symptom,
                'severity': severity,
                'notes': notes
            }])
            
            # Append and save
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv('data/symptoms.csv', index=False)
            
            st.success("Symptom logged successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display recent symptoms
st.subheader("Recent Symptoms")
try:
    df = pd.read_csv('data/symptoms.csv')
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        recent_symptoms = df.sort_values('date', ascending=False).head(5)
        st.dataframe(recent_symptoms[['date', 'symptom', 'severity', 'notes']])
    else:
        st.info("No symptoms logged yet.")
except Exception as e:
    st.error(f"Error loading symptoms: {str(e)}")
