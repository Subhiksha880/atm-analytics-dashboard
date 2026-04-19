"""
========================================
Dark Theme Animated ATM Dashboard with Videos and Images
Stunning visual effects with dark theme
========================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import base64
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

# Dark theme with animations and images CSS
def set_dark_animated_style():
    st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 20px rgba(0, 255, 255, 0.7); }
        50% { transform: scale(1.05); box-shadow: 0 0 40px rgba(0, 255, 255, 0.9); }
        100% { transform: scale(1); box-shadow: 0 0 20px rgba(0, 255, 255, 0.7); }
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
    
    @keyframes glow {
        0% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.5); }
        50% { box-shadow: 0 0 20px rgba(0, 255, 255, 0.8), 0 0 30px rgba(255, 0, 255, 0.6); }
        100% { box-shadow: 0 0 5px rgba(0, 255, 255, 0.5); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* Dark theme background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
        color: #ffffff;
    }
    
    /* Main header with neon effect */
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(45deg, #00ffff, #ff00ff, #00ff00, #ffff00);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 3s ease infinite, glow 2s ease-in-out infinite;
        margin-bottom: 2rem;
        text-shadow: 0 0 30px rgba(0, 255, 255, 0.8);
        font-family: 'Arial Black', sans-serif;
    }
    
    /* Animated metric cards with dark theme */
    .metric-card {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1) 0%, rgba(255, 0, 255, 0.1) 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0, 255, 255, 0.3);
        margin: 1rem 0;
        transition: all 0.4s ease;
        animation: fadeIn 0.8s ease-out, glow 3s ease-in-out infinite;
        border: 2px solid rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
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
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    .metric-card:hover {
        transform: translateY(-8px) scale(1.03);
        box-shadow: 0 20px 40px rgba(255, 0, 255, 0.4);
        border-color: rgba(255, 0, 255, 0.5);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        color: #00ffff;
        margin: 0;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
        animation: pulse 2s infinite;
        font-family: 'Courier New', monospace;
    }
    
    .metric-label {
        font-size: 1rem;
        color: #ff00ff;
        margin: 0;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 0 10px rgba(255, 0, 255, 0.8);
    }
    
    /* Section headers with neon effect */
    .section-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #00ff00;
        margin: 3rem 0 1.5rem 0;
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 50%, #00ff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 1rem;
        border-bottom: 3px solid transparent;
        border-image: linear-gradient(90deg, #00ffff 0%, #ff00ff 50%, #00ff00 100%) 1;
        animation: slideIn 0.8s ease-out, glow 2s ease-in-out infinite;
        text-shadow: 0 0 20px rgba(0, 255, 0, 0.8);
    }
    
    /* Insight boxes with dark theme */
    .insight-box {
        background: linear-gradient(135deg, rgba(0, 255, 0, 0.1) 0%, rgba(255, 255, 0, 0.1) 100%);
        color: #ffffff;
        padding: 2rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        box-shadow: 0 10px 30px rgba(0, 255, 0, 0.3);
        animation: fadeIn 1.2s ease-out, glow 3s ease-in-out infinite;
        border: 2px solid rgba(0, 255, 0, 0.3);
        backdrop-filter: blur(10px);
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
        background: linear-gradient(90deg, transparent, rgba(0, 255, 0, 0.3), transparent);
        animation: shimmer 3s infinite;
    }
    
    .insight-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(255, 255, 0, 0.4);
        border-color: rgba(255, 255, 0, 0.5);
    }
    
    .insight-title {
        font-weight: 800;
        color: #ffff00;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
        text-shadow: 0 0 15px rgba(255, 255, 0, 0.8);
    }
    
    .insight-text {
        color: rgba(255, 255, 255, 0.95);
        margin: 0;
        font-weight: 600;
        line-height: 1.6;
        font-size: 1.1rem;
    }
    
    /* Chart containers with dark theme */
    .chart-container {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.8) 0%, rgba(0, 255, 255, 0.1) 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0, 255, 255, 0.2);
        margin: 1.5rem 0;
        animation: fadeIn 1.4s ease-out;
        border: 2px solid rgba(0, 255, 255, 0.2);
        transition: all 0.4s ease;
        backdrop-filter: blur(10px);
    }
    
    .chart-container:hover {
        transform: translateY(-3px);
        box-shadow: 0 20px 40px rgba(255, 0, 255, 0.3);
        border-color: rgba(255, 0, 255, 0.4);
    }
    
    /* Sidebar dark theme */
    .stSidebar {
        background: linear-gradient(135deg, rgba(0, 0, 0, 0.9) 0%, rgba(0, 255, 255, 0.1) 100%);
        backdrop-filter: blur(20px);
    }
    
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #00ffff;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        background: linear-gradient(90deg, #00ffff 0%, #ff00ff 50%, #00ff00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: slideIn 0.6s ease-out, glow 2s ease-in-out infinite;
        text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
    }
    
    /* Select boxes dark theme */
    .stSelectbox > div > div > select {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2) 0%, rgba(255, 0, 255, 0.2) 100%);
        color: #ffffff;
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 12px;
        padding: 0.8rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(0, 255, 255, 0.3);
    }
    
    .stSelectbox > div > div > select:hover {
        background: linear-gradient(135deg, rgba(255, 0, 255, 0.3) 0%, rgba(0, 255, 0, 0.3) 100%);
        transform: scale(1.02);
        box-shadow: 0 8px 20px rgba(255, 0, 255, 0.4);
        border-color: rgba(255, 0, 255, 0.5);
    }
    
    /* Data table dark theme */
    .stDataFrame {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(0, 255, 255, 0.2);
        animation: fadeIn 1.6s ease-out;
        border: 2px solid rgba(0, 255, 255, 0.2);
        background: rgba(0, 0, 0, 0.8);
    }
    
    /* Video container */
    .video-container {
        position: relative;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 20px 40px rgba(0, 255, 255, 0.4);
        margin: 2rem 0;
        animation: fadeIn 1s ease-out, glow 3s ease-in-out infinite;
        border: 3px solid rgba(0, 255, 255, 0.5);
    }
    
    .video-container video {
        width: 100%;
        border-radius: 20px;
    }
    
    /* Image gallery */
    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .gallery-image {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 15px 35px rgba(255, 0, 255, 0.3);
        animation: fadeIn 1s ease-out, float 3s ease-in-out infinite;
        border: 2px solid rgba(255, 0, 255, 0.4);
        transition: all 0.4s ease;
    }
    
    .gallery-image:hover {
        transform: scale(1.05);
        box-shadow: 0 20px 40px rgba(255, 255, 0, 0.4);
        border-color: rgba(255, 255, 0, 0.5);
    }
    
    .gallery-image img {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 20px;
    }
    
    /* Loading spinner dark theme */
    .stSpinner > div {
        border-top-color: #00ffff !important;
        animation: spin 1s linear infinite;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
    }
    
    /* Custom scrollbar dark theme */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00ffff 0%, #ff00ff 100%);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.8);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ff00ff 0%, #00ff00 100%);
        box-shadow: 0 0 15px rgba(255, 0, 255, 0.8);
    }
    
    /* Hide streamlit default elements */
    .stDeployButton {
        display: none;
    }
    
    /* Animated background particles */
    .particles {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    </style>
    """, unsafe_allow_html=True)

