"""
Generate Custom ATM Dataset
"""

import pandas as pd
import mysql.connector
from web_data_collector import generate_realistic_atm_data, create_csv_dataset, connect_to_database, import_to_database

def main():
    # Generate 1000 transactions
    print('Generating 1000 realistic ATM transactions...')
    df = generate_realistic_atm_data(1000)
    
    # Create CSV
    csv_file, summary = create_csv_dataset(df, 'large_atm_dataset.csv')
    
    # Display summary
    print('\n=== Dataset Summary ===')
    for key, value in summary.items():
        print(f'{key.replace("_", " ").title()}: {value}')
    
    # Import to database
    connection = connect_to_database()
    if connection:
        import_to_database(connection, df)
        connection.close()
        
        print(f'\nSuccess! Your dashboard at http://localhost:8502 now shows 1000 transactions.')
        print(f'CSV file saved as: {csv_file}')

if __name__ == "__main__":
    main()
