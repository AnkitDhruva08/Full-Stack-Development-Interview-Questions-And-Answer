import psycopg2

DB_HOST = "localhost"
DB_USER = "postgres"
DB_PASS = "root"
DB_NAME = "practice"
DB_PORT = "5432"

# postgresql connection table 
connection = psycopg2.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASS,
    dbname=DB_NAME,
    port=DB_PORT
)


# cursor for create connection
cursor = connection.cursor()

create_table_query = """
CREATE TABLE IF NOT EXISTS employees (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(10),
    salary NUMERIC(10, 2),
    active BOOLEAN DEFAULT TRUE   
);
"""

cursor.execute(create_table_query)
connection.commit()

print("✅ Table 'employees' created with ACTIVE column (default TRUE)!")

cursor.close()
connection.close()