def create_animated_background():
    """Create animated background with particles"""
    return """
    <div class="particles">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:rgb(0,255,255);stop-opacity:0.3" />
                    <stop offset="100%" style="stop-color:rgb(255,0,255);stop-opacity:0.3" />
                </linearGradient>
            </defs>
            <circle cx="10%" cy="10%" r="2" fill="url(#grad1)">
                <animate attributeName="cy" from="10%" to="90%" dur="5s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0;1;0" dur="5s" repeatCount="indefinite" />
            </circle>
            <circle cx="90%" cy="90%" r="2" fill="url(#grad1)">
                <animate attributeName="cy" from="90%" to="10%" dur="4s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0;1;0" dur="4s" repeatCount="indefinite" />
            </circle>
            <circle cx="50%" cy="50%" r="1" fill="url(#grad1)">
                <animate attributeName="r" values="1;3;1" dur="3s" repeatCount="indefinite" />
                <animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite" />
            </circle>
        </svg>
    </div>
    """

def create_video_placeholder():
    """Create a video placeholder with animation"""
    return """
    <div class="video-container">
        <video autoplay muted loop style="width: 100%; border-radius: 20px;">
            <source src="data:video/mp4;base64,VIDEO_DATA_HERE" type="video/mp4">
            <!-- Animated placeholder -->
            <div style="width: 100%; height: 300px; background: linear-gradient(45deg, #00ffff, #ff00ff, #00ff00, #ffff00); 
                        border-radius: 20px; display: flex; align-items: center; justify-content: center;
                        animation: gradient 3s ease infinite; position: relative; overflow: hidden;">
                <div style="color: white; font-size: 2rem; font-weight: bold; text-shadow: 0 0 20px rgba(255,255,255,0.8); z-index: 2;">
                    ATM Analytics Video
                </div>
                <div style="position: absolute; top: 0; left: -100%; width: 100%; height: 100%; 
                            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                            animation: shimmer 2s infinite;"></div>
            </div>
        </video>
    </div>
    """

