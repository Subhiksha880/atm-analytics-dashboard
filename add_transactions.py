"""
========================================
ATM Transaction Pattern Analysis Project
Add New Transactions Script
========================================
"""

import mysql.connector
import pandas as pd
from datetime import datetime, timedelta
import random

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

def add_sample_transactions(connection, num_transactions=10):
    """Add random sample transactions"""
    
    # ATM locations
    locations = ['Downtown Branch', 'Airport Terminal', 'Shopping Mall', 'University Campus', 'Hospital Complex']
    
    # Transaction types
    transaction_types = ['withdrawal', 'balance_check', 'deposit', 'transfer']
    
    # Generate random transactions
    transactions = []
    
    for i in range(num_transactions):
        transaction_id = f"TXN{str(i+100).zfill(3)}"  # TXN100, TXN101, etc.
        location = random.choice(locations)
        trans_type = random.choice(transaction_types)
        
        # Generate amount based on transaction type
        if trans_type == 'balance_check':
            amount = 0.00
        elif trans_type == 'withdrawal':
            amount = round(random.uniform(50, 1000), 2)
        elif trans_type == 'deposit':
            amount = round(random.uniform(100, 2000), 2)
        else:  # transfer
            amount = round(random.uniform(50, 800), 2)
        
        # Generate random time within last 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
        
        customer_id = f"CUST{str(i+100).zfill(3)}"
        status = random.choice(['success', 'success', 'success', 'failed'])  # 75% success rate
        
        transactions.append({
            'transaction_id': transaction_id,
            'atm_location': location,
            'transaction_type': trans_type,
            'amount': amount,
            'transaction_time': transaction_time,
            'customer_id': customer_id,
            'status': status
        })
    
    # Insert transactions into database
    cursor = connection.cursor()
    
    for trans in transactions:
        query = """
        INSERT INTO transactions 
        (transaction_id, atm_location, transaction_type, amount, transaction_time, customer_id, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            trans['transaction_id'],
            trans['atm_location'],
            trans['transaction_type'],
            trans['amount'],
            trans['transaction_time'],
            trans['customer_id'],
            trans['status']
        )
        
        try:
            cursor.execute(query, values)
            print(f"Added transaction: {trans['transaction_id']} - {trans['transaction_type']} - ${trans['amount']}")
        except mysql.connector.Error as e:
            print(f"Error adding transaction {trans['transaction_id']}: {e}")
    
    connection.commit()
    cursor.close()
    
    print(f"\nSuccessfully added {len(transactions)} new transactions!")

def add_custom_transaction(connection):
    """Add a custom transaction with user input"""
    
    print("\n=== Add Custom Transaction ===")
    
    transaction_id = input("Transaction ID (e.g., TXN999): ")
    location = input("ATM Location (Downtown Branch/Airport Terminal/Shopping Mall/University Campus/Hospital Complex): ")
    trans_type = input("Transaction Type (withdrawal/balance_check/deposit/transfer): ")
    amount = float(input("Amount (0.00 for balance_check): "))
    
    # Get date from user
    date_str = input("Date (YYYY-MM-DD, press Enter for today): ")
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = datetime.now().date()
    
    time_str = input("Time (HH:MM, press Enter for current time): ")
    if time_str:
        hour, minute = map(int, time_str.split(':'))
        transaction_time = datetime.combine(date, datetime.min.time().replace(hour=hour, minute=minute))
    else:
        transaction_time = datetime.now()
    
    customer_id = input("Customer ID (e.g., CUST999): ")
    status = input("Status (success/failed/pending): ")
    
    # Insert transaction
    cursor = connection.cursor()
    
    query = """
    INSERT INTO transactions 
    (transaction_id, atm_location, transaction_type, amount, transaction_time, customer_id, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (transaction_id, location, trans_type, amount, transaction_time, customer_id, status)
    
    try:
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print(f"Successfully added transaction: {transaction_id}")
    except mysql.connector.Error as e:
        print(f"Error adding transaction: {e}")

def view_current_transactions(connection):
    """View current transactions in database"""
    query = "SELECT * FROM transactions ORDER BY transaction_time DESC LIMIT 10"
    df = pd.read_sql(query, connection)
    
    print("\n=== Current Transactions (Last 10) ===")
    print(df.to_string(index=False))
    print(f"\nTotal transactions in database: {len(df)}")

def main():
    """Main function"""
    print("=== ATM Transaction Management ===")
    
    # Connect to database
    connection = connect_to_database()
    if connection is None:
        return
    
    while True:
        print("\nOptions:")
        print("1. Add sample transactions (random)")
        print("2. Add custom transaction")
        print("3. View current transactions")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ")
        
        if choice == '1':
            num = int(input("How many sample transactions to add? (default 10): ") or "10")
            add_sample_transactions(connection, num)
            
        elif choice == '2':
            add_custom_transaction(connection)
            
        elif choice == '3':
            view_current_transactions(connection)
            
        elif choice == '4':
            break
            
        else:
            print("Invalid choice. Please try again.")
    
    connection.close()
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
