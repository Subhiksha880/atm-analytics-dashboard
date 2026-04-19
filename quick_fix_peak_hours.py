"""
Quick Fix for Peak Hours - Create Realistic Data
"""

import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime, timedelta

def connect_to_database():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root123',
            database='atm_project'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_realistic_data():
    """Create realistic ATM data with proper peak hours"""
    print("Creating realistic ATM data with proper peak hours...")
    
    locations = ['Downtown Branch', 'Airport Terminal', 'Shopping Mall', 'University Campus', 'Hospital Complex']
    data = []
    
    # Create transactions with realistic peak hours
    for i in range(2500):
        # Realistic peak hours: 8 AM, 12 PM, 5 PM
        hour_choices = [8, 12, 17]  # Peak hours
        non_peak_hours = [0, 1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 13, 14, 15, 16, 18, 19, 20, 21, 22, 23]
        
        # 60% peak hours, 40% other hours
        if np.random.random() < 0.6:
            hour = np.random.choice(hour_choices)
        else:
            hour = np.random.choice(non_peak_hours)
        
        # Create realistic timestamp
        days_ago = int(np.random.randint(0, 60))
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=int(hour), minutes=int(np.random.randint(0, 59)))
        
        # Transaction type
        trans_type = np.random.choice(['withdrawal', 'balance_check', 'deposit', 'transfer'], p=[0.65, 0.20, 0.10, 0.05])
        
        # Amount
        if trans_type == 'balance_check':
            amount = 0.0
        elif trans_type == 'withdrawal':
            amount = np.random.uniform(20, 500)
        elif trans_type == 'deposit':
            amount = np.random.uniform(100, 2000)
        else:
            amount = np.random.uniform(50, 1000)
        
        # Location
        location = np.random.choice(locations)
        
        # Status
        status = np.random.choice(['success', 'failed', 'pending'], p=[0.96, 0.035, 0.005])
        
        data.append({
            'transaction_id': f"REAL{i+1:06d}",
            'atm_location': location,
            'transaction_type': trans_type,
            'amount': round(amount, 2),
            'transaction_time': transaction_time,
            'customer_id': f"CUST{np.random.randint(1000, 9999)}",
            'status': status
        })
    
    return pd.DataFrame(data)

def analyze_peak_hours(df):
    """Analyze and show peak hours"""
    print("\n" + "="*50)
    print("PEAK HOUR ANALYSIS")
    print("="*50)
    
    df['hour'] = df['transaction_time'].dt.hour
    hourly_counts = df['hour'].value_counts().sort_index()
    
    print("\nHOURLY DISTRIBUTION:")
    for hour in range(24):
        count = hourly_counts.get(hour, 0)
        bar = " " * int(count/15) + ">"
        
        if hour in [8, 12, 17]:
            marker = " <-- PEAK"
        else:
            marker = ""
        
        print(f"  {hour:02d}:00 | {count:3d} {bar}{marker}")
    
    peak_hour = hourly_counts.idxmax()
    peak_count = hourly_counts.max()
    
    print(f"\nPEAK HOUR: {peak_hour}:00 ({peak_count} transactions)")
    
    if peak_hour in [8, 12, 17]:
        print("PERFECT! Peak hour is realistic!")
    else:
        print("Peak hour should be 8 AM, 12 PM, or 5 PM")

def import_to_database(connection, df):
    """Import data to database"""
    print("Importing data...")
    
    cursor = connection.cursor()
    cursor.execute("TRUNCATE TABLE transactions")
    
    for index, row in df.iterrows():
        query = """
        INSERT INTO transactions 
        (transaction_id, atm_location, transaction_type, amount, transaction_time, customer_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            row['transaction_id'],
            row['atm_location'],
            row['transaction_type'],
            row['amount'],
            row['transaction_time'],
            row['customer_id'],
            row['status']
        )
        
        cursor.execute(query, values)
        
        if (index + 1) % 250 == 0:
            print(f"Imported {index + 1} records...")
    
    connection.commit()
    cursor.close()
    print(f"Successfully imported {len(df)} records!")

def main():
    print("="*50)
    print("QUICK FIX - REALISTIC PEAK HOURS")
    print("="*50)
    
    # Create data
    df = create_realistic_data()
    
    # Analyze
    analyze_peak_hours(df)
    
    # Save
    df.to_csv('realistic_peak_hours_fixed.csv', index=False)
    
    # Import
    connection = connect_to_database()
    if connection:
        import_to_database(connection, df)
        connection.close()
        
        print(f"\nSUCCESS!")
        print(f"Refresh dashboard: http://localhost:8503")
        print(f"You should see realistic peak hours now!")

if __name__ == "__main__":
    main()
