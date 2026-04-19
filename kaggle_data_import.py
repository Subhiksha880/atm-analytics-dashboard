"""
========================================
ATM Transaction Pattern Analysis Project
Kaggle Data Import Script
========================================
"""

import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime, timedelta
import random
import os

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

def create_sample_kaggle_dataset():
    """Create a realistic dataset similar to Kaggle ATM datasets"""
    
    # Generate realistic ATM data
    np.random.seed(42)
    
    # Parameters
    num_transactions = 1000
    start_date = datetime.now() - timedelta(days=90)
    
    # ATM locations (realistic)
    locations = [
        'Downtown Branch', 'Airport Terminal', 'Shopping Mall', 
        'University Campus', 'Hospital Complex', 'Train Station',
        'Business District', 'Residential Area', 'Tourist Center', 'Industrial Zone'
    ]
    
    # Customer IDs
    customer_ids = [f"CUST{str(i).zfill(4)}" for i in range(1, 501)]
    
    data = []
    
    for i in range(num_transactions):
        # Generate random transaction time
        random_days = random.randint(0, 89)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)
        
        transaction_time = start_date + timedelta(days=random_days, hours=random_hours, minutes=random_minutes)
        
        # Transaction type with realistic probabilities
        trans_type_probs = [0.6, 0.2, 0.15, 0.05]  # withdrawal, balance_check, deposit, transfer
        transaction_type = np.random.choice(['withdrawal', 'balance_check', 'deposit', 'transfer'], p=trans_type_probs)
        
        # Amount based on transaction type and location
        if transaction_type == 'balance_check':
            amount = 0.0
        elif transaction_type == 'withdrawal':
            # Different withdrawal patterns by location
            location_multipliers = {
                'Airport Terminal': 1.5,
                'Shopping Mall': 1.2,
                'Business District': 1.3,
                'Tourist Center': 1.4,
                'Downtown Branch': 1.1,
                'Train Station': 1.0,
                'University Campus': 0.6,
                'Hospital Complex': 0.9,
                'Residential Area': 0.8,
                'Industrial Zone': 1.0
            }
            base_amount = random.uniform(20, 500)
            location = random.choice(locations)
            amount = round(base_amount * location_multipliers[location], 2)
        elif transaction_type == 'deposit':
            amount = round(random.uniform(100, 2000), 2)
        else:  # transfer
            amount = round(random.uniform(50, 1000), 2)
        
        # Status with realistic success rates
        status_probs = [0.95, 0.04, 0.01]  # success, failed, pending
        status = np.random.choice(['success', 'failed', 'pending'], p=status_probs)
        
        # Generate transaction ID
        transaction_id = f"TXN{str(i+1).zfill(6)}"
        
        # Random customer
        customer_id = random.choice(customer_ids)
        
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

def save_to_csv(df, filename='atm_transactions_kaggle_style.csv'):
    """Save dataset to CSV file"""
    df.to_csv(filename, index=False)
    print(f"Dataset saved to {filename}")
    print(f"Shape: {df.shape}")
    print(f"Date range: {df['transaction_time'].min()} to {df['transaction_time'].max()}")
    return filename

def import_csv_to_database(connection, csv_file):
    """Import CSV data to MySQL database"""
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file)
        
        # Convert transaction_time to datetime
        df['transaction_time'] = pd.to_datetime(df['transaction_time'])
        
        # Clear existing data (optional)
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE transactions")
        
        # Insert data row by row
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
            
            if (index + 1) % 100 == 0:
                print(f"Imported {index + 1} records...")
        
        connection.commit()
        cursor.close()
        
        print(f"Successfully imported {len(df)} records to database!")
        
    except Exception as e:
        print(f"Error importing data: {e}")

def analyze_dataset(df):
    """Analyze the generated dataset"""
    print("\n=== Dataset Analysis ===")
    print(f"Total Transactions: {len(df):,}")
    print(f"Date Range: {df['transaction_time'].min()} to {df['transaction_time'].max()}")
    print(f"Total Amount: ${df['amount'].sum():,.2f}")
    print(f"Average Amount: ${df['amount'].mean():.2f}")
    
    print("\nTransactions by Location:")
    location_counts = df['atm_location'].value_counts()
    for location, count in location_counts.head(5).items():
        print(f"  {location}: {count} transactions")
    
    print("\nTransaction Types:")
    type_counts = df['transaction_type'].value_counts()
    for trans_type, count in type_counts.items():
        print(f"  {trans_type}: {count} ({count/len(df)*100:.1f}%)")
    
    print("\nSuccess Rate:")
    success_rate = (df['status'] == 'success').mean() * 100
    print(f"  {success_rate:.1f}%")
    
    print("\nPeak Hours:")
    df['hour'] = df['transaction_time'].dt.hour
    peak_hour = df['hour'].value_counts().idxmax()
    print(f"  {peak_hour}:00 ({df['hour'].value_counts().max()} transactions)")

def download_real_kaggle_instructions():
    """Print instructions for downloading real Kaggle datasets"""
    print("\n=== How to Download Real Kaggle Datasets ===")
    print("\n1. Install Kaggle API:")
    print("   pip install kaggle")
    
    print("\n2. Get Kaggle API Token:")
    print("   - Go to kaggle.com")
    print("   - Account > Create New API Token")
    print("   - Download kaggle.json")
    print("   - Place it in C:\\Users\\NAVANEETHAN\\.kaggle\\")
    
    print("\n3. Search for ATM/Banking Datasets:")
    print("   Recommended datasets:")
    print("   - 'bank-transaction-dataset'")
    print("   - 'credit-card-fraud-detection'")
    print("   - 'bank-customer-churn'")
    
    print("\n4. Download dataset:")
    print("   kaggle datasets download -d [dataset-name]")
    
    print("\n5. Example code to load real dataset:")
    print("""
    import pandas as pd
    from kaggle.api.kaggle_api_extended import KaggleApi
    
    # Authenticate
    api = KaggleApi()
    api.authenticate()
    
    # Download dataset
    api.dataset_download_files('dataset-name', path='./data')
    
    # Load and process
    df = pd.read_csv('./data/file.csv')
    """)

def main():
    """Main function"""
    print("=== Kaggle Data Import for ATM Analysis ===")
    
    print("\nOptions:")
    print("1. Generate realistic sample dataset (Kaggle-style)")
    print("2. Import from existing CSV file")
    print("3. Learn how to download real Kaggle datasets")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == '1':
        print("\nGenerating realistic ATM dataset...")
        df = create_sample_kaggle_dataset()
        
        # Save to CSV
        csv_file = save_to_csv(df)
        
        # Analyze
        analyze_dataset(df)
        
        # Import to database
        connection = connect_to_database()
        if connection:
            import_csv_to_database(connection, csv_file)
            connection.close()
            
        print(f"\nDataset ready! Your dashboard at http://localhost:8502 will show {len(df)} transactions.")
        
    elif choice == '2':
        csv_file = input("Enter CSV file path: ")
        if os.path.exists(csv_file):
            connection = connect_to_database()
            if connection:
                df = pd.read_csv(csv_file)
                analyze_dataset(df)
                import_csv_to_database(connection, csv_file)
                connection.close()
        else:
            print("File not found!")
            
    elif choice == '3':
        download_real_kaggle_instructions()
        
    elif choice == '4':
        pass
        
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
