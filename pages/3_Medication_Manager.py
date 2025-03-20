import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Medication Manager")

# Medication tracking form
with st.form("medication_form"):
    st.write("Log Your Medication")
    
    date = st.date_input("Date", value=datetime.now())
    
    medication_name = st.selectbox(
        "Medication",
        ["Diuretics", "Lactulose", "Beta Blockers", "Other"]
    )
    
    dosage = st.text_input("Dosage (e.g., 50mg)")
    
    taken = st.checkbox("Medication Taken")
    
    notes = st.text_area("Additional Notes")
    
    submitted = st.form_submit_button("Log Medication")
    
    if submitted:
        try:
            # Read existing data
            df = pd.read_csv('data/medications.csv')
            
            # Add new entry
            new_entry = pd.DataFrame([{
                'date': date,
                'medication_name': medication_name,
                'dosage': dosage,
                'taken': taken,
                'notes': notes
            }])
            
            # Append and save
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv('data/medications.csv', index=False)
            
            st.success("Medication logged successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display recent medications
st.subheader("Recent Medications")
try:
    df = pd.read_csv('data/medications.csv')
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        recent_meds = df.sort_values('date', ascending=False).head(5)
        st.dataframe(recent_meds[['date', 'medication_name', 'dosage', 'taken', 'notes']])
    else:
        st.info("No medications logged yet.")
except Exception as e:
    st.error(f"Error loading medications: {str(e)}")
