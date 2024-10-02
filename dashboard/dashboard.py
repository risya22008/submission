import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

@st.cache
def load_data():
    return pd.read_csv('cleaned_bike_sharing_data.csv')

data = load_data()

if 'hour' not in data.columns:
    if 'datetime_column' in data.columns:
        data['hour'] = pd.to_datetime(data['datetime_column']).dt.hour  # Adjust 'datetime_column'
    else:
        st.error("Column 'hour' or a datetime column to derive it from is missing.")
        st.stop()

if st.checkbox('Show raw data'):
    st.write(data)

st.subheader('Bike Usage by Hour')
hourly_usage = data.groupby('hour')['total_rentals'].sum()
st.bar_chart(hourly_usage)