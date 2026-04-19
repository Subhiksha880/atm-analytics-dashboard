"""
========================================
ATM Transaction Pattern Analysis Project
Database Connection and Data Loading Script
========================================
"""

import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change this to your MySQL username
    'password': 'root123',  # Change this to your MySQL password
    'database': 'atm_project'
}

def connect_to_database():
    """
    Connect to MySQL database
    Returns: connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            print("✅ Successfully connected to MySQL database!")
            return connection
    except mysql.connector.Error as e:
        print(f"❌ Error connecting to database: {e}")
        return None

def load_data_to_dataframe(connection):
    """
    Load transaction data from MySQL to Pandas DataFrame
    Returns: DataFrame with transaction data
    """
    try:
        query = "SELECT * FROM transactions"
        df = pd.read_sql(query, connection)
        
        # Convert transaction_time to datetime
        df['transaction_time'] = pd.to_datetime(df['transaction_time'])
        
        # Extract hour from transaction_time for peak time analysis
        df['hour'] = df['transaction_time'].dt.hour
        
        print(f"✅ Successfully loaded {len(df)} records into DataFrame!")
        return df
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def analyze_transactions(df):
    """
    Perform basic analysis on transaction data
    Returns: dictionary with analysis results
    """
    if df is None:
        return None
    
    analysis = {}
    
    # Total transactions
    analysis['total_transactions'] = len(df)
    
    # Total amount transacted
    analysis['total_amount'] = df['amount'].sum()
    
    # Transactions by location
    analysis['transactions_by_location'] = df['atm_location'].value_counts().to_dict()
    
    # Amount by location
    analysis['amount_by_location'] = df.groupby('atm_location')['amount'].sum().to_dict()
    
    # Peak usage hour
    hourly_transactions = df['hour'].value_counts().sort_index()
    analysis['peak_hour'] = hourly_transactions.idxmax()
    analysis['peak_hour_transactions'] = hourly_transactions.max()
    analysis['hourly_distribution'] = hourly_transactions.to_dict()
    
    # Transaction types
    analysis['transaction_types'] = df['transaction_type'].value_counts().to_dict()
    
    # Success rate
    analysis['success_rate'] = (df['status'] == 'success').mean() * 100
    
    return analysis

def main():
    """
    Main function to test database connection and analysis
    """
    print("🏦 ATM Transaction Pattern Analysis - Database Connection Test")
    print("=" * 60)
    
    # Connect to database
    connection = connect_to_database()
    if connection is None:
        return
    
    # Load data
    df = load_data_to_dataframe(connection)
    if df is None:
        connection.close()
        return
    
    # Perform analysis
    analysis = analyze_transactions(df)
    if analysis is None:
        connection.close()
        return
    
    # Display results
    print("\n📊 Analysis Results:")
    print(f"Total Transactions: {analysis['total_transactions']:,}")
    print(f"Total Amount: ${analysis['total_amount']:,.2f}")
    print(f"Peak Hour: {analysis['peak_hour']}:00 ({analysis['peak_hour_transactions']} transactions)")
    print(f"Success Rate: {analysis['success_rate']:.1f}%")
    
    print("\n📍 Transactions by Location:")
    for location, count in analysis['transactions_by_location'].items():
        print(f"  {location}: {count} transactions")
    
    print("\n💰 Amount by Location:")
    for location, amount in analysis['amount_by_location'].items():
        print(f"  {location}: ${amount:,.2f}")
    
    # Close connection
    connection.close()
    print("\n✅ Database connection closed successfully!")

if __name__ == "__main__":
    main()
