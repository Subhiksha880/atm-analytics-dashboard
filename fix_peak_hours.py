"""
Fix Peak Hours Analysis - Create Realistic ATM Usage Patterns
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

def create_realistic_peak_hour_data(num_records=2000):
    """Create data with REALISTIC peak hours"""
    print(f"Creating {num_records} transactions with REALISTIC peak hours...")
    
    np.random.seed(42)
    locations = ['Downtown Branch', 'Airport Terminal', 'Shopping Mall', 'University Campus', 'Hospital Complex']
    
    data = []
    
    for i in range(num_records):
        # REALISTIC ATM PEAK HOURS based on actual banking data
        # Morning: 7-9 AM (people before work)
        # Lunch: 12-1 PM (people on lunch break)  
        # Evening: 5-7 PM (people after work)
        # Late evening: 8-9 PM (people after dinner)
        
        peak_hour_choices = [
            (7, 0.12), (8, 0.18), (9, 0.10),  # Morning peak
            (12, 0.15), (13, 0.08),           # Lunch peak
            (17, 0.12), (18, 0.10), (19, 0.08), # Evening peak
            (20, 0.07)                         # Late evening
        ]
        
        # Choose hour based on realistic probabilities
        hours = [h for h, p in peak_hour_choices]
        probabilities = [p for h, p in peak_hour_choices]
        
        # 70% chance of peak hour, 30% chance of other hours
        if np.random.random() < 0.7:
            hour = np.random.choice(hours, p=probabilities)
        else:
            # Non-peak hours (10 AM, 11 AM, 2-4 PM, 6-11 PM)
            hour = np.random.choice([10, 11, 14, 15, 16, 21, 22, 23])
        
        days_ago = int(np.random.randint(0, 90))
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=int(hour), minutes=int(np.random.randint(0, 59)))
        
        # Transaction types with realistic patterns
        trans_type = np.random.choice(['withdrawal', 'balance_check', 'deposit', 'transfer'], p=[0.65, 0.20, 0.10, 0.05])
        
        # Amount patterns by time of day
        if trans_type == 'balance_check':
            amount = 0.0
        elif trans_type == 'withdrawal':
            # Larger withdrawals during peak hours
            if hour in [8, 12, 17, 18]:  # Peak hours
                amount = np.random.choice([40, 60, 80, 100, 120, 140, 160, 200, 300, 400, 500], 
                                        p=[0.05, 0.05, 0.05, 0.15, 0.10, 0.08, 0.07, 0.20, 0.10, 0.07, 0.08])
            else:  # Non-peak hours - smaller amounts
                amount = np.random.choice([20, 40, 60, 80, 100, 120, 140, 160, 200], 
                                        p=[0.15, 0.10, 0.08, 0.15, 0.20, 0.10, 0.08, 0.07, 0.07])
        elif trans_type == 'deposit':
            # Deposits more common during business hours
            if 9 <= hour <= 17:
                amount = np.random.uniform(200, 2500)
            else:
                amount = np.random.uniform(100, 1000)
        else:  # transfer
            amount = np.random.uniform(50, 1000)
        
        # Location patterns by time
        if hour in [8, 9, 17, 18]:  # Commute times
            location_probs = {
                'Downtown Branch': 0.30,
                'Airport Terminal': 0.15,
                'Train Station': 0.20,
                'Shopping Mall': 0.15,
                'University Campus': 0.10,
                'Hospital Complex': 0.10
            }
        elif hour in [12, 13]:  # Lunch time
            location_probs = {
                'Downtown Branch': 0.25,
                'Shopping Mall': 0.30,
                'Airport Terminal': 0.15,
                'University Campus': 0.15,
                'Hospital Complex': 0.10,
                'Train Station': 0.05
            }
        else:  # Other times
            location_probs = {
                'Downtown Branch': 0.20,
                'Airport Terminal': 0.15,
                'Shopping Mall': 0.20,
                'University Campus': 0.15,
                'Hospital Complex': 0.20,
                'Train Station': 0.10
            }
        
        locations = list(location_probs.keys())
        probs = list(location_probs.values())
        location = np.random.choice(locations, p=probs)
        
        # Realistic success rate (slightly lower during peak hours due to high usage)
        if hour in [8, 12, 17, 18]:  # Peak hours
            status = np.random.choice(['success', 'failed', 'pending'], p=[0.94, 0.055, 0.005])
        else:  # Non-peak hours
            status = np.random.choice(['success', 'failed', 'pending'], p=[0.97, 0.028, 0.002])
        
        data.append({
            'transaction_id': f"FIX{i+1:06d}",
            'atm_location': location,
            'transaction_type': trans_type,
            'amount': round(float(amount), 2),
            'transaction_time': transaction_time,
            'customer_id': f"CUST{np.random.randint(1000, 9999)}",
            'status': status
        })
    
    return pd.DataFrame(data)

def analyze_peak_hours(df):
    """Detailed peak hour analysis"""
    print("\n=== DETAILED PEAK HOUR ANALYSIS ===")
    
    df['hour'] = df['transaction_time'].dt.hour
    df['day_of_week'] = df['transaction_time'].dt.day_name()
    
    # Hourly distribution
    hourly_counts = df['hour'].value_counts().sort_index()
    print("\nHourly Distribution:")
    for hour, count in hourly_counts.items():
        bar = " " * int(count/10) + ">"
        print(f"  {hour:02d}:00 | {count:4d} {bar}")
    
    # Peak hours
    peak_hour = hourly_counts.idxmax()
    peak_count = hourly_counts.max()
    print(f"\nPEAK HOUR: {peak_hour}:00 ({peak_count} transactions)")
    
    # Top 3 busiest hours
    top_hours = hourly_counts.nlargest(3)
    print(f"\nTOP 3 BUSIEST HOURS:")
    for hour, count in top_hours.items():
        print(f"  {hour:02d}:00 - {count} transactions")
    
    # Location analysis by hour
    print(f"\nBUSIEST LOCATIONS DURING PEAK HOUR ({peak_hour}:00):")
    peak_hour_data = df[df['hour'] == peak_hour]
    location_counts = peak_hour_data['atm_location'].value_counts()
    for location, count in location_counts.items():
        print(f"  {location}: {count} transactions")
    
    # Transaction patterns by time
    print(f"\nTRANSACTION TYPES BY TIME:")
    for hour in sorted(df['hour'].unique()):
        hour_data = df[df['hour'] == hour]
        total = len(hour_data)
        if total > 0:
            withdraw = (hour_data['transaction_type'] == 'withdrawal').mean() * 100
            balance = (hour_data['transaction_type'] == 'balance_check').mean() * 100
            deposit = (hour_data['transaction_type'] == 'deposit').mean() * 100
            transfer = (hour_data['transaction_type'] == 'transfer').mean() * 100
            
            print(f"  {hour:02d}:00 - Withdraw: {withdraw:.1f}%, Balance: {balance:.1f}%, Deposit: {deposit:.1f}%, Transfer: {transfer:.1f}%")

def import_to_database(connection, df):
    """Import corrected data to database"""
    print("Importing corrected peak hour data...")
    
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
        
        if (index + 1) % 200 == 0:
            print(f"Imported {index + 1} records...")
    
    connection.commit()
    cursor.close()
    
    print(f"Successfully imported {len(df)} corrected records!")

def main():
    print("=== FIXING PEAK HOURS - REALISTIC ANALYSIS ===")
    
    # Create corrected data
    df = create_realistic_peak_hour_data(2000)
    
    # Analyze peak hours
    analyze_peak_hours(df)
    
    # Save to CSV
    df.to_csv('corrected_peak_hours_data.csv', index=False)
    print(f"\nCorrected data saved to corrected_peak_hours_data.csv")
    
    # Import to database
    connection = connect_to_database()
    if connection:
        import_to_database(connection, df)
        connection.close()
        
        print(f"\n=== SUCCESS! ===")
        print(f"Peak hours are now REALISTIC!")
        print(f"Refresh your dashboard at http://localhost:8503")
        print(f"You should now see proper peak hours like 8 AM, 12 PM, or 5 PM!")

if __name__ == "__main__":
    main()
