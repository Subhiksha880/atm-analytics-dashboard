"""
========================================
Colorful Animated ATM Transaction Analysis Dashboard
Beautiful animations and attractive colors
========================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import time

# Set page configuration
st.set_page_config(
    page_title="ATM Transaction Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'atm_project'
}

# Beautiful animated CSS styling
def set_colorful_animated_style():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes shimmer {
        0% { background-position: -200% 0; }
        100% { background-position: 200% 0; }
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 4s ease infinite, fadeIn 1.5s ease-out;
        margin-bottom: 2rem;
        text-shadow: 0 0 40px rgba(255, 107, 107, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(255, 107, 107, 0.3);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: fadeIn 0.8s ease-out;
        border: 3px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px rgba(255, 107, 107, 0.4);
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        animation: pulse 2s infinite;
    }
    
    .metric-label {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.95);
        margin: 0;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .section-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2d3436;
        margin: 3rem 0 1.5rem 0;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 1rem;
        border-bottom: 4px solid transparent;
        border-image: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%) 1;
        animation: slideIn 0.8s ease-out;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #45B7D1 0%, #96CEB4 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(69, 183, 209, 0.3);
        animation: fadeIn 1.2s ease-out;
        border: 3px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(15px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .insight-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    .insight-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(69, 183, 209, 0.4);
        background: linear-gradient(135deg, #96CEB4 0%, #FFEAA7 100%);
    }
    
    .insight-title {
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
        text-shadow: 0 3px 10px rgba(0, 0, 0, 0.3);
    }
    
    .insight-text {
        color: rgba(255, 255, 255, 0.95);
        margin: 0;
        font-weight: 600;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
        animation: fadeIn 1.4s ease-out;
        border: 2px solid rgba(255, 107, 107, 0.1);
        transition: all 0.4s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        border-color: rgba(78, 205, 196, 0.3);
    }
    
    .stSelectbox > div > div > select {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
    }
    
    .stSelectbox > div > div > select:hover {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
    }
    
    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1.6s ease-out;
        border: 2px solid rgba(255, 107, 107, 0.1);
    }
    
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2d3436;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 50%, #45B7D1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: slideIn 0.6s ease-out;
    }
    
    .stSidebar {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        backdrop-filter: blur(20px);
    }
    
    .stApp {
        background: linear-gradient(-45deg, #ffecd2 0%, #fcb69f 25%, #ff8177 50%, #ff6b6b 75%, #ee5a6f 100%);
        background-size: 400% 400%;
        animation: gradient 20s ease infinite;
    }
    
    .success-animation {
        animation: pulse 0.5s ease 3;
        color: #00b894;
    }
    
    /* Loading animation */
    .stSpinner > div {
        border-top-color: #FF6B6B !important;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Hide streamlit default elements */
    .stDeployButton {
        display: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: linear-gradient(135deg, #f1f2f6 0%, #dfe6e9 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FF6B6B 0%, #4ECDC4 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #4ECDC4 0%, #45B7D1 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def connect_to_database():
    """Connect to MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def load_data(connection):
    """Load transaction data from database"""
    try:
        query = "SELECT * FROM transactions"
        df = pd.read_sql(query, connection)
        
        # Convert transaction_time to datetime
        df['transaction_time'] = pd.to_datetime(df['transaction_time'])
        
        # Extract hour and date for analysis
        df['hour'] = df['transaction_time'].dt.hour
        df['date'] = df['transaction_time'].dt.date
        df['day_of_week'] = df['transaction_time'].dt.day_name()
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def filter_data(df, selected_location, selected_date_range):
    """Filter data based on user selections"""
    filtered_df = df.copy()
    
    # Location filter
    if selected_location != "All Locations":
        filtered_df = filtered_df[filtered_df['atm_location'] == selected_location]
    
    # Date range filter
    if selected_date_range and len(selected_date_range) == 2:
        start_date, end_date = selected_date_range
        filtered_df = filtered_df[
            (filtered_df['transaction_time'].dt.date >= start_date) &
            (filtered_df['transaction_time'].dt.date <= end_date)
        ]
    
    return filtered_df

