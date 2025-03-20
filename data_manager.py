import pandas as pd
import os
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample data for testing"""
    # Generate dates for the last 30 days
    end_date = datetime.now()
    dates = [(end_date - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(30)]

    # Sample symptoms data
    symptoms = []
    for date in dates:
        # Add 1-3 symptoms per day
        for _ in range(random.randint(1, 3)):
            symptoms.append({
                'date': date,
                'symptom': random.choice(['Fatigue', 'Jaundice', 'Abdominal Swelling', 'Nausea']),
                'severity': random.randint(1, 10),
                'notes': 'Sample symptom entry'
            })

    # Sample diet data
    diet = []
    for date in dates:
        # Add 2-4 meals per day
        for _ in range(random.randint(2, 4)):
            diet.append({
                'date': date,
                'meal_type': random.choice(['Breakfast', 'Lunch', 'Dinner', 'Snack']),
                'food_items': 'Sample food items',
                'sodium_level': random.choice(['Low', 'Medium', 'High']),
                'protein_level': random.choice(['Low', 'Medium', 'High']),
                'notes': 'Sample diet entry'
            })

    # Sample medications data
    medications = []
    for date in dates:
        # Add 1-2 medications per day
        for _ in range(random.randint(1, 2)):
            medications.append({
                'date': date,
                'medication_name': random.choice(['Diuretics', 'Lactulose', 'Beta Blockers']),
                'dosage': '50mg',
                'taken': random.choice([True, False]),
                'notes': 'Sample medication entry'
            })

    return {
        'symptoms': pd.DataFrame(symptoms),
        'diet': pd.DataFrame(diet),
        'medications': pd.DataFrame(medications)
    }

def ensure_data_files_exist():
    """Ensure all necessary data files exist with correct structure"""
    if not os.path.exists('data'):
        os.makedirs('data')

    # Always generate fresh sample data
    sample_data = generate_sample_data()

    # Save sample data to CSV files
    sample_data['symptoms'].to_csv('data/symptoms.csv', index=False)
    sample_data['diet'].to_csv('data/diet.csv', index=False)
    sample_data['medications'].to_csv('data/medications.csv', index=False)