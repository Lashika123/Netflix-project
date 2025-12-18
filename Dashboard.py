import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import re
from datetime import datetime, timedelta
from collections import Counter
import warnings
from plotly.subplots import make_subplots
warnings.filterwarnings("ignore")

# ----------------------------
# Enhanced Color Palettes Definition
# ----------------------------
VIBRANT_PALETTES = {
    'rainbow': ['#FF355E', '#FD5B78', '#FF6037', '#FF9966', '#FF9933', 
                '#FFCC33', '#FFFF66', '#CCFF00', '#66FF66', '#50BFE6',
                '#FF6EFF', '#EE34D2', '#FF00CC', '#FF3855', '#FFD700'],
    
    'vibrant': ['#FF0000', '#FF4D00', '#FF8000', '#FFB300', '#FFE600',
                '#CCFF00', '#80FF00', '#33FF00', '#00FF66', '#00FFCC',
                '#00FFFF', '#00BFFF', '#0080FF', '#0040FF', '#0000FF'],
    
    'electric': ['#FF00FF', '#00FFFF', '#FFFF00', '#FF0080', '#00FF80',
                 '#8000FF', '#FF8000', '#00FF00', '#FF0000', '#0000FF',
                 '#FF00CC', '#00FFCC', '#FFCC00', '#CC00FF', '#00CCFF'],
    
    'neon_gradient': ['#FF00FF', '#FF0080', '#FF0066', '#FF0044', '#FF0022',
                      '#FF0000', '#FF3300', '#FF6600', '#FF9900', '#FFCC00',
                      '#FFFF00', '#CCFF00', '#99FF00', '#66FF00', '#33FF00'],
    
    'jewel_bright': ['#FF0000', '#FF6A00', '#FFD700', '#ADFF2F', '#32CD32',
                     '#00FA9A', '#00CED1', '#1E90FF', '#4169E1', '#8A2BE2',
                     '#FF00FF', '#FF1493', '#FF4500', '#FF8C00', '#FFD700'],
    
    'cyberpunk': ['#FF00FF', '#00FFFF', '#FFFF00', '#FF0066', '#00FF99',
                  '#6600FF', '#FF6600', '#00FF00', '#FF0000', '#0066FF',
                  '#FF0099', '#00FFCC', '#FFCC00', '#CC00FF', '#00CCFF'],
    
    'fire': ['#FF0000', '#FF3300', '#FF6600', '#FF9900', '#FFCC00',
             '#FFFF00', '#FFCC33', '#FF9966', '#FF6699', '#FF33CC',
             '#FF00FF', '#FF33FF', '#FF66FF', '#FF99FF', '#FFCCFF'],
    
    'ocean_waves': ['#0000FF', '#0033FF', '#0066FF', '#0099FF', '#00CCFF',
                    '#00FFFF', '#33FFFF', '#66FFFF', '#99FFFF', '#CCFFFF',
                    '#CCCCFF', '#9999FF', '#6666FF', '#3333FF', '#0000CC'],
    
    'content_type': ['#FF0000', '#00FF00'],  # Red for Movies, Green for TV Shows
    
    'tv_seasons': ['#FF0000', '#FF3300', '#FF6600', '#FF9900', '#FFCC00',
                   '#FFFF00', '#CCFF00', '#99FF00', '#66FF00', '#33FF00',
                   '#00FF00', '#00FF33', '#00FF66', '#00FF99', '#00FFCC']
}

NETFLIX_RED = '#E50914'

