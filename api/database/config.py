import sqlite3

# Path to the schema file
SCHEMA_FILE = "./api/database/schema.sql"

# Path to the SQLite database file (it will be created if it doesn't exist)
DATABASE_PATH = "./api/database/database.db"


def execute(query, params=(), fetchall=False):
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # Enables row access by column name
    cursor = conn.cursor()

    if not fetchall:
        data = cursor.execute(query, params).fetchone()
    else:
        data = cursor.execute(query, params).fetchall()

    conn.commit()
    conn.close()

    return data


def connect():
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        print("Connected to the database successfully!")

        # Read the schema.sql file
        with open(SCHEMA_FILE, "r") as file:
            schema_sql = file.read()
            # Execute the schema SQL script
            cursor.executescript(schema_sql)
            print("Schema executed successfully!")

            # Commit changes and close the connection
            conn.commit()
            conn.close()
            print("Database connection closed.")
    except Exception as e:
        print(f"An error occurred: {e}")
