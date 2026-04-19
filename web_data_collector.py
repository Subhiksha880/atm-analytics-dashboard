"""
========================================
ATM Transaction Pattern Analysis Project
Web Data Collection Script
========================================
"""

import requests
import pandas as pd
import mysql.connector
from datetime import datetime, timedelta
import random
import json
import time

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'atm_project'
}

def connect_to_database():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def generate_realistic_atm_data(num_records=500):
    """Generate realistic ATM transaction data similar to real banking patterns"""
    
    print(f"Generating {num_records} realistic ATM transactions...")
    
    # Realistic parameters based on banking industry data
    locations = [
        'Downtown Branch', 'Airport Terminal', 'Shopping Mall North', 'Shopping Mall South',
        'University Campus Main', 'University Campus Science', 'Hospital Complex',
        'Train Station Central', 'Business District', 'Residential Area East',
        'Residential Area West', 'Tourist Center', 'Industrial Zone', 'Sports Stadium'
    ]
    
    # Peak hours based on real ATM usage patterns
    peak_hours = [8, 9, 12, 13, 17, 18, 19, 20]  # Morning, lunch, evening peaks
    
    data = []
    
    for i in range(num_records):
        # Generate realistic timestamp
        days_ago = random.randint(0, 30)
        
        # Higher probability for peak hours
        if random.random() < 0.6:  # 60% chance of peak hour
            hour = random.choice(peak_hours)
        else:
            hour = random.randint(0, 23)
        
        minute = random.randint(0, 59)
        
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=minute)
        
        # Transaction type distribution (realistic)
        transaction_type = random.choices(
            ['withdrawal', 'balance_check', 'deposit', 'transfer'],
            weights=[0.65, 0.20, 0.10, 0.05]
        )[0]
        
        # Amount distribution based on transaction type and location
        if transaction_type == 'balance_check':
            amount = 0.0
        elif transaction_type == 'withdrawal':
            # Realistic withdrawal amounts (most people withdraw $20-$500)
            amount = round(random.choices(
                [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 300, 400, 500],
                weights=[5, 3, 2, 2, 8, 3, 2, 2, 2, 15, 8, 5, 3]
            )[0] * random.uniform(0.9, 1.1), 2)
        elif transaction_type == 'deposit':
            # Deposit amounts are typically larger
            amount = round(random.uniform(100, 2000), 2)
        else:  # transfer
            amount = round(random.uniform(50, 1000), 2)
        
        # Location selection with realistic probabilities
        location = random.choices(
            locations,
            weights=[15, 8, 10, 8, 5, 3, 7, 6, 12, 8, 6, 5, 4, 3]  # Downtown busiest
        )[0]
        
        # Customer ID (simulate regular customers)
        customer_id = f"CUST{random.randint(1000, 9999)}"
        
        # Status (high success rate for ATMs)
        status = random.choices(
            ['success', 'failed', 'pending'],
            weights=[96, 3.5, 0.5]  # 96% success rate
        )[0]
        
        # Transaction ID
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d')}{str(i+1).zfill(4)}"
        
        data.append({
            'transaction_id': transaction_id,
            'atm_location': location,
            'transaction_type': transaction_type,
            'amount': amount,
            'transaction_time': transaction_time,
            'customer_id': customer_id,
            'status': status
        })
    
    return pd.DataFrame(data)

def fetch_public_financial_data():
    """Fetch public financial data that can be adapted for ATM analysis"""
    
    print("Fetching public financial data...")
    
    # Example: Fetch currency exchange rates (can be used for international ATM analysis)
    try:
        # Using a free API for demonstration
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print("Successfully fetched exchange rate data")
            return data
        else:
            print("Failed to fetch data")
            return None
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def create_csv_dataset(df, filename='realistic_atm_data.csv'):
    """Create CSV dataset for easy sharing and analysis"""
    
    # Add additional columns for better analysis
    df['date'] = df['transaction_time'].dt.date
    df['hour'] = df['transaction_time'].dt.hour
    df['day_of_week'] = df['transaction_time'].dt.day_name()
    df['month'] = df['transaction_time'].dt.month_name()
    
    # Save to CSV
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")
    
    # Create summary statistics
    summary = {
        'total_transactions': len(df),
        'total_amount': df['amount'].sum(),
        'average_amount': df['amount'].mean(),
        'date_range': f"{df['transaction_time'].min()} to {df['transaction_time'].max()}",
        'unique_locations': df['atm_location'].nunique(),
        'unique_customers': df['customer_id'].nunique()
    }
    
    # Save summary
    with open('dataset_summary.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    return filename, summary

def import_to_database(connection, df):
    """Import the generated data to MySQL database"""
    
    print("Importing data to database...")
    
    cursor = connection.cursor()
    
    # Clear existing data (optional - comment out if you want to keep existing data)
    cursor.execute("TRUNCATE TABLE transactions")
    
    # Insert data in batches for better performance
    batch_size = 100
    total_inserted = 0
    
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i+batch_size]
        
        for _, row in batch.iterrows():
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
        
        total_inserted += len(batch)
        print(f"Imported {total_inserted}/{len(df)} records...")
    
    connection.commit()
    cursor.close()
    
    print(f"Successfully imported {total_inserted} records!")

def main():
    """Main function"""
    print("=== Web Data Collection for ATM Analysis ===")
    
    print("\nOptions:")
    print("1. Generate realistic ATM dataset (500 transactions)")
    print("2. Generate large dataset (2000 transactions)")
    print("3. Generate custom size dataset")
    print("4. Fetch public financial data")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice in ['1', '2', '3']:
        if choice == '1':
            num_records = 500
        elif choice == '2':
            num_records = 2000
        else:
            num_records = int(input("Enter number of records to generate: "))
        
        # Generate data
        df = generate_realistic_atm_data(num_records)
        
        # Create CSV
        csv_file, summary = create_csv_dataset(df)
        
        # Display summary
        print("\n=== Dataset Summary ===")
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        # Import to database
        connection = connect_to_database()
        if connection:
            import_to_database(connection, df)
            connection.close()
            
            print(f"\nSuccess! Your dashboard at http://localhost:8502 now shows {num_records} transactions.")
            print(f"CSV file saved as: {csv_file}")
        
    elif choice == '4':
        data = fetch_public_financial_data()
        if data:
            print("Public data fetched successfully!")
            print("This can be used for currency analysis in your ATM dashboard.")
        
    elif choice == '5':
        print("Goodbye!")
        
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
