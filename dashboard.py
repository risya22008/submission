import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Bike Sharing Data Analysis Dashboard")

@st.cache
def load_data():
    data = pd.read_csv('bike_sharing_data.csv') 
    return data

data = load_data()

if st.checkbox('Show raw data'):
    st.write(data)

st.subheader('Bike Usage by Hour')
hourly_usage = data.groupby('hour')['total_rentals'].sum()
st.bar_chart(hourly_usage)

user_type = st.selectbox('Select User Type', ['Casual', 'Registered'])
filtered_data = data[data['user_type'] == user_type]

st.subheader(f'Bike Usage for {user_type} Users')
st.line_chart(filtered_data.groupby('hour')['total_rentals'].sum())

st.write("Dashboard created using Streamlit")
