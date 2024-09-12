import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up dummy data for cybersecurity incidents
np.random.seed(42)
data = pd.DataFrame({
    'Incident_ID': range(1, 101),
    'Risk_Level': np.random.choice(['Low', 'Medium', 'High'], size=100, p=[0.2, 0.5, 0.3]),
    'Attack_Type': np.random.choice(['Phishing', 'Malware', 'DDoS', 'Ransomware'], size=100),
    'Loss_Amount($)': np.random.randint(1000, 50000, size=100),
    'Date': pd.date_range('2024-01-01', periods=100, freq='D')
})

# Streamlit app
st.title("Cybersecurity Risk Assessment Dashboard")

# Sidebar filters
st.sidebar.title("Filter Options")
selected_risk = st.sidebar.multiselect('Select Risk Level', options=['Low', 'Medium', 'High'], default=['Low', 'Medium', 'High'])
selected_attack = st.sidebar.multiselect('Select Attack Type', options=['Phishing', 'Malware', 'DDoS', 'Ransomware'], default=['Phishing', 'Malware', 'DDoS', 'Ransomware'])

# Filter data based on selections
filtered_data = data[(data['Risk_Level'].isin(selected_risk)) & (data['Attack_Type'].isin(selected_attack))]

# Display data table
st.subheader("Incident Data")
st.dataframe(filtered_data)

# Risk level pie chart
st.subheader("Risk Level Distribution")
risk_count = filtered_data['Risk_Level'].value_counts()
fig, ax = plt.subplots()
ax.pie(risk_count, labels=risk_count.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig)

# Loss amount by attack type bar chart
st.subheader("Total Loss by Attack Type")
loss_by_attack = filtered_data.groupby('Attack_Type')['Loss_Amount($)'].sum()
st.bar_chart(loss_by_attack)

# Date-wise risk level trend
st.subheader("Incident Trend Over Time")
incident_trend = filtered_data.groupby('Date').size()
st.line_chart(incident_trend)

# Summary statistics
st.subheader("Summary Statistics")
st.write(filtered_data.describe())

# Provide download button for filtered data
st.sidebar.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_data.to_csv(index=False),
    file_name='filtered_cybersecurity_data.csv',
    mime='text/csv',
)
