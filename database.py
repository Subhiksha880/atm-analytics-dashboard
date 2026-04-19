"""
========================================
Database Connection Module
ATM Transaction Pattern Analysis Project
========================================
"""

import mysql.connector
from mysql.connector import Error
import pandas as pd
import logging

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'atm_project'
}

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_atm_transactions_table():
    """Create ATM transactions table if it doesn't exist"""
    connection = None
    cursor = None
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()
        
        # Create table if not exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            transaction_id VARCHAR(50) UNIQUE,
            atm_location VARCHAR(100) NOT NULL,
            transaction_type ENUM('withdrawal','balance_check','deposit','transfer') NOT NULL,
            amount DECIMAL(10,2) NOT NULL,
            transaction_time DATETIME NOT NULL,
            customer_id VARCHAR(50),
            status ENUM('success','failed','pending') NOT NULL
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        logging.info("ATM transactions table created or verified")
        
        return True
        
    except Error as e:
        logging.error(f"Error creating table: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def connect_to_database():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logging.info("Successfully connected to MySQL database")
            return connection
        else:
            logging.error("Failed to connect to database")
            return None
            
    except Error as e:
        logging.error(f"Database connection error: {e}")
        return None

def load_atm_data():
    """Load ATM transaction data from database"""
    connection = connect_to_database()
    if connection is None:
        return None
    
    try:
        query = "SELECT transaction_id, atm_location as location, transaction_type, amount, transaction_time, status FROM transactions ORDER BY transaction_time DESC"
        df = pd.read_sql(query, connection)
        
        # Convert transaction_time to datetime
        df['transaction_time'] = pd.to_datetime(df['transaction_time'])
        
        # Extract time components for analysis
        df['hour'] = df['transaction_time'].dt.hour
        df['date'] = df['transaction_time'].dt.date
        df['day_of_week'] = df['transaction_time'].dt.day_name()
        
        logging.info(f"Loaded {len(df)} records from database")
        return df
        
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None
        
    finally:
        if connection.is_connected():
            connection.close()

def save_atm_data(df):
    """Save ATM transaction data to database"""
    connection = connect_to_database()
    if connection is None:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Insert data row by row
        for _, row in df.iterrows():
            insert_query = """
            INSERT INTO transactions (transaction_id, atm_location, transaction_type, amount, transaction_time, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            atm_location = VALUES(atm_location),
            transaction_type = VALUES(transaction_type),
            amount = VALUES(amount),
            transaction_time = VALUES(transaction_time),
            status = VALUES(status)
            """
            
            cursor.execute(insert_query, (
                row['transaction_id'],
                row['location'],
                row['transaction_type'],
                row['amount'],
                row['transaction_time'],
                row['status']
            ))
        
        connection.commit()
        logging.info(f"Saved {len(df)} records to database")
        return True
        
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

def check_database_connection():
    """Check if database connection is working"""
    connection = connect_to_database()
    if connection:
        connection.close()
        return True
    return False

if __name__ == "__main__":
    # Test database connection
    if check_database_connection():
        print("Database connection is working properly")
    else:
        print("Database connection failed")
