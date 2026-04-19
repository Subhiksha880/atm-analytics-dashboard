# 🏦 ATM Transaction Pattern Analysis Project

A beautiful and professional dashboard for analyzing ATM transaction patterns using Python, MySQL, and Streamlit.

## 📋 Project Overview

This project analyzes ATM transaction data to provide insights about:
- Transaction patterns by location
- Peak usage hours
- Transaction types distribution
- Success rates
- Operational insights for ATM management

## 🛠️ Technologies Used

- **Backend**: Python, MySQL
- **Frontend**: Streamlit
- **Data Analysis**: Pandas, NumPy
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Database**: MySQL

## 📁 Project Structure

```
atm_project/
├── 01_create_database.sql    # Database and table creation
├── 02_insert_sample_data.sql # Sample data insertion
├── 03_database_connection.py # Database connection test script
├── app.py                    # Main Streamlit dashboard
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Setup Instructions

### Step 1: Database Setup

1. **Open MySQL Workbench**
2. **Execute the database creation script:**
   ```sql
   -- Copy and paste the content from 01_create_database.sql
   -- Or run: source /path/to/01_create_database.sql
   ```

3. **Insert sample data:**
   ```sql
   -- Copy and paste the content from 02_insert_sample_data.sql
   -- Or run: source /path/to/02_insert_sample_data.sql
   ```

4. **Verify the setup:**
   ```sql
   USE atm_project;
   SELECT COUNT(*) FROM transactions;
   -- Should show 55 records
   ```

### Step 2: Python Environment Setup

1. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update database credentials:**
   - Open `03_database_connection.py` and `app.py`
   - Update the `DB_CONFIG` dictionary with your MySQL credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',    # Change this
       'password': 'your_password', # Change this
       'database': 'atm_project'
   }
   ```

### Step 3: Test Database Connection

Run the test script to verify everything works:
```bash
python 03_database_connection.py
```

You should see output like:
```
✅ Successfully connected to MySQL database!
✅ Successfully loaded 55 records into DataFrame!

📊 Analysis Results:
Total Transactions: 55
Total Amount: $15,830.00
Peak Hour: 8:00 (6 transactions)
Success Rate: 100.0%
```

### Step 4: Run the Streamlit Dashboard

```bash
streamlit run app.py
```

The dashboard will automatically open in your web browser at `http://localhost:8501`

## 🎯 Dashboard Features

### 📊 Key Metrics Section
- **Total Transactions**: Live count of all transactions
- **Total Amount**: Sum of all transaction amounts
- **Peak Hour**: Busiest time of day
- **Success Rate**: Percentage of successful transactions

### 📈 Visual Analytics
- **Location Bar Chart**: Transactions by ATM location
- **Hourly Line Chart**: Peak usage time analysis
- **Transaction Type Pie Chart**: Distribution of transaction types
- **Amount by Location Chart**: Total transaction amounts per location

### 🔍 Interactive Filters
- **Location Filter**: Select specific ATM locations or view all
- **Date Range Filter**: Analyze specific time periods

### 💡 Key Insights
- Peak usage time recommendations
- Busiest location identification
- Success rate analysis
- Best refill time suggestions

### 📋 Data Table
- Recent transactions display
- Sortable and searchable data

## 🎨 Dashboard UI Features

- **Modern Clean Layout**: Wide screen design with professional styling
- **Beautiful Color Scheme**: Gradient headers and card-based layout
- **Responsive Design**: Works on different screen sizes
- **Interactive Charts**: Hover effects and detailed tooltips
- **Real-time Updates**: Dynamic filtering and instant results

## 📊 Sample Data Insights

The sample data includes:
- **5 ATM Locations**: Downtown Branch, Airport Terminal, Shopping Mall, University Campus, Hospital Complex
- **55 Sample Transactions**: Various types and amounts
- **Different Time Periods**: Transactions from 6:00 AM to 9:30 PM
- **Multiple Transaction Types**: Withdrawal, Balance Check, Deposit, Transfer

## 🔧 Customization Options

### Adding More Data
To add more transactions, use this SQL template:
```sql
INSERT INTO transactions (transaction_id, atm_location, transaction_type, amount, transaction_time, customer_id, status) 
VALUES ('TXN056', 'Your Location', 'withdrawal', 100.00, '2024-01-15 10:00:00', 'CUST056', 'success');
```

### Adding New Locations
Simply use new location names in the `atm_location` field when inserting data.

### Customizing Charts
All charts are created using Plotly and can be customized in the `create_*_chart()` functions in `app.py`.

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check MySQL server is running
   - Verify username and password
   - Ensure database `atm_project` exists

2. **Module Import Error**:
   - Install all requirements: `pip install -r requirements.txt`
   - Check Python version compatibility

3. **Dashboard Not Loading**:
   - Ensure all files are in the same directory
   - Check database connection first with test script

4. **Port Already in Use**:
   ```bash
   # Run on different port
   streamlit run app.py --server.port 8502
   ```

## 📈 Future Enhancements

- **Real-time Data**: Live transaction monitoring
- **Predictive Analytics**: ML models for cash demand forecasting
- **Alert System**: Notifications for low cash or technical issues
- **Export Features**: Download reports in PDF/Excel
- **User Authentication**: Role-based access control
- **Mobile App**: React Native or Flutter mobile version

## 📞 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all setup steps are completed correctly
3. Ensure MySQL server is running and accessible
4. Test database connection with the provided test script

## 🎉 Congratulations!

You've successfully built a professional ATM Transaction Pattern Analysis dashboard! This project demonstrates:
- Database design and management
- Data analysis and visualization
- Web dashboard development
- Interactive user interface design

Keep exploring and enhancing your dashboard with new features! 🚀
