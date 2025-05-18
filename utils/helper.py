import sqlite3

def get_column_info(db_file, table_name):
    """
    Retrieves the column ID, name, and data type of a specified table
    from an SQLite database and formats it as a list of dictionaries
    suitable for an LLM.

    Args:
        db_file (str): The path to the SQLite database file.
        table_name (str): The name of the table to inspect.

    Returns:
        list: A list of dictionaries, where each dictionary represents a column
              and has keys 'id', 'name', and 'type'.
              Returns None if the table is not found.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Fetch column information using PRAGMA table_info()
        cursor.execute(f"PRAGMA table_info('{table_name}')")
        schema_info = cursor.fetchall()

        conn.close()

        # Create a list of dictionaries with clear labels
        column_details = []
        for row in schema_info:
            column_details.append({
                'column_id': row[0],
                'name': row[1],
                'type': row[2]
            })
        return column_details

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
def get_table_sample(db_file, table_name):
    """
    Retrieves the first three rows from a specified table in an SQLite database.

    Args:
        db_file (str): The path to the SQLite database file.
        table_name (str): The name of the table to query.

    Returns:
        list: A list containing the first three rows of the table.
              Each row is a tuple of column values.
              Returns an empty list if the table is empty or not found.
    """
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Execute a SELECT query with a LIMIT clause
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
        first_three = cursor.fetchall()

        conn.close()
        return first_three
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []