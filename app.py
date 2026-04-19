"""
========================================
ATM Transaction Pattern Analysis Dashboard
Professional Dark Theme with Complete Analytics
========================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt
from database import load_atm_data, create_atm_transactions_table
from data_generator import generate_realistic_atm_data, analyze_time_patterns, generate_insights

# Configure page
st.set_page_config(
    page_title="ATM Transaction Pattern Analysis",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional dark theme CSS
def set_professional_dark_theme():
    """Apply professional dark theme styling"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0E1117 0%, #1E293B 50%, #334155 100%);
        background-size: 400% 400%;
        animation: gradientShift 15s ease infinite;
        color: #FFFFFF;
        min-height: 100vh;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        text-align: center;
        color: #FFFFFF;
        margin-bottom: 1rem;
        text-shadow: 0 2px 10px rgba(0, 255, 255, 0.3);
        animation: fadeIn 1s ease-out;
    }
    
    .sub-header {
        font-size: 1.1rem;
        font-weight: 500;
        text-align: center;
        color: #94A3B8;
        margin-bottom: 2rem;
        animation: fadeIn 1.2s ease-out;
    }
    
    /* KPI Cards */
    .kpi-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        animation: fadeIn 0.8s ease-out;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.4);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #00D9FF;
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 3px rgba(0, 217, 255, 0.3);
    }
    
    .kpi-label {
        font-size: 0.9rem;
        font-weight: 600;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .kpi-change {
        font-size: 0.8rem;
        font-weight: 500;
        padding: 0.25rem 0.75rem;
        border-radius: 8px;
        display: inline-block;
        margin-top: 0.5rem;
    }
    
    .kpi-change.positive {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .kpi-change.negative {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
        animation: slideIn 0.6s ease-out;
    }
    
    /* Chart containers */
    .chart-container {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-out;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar styling */
    .stSidebar {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(99, 102, 241, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(99, 102, 241, 0.3);
    }
    
    /* Filter styling */
    .filter-container {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Table styling */
    .data-table-container {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        overflow-x: auto;
    }
    
    /* Insights styling */
    .insight-container {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    
    .insight-card {
        background: rgba(15, 23, 42, 0.8);
        border-left: 4px solid #00D9FF;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        animation: fadeIn 1.2s ease-out;
    }
    
    .insight-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #00D9FF;
        margin-bottom: 0.5rem;
    }
    
    .insight-description {
        font-size: 0.95rem;
        font-weight: 500;
        color: #E2E8F0;
        line-height: 1.6;
    }
    
    /* Form styling */
    .stSelectbox > div > div > select {
        background: rgba(30, 41, 59, 0.9);
        color: #FFFFFF;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        font-weight: 500;
    }
    
    .stDateInput > div > div > input {
        background: rgba(30, 41, 59, 0.9);
        color: #FFFFFF;
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(30, 41, 59, 0.9);
        border-radius: 12px;
        padding: 0.5rem;
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        color: #94A3B8;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(0, 217, 255, 0.2);
        color: #00D9FF;
        border: 1px solid rgba(0, 217, 255, 0.4);
    }
    
    /* Data table styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(99, 102, 241, 0.2);
    }
    
    /* Hide streamlit default elements */
    .stDeployButton {
        display: none;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(15, 23, 42, 0.8);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00D9FF 0%, #6366F1 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #00D9FF 0%, #0066FF 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def create_kpi_cards(df):
    """Create professional KPI cards"""
    if df.empty:
        return {}
    
    # Calculate metrics
    total_transactions = len(df)
    total_amount = df['amount'].sum()
    avg_amount = df['amount'].mean()
    success_rate = (df['status'] == 'Success').mean() * 100
    
    # Time analysis
    time_analysis = analyze_time_patterns(df)
    peak_hour_12 = time_analysis.get('peak_hour_12', 'N/A')
    peak_transactions = time_analysis.get('peak_transactions', 0)
    
    # Location analysis
    location_counts = df['location'].value_counts()
    busiest_location = location_counts.idxmax()
    busiest_location_count = location_counts.max()
    
    return {
        'total_transactions': total_transactions,
        'total_amount': total_amount,
        'avg_amount': avg_amount,
        'success_rate': success_rate,
        'peak_hour_12': peak_hour_12,
        'peak_transactions': peak_transactions,
        'busiest_location': busiest_location,
        'busiest_location_count': busiest_location_count
    }

def create_charts(df):
    """Create interactive charts for analysis"""
    if df.empty:
        return {}
    
    charts = {}
    
    # Bar chart - Transactions by location
    location_data = df['location'].value_counts().reset_index()
    location_data.columns = ['Location', 'Transactions']
    
    charts['location'] = px.bar(
        location_data,
        x='Location',
        y='Transactions',
        title='Transaction Volume by Location',
        color_discrete_sequence=['#00D9FF'],
        template='plotly_dark'
    )
    charts['location'].update_layout(
        xaxis_title="ATM Location",
        yaxis_title="Number of Transactions",
        height=500,
        showlegend=False
    )
    
    # Line chart - Transactions over time
    df['date'] = pd.to_datetime(df['transaction_time']).dt.date
    daily_data = df.groupby('date').size().reset_index()
    daily_data.columns = ['Date', 'Transactions']
    
    charts['time_trend'] = px.line(
        daily_data,
        x='Date',
        y='Transactions',
        title='Transaction Trend Over Time',
        color_discrete_sequence=['#00D9FF'],
        template='plotly_dark'
    )
    charts['time_trend'].update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Transactions",
        height=500,
        showlegend=False
    )
    
    # Pie chart - Transaction type distribution
    type_data = df['transaction_type'].value_counts().reset_index()
    type_data.columns = ['Transaction Type', 'Count']
    
    charts['transaction_type'] = px.pie(
        type_data,
        values='Count',
        names='Transaction Type',
        title='Transaction Type Distribution',
        color_discrete_sequence=['#00D9FF', '#10B981', '#F59E0B', '#EF4444'],
        template='plotly_dark'
    )
    charts['transaction_type'].update_layout(
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            xanchor="left",
            font=dict(size=12, color="#E2E8F0")
        )
    )
    
    # Histogram - Amount distribution
    charts['amount_dist'] = px.histogram(
        df,
        x='amount',
        title='Transaction Amount Distribution',
        nbins=30,
        color_discrete_sequence=['#00D9FF'],
        template='plotly_dark'
    )
    charts['amount_dist'].update_layout(
        xaxis_title="Transaction Amount ($)",
        yaxis_title="Frequency",
        height=500,
        showlegend=False
    )
    
    # Heatmap - Time vs Location
    df['hour'] = pd.to_datetime(df['transaction_time']).dt.hour
    heatmap_data = df.groupby(['location', 'hour']).size().reset_index()
    heatmap_data.columns = ['Location', 'Hour', 'Transactions']
    heatmap_pivot = heatmap_data.pivot(index='Location', columns='Hour', values='Transactions').fillna(0)
    
    charts['heatmap'] = px.imshow(
        heatmap_pivot.values,
        labels=dict(x="Hour", y="Location", color="Transactions"),
        x=heatmap_pivot.columns,
        y=heatmap_pivot.index,
        title='Transaction Heatmap - Location vs Time',
        color_continuous_scale='Blues',
        template='plotly_dark'
    )
    charts['heatmap'].update_layout(
        xaxis_title="Hour of Day",
        yaxis_title="ATM Location",
        height=500
    )
    
    return charts

def display_insights(insights):
    """Display professional insights section"""
    st.markdown('<div class="section-header">Business Intelligence & Insights</div>', unsafe_allow_html=True)
    
    for insight in insights:
        st.markdown(f"""
        <div class="insight-container">
            <div class="insight-card">
                <div class="insight-title">{insight['title']}</div>
                <div class="insight-description">{insight['description']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard application"""
    # Apply professional dark theme
    set_professional_dark_theme()
    
    # Header
    st.markdown('<div class="main-header">ATM Transaction Pattern Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Analytics Dashboard for ATM Network Optimization</div>', unsafe_allow_html=True)
    
    # Load data
    with st.spinner('Loading transaction data...'):
        # Generate realistic data with proper business hours
        df = generate_realistic_atm_data(2000)
    
    # Sidebar filters
    st.sidebar.markdown('<div class="sidebar-header">Filters & Controls</div>', unsafe_allow_html=True)
    
    with st.sidebar.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        
        # Location filter
        all_locations = ["All Locations"] + list(df['location'].unique())
        selected_location = st.selectbox("ATM Location", all_locations)
        
        # Transaction type filter
        all_types = ["All Types"] + list(df['transaction_type'].unique())
        selected_type = st.selectbox("Transaction Type", all_types)
        
        # Status filter
        all_status = ["All Status"] + list(df['status'].unique())
        selected_status = st.selectbox("Transaction Status", all_status)
        
        # Date range filter
        min_date = pd.to_datetime(df['transaction_time']).min().date()
        max_date = pd.to_datetime(df['transaction_time']).max().date()
        date_range = st.date_input("Date Range", [min_date, max_date])
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if selected_location != "All Locations":
        filtered_df = filtered_df[filtered_df['location'] == selected_location]
    
    if selected_type != "All Types":
        filtered_df = filtered_df[filtered_df['transaction_type'] == selected_type]
    
    if selected_status != "All Status":
        filtered_df = filtered_df[filtered_df['status'] == selected_status]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['transaction_time']).dt.date >= start_date) &
            (pd.to_datetime(filtered_df['transaction_time']).dt.date <= end_date)
        ]
    
    # KPI Section
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    kpi_metrics = create_kpi_cards(filtered_df)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpi_metrics['total_transactions']:,}</div>
            <div class="kpi-label">Total Transactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">${kpi_metrics['total_amount']:,.2f}</div>
            <div class="kpi-label">Total Amount Processed</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpi_metrics['success_rate']:.1f}%</div>
            <div class="kpi-label">Success Rate</div>
            <div class="kpi-change positive">Peak: {kpi_metrics['peak_hour_12']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpi_metrics['busiest_location']}</div>
            <div class="kpi-label">Most Active Location</div>
            <div class="kpi-change positive">{kpi_metrics['busiest_location_count']} transactions</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts Section
    st.markdown('<div class="section-header">Visual Analytics</div>', unsafe_allow_html=True)
    
    charts = create_charts(filtered_df)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Location Analysis", "Time Trends", "Transaction Types", "Amount Distribution"])
    
    with tab1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if 'location' in charts:
            st.plotly_chart(charts['location'], width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if 'time_trend' in charts:
            st.plotly_chart(charts['time_trend'], width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if 'transaction_type' in charts:
            st.plotly_chart(charts['transaction_type'], width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        if 'amount_dist' in charts:
            st.plotly_chart(charts['amount_dist'], width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Heatmap Section
    st.markdown('<div class="section-header">Activity Heatmap</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    if 'heatmap' in charts:
        st.plotly_chart(charts['heatmap'], width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Insights Section
    insights = generate_insights(filtered_df)
    display_insights(insights)
    
    # Recent Transactions Table
    st.markdown('<div class="section-header">Recent Transactions</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="data-table-container">', unsafe_allow_html=True)
    
    recent_df = filtered_df.sort_values('transaction_time', ascending=False).head(10)
    display_df = recent_df.copy()
    display_df['Amount'] = display_df['amount'].apply(lambda x: f'${x:,.2f}')
    display_df['Time'] = pd.to_datetime(display_df['transaction_time']).dt.strftime('%Y-%m-%d %I:%M %p')
    
    st.dataframe(
        display_df[['transaction_id', 'location', 'transaction_type', 'Amount', 'Time', 'status']],
        width='stretch',
        hide_index=True
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #94A3B8; font-size: 0.9rem;">ATM Transaction Pattern Analysis Dashboard | Professional Analytics Platform</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Create database table if needed
    create_atm_transactions_table()
    
    # Run main dashboard
    main()
