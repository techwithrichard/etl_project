import pandas as pd
from datetime import datetime

def transform_data(mysql_df, weather_df, web_df, excel_df):
    """
    Transform all extracted data
    Returns a dictionary of transformed DataFrames
    """
    transformed_data = {}
    
    # Transform MySQL data
    if not mysql_df.empty:
        mysql_df = mysql_df.copy()
        # addding a processing timestamp
        mysql_df['processed_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transformed_data['students'] = mysql_df
        print(f"Transformed {len(mysql_df)} MySQL records")
    
    # Transform weather data
    if not weather_df.empty:
        weather_df = weather_df.copy()
        # addding a category based on temperature
        if 'temperature' in weather_df.columns:
            weather_df['temp_category'] = weather_df['temperature'].apply(
                lambda x: (
                    'Unknown' if x is None or pd.isna(x)
                    else 'Hot' if x > 25
                    else 'Warm' if x > 15
                    else 'Cool' if x > 5
                    else 'Cold'
                )
            )

        transformed_data['weather'] = weather_df
        print(f"Transformed {len(weather_df)} weather records")
    
    # Transform web data
    if not web_df.empty:
        web_df = web_df.copy()
        # addding word count for headlines
        if 'headline' in web_df.columns:
            web_df['word_count'] = web_df['headline'].apply(lambda x: len(str(x).split()))
        transformed_data['news'] = web_df
        print(f"Transformed {len(web_df)} web records")
    
    # Transform Excel data
    if not excel_df.empty:
        excel_df = excel_df.copy()
        # addding grade category if Score column exists
        if 'Score' in excel_df.columns:
            excel_df['grade_category'] = excel_df['Score'].apply(
                lambda x: 'A' if x >= 90 else 'B' if x >= 80 else 'C' if x >= 70 else 'D' if x >= 60 else 'F'
            )
        transformed_data['scores'] = excel_df
        print(f"Transformed {len(excel_df)} Excel records")
    
    print("Successfully transformed all data")
    return transformed_data