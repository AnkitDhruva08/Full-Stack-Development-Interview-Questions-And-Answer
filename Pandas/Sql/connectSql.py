import pandas as pd
from sqlalchemy import create_engine

# Database credentials
DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "root"
DB_NAME = "employee_management"
DB_PORT = "5432"

# Create SQLAlchemy engine
engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Example query: fetch all rows from "patients" table
query = "SELECT * FROM core_user;"
df = pd.read_sql(query, engine)

print("\nData from PostgreSQL:")
print(df.head())

