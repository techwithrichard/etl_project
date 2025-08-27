import pandas as pd
import json
import os

def load_data(transformed_data, output_format='json'):
    """
    Load transformed data to output files
    Returns the file paths of saved data
    """
    output_paths = {}
    
    # Creating output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    for name, df in transformed_data.items():
        if output_format == 'json':
            file_path = f'output/{name}.json'
            df.to_json(file_path, orient='records', indent=2)
        elif output_format == 'csv':
            file_path = f'output/{name}.csv'
            df.to_csv(file_path, index=False)
        else:
            file_path = f'output/{name}.xlsx'
            df.to_excel(file_path, index=False)
        
        output_paths[name] = file_path
        print(f"Saved {name} data to {file_path}")
    
    #combined summary
    summary = {
        'datasets': list(transformed_data.keys()),
        'record_counts': {name: len(df) for name, df in transformed_data.items()},
        'processed_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('output/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("ETL pipeline completed successfully!")
    return output_paths