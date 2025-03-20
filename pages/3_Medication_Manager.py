import streamlit as st
import pandas as pd
from datetime import datetime, time

st.title("Medication Manager")

# Create tabs for different sections
tab1, tab2 = st.tabs(["💊 Medication Log", "⏰ Reminders"])

with tab1:
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

with tab2:
    st.subheader("Medication Reminders")

    # Add new reminder
    with st.form("reminder_form"):
        st.write("Set Up Medication Reminder")

        reminder_med = st.selectbox(
            "Medication",
            ["Diuretics", "Lactulose", "Beta Blockers", "Other"],
            key="reminder_med"
        )

        reminder_time = st.time_input(
            "Reminder Time",
            value=time(9, 0)
        )

        frequency = st.selectbox(
            "Frequency",
            ["Daily", "Twice Daily", "Weekly", "Monthly"]
        )

        enabled = st.checkbox("Enable Reminder", value=True)

        reminder_submitted = st.form_submit_button("Set Reminder")

        if reminder_submitted:
            try:
                # Read existing reminders
                reminders_df = pd.read_csv('data/reminders.csv')

                # Add new reminder
                new_reminder = pd.DataFrame([{
                    'medication_name': reminder_med,
                    'time': reminder_time.strftime("%H:%M"),
                    'frequency': frequency,
                    'enabled': enabled
                }])

                # Append and save
                reminders_df = pd.concat([reminders_df, new_reminder], ignore_index=True)
                reminders_df.to_csv('data/reminders.csv', index=False)

                st.success("Reminder set successfully!")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Display existing reminders
    st.subheader("Active Reminders")
    try:
        reminders_df = pd.read_csv('data/reminders.csv')
        if not reminders_df.empty:
            active_reminders = reminders_df[reminders_df['enabled']]
            if not active_reminders.empty:
                for _, reminder in active_reminders.iterrows():
                    with st.expander(f"{reminder['medication_name']} - {reminder['time']}"):
                        st.write(f"Frequency: {reminder['frequency']}")
                        if st.button("Disable", key=f"disable_{_}"):
                            reminders_df.loc[_, 'enabled'] = False
                            reminders_df.to_csv('data/reminders.csv', index=False)
                            st.rerun()
            else:
                st.info("No active reminders.")
        else:
            st.info("No reminders set yet.")
    except Exception as e:
        st.error(f"Error loading reminders: {str(e)}")

    st.markdown("""
    #### Reminder Tips:
    - Set reminders for the same time each day to build a routine
    - Enable notifications on your device to receive alerts
    - Keep your medication schedule consistent
    """)