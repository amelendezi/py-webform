import psycopg2
import json

def saveDataToDatabase(data, definition):
    try:
        # Load connection details from JSON file
        with open('./config/db_config.json', 'r') as f:
            db_config = json.load(f)
            
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname=db_config["dbname"],
            user=db_config["user"],
            password=db_config["password"],
            host=db_config["host"]
        )
        
        # Get the schema
        schema = db_config["schema"]
        
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Create table if not exists
        table_name = definition['componentName']        
        attributes = definition['attributes']
        
        columns = []    
        
        def handle_text(attr, details):
            maxLength = next((validator['maxLength'] for validator in details.get('validators', []) if validator['name'] == 'maxLengthValidator'), None)
            isMandatory = next((validator['value'] for validator in details.get('validators', []) if validator['name'] == 'requiredValidator'), False)
            return f"{attr} VARCHAR({maxLength}) {'NOT NULL' if isMandatory else ''}"

        def handle_date(attr, details):
            isMandatory = next((validator['value'] for validator in details.get('validators', []) if validator['name'] == 'requiredValidator'), False)
            return f"{attr} DATE {'NOT NULL' if isMandatory else ''}"

        def handle_number(attr, details):
            isMandatory = next((validator['value'] for validator in details.get('validators', []) if validator['name'] == 'requiredValidator'), False)
            return f"{attr} INT {'NOT NULL' if isMandatory else ''}"

        type_handlers = {
            'text': handle_text,
            'date': handle_date,
            'number': handle_number,
        }

        for attr, details in attributes.items():
            handler = type_handlers.get(details['type'])
            if handler:
                columns.append(handler(attr, details))

        columns_str = ', '.join(columns)
        create_table_query = f"CREATE TABLE IF NOT EXISTS {schema}.{table_name} ({columns_str})"
        cur.execute(create_table_query)

        # Insert data into table
        columns = ', '.join(data.keys())
        values = ', '.join(f"'{value}'" for value in data.values())
        insert_query = f"INSERT INTO {schema}.{table_name} ({columns}) VALUES ({values})"
        cur.execute(insert_query)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cur.close()
        conn.close()

    except Exception as e:
        print(e)