def calculate_metrics(df):
    """Calculate key metrics"""
    if df.empty:
        return {
            'total_transactions': 0,
            'total_amount': 0,
            'average_amount': 0,
            'peak_hour': 'N/A',
            'success_rate': 0,
            'unique_customers': 0
        }
    
    metrics = {
        'total_transactions': len(df),
        'total_amount': df['amount'].sum(),
        'average_amount': df['amount'].mean(),
        'peak_hour': df['hour'].value_counts().idxmax() if not df['hour'].empty else 'N/A',
        'success_rate': (df['status'] == 'success').mean() * 100,
        'unique_customers': df['customer_id'].nunique()
    }
    return metrics

def create_colorful_location_chart(df):
    """Create colorful bar chart for transactions by location"""
    if df.empty:
        return go.Figure()
    
    location_counts = df['atm_location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Transactions']
    
    # Beautiful color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
    
    fig = go.Figure(data=[
        go.Bar(
            x=location_counts['Location'],
            y=location_counts['Transactions'],
            marker=dict(
                color=colors[:len(location_counts)],
                line=dict(color='white', width=2)
            ),
            text=location_counts['Transactions'],
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold'),
            hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Transactions by Location',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2d3436', 'weight': 'bold'}
        },
        xaxis_title="Location",
        yaxis_title="Number of Transactions",
        height=500,
        plot_bgcolor='rgba(255, 255, 255, 0.95)',
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
        font=dict(color='#2d3436', size=14),
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        tickangle=45, 
        gridcolor='rgba(255, 107, 107, 0.1)',
        tickfont=dict(size=12, weight='bold')
    )
    fig.update_yaxes(
        gridcolor='rgba(78, 205, 196, 0.1)',
        tickfont=dict(size=12, weight='bold')
    )
    
    return fig

def create_colorful_hourly_chart(df):
    """Create colorful line chart for hourly transaction pattern"""
    if df.empty:
        return go.Figure()
    
    hourly_counts = df['hour'].value_counts().sort_index().reset_index()
    hourly_counts.columns = ['Hour', 'Transactions']
    
    fig = go.Figure()
    
    # Add colorful line
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='lines+markers',
        line=dict(
            color='#FF6B6B',
            width=5,
            shape='spline'
        ),
        marker=dict(
            color='#4ECDC4',
            size=12,
            symbol='diamond',
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Hour: %{x}:00</b><br>Transactions: %{y}<extra></extra>'
    ))
    
    # Add colorful area fill
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(255, 107, 107, 0.2)',
        showlegend=False,
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title={
            'text': 'Transaction Volume by Hour',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2d3436', 'weight': 'bold'}
        },
        xaxis_title="Hour of Day",
        yaxis_title="Number of Transactions",
        height=500,
        plot_bgcolor='rgba(255, 255, 255, 0.95)',
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
        font=dict(color='#2d3436', size=14),
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        dtick=1, 
        gridcolor='rgba(255, 107, 107, 0.1)',
        tickfont=dict(size=12, weight='bold')
    )
    fig.update_yaxes(
        gridcolor='rgba(78, 205, 196, 0.1)',
        tickfont=dict(size=12, weight='bold')
    )
    
    return fig

def create_colorful_transaction_type_chart(df):
    """Create colorful pie chart for transaction types"""
    if df.empty:
        return go.Figure()
    
    type_counts = df['transaction_type'].value_counts().reset_index()
    type_counts.columns = ['Transaction Type', 'Count']
    
    # Beautiful color palette
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=type_counts['Transaction Type'],
            values=type_counts['Count'],
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold'),
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            pull=[0.1, 0.1, 0.1, 0.1],
            rotation=45
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Transaction Type Distribution',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2d3436', 'weight': 'bold'}
        },
        height=500,
        plot_bgcolor='rgba(255, 255, 255, 0.95)',
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
        font=dict(color='#2d3436', size=14),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12, weight='bold')
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

