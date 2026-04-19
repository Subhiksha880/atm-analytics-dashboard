"""
========================================
Fixed Analytics Dashboard
Correct peak hour analysis with AM/PM
========================================
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Set page configuration
st.set_page_config(
    page_title="Fixed Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Fixed CSS styling
def set_fixed_style():
    st.markdown("""
    <style>
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #ffffff;
    }
    
    .header {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        color: #ffffff;
        margin-bottom: 1rem;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
    }
    
    .kpi-card {
        background: rgba(30, 41, 59, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 255, 255, 0.3);
        text-align: center;
    }
    
    .kpi-value {
        font-size: 2rem;
        font-weight: 800;
        color: #00ffff;
        margin: 0;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #94a3b8;
        margin: 0.5rem 0 0 0;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .peak-info {
        color: #00ff00;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    .chart-container {
        background: rgba(30, 41, 59, 0.9);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .stSidebar {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.9);
        color: #ffffff;
        border: 1px solid rgba(0, 255, 255, 0.3);
        border-radius: 6px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 6px;
        padding: 0.25rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        color: #94a3b8;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 255, 255, 0.2);
        color: #00ffff;
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        background: rgba(30, 41, 59, 0.9);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_realistic_data():
    """Generate realistic financial data with proper peak hours"""
    np.random.seed(42)
    
    locations = ['New York', 'London', 'Tokyo', 'Singapore', 'Hong Kong']
    transaction_types = ['withdrawal', 'deposit', 'transfer', 'payment']
    
    data = []
    for i in range(1500):
        # Realistic peak hours - 8AM, 12PM, 5PM are busiest
        hour_weights = [0.02, 0.01, 0.02, 0.03, 0.04, 0.06, 0.08, 0.10, 0.09, 0.07, 0.06, 0.08, 0.10, 0.09, 0.07, 0.06, 0.08, 0.12, 0.15, 0.14, 0.08, 0.04, 0.02, 0.01]
        hour = np.random.choice(24, p=hour_weights)
        
        # Realistic timestamp
        days_ago = np.random.randint(0, 30)
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=np.random.randint(0, 59))
        
        # Transaction type
        trans_type = np.random.choice(transaction_types, p=[0.5, 0.25, 0.15, 0.1])
        
        # Realistic amounts
        if trans_type == 'withdrawal':
            amount = np.random.choice([20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 300, 400, 500], 
                                    p=[0.08, 0.05, 0.04, 0.04, 0.20, 0.08, 0.06, 0.05, 0.04, 0.15, 0.08, 0.06, 0.07])
        elif trans_type == 'deposit':
            amount = np.random.uniform(100, 5000)
        elif trans_type == 'transfer':
            amount = np.random.uniform(50, 3000)
        else:  # payment
            amount = np.random.choice([10, 20, 25, 30, 40, 50, 75, 100, 150, 200], 
                                    p=[0.05, 0.08, 0.06, 0.12, 0.15, 0.20, 0.10, 0.12, 0.06, 0.04])
        
        # Status
        status = np.random.choice(['success', 'failed', 'pending'], p=[0.97, 0.025, 0.005])
        
        data.append({
            'transaction_id': f"FIX{i+1:06d}",
            'atm_location': np.random.choice(locations),
            'transaction_type': trans_type,
            'amount': round(float(amount), 2),
            'transaction_time': transaction_time,
            'customer_id': f"CUST{np.random.randint(1000, 9999)}",
            'status': status
        })
    
    return pd.DataFrame(data)

def convert_to_12hr(hour_24):
    """Convert 24-hour to 12-hour format with AM/PM"""
    if hour_24 == 0:
        return "12:00 AM"
    elif hour_24 < 12:
        return f"{hour_24}:00 AM"
    elif hour_24 == 12:
        return "12:00 PM"
    else:
        return f"{hour_24 - 12}:00 PM"

def calculate_peak_hour_correctly(df):
    """Calculate peak hour correctly"""
    if df.empty:
        return 0, 0
    
    # Extract hour from transaction_time
    df['hour'] = df['transaction_time'].dt.hour
    
    # Count transactions by hour
    hourly_counts = df['hour'].value_counts().sort_index()
    
    if hourly_counts.empty:
        return 0, 0
    
    # Find peak hour
    peak_hour_24 = hourly_counts.idxmax()
    peak_transactions = hourly_counts.max()
    
    return peak_hour_24, peak_transactions

def main():
    """Main fixed dashboard"""
    set_fixed_style()
    
    # Header
    st.markdown('<h1 class="header">Fixed Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Generate data
    with st.spinner('Loading realistic data...'):
        df = generate_realistic_data()
    
    if df.empty:
        st.error("No data available")
        return
    
    # Sidebar
    st.sidebar.header("Filters")
    
    # Location filter
    all_locations = ["All"] + list(df['atm_location'].unique())
    selected_location = st.sidebar.selectbox("Location", all_locations)
    
    # Date range
    min_date = df['transaction_time'].min().date()
    max_date = df['transaction_time'].max().date()
    selected_date_range = st.sidebar.date_input("Date Range", [min_date, max_date])
    
    # Filter data
    filtered_df = df.copy()
    if selected_location != "All":
        filtered_df = filtered_df[filtered_df['atm_location'] == selected_location]
    
    if len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        filtered_df = filtered_df[
            (filtered_df['transaction_time'].dt.date >= start_date) &
            (filtered_df['transaction_time'].dt.date <= end_date)
        ]
    
    # Calculate peak hour CORRECTLY
    peak_hour_24, peak_transactions = calculate_peak_hour_correctly(filtered_df)
    peak_hour_12 = convert_to_12hr(peak_hour_24)
    
    # Calculate other metrics
    total_transactions = len(filtered_df)
    total_amount = filtered_df['amount'].sum()
    success_rate = (filtered_df['status'] == 'success').mean() * 100
    unique_customers = filtered_df['customer_id'].nunique()
    
    # KPI Section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{total_transactions:,}</div>
            <div class="kpi-label">Total Transactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">${total_amount:,.2f}</div>
            <div class="kpi-label">Total Amount</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{success_rate:.1f}%</div>
            <div class="kpi-label">Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{peak_hour_12}</div>
            <div class="kpi-label">Peak Hour</div>
            <div class="peak-info">{peak_transactions} transactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed Peak Hour Analysis
    st.header("Peak Hour Analysis")
    
    if not filtered_df.empty:
        # Create hourly breakdown
        hourly_breakdown = filtered_df.copy()
        hourly_breakdown['hour'] = hourly_breakdown['transaction_time'].dt.hour
        hourly_stats = hourly_breakdown.groupby('hour').agg({
            'transaction_id': 'count',
            'amount': 'sum'
        }).round(2)
        hourly_stats.columns = ['Transactions', 'Total Amount']
        hourly_stats = hourly_stats.sort_values('Transactions', ascending=False)
        
        # Show top 5 busiest hours
        st.subheader("Top 5 Busiest Hours")
        top_5_hours = hourly_stats.head(5)
        
        for idx, (hour, row) in enumerate(top_5_hours.iterrows()):
            hour_12 = convert_to_12hr(hour)
            transactions = row['Transactions']
            amount = row['Total Amount']
            
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(30, 41, 59, 0.9); padding: 1rem; margin: 0.5rem 0; border-radius: 8px; border: 1px solid rgba(0, 255, 255, 0.3);">
                <div style="flex: 1;">
                    <div style="font-size: 1.2rem; font-weight: 700; color: #00ffff;">{hour_12}</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">Busiest Time</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1rem; font-weight: 600; color: #ffffff;">{transactions:,} transactions</div>
                    <div style="color: #00ff00; font-size: 0.8rem;">${amount:,.2f}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Charts Section
    st.header("Analytics Charts")
    
    if not filtered_df.empty:
        # Hourly chart
        hourly_data = filtered_df.copy()
        hourly_data['hour'] = hourly_data['transaction_time'].dt.hour
        hourly_counts = hourly_data['hour'].value_counts().sort_index().reset_index()
        hourly_counts.columns = ['Hour', 'Transactions']
        
        fig_hourly = px.line(hourly_counts, x='Hour', y='Transactions', 
                            title='Hourly Transaction Pattern',
                            color_discrete_sequence=['#00ffff'])
        fig_hourly.update_layout(
            plot_bgcolor='rgba(15, 23, 42, 0.8)',
            paper_bgcolor='rgba(15, 23, 42, 0.6)',
            font=dict(color='#ffffff'),
            height=400
        )
        
        # Location chart
        location_data = filtered_df['atm_location'].value_counts().reset_index()
        location_data.columns = ['Location', 'Transactions']
        
        fig_location = px.bar(location_data, x='Location', y='Transactions',
                           title='Transactions by Location',
                           color_discrete_sequence=['#ff00ff'])
        fig_location.update_layout(
            plot_bgcolor='rgba(15, 23, 42, 0.8)',
            paper_bgcolor='rgba(15, 23, 42, 0.6)',
            font=dict(color='#ffffff'),
            height=400
        )
        
        # Transaction type chart
        type_data = filtered_df['transaction_type'].value_counts().reset_index()
        type_data.columns = ['Type', 'Count']
        
        fig_type = px.pie(type_data, values='Count', names='Type',
                         title='Transaction Type Distribution',
                         color_discrete_sequence=['#00ff00', '#ffff00', '#ff6600', '#ff00ff'])
        fig_type.update_layout(
            plot_bgcolor='rgba(15, 23, 42, 0.8)',
            paper_bgcolor='rgba(15, 23, 42, 0.6)',
            font=dict(color='#ffffff'),
            height=400
        )
        
        # Display charts
        tab1, tab2, tab3 = st.tabs(["Hourly Pattern", "Location Analysis", "Transaction Types"])
        
        with tab1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_hourly, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_location, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with tab3:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.plotly_chart(fig_type, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Recent Transactions
        st.header("Recent Transactions")
        recent_df = filtered_df.sort_values('transaction_time', ascending=False).head(10)
        recent_df['Amount'] = recent_df['amount'].apply(lambda x: f'${x:,.2f}')
        recent_df['Time'] = recent_df['transaction_time'].dt.strftime('%Y-%m-%d %H:%M')
        st.dataframe(recent_df[['transaction_id', 'atm_location', 'transaction_type', 'Amount', 'Time', 'status']])

if __name__ == "__main__":
    main()
