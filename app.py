from flask import Flask, render_template, jsonify, request
import json
import os
import pandas as pd
from etl_pipeline import run_etl_pipeline
from warehouse.warehouse_manager import WarehouseManager
from utils import dataframe_to_json, clean_analytics_data

app = Flask(__name__)

# Initialize warehouse
warehouse = WarehouseManager()

# Store data in memory for the dashboard
dashboard_data = {
    'data': {},
    'summary': {},
    'last_run': None
}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/simple')
def simple():
    """Simple dashboard page"""
    return render_template('simple.html')

@app.route('/run_etl')
def run_etl():
    """Run the ETL pipeline and return results"""
    try:
        result = run_etl_pipeline()
        
        # Store data for the dashboard
        dashboard_data['data'] = result['transformed_data']
        
        # Clean analytics data to prevent NaN values
        analytics = result.get('analytics', {})
        cleaned_analytics = clean_analytics_data(analytics)
        
        dashboard_data['summary'] = {
            'run_id': result['run_id'],
            'datasets': list(result['transformed_data'].keys()),
            'record_counts': {name: len(df) for name, df in result['transformed_data'].items()},
            'processed_at': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
            'validation_results': result.get('validation_results', {}),
            'warehouse_summary': result.get('warehouse_summary', {}),
            'analytics': cleaned_analytics
        }
        dashboard_data['last_run'] = result['run_id']
        
        # Convert DataFrames to JSON for display
        json_data = {}
        for name, df in result['transformed_data'].items():
            # Use utility function to handle NaN values properly
            json_data[name] = dataframe_to_json(df)
        
        return jsonify({
            'data': json_data,
            'summary': dashboard_data['summary'],
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'ETL pipeline failed: {str(e)}',
            'success': False
        })

@app.route('/get_data')
def get_data():
    """Get the latest data from memory"""
    try:
        if not dashboard_data['data']:
            return jsonify({
                'error': 'No data available. Run ETL first.',
                'success': False
            })
        
        # Convert DF to JSON for display
        json_data = {}
        for name, df in dashboard_data['data'].items():
            # Use utility function to handle NaN values properly
            json_data[name] = dataframe_to_json(df)
        
        return jsonify({
            'data': json_data,
            'summary': dashboard_data['summary'],
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving data: {str(e)}',
            'success': False
        })

@app.route('/warehouse/summary')
def warehouse_summary():
    """Get warehouse summary statistics"""
    try:
        summary = warehouse.get_warehouse_summary()
        return jsonify({
            'summary': summary,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Error getting warehouse summary: {str(e)}',
            'success': False
        })

@app.route('/warehouse/analytics')
def warehouse_analytics():
    """Get analytics from warehouse"""
    try:
        analytics = warehouse.run_analytics()
        # Clean analytics data to prevent NaN values
        cleaned_analytics = clean_analytics_data(analytics)
        return jsonify({
            'analytics': cleaned_analytics,
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': f'Error running analytics: {str(e)}',
            'success': False
        })

@app.route('/warehouse/data/<table_name>')
def warehouse_data(table_name):
    """Get data from specific warehouse table"""
    try:
        limit = request.args.get('limit', 100, type=int)
        data = warehouse.get_data(table_name, limit)
        
        if data.empty:
            return jsonify({
                'data': [],
                'message': f'No data found in {table_name}',
                'success': True
            })
        
        # Use utility function to handle NaN values properly
        json_data = dataframe_to_json(data)
        return jsonify({
            'data': json_data,
            'count': len(json_data),
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error retrieving data from {table_name}: {str(e)}',
            'success': False
        })

@app.route('/clear_data', methods=['POST'])
def clear_data():
    """Clear the stored data and warehouse"""
    try:
        # Clear the in-memory data
        dashboard_data['data'] = {}
        dashboard_data['summary'] = {}
        dashboard_data['last_run'] = None
        
        # Clear the output files 
        output_dir = 'output'
        if os.path.exists(output_dir):
            for file in os.listdir(output_dir):
                if file.endswith('.json') or file.endswith('.csv'):
                    os.remove(os.path.join(output_dir, file))
        
        # Clear warehouse data
        warehouse.clear_warehouse()
        
        return jsonify({
            'message': 'Data cleared successfully from memory, files, and warehouse',
            'success': True
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Error clearing data: {str(e)}',
            'success': False
        })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check warehouse connection
        warehouse.get_warehouse_summary()
        return jsonify({
            'status': 'healthy',
            'warehouse': 'connected',
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'warehouse': 'disconnected',
            'error': str(e),
            'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 500

@app.route('/test')
def test():
    """Simple test endpoint"""
    return jsonify({
        'message': 'Flask app is working!',
        'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    print("Starting ETL Dashboard...")
    print("Main Dashboard: http://localhost:5000")
    print("Simple Dashboard: http://localhost:5000/simple")
    print("Test endpoint: http://localhost:5000/test")
    print("Health check: http://localhost:5000/health")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, port=5000, host='127.0.0.1')
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"\nFailed to start dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if port 5000 is available")
        print("3. Ensure all required modules are present")