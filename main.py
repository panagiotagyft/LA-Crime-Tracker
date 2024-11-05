import time
import psycopg2
import random
from psycopg2 import OperationalError, sql

def create_connection():
    connection = None
    for _ in range(5):  # Retry up to 5 times
        try:
            connection = psycopg2.connect(
                user="myuser",
                password="example",
                host="0.0.0.0",         # Use service name as defined in docker-compose.yml
                port="5432",
                database="mydatabase"
            )
            print("Connection to PostgreSQL successful")
            break
        except OperationalError as e:
            print(f"The error '{e}' occurred")
            print("PostgreSQL not ready, retrying in 5 seconds...")
            time.sleep(5)
    return connection

def execute_query(connection, query, values=None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()

# Example usage
if __name__ == "__main__":
    connection = create_connection()
    if connection:
        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            nationality TEXT
        );
        """
        execute_query(connection, create_table_query)

        # Insert sample users with random ages
        users = [
            ("James", random.randint(18, 60)),
            ("Alice", random.randint(18, 60)),
            ("John", random.randint(18, 60)),
            ("Sophia", random.randint(18, 60))
        ]
        
        add_user_query = """
        INSERT INTO users (name, age)
        VALUES (%s, %s);
        """
        for user in users:
            execute_query(connection, add_user_query, user)

        connection.close()