def create_image_gallery():
    """Create animated image gallery"""
    return """
    <div class="image-gallery">
        <div class="gallery-image">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgIDxkZWZzPgogICAgICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZDEiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICAgICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMDBmZmZmO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICAgICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmZjAwZmY7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICAgICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDwvZGVmcz4KICAgIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSJ1cmwoI2dyYWQxKSIgcng9IjIwIiAvPgogICAgPHRleHQgeD0iMTUwIiB5PSIxMDAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkFUTSBBbmFseXRpY3M8L3RleHQ+Cjwvc3ZnPg==" alt="ATM Analytics">
        </div>
        <div class="gallery-image">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgIDxkZWZzPgogICAgICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZDIiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICAgICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojZmYwMGZmO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICAgICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiMwMGZmMDA7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICAgICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDwvZGVmcz4KICAgIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSJ1cmwoI2dyYWQyKSIgcng9IjIwIiAvPgogICAgPHRleHQgeD0iMTUwIiB5PSIxMDAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPlRyYW5zYWN0aW9uczwvdGV4dD4KPC9zdmc+" alt="Transactions">
        </div>
        <div class="gallery-image">
            <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgIDxkZWZzPgogICAgICAgIDxsaW5lYXJHcmFkaWVudCBpZD0iZ3JhZDMiIHgxPSIwJSIgeTE9IjAlIiB4Mj0iMTAwJSIgeTI9IjEwMCUiPgogICAgICAgICAgICA8c3RvcCBvZmZzZXQ9IjAlIiBzdHlsZT0ic3RvcC1jb2xvcjojMDBmZjAwO3N0b3Atb3BhY2l0eToxIiAvPgogICAgICAgICAgICA8c3RvcCBvZmZzZXQ9IjEwMCUiIHN0eWxlPSJzdG9wLWNvbG9yOiNmZmZmMDA7c3RvcC1vcGFjaXR5OjEiIC8+CiAgICAgICAgPC9saW5lYXJHcmFkaWVudD4KICAgIDwvZGVmcz4KICAgIDxyZWN0IHdpZHRoPSIzMDAiIGhlaWdodD0iMjAwIiBmaWxsPSJ1cmwoI2dyYWQzKSIgcng9IjIwIiAvPgogICAgPHRleHQgeD0iMTUwIiB5PSIxMDAiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxOCIgZmlsbD0id2hpdGUiIHRleHQtYW5jaG9yPSJtaWRkbGUiPkRhc2hib2FyZDwvdGV4dD4KPC9zdmc+" alt="Dashboard">
        </div>
    </div>
    """

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

def create_dark_location_chart(df):
    """Create dark theme bar chart for transactions by location"""
    if df.empty:
        return go.Figure()
    
    location_counts = df['atm_location'].value_counts().reset_index()
    location_counts.columns = ['Location', 'Transactions']
    
    # Dark theme colors
    colors = ['#00ffff', '#ff00ff', '#00ff00', '#ffff00', '#ff6600']
    
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
            'font': {'size': 24, 'color': '#00ffff', 'weight': 'bold'}
        },
        xaxis_title="Location",
        yaxis_title="Number of Transactions",
        height=500,
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.6)',
        font=dict(color='white', size=14),
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        tickangle=45, 
        gridcolor='rgba(0, 255, 255, 0.2)',
        tickfont=dict(size=12, weight='bold', color='white')
    )
    fig.update_yaxes(
        gridcolor='rgba(255, 0, 255, 0.2)',
        tickfont=dict(size=12, weight='bold', color='white')
    )
    
    return fig

def create_dark_hourly_chart(df):
    """Create dark theme line chart for hourly transaction pattern"""
    if df.empty:
        return go.Figure()
    
    hourly_counts = df['hour'].value_counts().sort_index().reset_index()
    hourly_counts.columns = ['Hour', 'Transactions']
    
    fig = go.Figure()
    
    # Add neon line
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='lines+markers',
        line=dict(
            color='#00ffff',
            width=5,
            shape='spline'
        ),
        marker=dict(
            color='#ff00ff',
            size=12,
            symbol='diamond',
            line=dict(color='white', width=2)
        ),
        hovertemplate='<b>Hour: %{x}:00</b><br>Transactions: %{y}<extra></extra>'
    ))
    
    # Add glow area fill
    fig.add_trace(go.Scatter(
        x=hourly_counts['Hour'],
        y=hourly_counts['Transactions'],
        mode='none',
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.2)',
        showlegend=False,
        hoverinfo='none'
    ))
    
    fig.update_layout(
        title={
            'text': 'Transaction Volume by Hour',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'color': '#00ffff', 'weight': 'bold'}
        },
        xaxis_title="Hour of Day",
        yaxis_title="Number of Transactions",
        height=500,
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.6)',
        font=dict(color='white', size=14),
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        dtick=1, 
        gridcolor='rgba(0, 255, 255, 0.2)',
        tickfont=dict(size=12, weight='bold', color='white')
    )
    fig.update_yaxes(
        gridcolor='rgba(255, 0, 255, 0.2)',
        tickfont=dict(size=12, weight='bold', color='white')
    )
    
    return fig

