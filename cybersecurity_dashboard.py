import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Cybersecurity Basics Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .title {
        font-size: 2rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #34495e;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f8f9fa;
        border-left: 3px solid #3498db;
        padding: 15px;
        margin: 10px 0;
        border-radius: 3px;
    }
    .high-risk {
        color: #e74c3c;
        font-weight: bold;
    }
    .medium-risk {
        color: #f39c12;
        font-weight: bold;
    }
    .low-risk {
        color: #2ecc71;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)


# Function to generate sample data
def generate_sample_data():
    np.random.seed(42)

    # Create a date range for the last 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    # Number of incidents
    num_incidents = 100

    # Basic attack types for beginners
    attack_types = [
        'Phishing Email',
        'Malware',
        'Weak Password',
        'Missing Update',
        'USB Threat',
        'Suspicious Link'
    ]

    # Create simple status options
    status_options = ['Detected', 'Fixed', 'In Progress']

    # Generate the data
    data = pd.DataFrame({
        'Incident_ID': range(1, num_incidents + 1),
        'Date': np.random.choice(dates, size=num_incidents),
        'Attack_Type': np.random.choice(attack_types, size=num_incidents),
        'Risk_Level': np.random.choice(['Low', 'Medium', 'High'],
                                       size=num_incidents, p=[0.5, 0.3, 0.2]),
        'Status': np.random.choice(status_options, size=num_incidents),
        'Device_Type': np.random.choice(['Laptop', 'Desktop', 'Mobile', 'Server'], size=num_incidents),
        'Time_to_Fix_Hours': np.random.randint(1, 24, size=num_incidents)
    })

    # Sort by date
    data = data.sort_values('Date')

    return data


# Generate data
data = generate_sample_data()

# Header section
st.markdown("<h1 class='title'>🔒 Cybersecurity Basics Dashboard</h1>", unsafe_allow_html=True)

# Add an info box explaining the dashboard
st.markdown("""
<div class='info-box'>
    <p>This dashboard shows basic cybersecurity incidents and metrics from the last 30 days. 
    Use it to understand common threats, their risk levels, and how quickly they were resolved.</p>
    <p>Use the filters in the sidebar to explore different views of the data.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for filters
with st.sidebar:
    st.title("Filters")

    # Simple date filter
    st.subheader("Time Period")
    days_to_show = st.slider("Days to include", 1, 30, 30)

    cutoff_date = datetime.now() - timedelta(days=days_to_show)
    filtered_data = data[data['Date'] >= cutoff_date]

    # Risk level filter
    st.subheader("Risk Level")
    selected_risk = st.multiselect(
        'Select Risk Level',
        options=['Low', 'Medium', 'High'],
        default=['Low', 'Medium', 'High']
    )

    # Attack type filter
    st.subheader("Attack Type")
    attack_types = sorted(data['Attack_Type'].unique())
    selected_attack = st.multiselect(
        'Select Attack Type',
        options=attack_types,
        default=attack_types
    )

    # Apply filters
    filtered_data = filtered_data[
        (filtered_data['Risk_Level'].isin(selected_risk)) &
        (filtered_data['Attack_Type'].isin(selected_attack))
        ]

    # Help box
    st.markdown("""
    <div style="background-color:#f0f0f0; padding:10px; border-radius:5px; margin-top:20px;">
        <h4>Need Help?</h4>
        <p>This dashboard shows common cybersecurity incidents.</p>
        <ul>
            <li><b>Risk Level</b>: How serious the incident is</li>
            <li><b>Attack Type</b>: What kind of security threat it is</li>
            <li><b>Time to Fix</b>: How many hours it took to resolve</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Main content area
# Create two columns
col1, col2 = st.columns(2)

with col1:
    # Summary stats
    st.markdown("<h2 class='subtitle'>Security Summary</h2>", unsafe_allow_html=True)

    total_incidents = len(filtered_data)
    high_risk = len(filtered_data[filtered_data['Risk_Level'] == 'High'])
    medium_risk = len(filtered_data[filtered_data['Risk_Level'] == 'Medium'])
    low_risk = len(filtered_data[filtered_data['Risk_Level'] == 'Low'])

    # Calculate percentages safely
    high_pct = (high_risk / total_incidents * 100) if total_incidents > 0 else 0
    medium_pct = (medium_risk / total_incidents * 100) if total_incidents > 0 else 0
    low_pct = (low_risk / total_incidents * 100) if total_incidents > 0 else 0

    st.markdown(f"""
    <div class='info-box'>
        <p>Total incidents: <b>{total_incidents}</b></p>
        <p><span class='high-risk'>High Risk: {high_risk}</span> ({high_pct:.1f}%)</p>
        <p><span class='medium-risk'>Medium Risk: {medium_risk}</span> ({medium_pct:.1f}%)</p>
        <p><span class='low-risk'>Low Risk: {low_risk}</span> ({low_pct:.1f}%)</p>
    </div>
    """, unsafe_allow_html=True)

    # Risk level pie chart
    st.markdown("<h2 class='subtitle'>Risk Level Distribution</h2>", unsafe_allow_html=True)

    if not filtered_data.empty:
        fig = px.pie(
            filtered_data,
            names='Risk_Level',
            color='Risk_Level',
            color_discrete_map={
                'High': '#e74c3c',
                'Medium': '#f39c12',
                'Low': '#2ecc71'
            },
            title='Incidents by Risk Level'
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with col2:
    # Attack type bar chart
    st.markdown("<h2 class='subtitle'>Common Attack Types</h2>", unsafe_allow_html=True)

    if not filtered_data.empty:
        attack_counts = filtered_data['Attack_Type'].value_counts().reset_index()
        attack_counts.columns = ['Attack_Type', 'Count']

        fig = px.bar(
            attack_counts,
            x='Attack_Type',
            y='Count',
            color='Attack_Type',
            title='Frequency of Attack Types'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

    # Add a brief explanation of attack types
    st.markdown("""
    <div class='info-box'>
        <h3>What These Attacks Mean:</h3>
        <ul>
            <li><b>Phishing Email</b>: Fake emails trying to steal your information</li>
            <li><b>Malware</b>: Harmful software that damages your computer</li>
            <li><b>Weak Password</b>: Passwords that are easy to guess</li>
            <li><b>Missing Update</b>: Software that hasn't been updated with security fixes</li>
            <li><b>USB Threat</b>: Security risks from connected USB devices</li>
            <li><b>Suspicious Link</b>: Links that lead to harmful websites</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Timeline of incidents
st.markdown("<h2 class='subtitle'>Incident Timeline</h2>", unsafe_allow_html=True)

if not filtered_data.empty:
    # Group by date and count incidents
    timeline_data = filtered_data.groupby([filtered_data['Date'].dt.date, 'Risk_Level']).size().reset_index(
        name='count')
    timeline_data.columns = ['Date', 'Risk_Level', 'Count']

    fig = px.line(
        timeline_data,
        x='Date',
        y='Count',
        color='Risk_Level',
        color_discrete_map={
            'High': '#e74c3c',
            'Medium': '#f39c12',
            'Low': '#2ecc71'
        },
        title='Daily Security Incidents'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available for the selected time period.")

# Device type distribution
st.markdown("<h2 class='subtitle'>Affected Devices</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    if not filtered_data.empty:
        device_counts = filtered_data['Device_Type'].value_counts().reset_index()
        device_counts.columns = ['Device_Type', 'Count']

        fig = px.pie(
            device_counts,
            values='Count',
            names='Device_Type',
            title='Incidents by Device Type'
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")

with col2:
    st.markdown("""
    <div class='info-box'>
        <h3>Protection Tips by Device:</h3>
        <ul>
            <li><b>Laptops & Desktops</b>: Keep your antivirus updated and install system updates</li>
            <li><b>Mobile Devices</b>: Only install apps from official stores and use screen locks</li>
            <li><b>Servers</b>: Use strong access controls and regular backups</li>
        </ul>
        <p>Remember: No matter what device you use, strong passwords and regular updates are essential!</p>
    </div>
    """, unsafe_allow_html=True)

# Time to fix analysis
st.markdown("<h2 class='subtitle'>How Quickly Problems Were Fixed</h2>", unsafe_allow_html=True)

if not filtered_data.empty:
    # Average time to fix by risk level
    fix_time_by_risk = filtered_data.groupby('Risk_Level')['Time_to_Fix_Hours'].mean().reset_index()

    fig = px.bar(
        fix_time_by_risk,
        x='Risk_Level',
        y='Time_to_Fix_Hours',
        color='Risk_Level',
        color_discrete_map={
            'High': '#e74c3c',
            'Medium': '#f39c12',
            'Low': '#2ecc71'
        },
        title='Average Time to Fix by Risk Level (Hours)'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

# Display recent incidents in a table
st.markdown("<h2 class='subtitle'>Recent Security Incidents</h2>", unsafe_allow_html=True)

if not filtered_data.empty:
    # Sort by date and select most recent
    recent_incidents = filtered_data.sort_values('Date', ascending=False).head(10)

    # Format the date column
    display_df = recent_incidents.copy()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')

    # Show only relevant columns
    columns_to_show = ['Date', 'Attack_Type', 'Risk_Level', 'Device_Type', 'Status', 'Time_to_Fix_Hours']
    st.dataframe(display_df[columns_to_show], use_container_width=True)
else:
    st.info("No incidents to display for the selected filters.")

# Security tips section
st.markdown("<h2 class='subtitle'>Basic Security Tips</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='info-box'>
        <h3>Password Security</h3>
        <ul>
            <li>Use long, unique passwords for each account</li>
            <li>Consider using a password manager</li>
            <li>Enable two-factor authentication (2FA)</li>
            <li>Never share your passwords with others</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='info-box'>
        <h3>Email Safety</h3>
        <ul>
            <li>Be suspicious of unexpected emails</li>
            <li>Don't click links in emails you don't trust</li>
            <li>Never share sensitive information via email</li>
            <li>Check the sender's email address carefully</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='info-box'>
        <h3>Device Security</h3>
        <ul>
            <li>Keep your software and apps updated</li>
            <li>Use antivirus/anti-malware software</li>
            <li>Back up your important data regularly</li>
            <li>Be careful what you download</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# Footer with additional info
st.markdown("""
<div style="background-color:#f0f0f0; padding:10px; border-radius:5px; margin-top:20px; text-align:center;">
    <p>Cybersecurity Basics Dashboard | Stay Safe Online!</p>
</div>
""", unsafe_allow_html=True)