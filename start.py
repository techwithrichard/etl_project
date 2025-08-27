#!/usr/bin/env python3
"""
Simple startup script for ETL Dashboard
Just runs the main app.py
"""

if __name__ == "__main__":
    print("Starting ETL Dashboard...")
    print("This will launch the main dashboard at http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    try:
        from app import app
        app.run(debug=True, port=5000, host='127.0.0.1')
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"\nFailed to start dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check if port 5000 is available")
        print("3. Ensure all required modules are present")