# ----------------------------
# Page config & Netflix-Themed CSS
# ----------------------------
st.set_page_config(page_title="Netflix Content Analytics Dashboard",
                   page_icon="🎬", 
                   layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Netflix Theme Styling */
html, body, .stApp { 
    background: #141414;
    color: #ffffff;
    font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

/* Netflix Red Header */
.header-container {
    background: linear-gradient(135deg, #141414 0%, #181818 100%);
    padding: 2.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    border-left: 6px solid #E50914;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
    position: relative;
    overflow: hidden;
}

.header-container::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 200px;
    height: 200px;
    background: radial-gradient(circle, rgba(229,9,20,0.15) 0%, transparent 70%);
    z-index: 0;
}

.header-title {
    font-size: 3rem;
    font-weight: 900;
    color: white;
    margin-bottom: 0.5rem;
    background: linear-gradient(90deg, #E50914 0%, #B81D24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
    position: relative;
    z-index: 1;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}

.header-sub {
    color: #b3b3b3;
    font-size: 1.2rem;
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
    font-weight: 300;
}

/* Netflix-style KPI Cards */
.kpi-card {
    background: linear-gradient(145deg, #1f1f1f 0%, #2a2a2a 100%);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid #333333;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    height: 140px;
    display: flex;
    flex-direction: column;
    position: relative;
    overflow: hidden;
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(229, 9, 20, 0.3);
    border-color: #E50914;
}

.kpi-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    z-index: 2;
}

.kpi-label {
    font-size: 0.8rem;
    color: #808080;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 700;
    margin-bottom: 0.5rem;
    line-height: 1.2;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.kpi-value {
    font-size: 2rem;
    font-weight: 900;
    color: #ffffff;
    line-height: 1.1;
    margin: 0.25rem 0;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.kpi-change {
    font-size: 0.8rem;
    font-weight: 600;
    margin-top: 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.25rem;
}

.kpi-icon {
    font-size: 2.5rem;
    position: absolute;
    right: 1.5rem;
    bottom: 1.5rem;
    opacity: 0.2;
    z-index: 1;
    transition: all 0.3s ease;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.8);
}

.kpi-card:hover .kpi-icon {
    opacity: 0.3;
    transform: scale(1.1);
}

/* Netflix-themed Section Headers */
.section-header {
    background: linear-gradient(90deg, rgba(20,20,20,0.95) 0%, rgba(40,40,40,0.95) 100%);
    padding: 1.5rem 2rem;
    border-radius: 12px;
    margin: 3rem 0 2rem 0;
    border-left: 6px solid #E50914;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    position: relative;
    overflow: hidden;
}

.section-header::before {
    content: 'NETFLIX';
    position: absolute;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 4rem;
    font-weight: 900;
    color: rgba(229, 9, 20, 0.05);
    font-family: 'Netflix Sans', sans-serif;
    letter-spacing: 2px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    position: relative;
    z-index: 1;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.section-subtitle {
    font-size: 1rem;
    color: #b3b3b3;
    margin: 0.5rem 0 0 0;
    position: relative;
    z-index: 1;
    font-weight: 300;
}

/* Chart Containers */
.chart-container {
    background: linear-gradient(145deg, #1a1a1a 0%, #242424 100%);
    padding: 1.75rem;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    margin-bottom: 2rem;
    border: 1px solid #333333;
    transition: all 0.3s ease;
}

.chart-container:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5);
    border-color: #404040;
}

/* Enhanced Sidebar */
.css-1d391kg, .css-1lcbmhc {
    background: #181818;
    border-right: 1px solid #333333;
}

/* Filter Header - WHITE TEXT */
.filter-header {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%);
    padding: 1.25rem;
    border-radius: 10px;
    margin-bottom: 1.5rem;
    border-left: 4px solid #E50914;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    color: #ffffff !important;
    font-size: 1.2rem !important;
    font-weight: 700 !important;
}

/* Sidebar labels - WHITE TEXT */
div[data-testid="stSidebar"] label {
    color: #ffffff !important;
    font-weight: 600 !important;
}

div[data-testid="stSidebar"] .stSelectbox label,
div[data-testid="stSidebar"] .stMultiselect label,
div[data-testid="stSidebar"] .stSlider label,
div[data-testid="stSidebar"] .stCheckbox label,
div[data-testid="stSidebar"] .stRadio label {
    color: #ffffff !important;
}

/* Metric Badges */
.metric-badge {
    display: inline-block;
    padding: 0.5rem 1.25rem;
    background: linear-gradient(135deg, rgba(229,9,20,0.15) 0%, rgba(184,29,36,0.15) 100%);
    color: #ffffff;
    border-radius: 25px;
    font-size: 0.9rem;
    font-weight: 600;
    margin-right: 0.75rem;
    margin-bottom: 0.75rem;
    border: 1px solid rgba(229, 9, 20, 0.3);
    transition: all 0.3s ease;
    backdrop-filter: blur(10px);
}

.metric-badge:hover {
    background: linear-gradient(135deg, rgba(229,9,20,0.25) 0%, rgba(184,29,36,0.25) 100%);
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(229, 9, 20, 0.3);
    border-color: #E50914;
}

/* Netflix-style Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: #1a1a1a;
    padding: 0.75rem;
    border-radius: 12px;
    border: 1px solid #333333;
}

.stTabs [data-baseweb="tab"] {
    background-color: #2a2a2a;
    border-radius: 10px;
    padding: 1rem 2rem;
    border: 1px solid #333333;
    color: #b3b3b3;
    font-weight: 700;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.stTabs [data-baseweb="tab"]:hover {
    background-color: #333333;
    color: #ffffff;
    border-color= #404040;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #E50914 0%, #B81D24 100%) !important;
    color: white !important;
    border-color: #E50914 !important;
    box-shadow: 0 6px 12px rgba(229, 9, 20, 0.4);
    transform: translateY(-1px);
}

/* Data Table */
.dataframe {
    background: #1a1a1a;
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid #333333;
    font-size: 0.9rem;
}

.dataframe th {
    background: linear-gradient(135deg, #2a2a2a 0%, #1f1f1f 100%) !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    border-bottom: 2px solid #E50914 !important;
    padding: 1rem !important;
}

.dataframe td {
    background: #242424 !important;
    color: #ffffff !important;
    border-bottom: 1px solid #333333 !important;
    padding: 0.75rem !important;
}

.dataframe tr:hover {
    background: rgba(229, 9, 20, 0.1) !important;
}

/* Feature Cards */
.feature-card {
    background: linear-gradient(145deg, #1f1f1f 0%, #2a2a2a 100%);
    border-radius: 14px;
    padding: 2rem;
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    border: 1px solid #333333;
    margin-bottom: 2rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    height: 100%;
}

.feature-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(229, 9, 20, 0.2);
    border-color: #E50914;
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1.5rem;
    background: linear-gradient(135deg, #E50914 0%, #B81D24 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: inline-block;
    text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Netflix Badge */
.feature-badge {
    display: inline-block;
    padding: 0.5rem 1.25rem;
    background: linear-gradient(135deg, #E50914 0%, #B81D24 100%);
    color: white;
    border-radius: 25px;
    font-size: 0.8rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0 4px 8px rgba(229, 9, 20, 0.3);
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #1a1a1a;
    border-radius: 5px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #E50914 0%, #B81D24 100%);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #ff0a16 0%, #c11119 100%);
}

/* Button Styles */
.stButton > button {
    background: linear-gradient(135deg, #E50914 0%, #B81D24 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    font-weight: 700;
    font-size: 0.9rem;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(229, 9, 20, 0.4);
    background: linear-gradient(135deg, #ff0a16 0%, #c11119 100%);
}

/* Select Box */
.stSelectbox > div > div {
    background: #2a2a2a;
    border: 1px solid #333333;
    color: #ffffff;
    border-radius: 8px;
}

.stSelectbox > div > div:hover {
    border-color: #E50914;
}

/* Slider */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #E50914 0%, #B81D24 100%);
}

/* Info Box */
.stAlert {
    background: rgba(229, 9, 20, 0.1) !important;
    border: 1px solid rgba(229, 9, 20, 0.3) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
}

/* Divider */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent 0%, #E50914 50%, transparent 100%);
    margin: 2rem 0;
}

/* Progress Bar */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #E50914 0%, #B81D24 100%);
}

/* Checkbox - WHITE TEXT */
.stCheckbox > label {
    color: #ffffff !important;
    font-weight: 400;
}

/* Metric Container */
[data-testid="metric-container"] {
    background: linear-gradient(145deg, #1f1f1f 0%, #2a2a2a 100%);
    border: 1px solid #333333;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

[data-testid="metric-container"]:hover {
    border-color: #E50914;
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(229, 9, 20, 0.2);
}

/* Radio Buttons - WHITE TEXT */
.stRadio > label {
    color: #ffffff !important;
    font-weight: 400;
}

.stRadio > div > label {
    background: #2a2a2a !important;
    border-color= #333333 !important;
}

.stRadio > div > label:hover {
    border-color: #E50914 !important;
}

/* Text Input */
.stTextInput > div > div > input {
    background: #2a2a2a !important;
    color: #ffffff !important;
    border-color: #333333 !important;
    border-radius: 8px;
}

.stTextInput > div > div > input:focus {
    border-color: #E50914 !important;
    box-shadow: 0 0 0 1px #E50914 !important;
}

/* Multi-select */
.stMultiSelect > div > div {
    background: #2a2a2a !important;
    border-color: #333333 !important;
    color: #ffffff !important;
}

.stMultiSelect > div > div:hover {
    border-color: #E50914 !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #2a2a2a !important;
    color: #ffffff !important;
    border-radius: 8px !important;
    border: 1px solid #333333 !important;
    font-weight: 600 !important;
}

.streamlit-expanderHeader:hover {
    background: #333333 !important;
    border-color: #E50914 !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #808080;
    font-size: 0.9rem;
    margin-top: 3rem;
    padding: 2rem;
    border-top: 1px solid #333333;
}

/* Responsive Design */
@media (max-width: 768px) {
    .header-title {
        font-size: 2rem;
    }
    
    .kpi-value {
        font-size: 1.5rem;
    }
    
    .metric-badge {
        font-size: 0.8rem;
        padding: 0.4rem 0.8rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ----------------------------
# Helper Functions
# ----------------------------
def safe_extract_number(s):
    if pd.isna(s):
        return np.nan
    m = re.search(r"(\d+\.?\d*)", str(s))
    return float(m.group(1)) if m else np.nan

def create_metric_card(label, value, change=None, icon="📊"):
    """Create Netflix-style metric card"""
    if change is not None:
        change_color = "#1DB954" if change > 0 else "#E50914"
        change_icon = "↗" if change > 0 else "↘"
        change_html = f'<span class="kpi-change" style="color: {change_color};">{change_icon} {abs(change):.1f}%</span>'
    else:
        change_html = ""
    
    return f"""
    <div class="kpi-card">
        <div class="kpi-content">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {change_html}
        </div>
        <div class="kpi-icon">{icon}</div>
    </div>
    """

def apply_vibrant_theme(fig, title=None, height=None, showlegend=True):
    """Apply vibrant theme to plotly chart"""
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.7)',
        paper_bgcolor='rgba(26, 26, 26, 0.7)',
        font=dict(
            family="'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif",
            color='white',
            size=12
        ),
        title=dict(
            text=title,
            font=dict(
                family="'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif",
                size=20,
                color='white',
                weight='bold'
            ),
            x=0.5,
            y=0.95,
            xanchor='center'
        ) if title else None,
        hovermode='closest',
        hoverlabel=dict(
            bgcolor='#E50914',
            font_size=12,
            font_family="'Netflix Sans', sans-serif",
            font_color='white'
        ),
        margin=dict(l=50, r=50, t=100 if title else 50, b=80),
        height=height or 450,
        autosize=True,
        showlegend=showlegend
    )
    
    if showlegend:
        fig.update_layout(
            legend=dict(
                bgcolor='rgba(26, 26, 26, 0.9)',
                bordercolor='#E50914',
                borderwidth=2,
                font=dict(color='white', size=11),
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
    
    fig.update_xaxes(
        gridcolor='rgba(80, 80, 80, 0.3)',
        gridwidth=1,
        zerolinecolor='rgba(80, 80, 80, 0.3)',
        linecolor='rgba(229, 9, 20, 0.5)',
        tickfont=dict(color='white', size=11),
        title_font=dict(color='white', size=13, weight='bold'),
        showgrid=True,
        ticks="outside",
        tickcolor='#E50914',
        linewidth=2
    )
    
    fig.update_yaxes(
        gridcolor='rgba(80, 80, 80, 0.3)',
        gridwidth=1,
        zerolinecolor='rgba(80, 80, 80, 0.3)',
        linecolor='rgba(229, 9, 20, 0.5)',
        tickfont=dict(color='white', size=11),
        title_font=dict(color='white', size=13, weight='bold'),
        showgrid=True,
        ticks="outside",
        tickcolor='#E50914',
        linewidth=2
    )
    
    return fig

def create_vibrant_bar_chart(df, x_col, y_col, title, palette='vibrant', height=400, showlegend=False):
    """Create vibrant bar chart with visible data"""
    colors = VIBRANT_PALETTES.get(palette, VIBRANT_PALETTES['vibrant'])
    
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    
    # Apply vibrant colors to each bar
    fig.update_traces(
        marker_color=[colors[i % len(colors)] for i in range(len(df))],
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>',
        marker_line_color='white',
        marker_line_width=1.5,
        texttemplate='%{y}',
        textposition='outside',
        textfont=dict(color='white', size=11, weight='bold')
    )
    
    return apply_vibrant_theme(fig, title, height, showlegend=showlegend)

def create_vibrant_line_chart(df, x_col, y_col, title, palette='neon_gradient', height=400, showlegend=False):
    """Create vibrant line chart"""
    colors = VIBRANT_PALETTES.get(palette, VIBRANT_PALETTES['neon_gradient'])
    
    fig = px.line(df, x=x_col, y=y_col, title=title)
    
    fig.update_traces(
        line=dict(width=4, color=colors[0]),
        mode='lines+markers',
        marker=dict(size=10, color=colors[0], line=dict(width=2, color='white')),
        hovertemplate='<b>%{x}</b><br>Value: %{y}<extra></extra>'
    )
    
    return apply_vibrant_theme(fig, title, height, showlegend=showlegend)

def create_vibrant_pie_chart(labels, values, title, palette='rainbow', height=400):
    """Create vibrant pie chart with visible labels"""
    colors = VIBRANT_PALETTES.get(palette, VIBRANT_PALETTES['rainbow'])
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(
            colors=colors[:len(labels)],
            line=dict(color='white', width=2)
        ),
        textinfo='label+percent+value',
        textposition='outside',
        textfont=dict(color='white', size=12, weight='bold'),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
        pull=[0.05 if i < 3 else 0 for i in range(len(labels))]
    )])
    
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.7)',
        paper_bgcolor='rgba(26, 26, 26, 0.7)',
        title=dict(
            text=title,
            font=dict(size=20, color='white', weight='bold'),
            x=0.5
        ),
        legend=dict(
            font=dict(color='white', size=11),
            bgcolor='rgba(26, 26, 26, 0.9)',
            bordercolor='#E50914',
            borderwidth=2
        ),
        height=height,
        margin=dict(t=100, b=100, l=50, r=50),
        showlegend=True
    )
    
    return fig

def create_vibrant_histogram(df, x_col, title, palette='jewel_bright', height=400, showlegend=False):
    """Create vibrant histogram"""
    colors = VIBRANT_PALETTES.get(palette, VIBRANT_PALETTES['jewel_bright'])
    
    fig = px.histogram(df, x=x_col, nbins=20, title=title)
    
    fig.update_traces(
        marker_color=colors[0],
        marker_line_color='white',
        marker_line_width=1.5,
        hovertemplate='<b>Range: %{x}</b><br>Count: %{y}<extra></extra>',
        texttemplate='%{y}',
        textposition='inside',
        textfont=dict(color='white', size=10, weight='bold')
    )
    
    return apply_vibrant_theme(fig, title, height, showlegend=showlegend)

def create_vibrant_area_chart(df, x_col, y_col, title, palette='fire', height=400, showlegend=False):
    """Create vibrant area chart"""
    colors = VIBRANT_PALETTES.get(palette, VIBRANT_PALETTES['fire'])
    
    fig = px.area(df, x=x_col, y=y_col, title=title)
    
    # Convert hex to rgba for fill
    rgb = tuple(int(colors[0].lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    
    fig.update_traces(
        fillcolor=f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, 0.6)',
        line_color=colors[0],
        line_width=3,
        hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
    )
    
    return apply_vibrant_theme(fig, title, height, showlegend=showlegend)

def calculate_content_score(row):
    """Calculate Netflix-style content quality score"""
    score = 0
    
    if not pd.isna(row.get('content_age')):
        age_score = max(0, 100 - (row['content_age'] * 1.5))
        score += age_score * 0.35
    
    if row['type'] == 'Movie' and not pd.isna(row.get('movie_minutes')):
        duration = row['movie_minutes']
        if 90 <= duration <= 120:
            score += 40
        elif 75 <= duration < 90 or 120 < duration <= 150:
            score += 30
        else:
            score += 20
    elif row['type'] == 'TV Show' and not pd.isna(row.get('tv_seasons')):
        seasons = row['tv_seasons']
        if 2 <= seasons <= 4:
            score += 40
        elif 1 == seasons or 5 <= seasons <= 6:
            score += 30
        else:
            score += 20
    
    rating_scores = {
        'TV-MA': 35, 'TV-14': 30, 'R': 30,
        'TV-PG': 25, 'PG-13': 25, 'PG': 20
    }
    score += rating_scores.get(str(row.get('rating', '')), 15)
    
    return min(100, max(0, int(score)))

# ----------------------------
# Load and Preprocess Data - ONLY netflix_cleaned.csv
# ----------------------------
@st.cache_data
def load_and_process_data():
    try:
        df = pd.read_csv("netflix_cleaned.csv")
        st.success("✅ Successfully loaded netflix_cleaned.csv")
    except FileNotFoundError:
        st.error("❌ 'netflix_cleaned.csv' file not found. Please ensure the file is in the same directory.")
        uploaded_file = st.file_uploader("📂 Upload Netflix CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            st.stop()
    
    df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
    
    column_mapping = {
        'type': ['type', 'content_type', 'show_type'],
        'title': ['title', 'name', 'show_title'],
        'release_year': ['release_year', 'year', 'release_date'],
        'rating': ['rating', 'content_rating', 'age_rating'],
        'duration': ['duration', 'run_time', 'length'],
        'country': ['country', 'countries', 'country_of_origin'],
        'listed_in': ['listed_in', 'genres', 'genre', 'category'],
        'date_added': ['date_added', 'added_date', 'netflix_added_date'],
        'director': ['director', 'directors']
    }
    
    for standard_name, possible_names in column_mapping.items():
        for possible in possible_names:
            if possible in df.columns:
                df.rename(columns={possible: standard_name}, inplace=True)
                break
    
    expected = ['type', 'title', 'release_year', 'rating', 'duration', 'country', 'listed_in']
    for col in expected:
        if col not in df.columns:
            df[col] = np.nan
    
    df['type'] = df['type'].fillna("Unknown").astype(str).str.strip()
    df['title'] = df['title'].fillna("").astype(str).str.strip()
    
    df['type'] = df['type'].replace({
        'Movie': 'Movie',
        'movie': 'Movie',
        'MOVIE': 'Movie',
        'TV Show': 'TV Show',
        'TV show': 'TV Show',
        'TV SHOW': 'TV Show',
        'Tv Show': 'TV Show',
        'Series': 'TV Show',
        'TV Series': 'TV Show'
    })
    
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce', dayfirst=False)
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
    df['duration_num'] = df['duration'].apply(safe_extract_number)
    
    def extract_seasons(duration_text):
        if pd.isna(duration_text):
            return np.nan
        text = str(duration_text).lower()
        if 'season' in text:
            return safe_extract_number(text)
        return np.nan
    
    def extract_minutes(duration_text):
        if pd.isna(duration_text):
            return np.nan
        text = str(duration_text).lower()
        if 'min' in text:
            return safe_extract_number(text)
        return np.nan
    
    df['movie_minutes'] = df['duration'].apply(extract_minutes)
    df['tv_seasons'] = df['duration'].apply(extract_seasons)
    
    df['genre_list'] = df['listed_in'].fillna("").apply(
        lambda x: [g.strip() for g in str(x).split(",") if g.strip()])
    
    df['country_list'] = df['country'].fillna("").apply(
        lambda x: [c.strip() for c in str(x).split(",") if c.strip()])
    
    df['year_added'] = df['date_added'].dt.year
    df['month_added'] = df['date_added'].dt.month
    df['quarter_added'] = df['date_added'].dt.quarter
    df['content_age'] = datetime.now().year - df['release_year']
    df['decade'] = (df['release_year'] // 10) * 10
    
    df['content_score'] = df.apply(calculate_content_score, axis=1)
    
    df['quality_category'] = pd.cut(df['content_score'], 
                                    bins=[0, 40, 70, 85, 100],
                                    labels=['Basic', 'Standard', 'Premium', 'Ultra'])
    
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    df['month_name'] = df['month_added'].apply(lambda x: month_names[int(x)-1] if not pd.isna(x) and 1 <= x <= 12 else 'Unknown')
    
    return df

# ----------------------------
# Main App
# ----------------------------
def main():
    df = load_and_process_data()
    
    # Calculate global metrics for display
    total_titles_all = len(df)
    movies_all = (df['type'] == 'Movie').sum()
    tv_shows_all = (df['type'] == 'TV Show').sum()
    unique_countries_all = df['country_list'].explode().nunique()
    avg_content_score = df['content_score'].mean()
    
    # Netflix Header
    st.markdown(f"""
    <div class="header-container">
        <h1 class="header-title">🎬 NETFLIX CONTENT ANALYTICS</h1>
        <p class="header-sub">Interactive Dashboard | Comprehensive Content Analysis</p>
        <div style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 2rem;">
            <span class="metric-badge">📊 {total_titles_all:,} TOTAL TITLES</span>
            <span class="metric-badge">🎥 {movies_all:,} MOVIES</span>
            <span class="metric-badge">📺 {tv_shows_all:,} TV SHOWS</span>
            <span class="metric-badge">🌍 {unique_countries_all:,} COUNTRIES</span>
            <span class="metric-badge">⭐ {avg_content_score:.0f}/100 AVG SCORE</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Filters
    with st.sidebar:
        st.markdown('<div class="filter-header">🔍 FILTER CONTENT</div>', unsafe_allow_html=True)
        
        type_options = ['All'] + sorted(df['type'].dropna().unique().tolist())
        selected_type = st.multiselect(
            "Content Type",
            options=type_options[1:],
            default=['Movie', 'TV Show'] if 'Movie' in type_options and 'TV Show' in type_options else type_options[1:3]
        )
        
        min_year = int(df['release_year'].min()) if not df['release_year'].isna().all() else 1900
        max_year = int(df['release_year'].max()) if not df['release_year'].isna().all() else datetime.now().year
        year_range = st.slider(
            "Release Year Range",
            min_year, max_year,
            (max(min_year, 2000), max_year)
        )
        
        quality_options = ['All', 'Ultra (85-100)', 'Premium (70-85)', 'Standard (40-70)', 'Basic (0-40)']
        selected_quality = st.selectbox("Quality Tier", options=quality_options, index=0)
        
        # FIX FOR RATING ERROR - SIMPLIFIED SOLUTION
        # Get the actual ratings available in the data
        available_ratings = sorted(df['rating'].dropna().unique().tolist())
        
        # Don't set any default ratings - let user choose from what's available
        selected_rating = st.multiselect(
            "Content Rating",
            options=available_ratings,
            default=[]  # NO DEFAULT VALUES - EMPTY LIST
        )
        
        try:
            all_genres = sorted(set([g for sublist in df['genre_list'] for g in sublist]))
            
            # Don't set any default genres
            selected_genres = st.multiselect(
                "Genres",
                options=all_genres,
                default=[],  # NO DEFAULT VALUES - EMPTY LIST
                max_selections=5
            )
        except:
            selected_genres = []
        
        try:
            top_countries = df['country_list'].explode().value_counts().head(20).index.tolist()
            
            # Don't set any default countries
            selected_countries = st.multiselect(
                "Countries",
                options=top_countries,
                default=[]  # NO DEFAULT VALUES - EMPTY LIST
            )
        except:
            selected_countries = []
    
    # Apply Filters
    filtered_df = df.copy()
    
    if selected_type and 'All' not in selected_type:
        filtered_df = filtered_df[filtered_df['type'].isin(selected_type)]
    
    filtered_df = filtered_df[
        (filtered_df['release_year'] >= year_range[0]) & 
        (filtered_df['release_year'] <= year_range[1])
    ]
    
    if selected_quality != 'All':
        quality_map = {
            'Ultra (85-100)': (85, 100),
            'Premium (70-85)': (70, 85),
            'Standard (40-70)': (40, 70),
            'Basic (0-40)': (0, 40)
        }
        if selected_quality in quality_map:
            min_score, max_score = quality_map[selected_quality]
            filtered_df = filtered_df[
                (filtered_df['content_score'] >= min_score) & 
                (filtered_df['content_score'] <= max_score)
            ]
    
    if selected_rating:  # Only apply rating filter if user selected something
        filtered_df = filtered_df[filtered_df['rating'].isin(selected_rating)]
    
    if selected_genres:
        filtered_df = filtered_df[
            filtered_df['genre_list'].apply(
                lambda x: any(genre in x for genre in selected_genres) if x else False
            )
        ]
    
    if selected_countries:
        filtered_df = filtered_df[
            filtered_df['country_list'].apply(
                lambda x: any(country in x for country in selected_countries) if x else False
            )
        ]
    
    # KPI Metrics
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">📊 CONTENT OVERVIEW</h3>
        <p class="section-subtitle">Key metrics for filtered content</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_titles = len(filtered_df)
        pct_of_total = (total_titles / total_titles_all * 100) if total_titles_all > 0 else 0
        st.markdown(create_metric_card("Titles in View", f"{total_titles:,}", change=pct_of_total, icon="🎬"), unsafe_allow_html=True)
    
    with col2:
        movies = (filtered_df['type'] == 'Movie').sum()
        movies_pct = (movies / total_titles * 100) if total_titles > 0 else 0
        st.markdown(create_metric_card("Movies", f"{movies:,}", change=movies_pct, icon="🎥"), unsafe_allow_html=True)
    
    with col3:
        tv_shows = (filtered_df['type'] == 'TV Show').sum()
        tv_pct = (tv_shows / total_titles * 100) if total_titles > 0 else 0
        st.markdown(create_metric_card("TV Shows", f"{tv_shows:,}", change=tv_pct, icon="📺"), unsafe_allow_html=True)
    
    with col4:
        avg_score = filtered_df['content_score'].mean()
        avg_score_all = df['content_score'].mean()
        change = ((avg_score - avg_score_all) / avg_score_all * 100) if avg_score_all > 0 else 0
        st.markdown(create_metric_card("Avg Quality Score", f"{avg_score:.0f}/100", change=change, icon="⭐"), unsafe_allow_html=True)
    
    with col5:
        unique_countries = filtered_df['country_list'].explode().nunique()
        unique_countries_all = df['country_list'].explode().nunique()
        change = ((unique_countries - unique_countries_all) / unique_countries_all * 100) if unique_countries_all > 0 else 0
        st.markdown(create_metric_card("Countries", f"{unique_countries}", change=change, icon="🌍"), unsafe_allow_html=True)
    
    st.info(f"**Showing {len(filtered_df):,} titles** ({len(filtered_df)/len(df)*100:.1f}% of total library)")
    
    # Calculate metrics needed for each tab
    # Tab 2: TV Show metrics
    tv_shows_df = filtered_df[filtered_df['type'] == 'TV Show']
    total_tv_shows = len(tv_shows_df)
    avg_seasons = tv_shows_df['tv_seasons'].mean() if not tv_shows_df.empty else 0
    max_seasons = tv_shows_df['tv_seasons'].max() if not tv_shows_df.empty else 0
    tv_percentage = (total_tv_shows / total_titles * 100) if total_titles > 0 else 0
    
    # Tab 4: Quality metrics
    quality_scores = filtered_df['content_score'].dropna()
    quality_range = quality_scores.max() - quality_scores.min()
    avg_quality = quality_scores.mean()
    min_quality = quality_scores.min()
    max_quality = quality_scores.max()
    
    # Tab 4: Content Type metrics
    total_movies = movies
    total_tv_shows_global = tv_shows
    movie_percentage = (total_movies / total_titles * 100) if total_titles > 0 else 0
    tv_percentage_global = (total_tv_shows_global / total_titles * 100) if total_titles > 0 else 0
    
    # 15 VIBRANT CHARTS IN TABS
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 TRENDS & GROWTH", 
        "🎭 GENRE & CONTENT", 
        "🌍 GEOGRAPHY", 
        "⚡ QUALITY & RATINGS"
    ])
    
    with tab1:
        st.markdown("### 📈 Content Trends & Growth Analysis")
        
        # Chart 1: Yearly Content Additions - Area Chart
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📈 Yearly Content Additions")
            yearly_additions = filtered_df.groupby('year_added').size().reset_index(name='count').sort_values('year_added')
            if not yearly_additions.empty and len(yearly_additions) > 1:
                fig1 = create_vibrant_area_chart(
                    yearly_additions,
                    'year_added',
                    'count',
                    "Content Additions by Year",
                    palette='fire',
                    height=450,
                    showlegend=False
                )
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("Insufficient date data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 2: Monthly Patterns - Bar Chart
        with col2:
            st.markdown("#### 📅 Monthly Addition Patterns")
            if filtered_df['month_added'].notna().any():
                monthly_counts = filtered_df['month_added'].value_counts().sort_index()
                monthly_df = pd.DataFrame({'month': range(1, 13)})
                monthly_df['count'] = monthly_df['month'].map(monthly_counts).fillna(0)
                monthly_df['month_name'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                
                fig2 = create_vibrant_bar_chart(
                    monthly_df,
                    'month_name',
                    'count',
                    "Content Additions by Month",
                    palette='cyberpunk',
                    height=450,
                    showlegend=False
                )
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No monthly data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 3: Release Trends by Decade - Line Chart
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🗓️ Release Trends by Decade")
            decade_counts = filtered_df['decade'].value_counts().sort_index()
            if not decade_counts.empty:
                decade_df = pd.DataFrame({
                    'decade': decade_counts.index.astype(str),
                    'count': decade_counts.values
                })
                fig3 = create_vibrant_line_chart(
                    decade_df,
                    'decade',
                    'count',
                    "Content Release by Decade",
                    palette='electric',
                    height=450,
                    showlegend=False
                )
                st.plotly_chart(fig3, use_container_width=True)
            else:
                st.info("No decade data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 4: Quarterly Additions - Bar Chart
        with col2:
            st.markdown("#### 📊 Quarterly Content Additions")
            quarterly_counts = filtered_df.groupby('quarter_added').size().reset_index(name='count')
            if not quarterly_counts.empty:
                fig4 = create_vibrant_bar_chart(
                    quarterly_counts,
                    'quarter_added',
                    'count',
                    "Content Additions by Quarter",
                    palette='jewel_bright',
                    height=450,
                    showlegend=False
                )
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No quarterly data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 5: Growth by Content Type - Line Chart 
        st.markdown("#### 📈 Growth by Content Type")
        type_year_growth = filtered_df.groupby(['year_added', 'type']).size().reset_index(name='count')
        if not type_year_growth.empty:
            fig5 = px.line(type_year_growth, x='year_added', y='count', color='type', 
                          title="Content Growth by Type Over Years")
            
            # Apply different vibrant colors to each line - RED for Movies, GREEN for TV Shows
            content_colors = VIBRANT_PALETTES['content_type']
            
            # Map colors to content types
            color_map = {}
            unique_types = type_year_growth['type'].unique()
            for i, content_type in enumerate(unique_types):
                if i < len(content_colors):
                    color_map[content_type] = content_colors[i]
                else:
                    # Fallback to rainbow colors if more than 2 types
                    color_map[content_type] = VIBRANT_PALETTES['rainbow'][i % len(VIBRANT_PALETTES['rainbow'])]
            
            for i, trace in enumerate(fig5.data):
                trace_name = trace.name
                if trace_name in color_map:
                    trace.line.color = color_map[trace_name]
                trace.line.width = 4
                trace.marker = dict(size=10, line=dict(width=2, color='white'))
                trace.mode = 'lines+markers'
                # Add different marker symbols for each line
                marker_symbols = ['circle', 'square', 'diamond', 'triangle-up', 'pentagon']
                trace.marker.symbol = marker_symbols[i % len(marker_symbols)]
                trace.marker.size = 12
            
            # Make legend more prominent
            fig5.update_layout(
                legend=dict(
                    title=dict(text="Content Type", font=dict(color='white', size=14, weight='bold')),
                    font=dict(color='white', size=12),
                    bgcolor='rgba(26, 26, 26, 0.9)',
                    bordercolor='#E50914',
                    borderwidth=2,
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig5 = apply_vibrant_theme(fig5, "Content Growth by Type", 450, showlegend=True)
            st.plotly_chart(fig5, use_container_width=True)
            
            # Add color explanation
            col_exp1, col_exp2 = st.columns(2)
            with col_exp1:
                st.markdown("""
                <div style="background: rgba(255, 0, 0, 0.1); padding: 0.75rem; border-radius: 8px; border-left: 4px solid #FF0000; margin-top: 1rem;">
                    <p style="margin: 0; color: #ffffff; font-weight: bold;">🎥 <span style="color: #FF0000;">Red Line</span>: Movies</p>
                </div>
                """, unsafe_allow_html=True)
            with col_exp2:
                st.markdown("""
                <div style="background: rgba(0, 255, 0, 0.1); padding: 0.75rem; border-radius: 8px; border-left: 4px solid #00FF00; margin-top: 1rem;">
                    <p style="margin: 0; color: #ffffff; font-weight: bold;">📺 <span style="color: #00FF00;">Green Line</span>: TV Shows</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No type-year data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🎭 Genre & Content Analysis")
        
        # TV SHOWS METRICS SECTION
        st.markdown("""
        <div class="section-header" style="margin-top: 0; margin-bottom: 2rem;">
            <h3 class="section-title" style="font-size: 1.8rem;">📺 TV SHOWS METRICS</h3>
            <p class="section-subtitle">Detailed statistics for TV shows in the library</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_tv1, col_tv2, col_tv3 = st.columns(3)
        
        with col_tv1:
            st.markdown(f"""
            <div class="kpi-card" style="height: 160px; background: linear-gradient(145deg, rgba(229,9,20,0.1) 0%, rgba(184,29,36,0.1) 100%); border: 2px solid #E50914;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #E50914; font-size: 0.9rem; font-weight: 800;">TOTAL TV SHOWS</div>
                    <div class="kpi-value" style="color: white; font-size: 2.5rem; margin: 0.5rem 0;">{total_tv_shows:,}</div>
                    <div style="font-size: 1rem; color: #b3b3b3; margin-top: 0.5rem;">
                        {tv_percentage:.1f}% of filtered content
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3;">📺</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_tv2:
            st.markdown(f"""
            <div class="kpi-card" style="height: 160px; background: linear-gradient(145deg, rgba(229,9,20,0.1) 0%, rgba(184,29,36,0.1) 100%); border: 2px solid #E50914;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #E50914; font-size: 0.9rem; font-weight: 800;">AVERAGE SEASONS</div>
                    <div class="kpi-value" style="color: white; font-size: 2.5rem; margin: 0.5rem 0;">{avg_seasons:.1f}</div>
                    <div style="font-size: 1rem; color: #b3b3b3; margin-top: 0.5rem;">
                        Per TV show
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3;">📊</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_tv3:
            st.markdown(f"""
            <div class="kpi-card" style="height: 160px; background: linear-gradient(145deg, rgba(229,9,20,0.1) 0%, rgba(184,29,36,0.1) 100%); border: 2px solid #E50914;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #E50914; font-size: 0.9rem; font-weight: 800;">MAXIMUM SEASONS</div>
                    <div class="kpi-value" style="color: white; font-size: 2.5rem; margin: 0.5rem 0;">{max_seasons:.0f}</div>
                    <div style="font-size: 1rem; color: #b3b3b3; margin-top: 0.5rem;">
                        Longest running series
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3;">🏆</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Chart 6: Top 15 Genres - Horizontal Bar Chart
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏆 Top 15 Genres")
            try:
                genre_counts = filtered_df['genre_list'].explode().value_counts().head(15)
                if not genre_counts.empty:
                    genre_df = pd.DataFrame({
                        'genre': genre_counts.index,
                        'count': genre_counts.values
                    })
                    
                    fig6 = px.bar(genre_df, y='genre', x='count', orientation='h',
                                 title="Top 15 Genres by Content Count")
                    
                    # Apply vibrant rainbow colors
                    colors = VIBRANT_PALETTES['rainbow']
                    fig6.update_traces(
                        marker_color=[colors[i % len(colors)] for i in range(len(genre_df))],
                        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>',
                        marker_line_color='white',
                        marker_line_width=1.5,
                        texttemplate='%{x}',
                        textposition='outside',
                        textfont=dict(color='white', size=11, weight='bold')
                    )
                    
                    fig6 = apply_vibrant_theme(fig6, "Top 15 Genres", 500, showlegend=False)
                    st.plotly_chart(fig6, use_container_width=True)
                else:
                    st.info("No genre data")
            except:
                st.info("Error processing genre data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 7: Movie Duration Distribution - Histogram
        with col2:
            st.markdown("#### 🎥 Movie Duration Distribution")
            movies_df = filtered_df[filtered_df['type'] == 'Movie'].dropna(subset=['movie_minutes'])
            if not movies_df.empty:
                fig7 = create_vibrant_histogram(
                    movies_df,
                    'movie_minutes',
                    "Movie Duration Distribution",
                    palette='electric',
                    height=500,
                    showlegend=False
                )
                st.plotly_chart(fig7, use_container_width=True)
            else:
                st.info("No movie duration data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 8: TV Seasons Distribution - Bar Chart WITH VIBRANT COLORS 
        st.markdown("#### 📺 TV Seasons Distribution")
        tv_df = filtered_df[filtered_df['type'] == 'TV Show'].dropna(subset=['tv_seasons'])
        if not tv_df.empty:
            season_counts = tv_df['tv_seasons'].value_counts().reset_index()
            season_counts.columns = ['seasons', 'count']
            season_counts = season_counts.sort_values('seasons')
            
            # Create the bar chart
            fig8 = px.bar(season_counts, x='seasons', y='count', 
                         title="TV Show Seasons Distribution")
            
            # Apply TV SEASONS specific vibrant colors - each bar different color
            tv_season_colors = VIBRANT_PALETTES['tv_seasons']
            
            fig8.update_traces(
                marker_color=[tv_season_colors[i % len(tv_season_colors)] for i in range(len(season_counts))],
                hovertemplate='<b>%{x} seasons</b><br>Count: %{y}<extra></extra>',
                marker_line_color='white',
                marker_line_width=2,
                texttemplate='%{y}',
                textposition='outside',
                textfont=dict(color='white', size=12, weight='bold')
            )
            
            fig8 = apply_vibrant_theme(fig8, "TV Show Seasons Distribution", 450, showlegend=False)
            st.plotly_chart(fig8, use_container_width=True)
        else:
            st.info("No TV seasons data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🌍 Geographic Analysis")
        
        # Chart 10: Top Content Producing Countries - Bar Chart
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🌐 Top 20 Content Countries")
            try:
                country_counts = filtered_df['country_list'].explode().value_counts().head(20)
                if not country_counts.empty:
                    country_df = pd.DataFrame({
                        'country': country_counts.index,
                        'count': country_counts.values
                    })
                    
                    fig10 = px.bar(country_df, y='country', x='count', orientation='h',
                                  title="Top 20 Countries by Content Count")
                    
                    # Apply ocean waves colors
                    colors = VIBRANT_PALETTES['ocean_waves']
                    fig10.update_traces(
                        marker_color=[colors[i % len(colors)] for i in range(len(country_df))],
                        hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>',
                        marker_line_color='white',
                        marker_line_width=1.5,
                        texttemplate='%{x}',
                        textposition='outside',
                        textfont=dict(color='white', size=11, weight='bold')
                    )
                    
                    fig10 = apply_vibrant_theme(fig10, "Top 20 Countries by Content", 500, showlegend=False)
                    st.plotly_chart(fig10, use_container_width=True)
                else:
                    st.info("No country data")
            except:
                st.info("Error processing country data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 11: Content by Region Treemap
        with col2:
            st.markdown("#### 🗺️ Content by Region & Type")
            try:
                exploded_df = filtered_df.explode('country_list')
                top_10_countries = exploded_df['country_list'].value_counts().head(10).index.tolist()
                treemap_df = exploded_df[exploded_df['country_list'].isin(top_10_countries)]
                
                if not treemap_df.empty:
                    country_type_counts = treemap_df.groupby(['country_list', 'type']).size().reset_index(name='count')
                    
                    fig11 = px.treemap(
                        country_type_counts,
                        path=['country_list', 'type'],
                        values='count',
                        color='count',
                        color_continuous_scale='Rainbow',
                        
                    )
                    
                    fig11.update_traces(
                        texttemplate='<b>%{label}</b><br>Count: %{value}',
                        textposition='middle center',
                        textfont=dict(color='white', size=14, weight='bold'),
                        hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>',
                        marker=dict(line=dict(width=2, color='white'))
                    )
                    
                    fig11.update_layout(
                        plot_bgcolor='rgba(26, 26, 26, 0.7)',
                        paper_bgcolor='rgba(26, 26, 26, 0.7)',
                        height=500,
                        margin=dict(t=100, b=50, l=50, r=50),
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig11, use_container_width=True)
                else:
                    st.info("Insufficient country data")
            except:
                st.info("Could not generate treemap")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 12: Content Quality by Country - Bar Chart
        st.markdown("#### ⭐ Content Quality by Country")
        try:
            exploded_df = filtered_df.explode('country_list')
            top_countries = exploded_df['country_list'].value_counts().head(15).index.tolist()
            country_quality = exploded_df[exploded_df['country_list'].isin(top_countries)]
            
            if not country_quality.empty:
                quality_by_country = country_quality.groupby('country_list')['content_score'].mean().reset_index()
                quality_by_country = quality_by_country.sort_values('content_score', ascending=False).head(10)
                
                fig12 = create_vibrant_bar_chart(
                    quality_by_country,
                    'country_list',
                    'content_score',
                    "Average Content Score by Top 10 Countries",
                    palette='neon_gradient',
                    height=450,
                    showlegend=False
                )
                st.plotly_chart(fig12, use_container_width=True)
            else:
                st.info("Insufficient quality data")
        except:
            st.info("Could not generate quality chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab4:
        st.markdown("### ⚡ Quality & Ratings Analysis")
        
        # SECTION 1: Quality Range metrics
        st.markdown("""
        <div class="section-header" style="margin-top: 0; margin-bottom: 2rem;">
            <h3 class="section-title" style="font-size: 1.8rem;">⭐ QUALITY ANALYSIS</h3>
            <p class="section-subtitle">Content quality metrics and scoring range</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_qual1, col_qual2 = st.columns(2)
        
        with col_qual1:
            st.markdown(f"""
            <div class="kpi-card" style="height: 160px; background: linear-gradient(145deg, rgba(255,215,0,0.1) 0%, rgba(255,165,0,0.1) 100%); border: 2px solid #FFD700;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #FFD700; font-size: 0.9rem; font-weight: 800;">QUALITY RANGE</div>
                    <div class="kpi-value" style="color: white; font-size: 2.5rem; margin: 0.5rem 0;">{quality_range:.1f} points</div>
                    <div style="font-size: 1rem; color: #1DB954; margin-top: 0.5rem; font-weight: 600;">
                        {avg_quality:.1f} average quality score
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3; color: #FFD700;">⭐</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_qual2:
            st.markdown(f"""
            <div class="kpi-card" style="height: 160px; background: linear-gradient(145deg, rgba(255,215,0,0.1) 0%, rgba(255,165,0,0.1) 100%); border: 2px solid #FFD700;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #FFD700; font-size: 0.9rem; font-weight: 800;">QUALITY SCORE RANGE</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem;">
                        <div style="text-align: center; flex: 1;">
                            <div style="color: #b3b3b3; font-size: 0.8rem; margin-bottom: 0.25rem;">Min</div>
                            <div style="color: white; font-size: 1.8rem; font-weight: 900;">{min_quality:.0f}</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div style="color: #b3b3b3; font-size: 0.8rem; margin-bottom: 0.25rem;">Avg</div>
                            <div style="color: white; font-size: 1.8rem; font-weight: 900;">{avg_quality:.1f}</div>
                        </div>
                        <div style="text-align: center; flex: 1;">
                            <div style="color: #b3b3b3; font-size: 0.8rem; margin-bottom: 0.25rem;">Max</div>
                            <div style="color: white; font-size: 1.8rem; font-weight: 900;">{max_quality:.0f}</div>
                        </div>
                    </div>
                    <div style="height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; margin-top: 1rem; position: relative;">
                        <div style="position: absolute; left: 0; top: 0; height: 100%; width: {(avg_quality - min_quality) / (max_quality - min_quality) * 100}%; 
                             background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%); border-radius: 4px;"></div>
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3; color: #FFD700;">📊</div>
            </div>
            """, unsafe_allow_html=True)
        
        # SECTION 2: Movies vs TV Shows Distribution
        st.markdown("""
        <div class="section-header" style="margin-top: 2rem; margin-bottom: 2rem;">
            <h3 class="section-title" style="font-size: 1.8rem;">🎬 CONTENT TYPE DISTRIBUTION</h3>
            <p class="section-subtitle">Movies vs TV Shows breakdown in the library</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_movie, col_tv = st.columns(2)
        
        with col_movie:
            st.markdown(f"""
            <div class="kpi-card" style="height: 180px; background: linear-gradient(145deg, rgba(255,0,0,0.15) 0%, rgba(184,29,36,0.15) 100%); border: 2px solid #FF0000;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #FF0000; font-size: 1rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem;">
                        <span>🎥</span> MOVIES
                    </div>
                    <div class="kpi-value" style="color: white; font-size: 3rem; margin: 0.5rem 0;">{total_movies:,}</div>
                    <div style="font-size: 1.2rem; color: #FF0000; margin-top: 0.5rem; font-weight: 700;">
                        {movie_percentage:.1f}% of total
                    </div>
                    <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin-top: 0.75rem;">
                        <div style="height: 100%; width: {movie_percentage}%; background: linear-gradient(90deg, #FF0000 0%, #B81D24 100%); border-radius: 3px;"></div>
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3; color: #FF0000; font-size: 3rem;">🎥</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_tv:
            st.markdown(f"""
            <div class="kpi-card" style="height: 180px; background: linear-gradient(145deg, rgba(0,255,0,0.15) 0%, rgba(0,184,36,0.15) 100%); border: 2px solid #00FF00;">
                <div class="kpi-content">
                    <div class="kpi-label" style="color: #00FF00; font-size: 1rem; font-weight: 800; display: flex; align-items: center; gap: 0.5rem;">
                        <span>📺</span> TV SHOWS
                    </div>
                    <div class="kpi-value" style="color: white; font-size: 3rem; margin: 0.5rem 0;">{total_tv_shows_global:,}</div>
                    <div style="font-size: 1.2rem; color: #00FF00; margin-top: 0.5rem; font-weight: 700;">
                        {tv_percentage_global:.1f}% of total
                    </div>
                    <div style="height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; margin-top: 0.75rem;">
                        <div style="height: 100%; width: {tv_percentage_global}%; background: linear-gradient(90deg, #00FF00 0%, #00B824 100%); border-radius: 3px;"></div>
                    </div>
                </div>
                <div class="kpi-icon" style="opacity: 0.3; color: #00FF00; font-size: 3rem;">📺</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Add a summary row
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(40,40,40,0.8) 0%, rgba(60,60,60,0.8) 100%); 
                    padding: 1.5rem; border-radius: 12px; margin: 1.5rem 0; border: 1px solid #333333;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1; text-align: center;">
                    <div style="color: #b3b3b3; font-size: 0.9rem; margin-bottom: 0.25rem;">Total Content</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: 900;">{total_titles:,}</div>
                </div>
                <div style="flex: 1; text-align: center; border-left: 1px solid #333333; border-right: 1px solid #333333;">
                    <div style="color: #b3b3b3; font-size: 0.9rem; margin-bottom: 0.25rem;">Movies Ratio</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: 900;">{movie_percentage:.1f}%</div>
                </div>
                <div style="flex: 1; text-align: center;">
                    <div style="color: #b3b3b3; font-size: 0.9rem; margin-bottom: 0.25rem;">TV Shows Ratio</div>
                    <div style="color: white; font-size: 1.8rem; font-weight: 900;">{tv_percentage_global:.1f}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Chart 13: Ratings Distribution - Pie Chart
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📋 Ratings Distribution")
            rating_counts = filtered_df['rating'].value_counts().head(10)
            if not rating_counts.empty:
                fig13 = create_vibrant_pie_chart(
                    rating_counts.index.tolist(),
                    rating_counts.values.tolist(),
                    "Top 10 Content Ratings Distribution",
                    palette='electric',
                    height=450
                )
                st.plotly_chart(fig13, use_container_width=True)
            else:
                st.info("No rating data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 14: Content Quality Distribution - Histogram
        with col2:
            st.markdown("#### ⭐ Content Quality Score Distribution")
            if not filtered_df.empty:
                fig14 = create_vibrant_histogram(
                    filtered_df,
                    'content_score',
                    "Content Quality Score Distribution",
                    palette='fire',
                    height=450,
                    showlegend=False
                )
                st.plotly_chart(fig14, use_container_width=True)
                
                # Show quality tier distribution
                if 'quality_category' in filtered_df.columns:
                    quality_tiers = filtered_df['quality_category'].value_counts()
                    for tier, count in quality_tiers.items():
                        percentage = (count / len(filtered_df)) * 100
                        st.progress(percentage/100, text=f"{tier}: {count:,} ({percentage:.1f}%)")
            else:
                st.info("No quality data")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Chart 15: Content Type Distribution - Pie Chart 
        st.markdown("#### 🎬 Content Type Distribution (Visual)")
        type_counts = filtered_df['type'].value_counts()
        if not type_counts.empty:
            fig15 = create_vibrant_pie_chart(
                type_counts.index.tolist(),
                type_counts.values.tolist(),
                "Movies vs TV Shows Distribution",
                palette='jewel_bright',
                height=450
            )
            st.plotly_chart(fig15, use_container_width=True)
        else:
            st.info("No type data")
        st.markdown('</div>', unsafe_allow_html=True)
    
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p style="margin: 0.5rem 0; font-size: 0.9rem;">🎬 <strong>NETFLIX CONTENT ANALYTICS DASHBOARD</strong></p>
        <p style="margin: 0.5rem 0; font-size: 0.8rem; color: #808080;"> Enhanced Charts • Interactive Analytics Platform</p>
        <p style="margin: 0.5rem 0; font-size: 0.8rem; color: #666666;">© 2024 Netflix Analytics • {}</p>
        <div style="margin-top: 1.5rem; display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem;">
            <span style="background: rgba(229,9,20,0.1); padding: 0.5rem 1.25rem; border-radius: 20px; font-size: 0.8rem; color: #E50914; border: 1px solid rgba(229,9,20,0.3);">
                📊  Titles Analyzed
            </span>
            <span style="background: rgba(229,9,20,0.1); padding: 0.5rem 1.25rem; border-radius: 20px; font-size: 0.8rem; color: #E50914; border: 1px solid rgba(229,9,20,0.3);">
                🎨 Enhanced Color Schemes
            </span>
            <span style="background: rgba(229,9,20,0.1); padding: 0.5rem 1.25rem; border-radius: 20px; font-size: 0.8rem; color: #E50914; border: 1px solid rgba(229,9,20,0.3);">
                🌍  Countries
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":

    main()
