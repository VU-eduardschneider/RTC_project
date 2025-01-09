import sqlite3
import pandas as pd
import os

def create_database_from_csv(csv_file, db_name='sensor_data.db', table_name='sensor_readings'):
    """
    Creates an SQLite database from a CSV file
    
    Args:
        csv_file (str): Path to the CSV file
        db_name (str): Name of the database to create
        table_name (str): Name of the table to create
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, delimiter=';')
        
        # Clean column names (remove spaces and special characters)
        df.columns = [col.strip().replace(' ', '_').replace('?', '').replace('(', '').replace(')', '').replace('.', '_') 
                     for col in df.columns]
        
        # Create a database connection
        conn = sqlite3.connect(db_name)
        
        # Write the data to SQLite
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def sqlite_connect(db_config):
    """
    Connects to SQLite database and returns the most recent row of data
    
    Args:
        db_config (list): List containing [database_name, table_name]
    
    Returns:
        dict: Dictionary containing the most recent row of data
    """
    try:
        db_name, table_name = db_config
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Get the column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Get the most recent row (assuming there's a timestamp or ID column)
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY ROWID DESC LIMIT 1")
        row = cursor.fetchone()
        
        # Create a dictionary of column names and values
        data = {columns[i]: row[i] for i in range(len(columns))}
        
        conn.close()
        return data
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def get_all_data(db_name, table_name):
    """
    Retrieves all data from the specified table
    
    Args:
        db_name (str): Name of the database
        table_name (str): Name of the table
    
    Returns:
        pd.DataFrame: DataFrame containing all data
    """
    try:
        conn = sqlite3.connect(db_name)
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error retrieving data: {e}")
        return None
