# app.py
# By: NKG-Systems + NathanGr33n
# Simple SMB Leads→Sales dashboard pulling live CSV from Google Sheets (published URL).

import io
import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st
from dateutil import parser

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="SMB Sales Dashboard", page_icon="📈", layout="wide")

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
    st.title("⚙️ Data Source")
    if not CSV_URL:
        CSV_URL = st.text_input(
            "Google Sheets CSV URL",
            placeholder="Paste your published-to-web CSV link...",
        )
    st.caption("Tip: File → Share → Publish to web → select the 'leads' sheet → CSV.")

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
st.title("📈 SMB Sales Dashboard")
st.caption("Live metrics from Google Sheets (Published CSV).")

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
# CHARTS
# -----------------------------
# Time series: Revenue by week
f["week"] = pd.to_datetime(f["date"]).dt.to_period("W").apply(lambda r: r.start_time)
rev_by_week = f[f["status"]=="Won"].groupby("week", as_index=False)["revenue"].sum()
if not rev_by_week.empty:
    fig_rev = px.bar(rev_by_week, x="week", y="revenue", title="Revenue by Week")
    st.plotly_chart(fig_rev, use_container_width=True)

# Funnel counts
funnel = (
    f.groupby("status", as_index=False)
     .size()
     .rename(columns={"size":"count"})
     .sort_values("count", ascending=False)
)
fig_fun = px.bar(funnel, x="status", y="count", title="Lead Funnel (counts)")
st.plotly_chart(fig_fun, use_container_width=True)

# Channel performance (conversion rate)
def _conv(g):
    return (g["status"]=="Won").sum() / len(g) * 100 if len(g) else 0

conv_by_channel = (
    f.groupby("channel")
     .apply(_conv)
     .reset_index(name="conversion_rate")
     .sort_values("conversion_rate", ascending=False)
)
fig_conv = px.bar(conv_by_channel, x="channel", y="conversion_rate",
                  title="Conversion Rate by Channel (%)")
st.plotly_chart(fig_conv, use_container_width=True)

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
