import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Diet Tracker")

# Diet tracking form
with st.form("diet_form"):
    st.write("Log Your Meal")
    
    date = st.date_input("Date", value=datetime.now())
    
    meal_type = st.selectbox(
        "Meal Type",
        ["Breakfast", "Lunch", "Dinner", "Snack"]
    )
    
    food_items = st.text_area("Food Items (one per line)")
    
    sodium_level = st.select_slider(
        "Sodium Level",
        options=["Low", "Medium", "High"],
        value="Medium"
    )
    
    protein_level = st.select_slider(
        "Protein Level",
        options=["Low", "Medium", "High"],
        value="Medium"
    )
    
    notes = st.text_area("Additional Notes")
    
    submitted = st.form_submit_button("Log Meal")
    
    if submitted:
        try:
            # Read existing data
            df = pd.read_csv('data/diet.csv')
            
            # Add new entry
            new_entry = pd.DataFrame([{
                'date': date,
                'meal_type': meal_type,
                'food_items': food_items,
                'sodium_level': sodium_level,
                'protein_level': protein_level,
                'notes': notes
            }])
            
            # Append and save
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv('data/diet.csv', index=False)
            
            st.success("Meal logged successfully!")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# Display recent meals
st.subheader("Recent Meals")
try:
    df = pd.read_csv('data/diet.csv')
    if not df.empty:
        df['date'] = pd.to_datetime(df['date'])
        recent_meals = df.sort_values('date', ascending=False).head(5)
        st.dataframe(recent_meals[['date', 'meal_type', 'food_items', 'sodium_level', 'protein_level']])
    else:
        st.info("No meals logged yet.")
except Exception as e:
    st.error(f"Error loading meals: {str(e)}")
