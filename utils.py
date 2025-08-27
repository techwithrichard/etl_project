"""
Utility functions for ETL Pipeline
"""

import pandas as pd
import json
import numpy as np

def clean_dataframe_for_json(df):
    """
    Clean DataFrame by replacing NaN, inf, and -inf values with None
    to ensure valid JSON conversion
    """
    if df is None or df.empty:
        return df
    
    # Create a copy to avoid modifying the original
    df_clean = df.copy()
    
    # Replace NaN, inf, and -inf values with None
    df_clean = df_clean.replace([np.nan, np.inf, -np.inf], [None, None, None])
    
    # Also handle string representations of NaN
    df_clean = df_clean.replace(['nan', 'NaN', 'NAN', 'inf', '-inf'], [None, None, None, None, None])
    
    # Handle any remaining NaN values in numeric columns
    for col in df_clean.select_dtypes(include=[np.number]).columns:
        df_clean[col] = df_clean[col].replace([np.nan, np.inf, -np.inf], [None, None, None])
    
    return df_clean

def dataframe_to_json(df, orient='records'):
    """
    Convert DataFrame to JSON with proper NaN handling
    """
    if df is None or df.empty:
        return []
    
    # Clean the DataFrame
    df_clean = clean_dataframe_for_json(df)
    
    try:
        #  different approaches for JSON conversion
        if hasattr(df_clean, 'to_json'):
            # Standard pandas DataFrame
            try:
                json_str = df_clean.to_json(orient=orient, na_rep=None, date_format='iso')
                return json.loads(json_str)
            except TypeError:
                # Fallback without na_rep parameter
                json_str = df_clean.to_json(orient=orient, date_format='iso')
                return json.loads(json_str)
        else:
            # Handle non-pandas DataFrames
            records = df_clean.to_dict(orient='records')
            return clean_records_manually(records)
    except Exception as e:
        # Fallback: convert to records and handle manually
        try:
            records = df_clean.to_dict(orient='records')
        except Exception:
            # Last resort: try to convert to list
            records = df_clean.tolist() if hasattr(df_clean, 'tolist') else []
        return clean_records_manually(records)

def clean_records_manually(records):
    """
    Clean records manually by replacing NaN and invalid values
    """
    if not records:
        return []
    
    cleaned_records = []
    for record in records:
        if isinstance(record, dict):
            cleaned_record = {}
            for key, value in record.items():
                if pd.isna(value) or value == 'nan' or value == 'NaN' or value == 'NAN':
                    cleaned_record[key] = None
                elif isinstance(value, (int, float)) and (np.isnan(value) or np.isinf(value)):
                    cleaned_record[key] = None
                else:
                    cleaned_record[key] = value
            cleaned_records.append(cleaned_record)
        else:
            # Handle non-dict records
            if pd.isna(record) or record == 'nan' or record == 'NaN' or record == 'NAN':
                cleaned_records.append(None)
            elif isinstance(record, (int, float)) and (np.isnan(record) or np.isinf(record)):
                cleaned_records.append(None)
            else:
                cleaned_records.append(record)
    
    return cleaned_records

def safe_json_serialize(obj):
    """
    Safely serialize objects to JSON, handling non-serializable types
    """
    def default_serializer(obj):
        if pd.isna(obj) or obj == 'nan' or obj == 'NaN' or obj == 'NAN':
            return None
        elif isinstance(obj, (int, float)) and (np.isnan(obj) or np.isinf(obj)):
            return None
        elif hasattr(obj, 'isoformat'):  # Handle datetime objects
            return obj.isoformat()
        else:
            return str(obj)
    
    try:
        return json.dumps(obj, default=default_serializer)
    except Exception as e:
        print(f"Error in JSON serialization: {e}")
        return json.dumps(str(obj))

def clean_analytics_data(analytics_dict):
    """
    Clean analytics dictionary to ensure no NaN values exist
    """
    if not isinstance(analytics_dict, dict):
        return analytics_dict
    
    cleaned = {}
    for key, value in analytics_dict.items():
        if isinstance(value, dict):
            cleaned[key] = clean_analytics_data(value)
        elif isinstance(value, (list, tuple)):
            cleaned[key] = [clean_analytics_data(item) for item in value]
        elif pd.isna(value) or value == 'nan' or value == 'NaN' or value == 'NAN':
            cleaned[key] = None
        elif isinstance(value, (int, float)) and (np.isnan(value) or np.isinf(value)):
            cleaned[key] = None
        else:
            cleaned[key] = value
        print("i love coding")
    
    return cleaned
