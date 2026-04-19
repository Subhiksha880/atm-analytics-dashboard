"""
========================================
Animated ATM Transaction Analysis Dashboard
Beautiful colors, animations, and modern design
========================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Animated and colorful CSS styling
def set_animated_style():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); }
        to { transform: translateX(0); }
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
    
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #fda085 100%);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite, fadeIn 1s ease-out;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
        border: 2px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        animation: pulse 2s infinite;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.9);
        margin: 0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .section-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
        animation: slideIn 0.6s ease-out;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: #ffffff;
        padding: 1.5rem;
        border-radius: 16px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3);
        animation: fadeIn 1s ease-out;
        border: 2px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .insight-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(240, 147, 251, 0.4);
        background: linear-gradient(135deg, #f5576c 0%, #fda085 100%);
    }
    
    .insight-title {
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
        text-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }
    
    .insight-text {
        color: rgba(255, 255, 255, 0.95);
        margin: 0;
        font-weight: 500;
        line-height: 1.5;
    }
    
    .chart-container {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        animation: fadeIn 1.2s ease-out;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
    }
    
    .chart-container:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stSelectbox > div > div > select {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div > select:hover {
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        transform: scale(1.02);
    }
    
    .stDataFrame {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1.4s ease-out;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: slideIn 0.5s ease-out;
    }
    
    .stSidebar {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        backdrop-filter: blur(10px);
    }
    
    /* Animated background */
    .stApp {
        background: linear-gradient(-45deg, #f8fafc, #e2e8f0, #cbd5e1, #94a3b8);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    /* Loading animation */
    .stSpinner {
        color: #667eea;
        animation: pulse 1s infinite;
    }
    
    /* Success animation */
    .success-animation {
        animation: pulse 0.5s ease 3;
        color: #10b981;
    }
    
    /* Hide streamlit default elements */
    .stDeployButton {
        display: none;
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

def create_animated_location_chart(df):
    """Create animated bar chart for transactions by location"""
    if df.empty:
        return go.Figure()
    
    location_counts = df['atm_location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Transactions']
    
    # Create animated gradient colors
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#fda085']
    
    fig = go.Figure(data=[
        go.Bar(
            x=location_counts['Location'],
            y=location_counts['Transactions'],
            marker=dict(
                color=location_counts['Transactions'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Transaction Volume")
            ),
            text=location_counts['Transactions'],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>',
            animation_frame=0
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Transactions by Location',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f2937'}
        },
        xaxis_title="Location",
        yaxis_title="Number of Transactions",
        height=450,
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(255, 255, 255, 0.7)',
        font=dict(color='#1f2937'),
        showlegend=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(tickangle=45, gridcolor='rgba(102, 126, 234, 0.1)')
    fig.update_yaxes(gridcolor='rgba(102, 126, 234, 0.1)')
    
    return fig

def create_animated_hourly_chart(df):
    """Create animated line chart for hourly transaction pattern"""
    if df.empty:
        return go.Figure()
    
    hourly_counts = df['hour'].value_counts().sort_index().reset_index()
    hourly_counts.columns = ['Hour', 'Transactions']
    
    fig = go.Figure()
    
    # Add animated line
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='lines+markers',
        line=dict(
            color='#667eea',
            width=4,
            shape='spline'
        ),
        marker=dict(
            color='#764ba2',
            size=10,
            symbol='circle'
        ),
        hovertemplate='<b>Hour: %{x}:00</b><br>Transactions: %{y}<extra></extra>'
    ))
    
    # Add animated area fill
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        showlegend=False,
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title={
            'text': 'Transaction Volume by Hour',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f2937'}
        },
        xaxis_title="Hour of Day",
        yaxis_title="Number of Transactions",
        height=450,
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(255, 255, 255, 0.7)',
        font=dict(color='#1f2937'),
        showlegend=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(dtick=1, gridcolor='rgba(102, 126, 234, 0.1)')
    fig.update_yaxes(gridcolor='rgba(102, 126, 234, 0.1)')
    
    return fig

def create_animated_transaction_type_chart(df):
    """Create animated pie chart for transaction types"""
    if df.empty:
        return go.Figure()
    
    type_counts = df['transaction_type'].value_counts().reset_index()
    type_counts.columns = ['Transaction Type', 'Count']
    
    # Beautiful color palette
    colors = ['#667eea', '#764ba2', '#f093fb', '#f5576c']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=type_counts['Transaction Type'],
            values=type_counts['Count'],
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
            pull=[0.05, 0.05, 0.05, 0.05]  # Pull out all slices slightly
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Transaction Type Distribution',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f2937'}
        },
        height=450,
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(255, 255, 255, 0.7)',
        font=dict(color='#1f2937'),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.01
        )
    )
    
    return fig

def create_animated_amount_chart(df):
    """Create animated bar chart for total amount by location"""
    if df.empty:
        return go.Figure()
    
    amount_by_location = df.groupby('atm_location')['amount'].sum().reset_index()
    amount_by_location = amount_by_location.sort_values('amount', ascending=False)
    
    # Gradient colors
    colors = ['#f093fb', '#f5576c', '#fda085', '#667eea', '#764ba2']
    
    fig = go.Figure(data=[
        go.Bar(
            x=amount_by_location['atm_location'],
            y=amount_by_location['amount'],
            marker=dict(
                color=amount_by_location['amount'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Total Amount ($)")
            ),
            text=amount_by_location['amount'].apply(lambda x: f'${x:,.0f}'),
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Total Amount: $%{y:,.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Total Transaction Amount by Location',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#1f2937'}
        },
        xaxis_title="Location",
        yaxis_title="Total Amount ($)",
        height=450,
        plot_bgcolor='rgba(255, 255, 255, 0.9)',
        paper_bgcolor='rgba(255, 255, 255, 0.7)',
        font=dict(color='#1f2937'),
        showlegend=False,
        hovermode='x unified'
    )
    
    fig.update_xaxes(tickangle=45, gridcolor='rgba(240, 147, 251, 0.1)')
    fig.update_yaxes(tickprefix='$', gridcolor='rgba(240, 147, 251, 0.1)')
    
    return fig

def generate_animated_insights(df, metrics):
    """Generate animated insights from the data"""
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
    # Apply animated styling
    set_animated_style()
    
    # Animated header
    st.markdown('<h1 class="main-header">ATM Transaction Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 1.1rem; animation: fadeIn 1s ease-out;">Real-time insights and analytics for ATM operations</p>', unsafe_allow_html=True)
    
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
    
    # Create animated metric cards
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
        fig_location = create_animated_location_chart(filtered_df)
        st.plotly_chart(fig_location, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_hourly = create_animated_hourly_chart(filtered_df)
        st.plotly_chart(fig_hourly, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Transaction Type and Amount charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_type = create_animated_transaction_type_chart(filtered_df)
        st.plotly_chart(fig_type, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_amount = create_animated_amount_chart(filtered_df)
        st.plotly_chart(fig_amount, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Animated Insights Section
    st.markdown('<h2 class="section-header">Business Insights</h2>', unsafe_allow_html=True)
    
    insights = generate_animated_insights(filtered_df, metrics)
    
    for i, insight in enumerate(insights):
        # Add delay animation for each insight
        st.markdown(f"""
        <div class="insight-box" style="animation-delay: {i * 0.2}s">
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
    st.markdown('<p style="text-align: center; color: #6b7280; animation: fadeIn 2s ease-out;">ATM Transaction Analysis Dashboard | Modern Analytics Platform</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
