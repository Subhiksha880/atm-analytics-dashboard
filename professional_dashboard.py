"""
========================================
Professional ATM Transaction Analysis Dashboard
Clean, Corporate Design without Emojis
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

# Set page configuration for professional layout
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

# Professional CSS styling
def set_professional_style():
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 600;
        text-align: center;
        color: #1f2937;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 3px solid #3b82f6;
    }
    
    .metric-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1f2937;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0;
        font-weight: 500;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        color: #1f2937;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
    }
    
    .insight-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .insight-text {
        color: #4b5563;
        margin: 0;
    }
    
    .chart-container {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div > select {
        background-color: #f9fafb;
        border: 1px solid #d1d5db;
        border-radius: 6px;
    }
    
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .sidebar-header {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
    
    /* Hide streamlit default elements */
    .stDeployButton {
        display: none;
    }
    
    /* Professional color scheme */
    .primary-color {
        color: #3b82f6;
    }
    
    .success-color {
        color: #10b981;
    }
    
    .warning-color {
        color: #f59e0b;
    }
    
    .error-color {
        color: #ef4444;
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

def create_professional_location_chart(df):
    """Create professional bar chart for transactions by location"""
    if df.empty:
        return go.Figure()
    
    location_counts = df['atm_location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Transactions']
    
    fig = go.Figure(data=[
        go.Bar(
            x=location_counts['Location'],
            y=location_counts['Transactions'],
            marker_color='#3b82f6',
            text=location_counts['Transactions'],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Transactions: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Transactions by Location',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        xaxis_title="Location",
        yaxis_title="Number of Transactions",
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1f2937'),
        showlegend=False
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(gridcolor='#e5e7eb')
    
    return fig

def create_professional_hourly_chart(df):
    """Create professional line chart for hourly transaction pattern"""
    if df.empty:
        return go.Figure()
    
    hourly_counts = df['hour'].value_counts().sort_index().reset_index()
    hourly_counts.columns = ['Hour', 'Transactions']
    
    fig = go.Figure()
    
    # Add line
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='lines+markers',
        line=dict(color='#3b82f6', width=3),
        marker=dict(color='#3b82f6', size=8),
        hovertemplate='<b>Hour: %{x}:00</b><br>Transactions: %{y}<extra></extra>'
    ))
    
    # Add area fill
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)',
        showlegend=False,
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title={
            'text': 'Transaction Volume by Hour',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        xaxis_title="Hour of Day",
        yaxis_title="Number of Transactions",
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1f2937'),
        showlegend=False
    )
    
    fig.update_xaxes(dtick=1, gridcolor='#e5e7eb')
    fig.update_yaxes(gridcolor='#e5e7eb')
    
    return fig

def create_professional_transaction_type_chart(df):
    """Create professional pie chart for transaction types"""
    if df.empty:
        return go.Figure()
    
    type_counts = df['transaction_type'].value_counts().reset_index()
    type_counts.columns = ['Transaction Type', 'Count']
    
    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=type_counts['Transaction Type'],
            values=type_counts['Count'],
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='auto',
            hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title={
            'text': 'Transaction Type Distribution',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 18, 'color': '#1f2937'}
        },
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
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

def create_professional_amount_chart(df):
    """Create professional bar chart for total amount by location"""
    if df.empty:
        return go.Figure()
    
    amount_by_location = df.groupby('atm_location')['amount'].sum().reset_index()
    amount_by_location = amount_by_location.sort_values('amount', ascending=False)
    
    fig = go.Figure(data=[
        go.Bar(
            x=amount_by_location['atm_location'],
            y=amount_by_location['amount'],
            marker_color='#10b981',
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
            'font': {'size': 18, 'color': '#1f2937'}
        },
        xaxis_title="Location",
        yaxis_title="Total Amount ($)",
        height=400,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(color='#1f2937'),
        showlegend=False
    )
    
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(tickprefix='$', gridcolor='#e5e7eb')
    
    return fig

def generate_professional_insights(df, metrics):
    """Generate professional insights from the data"""
    if df.empty:
        return ["No data available for analysis."]
    
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
            color = "success"
        elif metrics['success_rate'] >= 90:
            status = "good"
            color = "warning"
        else:
            status = "needs attention"
            color = "error"
        
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
    # Apply professional styling
    set_professional_style()
    
    # Professional header
    st.markdown('<h1 class="main-header">ATM Transaction Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #6b7280; font-size: 1rem;">Real-time insights and analytics for ATM operations</p>', unsafe_allow_html=True)
    
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
    
    # Sidebar for filters
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
    
    # Key Metrics Section
    st.markdown('<h2 class="section-header">Key Performance Metrics</h2>', unsafe_allow_html=True)
    
    # Create metric cards
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
    
    # Charts Section
    st.markdown('<h2 class="section-header">Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Row 1: Location and Hourly charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_location = create_professional_location_chart(filtered_df)
        st.plotly_chart(fig_location, use_container_width=True)
    
    with col2:
        fig_hourly = create_professional_hourly_chart(filtered_df)
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    # Row 2: Transaction Type and Amount charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_type = create_professional_transaction_type_chart(filtered_df)
        st.plotly_chart(fig_type, use_container_width=True)
    
    with col2:
        fig_amount = create_professional_amount_chart(filtered_df)
        st.plotly_chart(fig_amount, use_container_width=True)
    
    # Insights Section
    st.markdown('<h2 class="section-header">Business Insights</h2>', unsafe_allow_html=True)
    
    insights = generate_professional_insights(filtered_df, metrics)
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-box">
            <div class="insight-title">{insight['title']}</div>
            <div class="insight-text">{insight['text']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Data Table Section
    st.markdown('<h2 class="section-header">Recent Transactions</h2>', unsafe_allow_html=True)
    
    # Show recent transactions
    recent_transactions = filtered_df.sort_values('transaction_time', ascending=False).head(10)
    st.dataframe(
        recent_transactions[['transaction_id', 'atm_location', 'transaction_type', 'amount', 'transaction_time', 'status']],
        use_container_width=True,
        hide_index=True
    )
    
    # Footer
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #6b7280;">ATM Transaction Analysis Dashboard | Professional Analytics Platform</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
