"""
========================================
Data Generator Module
ATM Transaction Pattern Analysis Project
========================================
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_realistic_atm_data(num_records=1000):
    """
    Generate realistic ATM transaction data similar to Kaggle datasets
    
    Args:
        num_records: Number of records to generate (500-1000)
    
    Returns:
        DataFrame with realistic ATM transaction data
    """
    
    # Set seed for reproducibility
    np.random.seed(42)
    random.seed(42)
    
    # Define realistic parameters
    locations = [
        'Downtown Branch',
        'Airport Terminal', 
        'Shopping Mall',
        'University Campus',
        'Hospital Complex'
    ]
    
    transaction_types = [
        'Withdrawal',
        'Deposit',
        'Balance Inquiry',
        'Transfer'
    ]
    
    status_options = ['Success', 'Failed']
    
    data = []
    
    for i in range(num_records):
        # Generate realistic timestamp
        # Peak hours: 8AM-12PM, 5PM-9PM are busiest
        hour_weights = [
            0.01, 0.01, 0.01, 0.01, 0.02, 0.03,
            0.06, 0.08, 0.10, 0.12, 0.10, 0.08,
            0.07, 0.06, 0.05, 0.05, 0.06, 0.07,
            0.09, 0.10, 0.08, 0.06, 0.04, 0.02
        ]
        
        hour_weights = np.array(hour_weights)
        hour_weights = hour_weights / hour_weights.sum()
        
        hour = np.random.choice(range(24), p=hour_weights)
        
        # Generate date within last 30 days
        days_ago = np.random.randint(0, 30)
        base_date = datetime.now() - timedelta(days=days_ago)
        transaction_time = base_date.replace(hour=hour, minute=np.random.randint(0, 59))
        
        # Select transaction type with realistic weights
        type_weights = [0.65, 0.20, 0.10, 0.05]  # Withdrawal most common
        transaction_type = np.random.choice(transaction_types, p=type_weights)
        
        # Generate realistic amount based on transaction type
        if transaction_type == 'Withdrawal':
            # Common ATM withdrawal amounts
            withdrawal_amounts = [
                20, 40, 60, 80, 100, 120, 140, 160, 180, 200,  # Common amounts
                250, 300, 400, 500  # Larger withdrawals
            ]
            withdrawal_weights = [
                0.08, 0.05, 0.04, 0.04, 0.20, 0.08, 0.06, 0.05, 0.04,
                0.15, 0.08, 0.06, 0.07, 0.00
            ]
            amount = np.random.choice(withdrawal_amounts, p=withdrawal_weights)
            
        elif transaction_type == 'Deposit':
            # Deposit amounts (log-normal distribution)
            amount = np.random.lognormal(6.5, 0.8)
            amount = max(100, min(10000, amount))  # Clamp to realistic range
            
        elif transaction_type == 'Balance Inquiry':
            # Balance inquiries usually have no amount
            amount = 0.0
            
        else:  # Transfer
            # Transfer amounts
            amount = np.random.lognormal(6.0, 0.7)
            amount = max(50, min(5000, amount))  # Clamp to realistic range
        
        # Generate status (97% success rate)
        status = np.random.choice(status_options, p=[0.97, 0.03])
        
        # Generate transaction ID
        transaction_id = f"ATM{str(i+1).zfill(6)}"
        
        data.append({
            'transaction_id': transaction_id,
            'location': np.random.choice(locations),
            'transaction_type': transaction_type,
            'amount': round(float(amount), 2),
            'transaction_time': transaction_time,
            'status': status
        })
    
    return pd.DataFrame(data)

def analyze_time_patterns(df):
    """
    Analyze time patterns and categorize into periods
    
    Args:
        df: DataFrame with transaction data
    
    Returns:
        Dictionary with time-based analysis
    """
    
    if df.empty:
        return {}
    
    # Extract hour from transaction_time
    df['hour'] = pd.to_datetime(df['transaction_time']).dt.hour
    
    # Categorize time periods
    def categorize_time(hour):
        if 6 <= hour < 12:
            return 'Morning (6 AM - 12 PM)'
        elif 12 <= hour < 18:
            return 'Afternoon (12 PM - 6 PM)'
        elif 18 <= hour < 24:
            return 'Evening (6 PM - 12 AM)'
        else:
            return 'Night (12 AM - 6 AM)'
    
    df['time_period'] = df['hour'].apply(categorize_time)
    
    # Calculate peak hour
    hourly_counts = df['hour'].value_counts()
    peak_hour_24 = hourly_counts.idxmax()
    peak_transactions = hourly_counts.max()
    
    # Convert to 12-hour format
    if peak_hour_24 == 0:
        peak_hour_12 = '12:00 AM'
    elif peak_hour_24 < 12:
        peak_hour_12 = f'{peak_hour_24}:00 AM'
    elif peak_hour_24 == 12:
        peak_hour_12 = '12:00 PM'
    else:
        peak_hour_12 = f'{peak_hour_24 - 12}:00 PM'
    
    return {
        'peak_hour_24': peak_hour_24,
        'peak_hour_12': peak_hour_12,
        'peak_transactions': peak_transactions,
        'hourly_distribution': hourly_counts.to_dict(),
        'time_period_distribution': df['time_period'].value_counts().to_dict()
    }

def generate_insights(df):
    """
    Generate professional insights from ATM data
    
    Args:
        df: DataFrame with transaction data
    
    Returns:
        List of insight dictionaries
    """
    
    if df.empty:
        return [{'title': 'No Data Available', 'description': 'No transaction data to analyze.'}]
    
    insights = []
    
    # Basic statistics
    total_transactions = len(df)
    total_amount = df['amount'].sum()
    success_rate = (df['status'] == 'Success').mean() * 100
    
    # Location analysis
    location_counts = df['location'].value_counts()
    busiest_location = location_counts.idxmax()
    busiest_location_count = location_counts.max()
    
    # Transaction type analysis
    type_counts = df['transaction_type'].value_counts()
    most_common_type = type_counts.idxmax()
    
    # Time analysis
    time_analysis = analyze_time_patterns(df)
    
    # Generate insights
    insights.append({
        'title': 'Transaction Volume Overview',
        'description': f'Total of {total_transactions:,} transactions processed with a combined value of ${total_amount:,.2f}. Overall success rate is {success_rate:.1f}%.'
    })
    
    insights.append({
        'title': 'Peak Usage Analysis',
        'description': f'Highest activity occurs during {time_analysis["peak_hour_12"]} with {time_analysis["peak_transactions"]} transactions. This represents the optimal time for cash replenishment and maintenance.'
    })
    
    insights.append({
        'title': 'Location Performance',
        'description': f'{busiest_location} is the most active location with {busiest_location_count:,} transactions, indicating highest customer traffic and demand.'
    })
    
    insights.append({
        'title': 'Transaction Pattern',
        'description': f'{most_common_type} transactions are most frequent, suggesting customer preference and potential service optimization opportunities.'
    })
    
    # Cash management recommendation
    if total_transactions > 0:
        avg_withdrawal = df[df['transaction_type'] == 'Withdrawal']['amount'].mean()
        if not pd.isna(avg_withdrawal):
            insights.append({
                'title': 'Cash Management Strategy',
                'description': f'Average withdrawal amount is ${avg_withdrawal:.2f}. Consider adjusting cash replenishment schedules based on peak usage patterns.'
            })
    
    return insights

if __name__ == "__main__":
    # Test data generation
    test_data = generate_realistic_atm_data(100)
    print("Generated sample data:")
    print(test_data.head())
    print(f"\nTotal records: {len(test_data)}")
    
    # Test time analysis
    time_analysis = analyze_time_patterns(test_data)
    print(f"\nPeak hour: {time_analysis['peak_hour_12']} (24-hour: {time_analysis['peak_hour_24']})")
    
    # Test insights generation
    insights = generate_insights(test_data)
    print("\nGenerated insights:")
    for insight in insights:
        print(f"- {insight['title']}: {insight['description']}")
