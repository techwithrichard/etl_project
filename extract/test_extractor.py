# city                       |
# | country                    |
# db:sakila ->tables: country, customer, city



from sqlalchemy import create_engine, text
import pandas as pd


engine = create_engine("mysql+mysqlconnector://root:root@localhost/sakila")
    
my_customer = text("SELECT * FROM customer")
# my_country = text("SELECT * FROM country")

with engine.connect() as connection:
    df = pd.read_sql(my_customer, connection)
    print(df)
    
    print("Successfully extracted customers from sakila")

