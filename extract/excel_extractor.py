import pandas as pd
import os

# In extract/excel_extractor.py
def extract_student_data():
    #    stude data excel
    try:
        df = pd.read_excel('data/student_scores.xlsx')
        print(f"Extracted {len(df)} Kenyan student records")
        return df
    except Exception as e:
        print(f"Error extracting student data: {e}")
        return pd.DataFrame()

def extract_weather_data():
    # weather data excel
    try:
        df = pd.read_excel('data/weather_data.xlsx')
        print(f"Extracted {len(df)} Kenyan weather records")
        return df
    except Exception as e:
        print(f"Error extracting weather data: {e}")
        return pd.DataFrame()

def extract_events_data():
    # university data excel
    try:
        df = pd.read_excel('data/university_events.xlsx')
        print(f"Extracted {len(df)} university event records")
        return df
    except Exception as e:
        print(f"Error extracting events data: {e}")
        return pd.DataFrame()