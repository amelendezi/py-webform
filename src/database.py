import psycopg2

def saveDataToDatabase(data):
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="webformdb",
            user="postgres",
            password="admin",
            host="localhost"
        )
        
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Create table if not exists
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS wform.registration (
                name VARCHAR(30),
                lastname VARCHAR(30),
                dob DATE,
                age_years INT,
                age_days INT
            )
            """
        )

        # Execute a query
        cur.execute(
            """
            INSERT INTO wform.registration (name, lastname, dob, age_years, age_days)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['name'], data['lastname'], data['dob'], data['age_years'], data['age_days'])
        )

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        print("Unable to access database", e)