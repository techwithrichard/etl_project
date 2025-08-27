

from sqlalchemy import create_engine, text
import pandas as pd

def extract_from_mysql():
    """
    Extract student data from MySQL database using SQLAlchemy and return df student
    """
    try:
        # ,ysql engine
        engine = create_engine("mysql+mysqlconnector://root:1234@localhost/etl")
        
        # Query to get student data
        query = text("SELECT * FROM Students")
        with engine.connect() as connection:
            df = pd.read_sql(query, connection)
        
        print("Successfully extracted data from MySQL with SQLAlchemy")
        return df

    except Exception as e:
        print(f"Could not connect to MySQL: {e}")
        print("Returning sample student data instead...")

        # Return sample data if database doesn't exist
        return pd.DataFrame({
            'student_id': [1, 2, 3, 4, 5],
            'name': ['Michael', 'Sandra', 'Mike', 'Prudence', 'Daniel'],
            'age': [29, 31, 49, 30, 22],
            'major': ['Computer Science', 'Data Science', 'English Literature', 'Petrolium Englineering', 'Dancing and Arts']
        })