def create_dark_transaction_type_chart(df):
    """Create dark theme pie chart for transaction types"""
    if df.empty:
        return go.Figure()
    
    type_counts = df['transaction_type'].value_counts().reset_index()
    type_counts.columns = ['Transaction Type', 'Count']
    
    # Neon color palette
    colors = ['#00ffff', '#ff00ff', '#00ff00', '#ffff00']
    
    fig = go.Figure(data=[
        go.Pie(
            labels=type_counts['Transaction Type'],
            values=type_counts['Count'],
            hole=0.4,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='auto',
            textfont=dict(color='black', size=14, weight='bold'),
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
            'font': {'size': 24, 'color': '#00ffff', 'weight': 'bold'}
        },
        height=500,
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.6)',
        font=dict(color='white', size=14),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.05,
            font=dict(size=12, weight='bold', color='white')
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

def create_dark_amount_chart(df):
    """Create dark theme bar chart for total amount by location"""
    if df.empty:
        return go.Figure()
    
    amount_by_location = df.groupby('atm_location')['amount'].sum().reset_index()
    amount_by_location = amount_by_location.sort_values('amount', ascending=False)
    
    # Dark theme colors
    colors = ['#00ff00', '#ffff00', '#ff6600', '#00ffff', '#ff00ff']
    
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
            'font': {'size': 24, 'color': '#00ffff', 'weight': 'bold'}
        },
        xaxis_title="Location",
        yaxis_title="Total Amount ($)",
        height=500,
        plot_bgcolor='rgba(0, 0, 0, 0.8)',
        paper_bgcolor='rgba(0, 0, 0, 0.6)',
        font=dict(color='white', size=14),
        showlegend=False,
        hovermode='x unified',
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    fig.update_xaxes(
        tickangle=45, 
        gridcolor='rgba(0, 255, 0, 0.2)',
        tickfont=dict(size=12, weight='bold', color='white')
    )
    fig.update_yaxes(
        tickprefix='$', 
        gridcolor='rgba(255, 255, 0, 0.2)',
        tickfont=dict(size=12, weight='bold', color='white')
    )
    
    return fig

def generate_dark_insights(df, metrics):
    """Generate dark theme insights from the data"""
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
    """Main Streamlit application with dark theme and animations"""
    # Apply dark animated styling
    set_dark_animated_style()
    
    # Add animated background
    st.markdown(create_animated_background(), unsafe_allow_html=True)
    
    # Animated header
    st.markdown('<h1 class="main-header">ATM Transaction Analysis Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #00ffff; font-size: 1.3rem; animation: fadeIn 2s ease-out; font-weight: 600; text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);">Real-time insights and analytics for ATM operations</p>', unsafe_allow_html=True)
    
    # Video section
    st.markdown('<h2 class="section-header">Analytics Overview</h2>', unsafe_allow_html=True)
    st.markdown(create_video_placeholder(), unsafe_allow_html=True)
    
    # Image gallery
    st.markdown('<h2 class="section-header">Visual Analytics</h2>', unsafe_allow_html=True)
    st.markdown(create_image_gallery(), unsafe_allow_html=True)
    
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
    
    # Dark sidebar for filters
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
    
    # Dark Key Metrics Section
    st.markdown('<h2 class="section-header">Key Performance Metrics</h2>', unsafe_allow_html=True)
    
    # Create dark animated metric cards
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
    
    # Dark Charts Section
    st.markdown('<h2 class="section-header">Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    # Row 1: Location and Hourly charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_location = create_dark_location_chart(filtered_df)
        st.plotly_chart(fig_location, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_hourly = create_dark_hourly_chart(filtered_df)
        st.plotly_chart(fig_hourly, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Row 2: Transaction Type and Amount charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_type = create_dark_transaction_type_chart(filtered_df)
        st.plotly_chart(fig_type, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        fig_amount = create_dark_amount_chart(filtered_df)
        st.plotly_chart(fig_amount, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Dark Insights Section
    st.markdown('<h2 class="section-header">Business Insights</h2>', unsafe_allow_html=True)
    
    insights = generate_dark_insights(filtered_df, metrics)
    
    for i, insight in enumerate(insights):
        # Add delay animation for each insight
        st.markdown(f"""
        <div class="insight-box" style="animation-delay: {i * 0.3}s">
            <div class="insight-title">{insight['title']}</div>
            <div class="insight-text">{insight['text']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Dark Data Table Section
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
    st.markdown('<p style="text-align: center; color: #00ffff; animation: fadeIn 2.5s ease-out; font-weight: 600; text-shadow: 0 0 20px rgba(0, 255, 255, 0.8);">ATM Transaction Analysis Dashboard | Dark Theme Analytics Platform</p>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
