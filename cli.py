#!/usr/bin/env python3
"""
Command Line Interface for ETL Pipeline
"""

import argparse
import sys
import os

def run_etl():
    """Run the ETL pipeline"""
    print("🚀 Starting ETL Pipeline...")
    try:
        from etl_pipeline import run_etl_pipeline
        result = run_etl_pipeline()
        print("✅ ETL Pipeline completed successfully!")
        return result
    except Exception as e:
        print(f"❌ ETL Pipeline failed: {e}")
        return None

def start_dashboard():
    """Start the web dashboard"""
    print("🌐 Starting ETL Dashboard...")
    try:
        from app import app
        print("Dashboard will be available at: http://localhost:5000")
        app.run(debug=True, port=5000, host='127.0.0.1')
    except Exception as e:
        print(f"❌ Failed to start dashboard: {e}")

def run_tests():
    """Run the test suite"""
    print("🧪 Running tests...")
    try:
        from run_tests import run_tests
        return run_tests()
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return 1

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description='ETL Pipeline CLI')
    parser.add_argument('command', choices=['etl', 'dashboard', 'test', 'help'], 
                       help='Command to run')
    
    args = parser.parse_args()
    
    if args.command == 'etl':
        run_etl()
    elif args.command == 'dashboard':
        start_dashboard()
    elif args.command == 'test':
        sys.exit(run_tests())
    elif args.command == 'help':
        print("""
ETL Pipeline CLI Commands:
  etl       - Run the complete ETL pipeline
  dashboard - Start the web dashboard
  test      - Run the test suite
  help      - Show this help message

Examples:
  python cli.py etl
  python cli.py dashboard
  python cli.py test
        """)

if __name__ == '__main__':
    main()
