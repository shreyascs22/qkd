import psycopg2

# Use the Supabase Database URL
DATABASE_URL = "postgresql://postgres.uczrcjrxhmiwpkpolywj:Supabase%40123@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(DATABASE_URL)
    print("Connected to the database successfully!")

    # Create a cursor object
    cursor = conn.cursor()

    # Drop the existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS messages;')
    print("Old table dropped (if it existed).")

    # Create the new table with id, username, and password
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        );
    ''')
    print("New table created successfully with fields: id, username, and password.")

    # Example: Insert data into the new table
    cursor.execute('''
        INSERT INTO messages (username, password) VALUES (%s, %s);
    ''', ("Alice", "alice_123"))
    cursor.execute('''
        INSERT INTO messages (username, password) VALUES (%s, %s);
    ''', ("Bob", "bob_456"))
    print("Data inserted successfully.")

    # Commit changes
    conn.commit()

    # Fetch and display data
    cursor.execute('SELECT * FROM messages;')
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Username: {row[1]}, Password: {row[2]}")

except Exception as e:
    print("An error occurred:", e)
finally:
    # Close the connection
    if conn:
        cursor.close()
        conn.close()
        print("Database connection closed.")
