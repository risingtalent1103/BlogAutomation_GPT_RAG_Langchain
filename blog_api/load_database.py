import pandas as pd
from sqlalchemy import create_engine
# Replace 'your_csv_file.csv' with the actual file name and 'your_table_name' with the desired table name in the database
csv_file = '../database/subscribers.csv'
table_name = 'subscribers'
# Create a DataFrame from the CSV file
df = pd.read_csv(csv_file)
# Replace 'your_username', 'your_password', 'your_host', and 'your_database' with your actual PostgreSQL credentials
engine = create_engine('postgresql://postgres:password@localhost:5432/test_db')
# Load the DataFrame into the PostgreSQL database
df.to_sql(table_name, engine, if_exists='replace', index=False)