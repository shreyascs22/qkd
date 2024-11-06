import psycopg2

connection = None
cursor = None
#Connecting to PostgreSQL
try:
    connection = psycopg2.connect(
        database="users",  
        user="postgres",      
        password="password",  
        host="localhost",     
        port="5432"        
    )
    print("Connected to the database!")

    cursor = connection.cursor()

    insert_query = """
    INSERT INTO user_credentials (username, password)
    VALUES (%s, %s);
    """
    user_data = ("alice", "password123") 
    cursor.execute(insert_query, user_data)

    #Commit transaction
    connection.commit()
    print("User inserted successfully!")

    # Retrieve all users to verify the insertion
    cursor.execute("SELECT * FROM user_credentials;")
    users = cursor.fetchall()
    print("Users in the database:")
    for user in users:
        print(user)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    print("Database connection closed.")
