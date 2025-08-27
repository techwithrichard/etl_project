# city                       |
# | country                    |
# db:sakila ->tables: country, customer, city



from sqlalchemy import create_engine, text
import pandas as pd
import os


# Use environment variables for database connection
mysql_user = os.getenv("MYSQL_TEST_USER", "root")
mysql_password = os.getenv("MYSQL_TEST_PASSWORD", "root")
mysql_host = os.getenv("MYSQL_TEST_HOST", "localhost")
mysql_database = os.getenv("MYSQL_TEST_DATABASE", "sakila")

connection_string = f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}"
engine = create_engine(connection_string)
    
my_customer = text("SELECT * FROM customer")
# my_country = text("SELECT * FROM country")

with engine.connect() as connection:
    df = pd.read_sql(my_customer, connection)
    print(df)
    
    print("Successfully extracted customers from sakila")

