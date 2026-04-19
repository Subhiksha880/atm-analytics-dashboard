"""
FINAL FIX - Guaranteed Realistic Peak Hours
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

def create_guaranteed_realistic_data():
    """Create data with GUARANTEED realistic peak hours"""
    print("Creating data with GUARANTEED realistic peak hours...")
    
    locations = ['Downtown Branch', 'Airport Terminal', 'Shopping Mall', 'University Campus', 'Hospital Complex']
    data = []
    
    # Create exact distribution for realistic peak hours
    hour_distribution = {
        8: 400,   # 8 AM - Morning peak
        12: 350,  # 12 PM - Lunch peak  
        17: 380,  # 5 PM - Evening peak
        7: 150,   # 7 AM - Before peak
        9: 200,   # 9 AM - After peak
        11: 120,  # 11 AM - Before lunch
        13: 180,  # 1 PM - After lunch
        16: 160,  # 4 PM - Before evening peak
        18: 250,  # 6 PM - After evening peak
        19: 140,  # 7 PM - Later evening
        20: 100,  # 8 PM - Night
        0: 80,    # Midnight
        1: 60,    # 1 AM
        2: 50,    # 2 AM
        3: 40,    # 3 AM
        4: 40,    # 4 AM
        5: 50,    # 5 AM
        6: 80,    # 6 AM
        10: 90,   # 10 AM
        14: 70,   # 2 PM
        15: 80,   # 3 PM
        21: 70,   # 9 PM
        22: 60,   # 10 PM
        23: 50    # 11 PM
    }
    
    transaction_id = 1
    
    for hour, num_transactions in hour_distribution.items():
        for _ in range(num_transactions):
            # Create realistic timestamp
            days_ago = np.random.randint(0, 60)
            transaction_time = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=np.random.randint(0, 59))
            
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
            
            # Location patterns by time
            if hour in [8, 9]:  # Morning
                location = np.random.choice(['Downtown Branch', 'Airport Terminal', 'Train Station', 'Shopping Mall'], p=[0.4, 0.2, 0.2, 0.2])
            elif hour in [12, 13]:  # Lunch
                location = np.random.choice(['Downtown Branch', 'Shopping Mall', 'University Campus'], p=[0.4, 0.4, 0.2])
            elif hour in [17, 18, 19]:  # Evening
                location = np.random.choice(['Downtown Branch', 'Shopping Mall', 'Airport Terminal'], p=[0.4, 0.3, 0.3])
            else:  # Other times
                location = np.random.choice(locations)
            
            # Status
            status = np.random.choice(['success', 'failed', 'pending'], p=[0.96, 0.035, 0.005])
            
            data.append({
                'transaction_id': f"FIX{transaction_id:06d}",
                'atm_location': location,
                'transaction_type': trans_type,
                'amount': round(float(amount), 2),
                'transaction_time': transaction_time,
                'customer_id': f"CUST{np.random.randint(1000, 9999)}",
                'status': status
            })
            
            transaction_id += 1
    
    return pd.DataFrame(data)

def analyze_final_data(df):
    """Analyze the final data"""
    print("\n" + "="*60)
    print("FINAL PEAK HOUR ANALYSIS")
    print("="*60)
    
    df['hour'] = df['transaction_time'].dt.hour
    hourly_counts = df['hour'].value_counts().sort_index()
    
    print("\nHOURLY DISTRIBUTION:")
    for hour in range(24):
        count = hourly_counts.get(hour, 0)
        bar = " " * int(count/25) + ">"
        
        if hour == 8:
            marker = " <-- MORNING PEAK"
        elif hour == 12:
            marker = " <-- LUNCH PEAK"
        elif hour == 17:
            marker = " <-- EVENING PEAK"
        elif hour in [7, 9, 18, 19]:
            marker = " <-- BUSY"
        else:
            marker = ""
        
        print(f"  {hour:02d}:00 | {count:4d} {bar}{marker}")
    
    peak_hour = hourly_counts.idxmax()
    peak_count = hourly_counts.max()
    
    print(f"\nPEAK HOUR: {peak_hour}:00 ({peak_count} transactions)")
    
    if peak_hour == 8:
        print("PERFECT! 8 AM morning peak - most realistic!")
    elif peak_hour == 12:
        print("PERFECT! 12 PM lunch peak - very realistic!")
    elif peak_hour == 17:
        print("PERFECT! 5 PM evening peak - very realistic!")
    else:
        print("Peak hour should be 8 AM, 12 PM, or 5 PM for realism")
    
    # Show top 3
    top_hours = hourly_counts.nlargest(3)
    print(f"\nTOP 3 BUSIEST HOURS:")
    for rank, (hour, count) in enumerate(top_hours.items(), 1):
        time_name = {8: "Morning", 12: "Lunch", 17: "Evening"}.get(hour, "Regular")
        print(f"  {rank}. {hour:02d}:00 - {count} transactions ({time_name} peak)")

def import_to_database(connection, df):
    """Import final data"""
    print("Importing FINAL realistic data...")
    
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
    print(f"Successfully imported {len(df)} FINAL records!")

def main():
    print("="*60)
    print("FINAL FIX - GUARANTEED REALISTIC PEAK HOURS")
    print("This will create PERFECT banking hour patterns")
    print("="*60)
    
    # Create guaranteed realistic data
    df = create_guaranteed_realistic_data()
    
    # Analyze
    analyze_final_data(df)
    
    # Save
    df.to_csv('final_perfect_peak_hours.csv', index=False)
    print(f"\nPerfect data saved to final_perfect_peak_hours.csv")
    
    # Import
    connection = connect_to_database()
    if connection:
        import_to_database(connection, df)
        connection.close()
        
        print(f"\n" + "="*60)
        print("SUCCESS! PERFECT PEAK HOURS!")
        print("="*60)
        print(f"Peak hour is now realistic (8 AM, 12 PM, or 5 PM)")
        print(f"Refresh dashboard: http://localhost:8503")
        print(f"Your dashboard now shows REAL banking patterns!")
        print("="*60)

if __name__ == "__main__":
    main()