def create_colorful_amount_chart(df):
    """Create colorful bar chart for total amount by location"""
    if df.empty:
        return go.Figure()
    
    amount_by_location = df.groupby('atm_location')['amount'].sum().reset_index()
    amount_by_location = amount_by_location.sort_values('amount', ascending=False)
    
    # Beautiful color palette
    colors = ['#45B7D1', '#96CEB4', '#FFEAA7', '#FF6B6B', '#4ECDC4']
    
    fig = go.Figure(data=[
        go.Bar(
            x=amount_by_location['atm_location'],
            y=amount_by_location['amount'],
            marker=dict(
                color=colors[:len(amount_by_location)],
                line=dict(color='white', width=2)
            ),
            text=amount_by_location['amount'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            textfont=dict(color='white', size=14, weight='bold'),
            hovertemplate='<b>%{x}</b><br>Total Amount: $%{y:,.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Total Transaction Amount by Location',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#2d3436', 'weight': 'bold'}
        },
        xaxis_title="Location",
        yaxis_title="Total Amount ($)",
        height=500,
        plot_bgcolor='rgba(255, 255, 255, 0.95)',
        paper_bgcolor='rgba(255, 255, 255, 0.8)',
        font=dict(color='#2d3436', size=14),
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        tickangle=45, 
        gridcolor='rgba(69, 183, 209, 0.1)',
        tickfont=dict(size=12, weight='bold')
    )
    fig.update_yaxes(
        tickprefix='$', 
        gridcolor='rgba(150, 206, 180, 0.1)',
        tickfont=dict(size=12, weight='bold')
    )
    
    return fig

def generate_colorful_insights(df, metrics):
    """Generate colorful insights from the data"""
    if df.empty:
        return [{"title": "No Data", "text": "No data available for analysis."}]
    
    insights = []
    
    # Peak hour insight
    if metrics['peak_hour'] != 'N/A':
        peak_hour_data = df[df['hour'] == metrics['peak_hour']]
        insights.append({
            'title': 'Peak Usage Time',
            'text': f'Highest transaction volume occurs at {metrics["peak_hour"]}:00 with {len(peak_hour_data)} transactions'
        })
    
    # Most busy location
    if not df.empty:
        busiest_location = df['atm_location'].value_counts().idxmax()
        busiest_count = df['atm_location'].value_counts().max()
        insights.append({
            'title': 'Busiest Location',
            'text': f'{busiest_location} handles the highest volume with {busiest_count} transactions'
        })
    
    # Average transaction insight
    if metrics['average_amount'] > 0:
        insights.append({
            'title': 'Average Transaction',
            'text': f'Average transaction amount is ${metrics["average_amount"]:.2f}'
        })
    
    # Success rate insight
    if metrics['success_rate'] > 0:
        if metrics['success_rate'] >= 95:
            status = "excellent"
        elif metrics['success_rate'] >= 90:
            status = "good"
        else:
            status = "needs attention"
        
        insights.append({
            'title': 'System Performance',
            'text': f'Success rate is {metrics["success_rate"]:.1f}% - System performance is {status}'
        })
    
    # Best refill time
    if not df.empty:
        least_busy_hour = df['hour'].value_counts().idxmin()
        insights.append({
            'title': 'Maintenance Window',
            'text': f'Optimal time for maintenance: {least_busy_hour}:00 (lowest activity period)'
        })
    
    return insights

def create_real_sample_data():
    """Create realistic sample data for demonstration"""
    print("Creating realistic sample data...")
    
    np.random.seed(42)
    locations = ['Downtown Branch', 'Airport Terminal', 'Shopping Mall', 'University Campus', 'Hospital Complex']
    data = []
    
    for i in range(1000):
        # Realistic peak hours
        hour = np.random.choice([8, 12, 17, 18, 19], p=[0.25, 0.20, 0.20, 0.15, 0.10]) if np.random.random() < 0.7 else np.random.randint(0, 24)
        
        # Realistic timestamp
        days_ago = np.random.randint(0, 30)
        transaction_time = datetime.now() - timedelta(days=days_ago, hours=hour, minutes=np.random.randint(0, 59))
        
        # Transaction types
        trans_type = np.random.choice(['withdrawal', 'balance_check', 'deposit', 'transfer'], p=[0.65, 0.20, 0.10, 0.05])
        
        # Realistic amounts
        if trans_type == 'balance_check':
            amount = 0.0
        elif trans_type == 'withdrawal':
            amount = np.random.choice([20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 300, 400, 500], 
                                    p=[0.08, 0.05, 0.04, 0.04, 0.20, 0.08, 0.06, 0.05, 0.04, 0.15, 0.08, 0.06, 0.07])
        elif trans_type == 'deposit':
            amount = np.random.uniform(100, 2000)
        else:
            amount = np.random.uniform(50, 1000)
        
        # Location patterns
        if hour in [8, 9]:
            location = np.random.choice(['Downtown Branch', 'Airport Terminal'], p=[0.6, 0.4])
        elif hour in [12, 13]:
            location = np.random.choice(['Downtown Branch', 'Shopping Mall'], p=[0.5, 0.5])
        elif hour in [17, 18, 19]:
            location = np.random.choice(['Downtown Branch', 'Shopping Mall', 'Airport Terminal'], p=[0.4, 0.3, 0.3])
        else:
            location = np.random.choice(locations)
        
        # Status
        status = np.random.choice(['success', 'failed', 'pending'], p=[0.96, 0.035, 0.005])
        
        data.append({
            'transaction_id': f"REAL{i+1:06d}",
            'atm_location': location,
            'transaction_type': trans_type,
            'amount': round(float(amount), 2),
            'transaction_time': transaction_time,
            'customer_id': f"CUST{np.random.randint(1000, 9999)}",
            'status': status
        })
    
    return pd.DataFrame(data)

def main():
    """Main Streamlit application"""
    # Apply colorful animated styling
    set_colorful_animated_style()
    
    # Animated header
    st.markdown('<h1 class="main-header">ATM Transaction Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #636e72; font-size: 1.2rem; animation: fadeIn 2s ease-out; font-weight: 600;">Real-time insights and analytics for ATM operations</p>', unsafe_allow_html=True)
    
    # Connect to database or create sample data
    connection = connect_to_database()
    if connection:
        df = load_data(connection)
        connection.close()
    else:
        st.warning("Database connection failed. Using sample data for demonstration.")
        df = create_real_sample_data()
    
    if df is None or df.empty:
        st.error("No data available. Please check your database connection.")
        return
    
    # Animated sidebar for filters
    st.sidebar.markdown('<h3 class="sidebar-header">Filters</h3>', unsafe_allow_html=True)
    
    # Location filter
    all_locations = ["All Locations"] + list(df['atm_location'].unique())
    selected_location = st.sidebar.selectbox(
        "Location",
        all_locations,
        index=0
    )
    
    # Date range filter
    min_date = df['transaction_time'].min().date()
    max_date = df['transaction_time'].max().date()
    
    selected_date_range = st.sidebar.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter data
    filtered_df = filter_data(df, selected_location, selected_date_range)
    
    # Calculate metrics
    metrics = calculate_metrics(filtered_df)
    
    # Animated Key Metrics Section
    st.markdown('<h2 class="section-header">Key Performance Metrics</h2>', unsafe_allow_html=True)
    
    # Create colorful animated metric cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics['total_transactions']:,}</p>
            <p class="metric-label">Total Transactions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">${metrics['total_amount']:,.2f}</p>
            <p class="metric-label">Total Amount</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics['peak_hour']}:00</p>
            <p class="metric-label">Peak Hour</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{metrics['success_rate']:.1f}%</p>
            <p class="metric-label">Success Rate</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Animated Charts Section
    st.markdown('<h2 class="section-header">Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Row 1: Location and Hourly charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_location = create_colorful_location_chart(filtered_df)
        st.plotly_chart(fig_location, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_hourly = create_colorful_hourly_chart(filtered_df)
        st.plotly_chart(fig_hourly, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Transaction Type and Amount charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_type = create_colorful_transaction_type_chart(filtered_df)
        st.plotly_chart(fig_type, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_amount = create_colorful_amount_chart(filtered_df)
        st.plotly_chart(fig_amount, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Animated Insights Section
    st.markdown('<h2 class="section-header">Business Insights</h2>', unsafe_allow_html=True)
    
    insights = generate_colorful_insights(filtered_df, metrics)
    
    for i, insight in enumerate(insights):
        # Add delay animation for each insight
        st.markdown(f"""
        <div class="insight-box" style="animation-delay: {i * 0.3}s">
            <div class="insight-title">{insight['title']}</div>
            <div class="insight-text">{insight['text']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Animated Data Table Section
    st.markdown('<h2 class="section-header">Recent Transactions</h2>', unsafe_allow_html=True)
    
    # Show recent transactions
    recent_transactions = filtered_df.sort_values('transaction_time', ascending=False).head(10)
    st.dataframe(
        recent_transactions[['transaction_id', 'atm_location', 'transaction_type', 'amount', 'transaction_time', 'status']],
        use_container_width=True,
        hide_index=True
    )
    
    # Animated footer
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #636e72; animation: fadeIn 2.5s ease-out; font-weight: 600;">ATM Transaction Analysis Dashboard | Modern Analytics Platform</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
