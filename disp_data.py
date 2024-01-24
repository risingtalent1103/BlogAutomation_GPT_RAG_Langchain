import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(database="test_db", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

# Execute a SELECT query to fetch all data from a specific table
cur.execute("SELECT * FROM users")
data = cur.fetchall()

# Print the fetched data
for row in data:
    print(row)

# Close the cursor and the connection
cur.close()
conn.close()