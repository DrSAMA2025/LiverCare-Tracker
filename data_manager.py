import pandas as pd
import os

def ensure_data_files_exist():
    """Ensure all necessary data files exist with correct structure"""
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Symptoms data structure
    if not os.path.exists('data/symptoms.csv'):
        symptoms_df = pd.DataFrame(columns=[
            'date', 'symptom', 'severity', 'notes'
        ])
        symptoms_df.to_csv('data/symptoms.csv', index=False)
    
    # Diet data structure
    if not os.path.exists('data/diet.csv'):
        diet_df = pd.DataFrame(columns=[
            'date', 'meal_type', 'food_items', 'sodium_level', 'protein_level', 'notes'
        ])
        diet_df.to_csv('data/diet.csv', index=False)
    
    # Medications data structure
    if not os.path.exists('data/medications.csv'):
        medications_df = pd.DataFrame(columns=[
            'date', 'medication_name', 'dosage', 'taken', 'notes'
        ])
        medications_df.to_csv('data/medications.csv', index=False)
