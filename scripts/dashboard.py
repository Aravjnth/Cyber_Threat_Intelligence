import streamlit as st
import pandas as pd
import time
import altair as alt

# Page Config
st.set_page_config(
    page_title="Cyber Threat Intelligence Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# Dashboard Title
st.title("🛡️ Live Cyber Threat Intelligence Dashboard")

# Function to load data
def load_data():
    try:
        # Read the CSV. On busy files, sometimes read fails, so we retry.
        df = pd.read_csv("data/live_threats.csv")
        # Ensure Timestamp is datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        return df
    except Exception as e:
        return pd.DataFrame()

# Layout Placeholders
kpi1, kpi2, kpi3 = st.columns(3)
chart1, chart2 = st.columns(2)
recent_alerts = st.container()

st.markdown("### 📡 Live Threat Feed")
data_placeholder = st.empty()

# Auto-refresh loop
while True:
    df = load_data()
    
    if not df.empty:
        # KPI calculations
        total_threats = len(df)
        critical_threats = len(df[df['Severity'] == 'Critical'])
        last_update = df['Timestamp'].max().strftime('%H:%M:%S')

        # Update KPIs
        with kpi1:
            st.metric(label="Total Threats Detected", value=total_threats)
        with kpi2:
            st.metric(label="CRITICAL Threats", value=critical_threats, delta_color="inverse")
        with kpi3:
            st.metric(label="Last Update", value=last_update)

        # Charts
        with chart1:
            st.markdown("#### 🚨 Threats by Severity")
            # Severity distribution
            severity_counts = df['Severity'].value_counts().reset_index()
            severity_counts.columns = ['Severity', 'Count']
            
            # Custom color scale
            domain = ['Critical', 'High', 'Medium', 'Low']
            range_ = ['red', 'orange', 'yellow', 'green']
            
            bar_chart = alt.Chart(severity_counts).mark_bar().encode(
                x=alt.X('Severity', sort=domain),
                y='Count',
                color=alt.Color('Severity', scale=alt.Scale(domain=domain, range=range_)),
                tooltip=['Severity', 'Count']
            ).properties(height=300)
            
            st.altair_chart(bar_chart, use_container_width=True)

        with chart2:
            st.markdown("#### 🦠 Threats by Type")
            # Type distribution
            type_counts = df['Threat_Type'].value_counts().reset_index()
            type_counts.columns = ['Threat_Type', 'Count']
            
            pie_chart = alt.Chart(type_counts).mark_arc(innerRadius=50).encode(
                theta='Count',
                color='Threat_Type',
                tooltip=['Threat_Type', 'Count']
            ).properties(height=300)
            
            st.altair_chart(pie_chart, use_container_width=True)

        # Recent Data Table
        with data_placeholder.container():
            # Show top 10 most recent
            recent_df = df.sort_values(by="Timestamp", ascending=False).head(10)
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
            
    # Wait for 1 second before refreshing
    time.sleep(1)
