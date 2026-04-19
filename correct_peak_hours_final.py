"""
FINAL FIX - Create REALISTIC Banking Peak Hours
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

def create_realistic_banking_hours(num_records=3000):
    """Create data with REAL banking peak hours"""
    print(f"Creating {num_records} transactions with REAL BANKING HOURS...")
    
    np.random.seed(42)
    locations = ['Downtown Branch', 'Airport Terminal', 'Shopping Mall', 'University Campus', 'Hospital Complex']
    
    data = []
    
    for i in range(num_records):
        # REAL BANKING HOURS - Based on actual ATM usage studies
        # Peak 1: 7-9 AM (Before work)
        # Peak 2: 12-1 PM (Lunch break)
        # Peak 3: 5-7 PM (After work)
        # Moderate: 8-10 PM (Evening)
        
        # Define realistic hour distribution
        hour_distribution = {
            0: 0.02, 1: 0.01, 2: 0.01, 3: 0.01, 4: 0.01, 5: 0.01, 6: 0.02,  # Night/Early morning
            7: 0.15, 8: 0.18, 9: 0.12,  # Morning peak
            10: 0.05, 11: 0.04,          # Late morning
            12: 0.15, 13: 0.08,          # Lunch peak
            14: 0.03, 15: 0.04, 16: 0.05, # Afternoon
            17: 0.12, 18: 0.10, 19: 0.08, # Evening peak
            20: 0.06, 21: 0.04, 22: 0.04, 23: 0.02  # Night
        }
        
        hours = list(hour_distribution.keys())
        probabilities = list(hour_distribution.values())
        
        # Choose hour based on realistic banking patterns
        hour = np.random.choice(hours, p=probabilities)
        
        days_ago = int(np.random.randint(0, 90))
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=int(hour), minutes=int(np.random.randint(0, 59)))
        
        # Transaction types
        trans_type = np.random.choice(['withdrawal', 'balance_check', 'deposit', 'transfer'], p=[0.65, 0.20, 0.10, 0.05])
        
        # Amount patterns
        if trans_type == 'balance_check':
            amount = 0.0
        elif trans_type == 'withdrawal':
            # Realistic withdrawal amounts
            amount = np.random.choice([20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 300, 400, 500], 
                                    p=[0.08, 0.05, 0.04, 0.04, 0.15, 0.06, 0.04, 0.04, 0.04, 0.20, 0.10, 0.06, 0.10])
        elif trans_type == 'deposit':
            amount = np.random.uniform(100, 2000)
        else:
            amount = np.random.uniform(50, 1000)
        
        # Location patterns by time
        if hour in [7, 8, 9]:  # Morning commute
            location = np.random.choice(['Downtown Branch', 'Airport Terminal', 'Train Station'], p=[0.5, 0.3, 0.2])
        elif hour in [12, 13]:  # Lunch time
            location = np.random.choice(['Downtown Branch', 'Shopping Mall', 'University Campus'], p=[0.4, 0.4, 0.2])
        elif hour in [17, 18, 19]:  # Evening commute
            location = np.random.choice(['Downtown Branch', 'Shopping Mall', 'Airport Terminal'], p=[0.4, 0.3, 0.3])
        else:  # Other times
            location = np.random.choice(locations)
        
        # Success rate
        status = np.random.choice(['success', 'failed', 'pending'], p=[0.96, 0.035, 0.005])
        
        data.append({
            'transaction_id': f"FINAL{i+1:06d}",
            'atm_location': location,
            'transaction_type': trans_type,
            'amount': round(float(amount), 2),
            'transaction_time': transaction_time,
            'customer_id': f"CUST{np.random.randint(1000, 9999)}",
            'status': status
        })
    
    return pd.DataFrame(data)

def analyze_and_show_peak_hours(df):
    """Show detailed peak hour analysis"""
    print("\n" + "="*60)
    print("REALISTIC PEAK HOUR ANALYSIS")
    print("="*60)
    
    df['hour'] = df['transaction_time'].dt.hour
    
    # Hourly distribution with visual bars
    hourly_counts = df['hour'].value_counts().sort_index()
    print("\nHOURLY TRANSACTION DISTRIBUTION:")
    print("-" * 40)
    
    for hour in range(24):
        count = hourly_counts.get(hour, 0)
        bar_length = int(count / 20)  # Scale bar
        bar = " " * bar_length + ">"
        
        # Mark peak hours
        marker = ""
        if hour in [8, 12, 17]:
            marker = " <-- PEAK HOUR"
        elif hour in [7, 9, 18, 19]:
            marker = " <-- BUSY"
        
        print(f"  {hour:02d}:00 | {count:4d} transactions {bar}{marker}")
    
    # Find peak hour
    peak_hour = hourly_counts.idxmax()
    peak_count = hourly_counts.max()
    
    print(f"\n" + "="*40)
    print(f"PEAK HOUR: {peak_hour}:00 ({peak_count} transactions)")
    print(f"This is realistic for ATM usage!")
    print("="*40)
    
    # Top 5 busiest hours
    top_hours = hourly_counts.nlargest(5)
    print(f"\nTOP 5 BUSIEST HOURS:")
    for rank, (hour, count) in enumerate(top_hours.items(), 1):
        print(f"  {rank}. {hour:02d}:00 - {count} transactions")
    
    # Busiest locations during peak hour
    peak_hour_data = df[df['hour'] == peak_hour]
    location_counts = peak_hour_data['atm_location'].value_counts()
    print(f"\nBUSIEST LOCATIONS DURING PEAK HOUR ({peak_hour}:00):")
    for location, count in location_counts.items():
        percentage = (count / len(peak_hour_data)) * 100
        print(f"  {location}: {count} ({percentage:.1f}%)")
    
    # Transaction patterns
    print(f"\nTRANSACTION PATTERNS AT PEAK HOUR ({peak_hour}:00):")
    peak_types = peak_hour_data['transaction_type'].value_counts()
    for trans_type, count in peak_types.items():
        percentage = (count / len(peak_hour_data)) * 100
        print(f"  {trans_type}: {count} ({percentage:.1f}%)")
    
    return peak_hour

def import_to_database(connection, df):
    """Import final corrected data"""
    print("Importing FINAL corrected data...")
    
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
        
        if (index + 1) % 300 == 0:
            print(f"Imported {index + 1} records...")
    
    connection.commit()
    cursor.close()
    
    print(f"Successfully imported {len(df)} FINAL corrected records!")

def main():
    print("="*60)
    print("FINAL PEAK HOURS CORRECTION")
    print("Creating REALISTIC banking hour patterns")
    print("="*60)
    
    # Create realistic data
    df = create_realistic_banking_hours(3000)
    
    # Analyze peak hours
    peak_hour = analyze_and_show_peak_hours(df)
    
    # Save to CSV
    df.to_csv('final_realistic_peak_hours.csv', index=False)
    print(f"\nFinal realistic data saved to final_realistic_peak_hours.csv")
    
    # Import to database
    connection = connect_to_database()
    if connection:
        import_to_database(connection, df)
        connection.close()
        
        print(f"\n" + "="*60)
        print("SUCCESS! PEAK HOURS ARE NOW REALISTIC!")
        print("="*60)
        print(f"Peak hour is now {peak_hour}:00 (realistic banking hour)")
        print(f"Refresh dashboard: http://localhost:8503")
        print(f"You should see proper peak hours like 8 AM, 12 PM, or 5 PM!")
        print("="*60)

if __name__ == "__main__":
    main()
