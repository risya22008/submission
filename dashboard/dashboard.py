import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load Dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/risya22008/submission/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/risya22008/submission/refs/heads/main/data/hour.csv")

# Convert dteday to datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Title and Description
st.title("Bike Sharing Data Analysis Dashboard")
st.write("""
### Exploratory Data Analysis (EDA) on Bike Sharing Dataset

This dashboard allows you to explore the bike sharing data, with options to filter by time and weather conditions, 
and visualize the peak times for bike usage, as well as the usage patterns by casual and registered users.
""")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_day = st.sidebar.multiselect("Select Day of the Week", options=day_df["weekday"].unique(), default=day_df["weekday"].unique())
selected_weather = st.sidebar.multiselect("Select Weather Condition", options=hour_df["weathersit"].unique(), default=hour_df["weathersit"].unique())

# Apply Filters
filtered_df = hour_df[(hour_df["weekday"].isin(selected_day)) & (hour_df["weathersit"].isin(selected_weather))]

# Show Data
if st.sidebar.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(filtered_df.head())

# Plotting Bike Usage by Hour
st.subheader("Hourly Bike Usage Distribution")
hourly_usage_df = filtered_df.groupby("hr").agg({"cnt": "sum"}).reset_index()
hourly_usage_df['hr'] = hourly_usage_df['hr'].apply(lambda x: f"{x}:00")

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(x="hr", y="cnt", data=hourly_usage_df, marker='o', color="#C80036", ax=ax)
plt.title("Total Bike Usage by Hour", fontsize=18)
plt.xlabel("Hour", fontsize=14)
plt.ylabel("Total Usage", fontsize=15)
plt.xticks(rotation=45)
st.pyplot(fig)

# Plotting Casual vs Registered Users by Hour
st.subheader("Casual vs Registered Users by Hour")
hourly_user_df = filtered_df.groupby("hr")[["casual", "registered"]].sum().reset_index()
fig, ax = plt.subplots(figsize=(12, 5))
plt.plot(hourly_user_df["hr"], hourly_user_df["casual"], marker='o', linewidth=2, color="#FFF455", label='Casual Users')
plt.plot(hourly_user_df["hr"], hourly_user_df["registered"], marker='o', linewidth=2, color="#059212", label='Registered Users')
plt.title("Bike Usage by Hour of the Day (Casual vs Registered)", fontsize=18)
plt.xlabel("Hour of the Day", fontsize=14)
plt.ylabel("Number of Rides", fontsize=14)
plt.legend()
st.pyplot(fig)

# Analysis of Bike Usage by Weather Condition
st.subheader("Bike Usage by Weather Condition")
weather_labels = {1: 'Clear/Partly Cloudy', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain'}
filtered_df['weathersit'] = filtered_df['weathersit'].map(weather_labels)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x="weathersit", y="cnt", data=filtered_df, estimator=sum, ci=None, palette="Set1", ax=ax)
plt.title("Total Bike Usage by Weather Condition", fontsize=18)
plt.xlabel("Weather Condition", fontsize=14)
plt.ylabel("Total Usage", fontsize=15)
st.pyplot(fig)

# Displaying insights
st.subheader("Key Insights")
st.write("""
- **Peak Usage Time**: The peak bike usage time is during morning rush hours (8-9 AM) and evening rush hours (5-6 PM).
- **Weekday vs Weekend**: Registered users tend to use bikes more during weekdays, while casual users are more active on weekends.
- **Weather Impact**: Bike usage significantly decreases during harsh weather conditions like heavy rain or snow.
""")