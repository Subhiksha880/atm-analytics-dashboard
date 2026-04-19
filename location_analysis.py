"""
ATM Location Usage Analysis
Shows which ATMs are used most/least
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

def analyze_location_usage():
    """Detailed location usage analysis"""
    print("="*60)
    print("ATM LOCATION USAGE ANALYSIS")
    print("="*60)
    
    # Connect to database
    connection = connect_to_database()
    if not connection:
        return
    
    # Load data
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, connection)
    connection.close()
    
    df['transaction_time'] = pd.to_datetime(df['transaction_time'])
    df['hour'] = df['transaction_time'].dt.hour
    
    print(f"\nTotal Transactions: {len(df):,}")
    print(f"Date Range: {df['transaction_time'].min().date()} to {df['transaction_time'].max().date()}")
    
    # Location analysis
    print(f"\n" + "="*50)
    print("LOCATION USAGE ANALYSIS")
    print("="*50)
    
    location_stats = {}
    
    for location in df['atm_location'].unique():
        location_data = df[df['atm_location'] == location]
        
        stats = {
            'total_transactions': len(location_data),
            'total_amount': location_data['amount'].sum(),
            'avg_amount': location_data['amount'].mean(),
            'peak_hour': location_data['hour'].value_counts().idxmax(),
            'success_rate': (location_data['status'] == 'success').mean() * 100,
            'withdrawals': (location_data['transaction_type'] == 'withdrawal').sum(),
            'deposits': (location_data['transaction_type'] == 'deposit').sum(),
            'balance_checks': (location_data['transaction_type'] == 'balance_check').sum(),
            'transfers': (location_data['transaction_type'] == 'transfer').sum()
        }
        
        location_stats[location] = stats
    
    # Sort by total transactions
    sorted_locations = sorted(location_stats.items(), key=lambda x: x[1]['total_transactions'], reverse=True)
    
    print(f"\nRANKED BY USAGE (Most to Least Busy):")
    print("-" * 50)
    
    for rank, (location, stats) in enumerate(sorted_locations, 1):
        transactions = stats['total_transactions']
        amount = stats['total_amount']
        peak_hour = stats['peak_hour']
        success_rate = stats['success_rate']
        
        # Determine usage level
        if transactions >= 500:
            usage_level = "HIGH USAGE"
            symbol = "HIGH"
        elif transactions >= 300:
            usage_level = "MODERATE USAGE"
            symbol = "MED"
        else:
            usage_level = "LOW USAGE"
            symbol = "LOW"
        
        print(f"\n{rank}. {location}")
        print(f"   Transactions: {transactions:,} ({symbol})")
        print(f"   Total Amount: ${amount:,.2f}")
        print(f"   Average Amount: ${stats['avg_amount']:.2f}")
        print(f"   Peak Hour: {peak_hour}:00")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Usage Level: {usage_level}")
    
    # Busiest and least busiest
    busiest = sorted_locations[0]
    least_busy = sorted_locations[-1]
    
    print(f"\n" + "="*50)
    print("KEY INSIGHTS")
    print("="*50)
    print(f"BUSIEST ATM: {busiest[0]}")
    print(f"  - {busiest[1]['total_transactions']:,} transactions")
    print(f"  - ${busiest[1]['total_amount']:,.2f} total amount")
    
    print(f"\nLEAST BUSY ATM: {least_busy[0]}")
    print(f"  - {least_busy[1]['total_transactions']:,} transactions")
    print(f"  - ${least_busy[1]['total_amount']:,.2f} total amount")
    
    # Transaction type analysis by location
    print(f"\nTRANSACTION TYPES BY LOCATION:")
    print("-" * 50)
    
    for location, stats in sorted_locations:
        print(f"\n{location}:")
        print(f"  Withdrawals: {stats['withdrawals']}")
        print(f"  Deposits: {stats['deposits']}")
        print(f"  Balance Checks: {stats['balance_checks']}")
        print(f"  Transfers: {stats['transfers']}")
    
    # Recommendations
    print(f"\n" + "="*50)
    print("RECOMMENDATIONS")
    print("="*50)
    
    print(f"\nHIGH USAGE LOCATIONS:")
    for location, stats in sorted_locations:
        if stats['total_transactions'] >= 500:
            print(f"  - {location}: Consider adding more ATMs or upgrading equipment")
            print(f"    Peak hour: {stats['peak_hour']}:00 - Staff accordingly")
    
    print(f"\nLOW USAGE LOCATIONS:")
    for location, stats in sorted_locations:
        if stats['total_transactions'] < 300:
            print(f"  - {location}: Consider relocating or removing ATM")
            print(f"    Only {stats['total_transactions']} transactions")
    
    print(f"\nMAINTENANCE RECOMMENDATIONS:")
    for location, stats in sorted_locations:
        if stats['success_rate'] < 95:
            print(f"  - {location}: Low success rate ({stats['success_rate']:.1f}%) - Needs maintenance")
    
    return location_stats

def show_location_comparison():
    """Show visual comparison of locations"""
    print(f"\n" + "="*50)
    print("LOCATION COMPARISON CHART")
    print("="*50)
    
    connection = connect_to_database()
    if not connection:
        return
    
    query = "SELECT * FROM transactions"
    df = pd.read_sql(query, connection)
    connection.close()
    
    location_counts = df['atm_location'].value_counts()
    
    print(f"\nVISUAL COMPARISON:")
    max_count = location_counts.max()
    
    for location, count in location_counts.items():
        bar_length = int((count / max_count) * 30)
        bar = " " * bar_length + ">"
        
        percentage = (count / len(df)) * 100
        
        if count >= 500:
            status = "HIGH"
        elif count >= 300:
            status = "MED"
        else:
            status = "LOW"
        
        print(f"{location:20} | {count:4d} ({percentage:5.1f}%) {bar} {status}")

def main():
    print("="*60)
    print("ATM LOCATION USAGE ANALYSIS")
    print("Find out which ATMs are used most/least")
    print("="*60)
    
    # Analyze location usage
    location_stats = analyze_location_usage()
    
    # Show comparison
    show_location_comparison()
    
    print(f"\n" + "="*60)
    print("DASHBOARD FEATURES FOR LOCATION ANALYSIS:")
    print("="*60)
    print("1. Bar Chart: Visual comparison of locations")
    print("2. Sidebar Filter: Analyze specific locations")
    print("3. Amount by Location: Shows money flow")
    print("4. Recent Transactions: Location-specific data")
    print("\nRefresh your dashboard: http://localhost:8503")
    print("="*60)

if __name__ == "__main__":
    main()
