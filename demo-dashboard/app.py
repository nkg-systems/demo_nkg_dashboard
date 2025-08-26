# app.py
# By: NKG-Systems + NathanGr33n
# Modern SMB Leads→Sales dashboard with dark theme pulling live CSV from Google Sheets (published URL)

import io
import os
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from dateutil import parser

# -----------------------------
# CONFIG & STYLING
# -----------------------------
st.set_page_config(
    page_title="Sales Intelligence", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern AI-themed dark design
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables for consistent theming */
    :root {
        --primary-violet: #8B5CF6;
        --primary-blue: #3B82F6;
        --accent-cyan: #06B6D4;
        --bg-primary: #0B0F1A;
        --bg-secondary: #11172A;
        --bg-tertiary: #1E2A3A;
        --text-primary: #E6EAF3;
        --text-secondary: #9CA3AF;
        --border-subtle: #1F2937;
        --gradient-primary: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%);
        --gradient-accent: linear-gradient(135deg, #06B6D4 0%, #8B5CF6 100%);
        --shadow-glow: 0 0 20px rgba(139, 92, 246, 0.15);
        --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
    }
    
    /* Global styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--bg-primary);
    }
    
    /* Header styling */
    .main-header {
        background: var(--gradient-primary);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: var(--shadow-card);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .main-header h1 {
        color: white !important;
        font-weight: 700 !important;
        font-size: 2.5rem !important;
        margin: 0 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.1rem !important;
        margin-top: 0.5rem !important;
        font-weight: 400 !important;
    }
    
    /* KPI Cards */
    .kpi-container {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .metric-card {
        background: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        box-shadow: var(--shadow-card);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--gradient-primary);
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-glow);
        border-color: var(--primary-violet);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-subtle);
    }
    
    .css-1d391kg .stTitle {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Filters styling */
    .stExpander {
        background: var(--bg-secondary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 12px !important;
        margin-bottom: 1rem !important;
    }
    
    .streamlit-expanderHeader {
        background: var(--bg-tertiary) !important;
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }
    
    /* Input widgets */
    .stSelectbox > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }
    
    .stMultiSelect > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }
    
    .stDateInput > div > div {
        background: var(--bg-tertiary) !important;
        border: 1px solid var(--border-subtle) !important;
        border-radius: 8px !important;
    }
    
    /* Charts container */
    .chart-container {
        background: var(--bg-secondary);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-subtle);
        margin: 1rem 0;
        box-shadow: var(--shadow-card);
    }
    
    /* Data table */
    .stDataFrame {
        background: var(--bg-secondary) !important;
        border-radius: 12px !important;
        border: 1px solid var(--border-subtle) !important;
        overflow: hidden !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--gradient-primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: var(--shadow-card) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadow-glow) !important;
    }
    
    .stDownloadButton > button {
        background: var(--gradient-accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Success/Info/Warning messages */
    .stSuccess, .stInfo, .stWarning, .stError {
        border-radius: 8px !important;
        border-left: 4px solid var(--primary-violet) !important;
    }
    
    /* Divider */
    hr {
        border: none !important;
        height: 1px !important;
        background: var(--gradient-primary) !important;
        margin: 2rem 0 !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-primary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-violet);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-blue);
    }
    
    /* AI Assistant Badge */
    .ai-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: var(--gradient-accent);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-card);
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        margin-right: 0.5rem;
    }
    
    .status-won { background: #10B981; }
    .status-qualified { background: #F59E0B; }
    .status-new { background: #3B82F6; }
    .status-lost { background: #EF4444; }
</style>
""", unsafe_allow_html=True)

# Optional simple gate using a shared access code in secrets
ACCESS_CODE = st.secrets.get("ACCESS_CODE", "")
if ACCESS_CODE:
    with st.sidebar:
        code = st.text_input("Access code", type="password", placeholder="Enter access code")
    if code != ACCESS_CODE:
        st.info("Enter the access code to view the dashboard.")
        st.stop()

# Prefer a secret in production (Streamlit Secrets) but allow manual entry for local dev
CSV_URL = st.secrets.get("CSV_URL", "")

with st.sidebar:
    # Modern themed sidebar header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0; margin-bottom: 2rem;">
        <h2 style="color: #8B5CF6; margin: 0; font-size: 1.5rem; font-weight: 600;">
            Control Panel
        </h2>
        <p style="color: #9CA3AF; margin: 0.5rem 0 0 0; font-size: 0.9rem;">
            Configure your data sources
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data source configuration
    with st.expander("📊 Data Source", expanded=not CSV_URL):
        if not CSV_URL:
            CSV_URL = st.text_input(
                "Google Sheets CSV URL",
                placeholder="Paste your published-to-web CSV link...",
                help="Get this from File → Share → Publish to web → CSV format"
            )
        else:
            st.success("✓ Data source configured")
            st.caption(f"Connected to: {CSV_URL[:50]}...")
            if st.button("🔄 Change Data Source"):
                st.rerun()
    
    # AI Features section  
    with st.expander("🤖 AI Features", expanded=False):
        st.info("🔥 **Smart Analytics Enabled**")
        st.markdown("""
        • **Real-time Processing**: Data updates every 15 minutes  
        • **Predictive Insights**: Conversion trend analysis  
        • **Intelligent Filtering**: Advanced data segmentation  
        • **Performance Optimization**: Cached data loading  
        """)
        
        # Performance stats will be shown after data is loaded
        st.caption("Performance stats will appear once data is loaded")

# -----------------------------
# LOAD DATA (cached)
# -----------------------------
@st.cache_data(ttl=15 * 60, show_spinner=True)
def load_data(csv_url: str) -> pd.DataFrame:
    if not csv_url:
        return pd.DataFrame()
    r = requests.get(csv_url, timeout=20)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))

    # Normalize columns
    df.columns = [c.strip().lower() for c in df.columns]
    expected = ["date","channel","campaign","lead_name","lead_email","lead_phone","status","revenue","cost","owner"]
    for col in expected:
        if col not in df.columns:
            df[col] = None

    # Parse types
    df["date"]     = pd.to_datetime(df["date"], errors="coerce")          # <-- Timestamp
    df["revenue"]  = pd.to_numeric(df["revenue"], errors="coerce").fillna(0.0)
    df["cost"]     = pd.to_numeric(df["cost"], errors="coerce").fillna(0.0)
    df["status"]   = df["status"].astype(str).str.strip().str.title()
    df["channel"]  = df["channel"].astype(str).str.strip().str.title()
    df["campaign"] = df["campaign"].astype(str).str.strip()
    df["owner"]    = df["owner"].astype(str).str.strip()

    df = df.dropna(subset=["date"]).copy()
    return df.sort_values("date")

try:
    df = load_data(CSV_URL)
except requests.HTTPError as e:
    st.error(f"Could not load CSV. Check your published link.\n\n{e}")
    st.stop()

# -----------------------------
# UI: Header
# -----------------------------
st.markdown("""
<div class="main-header">
    <h1>🤖 Sales Intelligence</h1>
    <p>Advanced analytics powered by real-time data • Insights for modern businesses</p>
</div>

<div class="badge">
    ⚡ Real-time Dashboard • 🔮 Predictive Analytics • 📊 Smart Insights
</div>
""", unsafe_allow_html=True)

if df.empty:
    st.warning("Add your CSV URL in the sidebar to load data.")
    st.stop()

# -----------------------------
# FILTERS
# -----------------------------
with st.expander("Filters", expanded=True):
    c1, c2, c3, c4 = st.columns(4)

    # Convert min/max to 'date' for the widget defaults
    min_ts, max_ts = df["date"].min(), df["date"].max()
    min_date, max_date = min_ts.date(), max_ts.date()

    date_range = c1.date_input("Date range", value=(min_date, max_date))
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    channels = sorted([x for x in df["channel"].dropna().unique() if x])
    channel_pick = c2.multiselect("Channel", options=channels, default=channels)

    owners = sorted([x for x in df["owner"].dropna().unique() if x])
    owner_pick = c3.multiselect("Owner", options=owners, default=owners)

    statuses = ["New", "Qualified", "Won", "Lost"]
    status_pick = c4.multiselect("Status", options=statuses, default=statuses)


# Apply filters
mask = (
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date)) &
    (df["channel"].isin(channel_pick) | df["channel"].isna()) &
    (df["owner"].isin(owner_pick) | df["owner"].isna()) &
    (df["status"].isin(status_pick))
)
f = df.loc[mask].copy()

# -----------------------------
# DERIVED METRICS
# -----------------------------
total_leads = len(f)
qualified = (f["status"] == "Qualified").sum()
won = (f["status"] == "Won").sum()
lost = (f["status"] == "Lost").sum()
revenue = float(f.loc[f["status"] == "Won", "revenue"].sum())
spend = float(f["cost"].sum())
avg_deal = (revenue / won) if won else 0.0
conv_rate = (won / total_leads * 100.0) if total_leads else 0.0
cac = (spend / won) if won else 0.0
roas = (revenue / spend) if spend > 0 else None

# -----------------------------
# KPI CARDS
# -----------------------------
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Leads", f"{total_leads:,}")
k2.metric("Qualified", f"{qualified:,}")
k3.metric("Won Deals", f"{won:,}")
k4.metric("Revenue", f"${revenue:,.0f}")
k5.metric("Avg Deal", f"${avg_deal:,.0f}")
k6.metric("Conv Rate", f"{conv_rate:.1f}%")

k7, k8 = st.columns(2)
k7.metric("Ad Spend", f"${spend:,.0f}")
k8.metric("CAC", f"${cac:,.0f}" if cac else "—")

if roas is not None:
    st.metric("ROAS", f"{roas:.2f}x")

st.divider()

# -----------------------------
# CHARTS - Styling
# -----------------------------

# Color scheme for charts
COLOR_SCHEME = {
    'primary': '#8B5CF6',
    'secondary': '#3B82F6', 
    'accent': '#06B6D4',
    'success': '#10B981',
    'warning': '#F59E0B',
    'error': '#EF4444',
    'background': '#11172A',
    'text': '#E6EAF3'
}

# Chart template for consistent styling
chart_template = {
    'layout': {
        'paper_bgcolor': COLOR_SCHEME['background'],
        'plot_bgcolor': COLOR_SCHEME['background'], 
        'font_color': COLOR_SCHEME['text'],
        'font_family': 'Inter',
        'title_font_size': 20,
        'title_font_color': COLOR_SCHEME['text'],
        'showlegend': False,
        'margin': dict(t=60, l=60, r=60, b=60)
    }
}

# Charts in organized layout
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📈 Revenue Trends")
    # Time series: Revenue by week
    f["week"] = pd.to_datetime(f["date"]).dt.to_period("W").apply(lambda r: r.start_time)
    rev_by_week = f[f["status"]=="Won"].groupby("week", as_index=False)["revenue"].sum()
    
    if not rev_by_week.empty:
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Scatter(
            x=rev_by_week["week"],
            y=rev_by_week["revenue"],
            mode='lines+markers',
            line=dict(color=COLOR_SCHEME['primary'], width=3),
            marker=dict(color=COLOR_SCHEME['secondary'], size=8),
            fill='tonexty',
            fillcolor=f"rgba(139, 92, 246, 0.1)",
            name='Revenue'
        ))
        
        fig_rev.update_layout(
            **chart_template['layout'],
            title="Weekly Revenue Performance",
            xaxis_title="Week",
            yaxis_title="Revenue ($)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_rev, use_container_width=True)
    else:
        st.info("No revenue data to display")

with chart_col2:
    st.subheader("📊 Lead Funnel")
    # Enhanced funnel with status colors
    funnel = (
        f.groupby("status", as_index=False)
         .size()
         .rename(columns={"size":"count"})
         .sort_values("count", ascending=False)
    )
    
    if not funnel.empty:
        # Color mapping for status
        status_colors = {
            'New': COLOR_SCHEME['secondary'],
            'Qualified': COLOR_SCHEME['warning'],
            'Won': COLOR_SCHEME['success'],
            'Lost': COLOR_SCHEME['error']
        }
        
        colors = [status_colors.get(status, COLOR_SCHEME['primary']) for status in funnel['status']]
        
        fig_fun = go.Figure()
        fig_fun.add_trace(go.Bar(
            x=funnel["status"],
            y=funnel["count"],
            marker_color=colors,
            text=funnel["count"],
            textposition='outside',
            textfont=dict(color=COLOR_SCHEME['text'])
        ))
        
        fig_fun.update_layout(
            **chart_template['layout'],
            title="Lead Status Distribution",
            xaxis_title="Status",
            yaxis_title="Count"
        )
        
        st.plotly_chart(fig_fun, use_container_width=True)
    else:
        st.info("No funnel data to display")

# Full width chart for conversion rates
st.subheader("🎦 Channel Performance")

# Channel performance (conversion rate)
def _conv(g):
    return (g["status"]=="Won").sum() / len(g) * 100 if len(g) else 0

conv_by_channel = (
    f.groupby("channel")
     .apply(_conv)
     .reset_index(name="conversion_rate")
     .sort_values("conversion_rate", ascending=True)  # Horizontal bar chart
)

if not conv_by_channel.empty:
    fig_conv = go.Figure()
    fig_conv.add_trace(go.Bar(
        x=conv_by_channel["conversion_rate"],
        y=conv_by_channel["channel"],
        orientation='h',
        marker=dict(
            color=conv_by_channel["conversion_rate"],
            colorscale=[[0, COLOR_SCHEME['error']], [0.5, COLOR_SCHEME['warning']], [1, COLOR_SCHEME['success']]],
            colorbar=dict(title="Conversion %")
        ),
        text=[f"{rate:.1f}%" for rate in conv_by_channel["conversion_rate"]],
        textposition='outside',
        textfont=dict(color=COLOR_SCHEME['text'])
    ))
    
    fig_conv.update_layout(
        **chart_template['layout'],
        title="Conversion Rate by Channel",
        xaxis_title="Conversion Rate (%)",
        yaxis_title="Channel",
        height=400
    )
    
    st.plotly_chart(fig_conv, use_container_width=True)
else:
    st.info("No channel performance data to display")

# -----------------------------
# DETAILS TABLE + EXPORT
# -----------------------------
st.subheader("Recent Leads")
show_cols = ["date","channel","campaign","lead_name","lead_email","lead_phone","status","revenue","cost","owner"]
st.dataframe(f.sort_values("date", ascending=False)[show_cols], use_container_width=True)

st.download_button(
    label="⬇️ Download filtered CSV",
    data=f.to_csv(index=False),
    file_name="filtered_leads.csv",
    mime="text/csv"
)

st.caption("Update the Google Sheet and refresh — the dashboard will reflect new data within ~15 minutes.")
