import psycopg2
import sys
from config import psqldb


def createPsqlDb():
    try:
        # Establish the connection using a with statement
        with psycopg2.connect(
            host=psqldb.DB_HOST,
            dbname=psqldb.DB_NAME,
            user=psqldb.DB_USER,
            password=psqldb.DB_PORT,
            port=psqldb.DB_PORT
            
        ) as conn:
            print("Connection successful!")

            # Open a cursor to perform database operations
            with conn.cursor() as cur:
                # Execute a sample query
                cur.execute("SELECT version();")

                # Retrieve query results
                db_version = cur.fetchone()
                print(f"PostgreSQL database version: {db_version}")
                
        return conn

    except psycopg2.OperationalError as e:
        print(f"Connection failed: {e}")
        sys.exit(1)

    print("Database connection closed.")
