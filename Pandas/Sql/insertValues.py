import psycopg2
from sqlalchemy import create_engine
import pandas as pd


DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "root"
DB_NAME = "practice"
DB_PORT = "5432"

# postgresql connection table 
# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

query = "SELECT * FROM employees;"
# read values by usuing pandas 
df = pd.read_sql(query, engine)


print(df.head())

