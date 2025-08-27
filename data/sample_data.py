"""
Sample data generator for ETL pipeline testing
"""

import pandas as pd
import os
from pathlib import Path

def create_sample_excel():
    """Create sample Excel file with student scores"""
    
    # Create data directory if it doesn't exist
    data_dir = Path(__file__).parent
    data_dir.mkdir(exist_ok=True)
    
    # Sample student scores data
    sample_data = {
        'Student_ID': ['S1001', 'S1002', 'S1003', 'S1004', 'S1005', 'S1006', 'S1007', 'S1008'],
        'First_Name': ['John', 'Sarah', 'Mike', 'Emily', 'David', 'Lisa', 'Tom', 'Anna'],
        'Last_Name': ['Doe', 'Smith', 'Johnson', 'Brown', 'Wilson', 'Davis', 'Miller', 'Garcia'],
        'Score': [85, 92, 78, 95, 88, 91, 76, 89],
        'Subject': ['Math', 'Science', 'History', 'English', 'Physics', 'Chemistry', 'Biology', 'Art']
    }
    
    df = pd.DataFrame(sample_data)
    excel_path = data_dir / "student_scores.xlsx"
    
    # Save to Excel
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    print(f"Sample Excel file created: {excel_path}")
    return excel_path

def create_sample_json():
    """Create sample JSON files for testing"""
    
    data_dir = Path(__file__).parent
    
    # Sample weather data
    weather_data = [
        {'city': 'Nairobi', 'temperature': 22.5, 'humidity': 65, 'conditions': 'Sunny'},
        {'city': 'Mombasa', 'temperature': 28.0, 'humidity': 70, 'conditions': 'Partly Cloudy'},
        {'city': 'Kisumu', 'temperature': 25.5, 'humidity': 68, 'conditions': 'Clear'},
        {'city': 'Nakuru', 'temperature': 20.0, 'humidity': 72, 'conditions': 'Cloudy'},
        {'city': 'Eldoret', 'temperature': 18.5, 'humidity': 75, 'conditions': 'Rainy'}
    ]
    
    # Sample news data
    news_data = [
        {'headline': 'New AI Breakthrough in Machine Learning', 'source': 'Tech News', 'scraped_at': '2024-01-15'},
        {'headline': 'Climate Change Conference Results', 'source': 'Science Daily', 'scraped_at': '2024-01-15'},
        {'headline': 'SpaceX Launches New Satellite', 'source': 'Space News', 'scraped_at': '2024-01-15'},
        {'headline': 'Global Economic Trends 2024', 'source': 'Business Weekly', 'scraped_at': '2024-01-15'},
        {'headline': 'Healthcare Innovation Summit', 'source': 'Health News', 'scraped_at': '2024-01-15'}
    ]
    
    # Save JSON files
    import json
    
    weather_path = data_dir / "sample_weather.json"
    with open(weather_path, 'w') as f:
        json.dump(weather_data, f, indent=2)
    
    news_path = data_dir / "sample_news.json"
    with open(news_path, 'w') as f:
        json.dump(news_data, f, indent=2)
    
    print(f"Sample JSON files created:")
    print(f"  - Weather: {weather_path}")
    print(f"  - News: {news_path}")
    

if __name__ == "__main__":
    print("Creating sample data files...")
    create_sample_excel()
    create_sample_json()
    print("Sample data generation completed!")
