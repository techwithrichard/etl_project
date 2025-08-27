import sqlite3
import pandas as pd
import json
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WarehouseManager:
    """Simple data warehouse manager using SQLite for persistent storage"""
    
    def __init__(self, db_path='warehouse/etl_warehouse.db'):
        """Initialize warehouse with SQLite database"""
        self.db_path = db_path
        self.ensure_warehouse_dir()
        self.init_database()
    
    def ensure_warehouse_dir(self):
        """Create warehouse directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def init_database(self):
        """Initialize the warehouse database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create tables for each data type
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER,
                        name TEXT,
                        age INTEGER,
                        major TEXT,
                        processed_at TEXT,
                        loaded_at TEXT
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        city TEXT,
                        temperature REAL,
                        humidity INTEGER,
                        conditions TEXT,
                        temp_category TEXT,
                        processed_at TEXT,
                        loaded_at TEXT
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS news (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        headline TEXT,
                        source TEXT,
                        scraped_at TEXT,
                        word_count INTEGER,
                        processed_at TEXT,
                        loaded_at TEXT
                    )
                ''')
                
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS scores (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        score INTEGER,
                        subject TEXT,
                        grade_category TEXT,
                        processed_at TEXT,
                        loaded_at TEXT
                    )
                ''')
                
                # Create pipeline metadata table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS pipeline_runs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        run_id TEXT,
                        start_time TEXT,
                        end_time TEXT,
                        status TEXT,
                        records_processed INTEGER,
                        error_message TEXT
                    )
                ''')
                
                conn.commit()
                logger.info("Warehouse database initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize warehouse: {e}")
            raise
    
    def map_columns(self, df, dataset_name):
        """Map source columns to warehouse schema columns"""
        if df.empty:
            return df
        
        df = df.copy()
        
        if dataset_name == 'students':
            # Map MySQL/sample student data columns
            column_mapping = {
                'student_id': 'student_id',
                'Student_ID': 'student_id',
                'id': 'student_id',
                'name': 'name',
                'Name': 'name',
                'First_Name': 'name',
                'first_name': 'name',
                'age': 'age',
                'Age': 'age',
                'major': 'major',
                'Major': 'major',
                'Course': 'major',
                'course': 'major'
            }
            
            # Rename columns to match warehouse schema
            for source_col, target_col in column_mapping.items():
                if source_col in df.columns:
                    df[target_col] = df[source_col]
            
            # Select only the columns we need
            required_columns = ['student_id', 'name', 'age', 'major']
            available_columns = [col for col in required_columns if col in df.columns]
            df = df[available_columns]
            
        elif dataset_name == 'weather':
            # Map weather API data columns
            column_mapping = {
                'city': 'city',
                'temperature': 'temperature',
                'humidity': 'humidity',
                'weather_condition': 'conditions'
            }
            
            # Rename columns to match warehouse schema
            for source_col, target_col in column_mapping.items():
                if source_col in df.columns:
                    df[target_col] = df[source_col]
            
            # Select only the columns we need
            required_columns = ['city', 'temperature', 'humidity', 'conditions']
            available_columns = [col for col in required_columns if col in df.columns]
            df = df[available_columns]
            
        elif dataset_name == 'news':
            # Map web scraped news data columns
            column_mapping = {
                'headline': 'headline',
                'source': 'source',
                'scraped_at': 'scraped_at'
            }
            
            # Rename columns to match warehouse schema
            for source_col, target_col in column_mapping.items():
                if source_col in df.columns:
                    df[target_col] = df[source_col]
            
            # Select only the columns we need
            required_columns = ['headline', 'source', 'scraped_at']
            available_columns = [col for col in required_columns if col in df.columns]
            df = df[available_columns]
            
        elif dataset_name == 'scores':
            # Map Excel scores data columns
            column_mapping = {
                'Student_ID': 'student_id',
                'student_id': 'student_id',
                'id': 'student_id',
                'First_Name': 'first_name',
                'first_name': 'first_name',
                'Last_Name': 'last_name',
                'last_name': 'last_name',
                'Score': 'score',
                'score': 'score',
                'Subject': 'subject',
                'subject': 'subject',
                'Course': 'subject',
                'course': 'subject'
            }
            
            # Rename columns to match warehouse schema
            for source_col, target_col in column_mapping.items():
                if source_col in df.columns:
                    df[target_col] = df[source_col]
            
            # Select only the columns we need
            required_columns = ['student_id', 'first_name', 'last_name', 'score', 'subject']
            available_columns = [col for col in required_columns if col in df.columns]
            df = df[available_columns]
        
        return df
    
    def store_data(self, dataset_name, data_df, run_id):
        """Store transformed data in the warehouse"""
        try:
            if data_df.empty:
                logger.warning(f"Empty dataset {dataset_name}, skipping storage")
                return 0
            
            # Map columns to warehouse schema
            mapped_df = self.map_columns(data_df, dataset_name)
            
            if mapped_df.empty:
                logger.warning(f"No valid columns found for {dataset_name}, skipping storage")
                return 0
            
            with sqlite3.connect(self.db_path) as conn:
                # Add loading timestamp
                mapped_df = mapped_df.copy()
                mapped_df['loaded_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Store data based on dataset type
                if dataset_name == 'students':
                    mapped_df.to_sql('students', conn, if_exists='append', index=False)
                elif dataset_name == 'weather':
                    mapped_df.to_sql('weather', conn, if_exists='append', index=False)
                elif dataset_name == 'news':
                    mapped_df.to_sql('news', conn, if_exists='append', index=False)
                elif dataset_name == 'scores':
                    mapped_df.to_sql('scores', conn, if_exists='append', index=False)
                else:
                    logger.warning(f"Unknown dataset type: {dataset_name}")
                    return 0
                
                records_stored = len(mapped_df)
                logger.info(f"Stored {records_stored} records for {dataset_name}")
                return records_stored
                
        except Exception as e:
            logger.error(f"Failed to store {dataset_name}: {e}")
            raise
    
    def get_data(self, table_name, limit=100):
        """Retrieve data from warehouse"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                query = f"SELECT * FROM {table_name} ORDER BY loaded_at DESC LIMIT {limit}"
                df = pd.read_sql(query, conn)
                return df
        except Exception as e:
            logger.error(f"Failed to retrieve data from {table_name}: {e}")
            return pd.DataFrame()
    
    def get_warehouse_summary(self):
        """Get summary statistics from warehouse"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                summary = {}
                tables = ['students', 'weather', 'news', 'scores']
                
                for table in tables:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    summary[table] = count
                
                # Get latest run info
                cursor.execute("""
                    SELECT run_id, start_time, end_time, status, records_processed 
                    FROM pipeline_runs 
                    ORDER BY start_time DESC 
                    LIMIT 1
                """)
                latest_run = cursor.fetchone()
                
                if latest_run:
                    summary['latest_run'] = {
                        'run_id': latest_run[0],
                        'start_time': latest_run[1],
                        'end_time': latest_run[2],
                        'status': latest_run[3],
                        'records_processed': latest_run[4]
                    }
                
                return summary
                
        except Exception as e:
            logger.error(f"Failed to get warehouse summary: {e}")
            return {}
    
    def log_pipeline_run(self, run_id, start_time, end_time, status, records_processed, error_message=None):
        """Log pipeline execution metadata"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO pipeline_runs (run_id, start_time, end_time, status, records_processed, error_message)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (run_id, start_time, end_time, status, records_processed, error_message))
                conn.commit()
                logger.info(f"Pipeline run logged: {run_id} - {status}")
        except Exception as e:
            logger.error(f"Failed to log pipeline run: {e}")
    
    def run_analytics(self):
        """Run basic analytics on warehouse data"""
        try:
            analytics = {}
            
            # Student analytics
            students_df = self.get_data('students')
            if not students_df.empty:
                # Only use columns that actually exist
                student_analytics = {
                    'total_count': len(students_df)
                }
                
                # Add available columns only
                if 'Score' in students_df.columns:
                    student_analytics['avg_score'] = float(students_df['Score'].mean())
                if 'Attendance_Percentage' in students_df.columns:
                    student_analytics['avg_attendance'] = float(students_df['Attendance_Percentage'].mean())
                if 'Hours_Studied' in students_df.columns:
                    student_analytics['avg_hours_studied'] = float(students_df['Hours_Studied'].mean())
                if 'Course' in students_df.columns:
                    student_analytics['courses'] = students_df['Course'].value_counts().to_dict()
                if 'Grade' in students_df.columns:
                    student_analytics['grade_distribution'] = students_df['Grade'].value_counts().to_dict()
                if 'County' in students_df.columns:
                    student_analytics['county_distribution'] = students_df['County'].value_counts().to_dict()
                
                analytics['students'] = student_analytics
            
            # Weather analytics
            weather_df = self.get_data('weather')
            if not weather_df.empty:
                weather_analytics = {
                    'total_records': len(weather_df)
                }
                
                if 'temperature' in weather_df.columns:
                    weather_analytics['avg_temperature'] = float(weather_df['temperature'].mean())
                if 'city' in weather_df.columns:
                    weather_analytics['cities'] = weather_df['city'].value_counts().to_dict()
                if 'humidity' in weather_df.columns:
                    weather_analytics['avg_humidity'] = float(weather_df['humidity'].mean())
                if 'pressure' in weather_df.columns:
                    weather_analytics['avg_pressure'] = float(weather_df['pressure'].mean())
                
                analytics['weather'] = weather_analytics
            
            # News analytics
            news_df = self.get_data('news')
            if not news_df.empty:
                news_analytics = {
                    'total_records': len(news_df)
                }
                
                if 'source' in news_df.columns:
                    news_analytics['sources'] = news_df['source'].value_counts().to_dict()
                if 'category' in news_df.columns:
                    news_analytics['categories'] = news_df['category'].value_counts().to_dict()
                
                analytics['news'] = news_analytics
            
            return analytics
            
        except Exception as e:
            logger.error(f"Failed to run analytics: {e}")
            return {}
    
    def clear_warehouse(self):
        """Clear all data from warehouse (for testing/reset)"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                tables = ['students', 'weather', 'news', 'scores', 'pipeline_runs']
                
                for table in tables:
                    cursor.execute(f"DELETE FROM {table}")
                
                conn.commit()
                logger.info("Warehouse cleared successfully")
                
        except Exception as e:
            logger.error(f"Failed to clear warehouse: {e}")
            raise
