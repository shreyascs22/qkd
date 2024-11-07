import psycopg2
import os

# Use the Supabase Database URL you copied from the dashboard
DATABASE_URL = "postgresql://postgres.uczrcjrxhmiwpkpolywj:Supabase%40123@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to the database successfully!")

    # Create a cursor object
    cursor = conn.cursor()

    # Example: Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            message TEXT
        );
    ''')
    print("Table created successfully (if it didn't exist already).")

    # Example: Insert data into the table
    cursor.execute('''
        INSERT INTO messages (username, message) VALUES (%s, %s);
    ''', ("Alice", "Hello from Supabase!"))
    print("Data inserted successfully.")
    
    # Commit changes
    conn.commit()

    # Example: Fetch and display data
    cursor.execute('SELECT * FROM messages;')
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Username: {row[1]}, Message: {row[2]}")

except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the connection
    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")
