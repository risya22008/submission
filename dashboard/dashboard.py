# dashboard.py

import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
day_df = pd.read_csv("https://raw.githubusercontent.com/risya22008/submission/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/risya22008/submission/refs/heads/main/data/hour.csv")

# Convert 'dteday' column to datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Dashboard title
st.title("Bike Sharing Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filter Data")
year_filter = st.sidebar.multiselect("Select Year", options=day_df['yr'].unique(), default=day_df['yr'].unique())
season_filter = st.sidebar.multiselect("Select Season", options=day_df['season'].unique(), default=day_df['season'].unique())

# Apply filters
filtered_data = day_df[(day_df['yr'].isin(year_filter)) & (day_df['season'].isin(season_filter))]

# Display dataset preview
st.subheader("Filtered Data Preview")
st.dataframe(filtered_data.head())

# Line chart for monthly usage
st.subheader("Monthly Bike Usage Over Time")
monthly_usage = filtered_data.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
monthly_usage['year'] = monthly_usage['yr'].apply(lambda x: 2011 if x == 0 else 2012)
monthly_usage.rename(columns={'mnth': 'month'}, inplace=True)
monthly_usage['date'] = pd.to_datetime(monthly_usage[['year', 'month']].assign(day=1))

plt.figure(figsize=(10, 6))
sns.lineplot(data=monthly_usage, x='date', y='cnt', marker="o")
plt.title('Monthly Bike Usage Over Time')
plt.xlabel('Date')
plt.ylabel('Total Bike Usage')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt.gcf())

# Bar plot for seasonal bike usage
st.subheader("Bike Usage by Season")
season_df = filtered_data.groupby("season")[["casual", "registered"]].sum().reset_index()
season_df["season"] = season_df["season"].replace({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
season_df = pd.melt(season_df, id_vars="season", var_name="user_type", value_name="ride_count")

plt.figure(figsize=(10, 6))
sns.barplot(x="season", y="ride_count", hue="user_type", data=season_df, palette=["#FFF455", "#059212"])
plt.title("Bike Usage by Season")
plt.xlabel("Season")
plt.ylabel("Number of Rides")
st.pyplot(plt.gcf())

# Line plot for hourly bike usage
st.subheader("Hourly Bike Usage")
hourly_usage_df = hour_df.groupby("hr")[["casual", "registered"]].sum().reset_index()
hourly_usage_df['hr'] = hourly_usage_df['hr'].apply(lambda x: f"{x}:00")

plt.figure(figsize=(12, 6))
plt.plot(hourly_usage_df["hr"], hourly_usage_df["casual"], marker='o', linewidth=2, color="#FFF455", label='Casual Users')
plt.plot(hourly_usage_df["hr"], hourly_usage_df["registered"], marker='o', linewidth=2, color="#059212", label='Registered Users')
plt.title("Bike Usage by Hour of the Day (Casual vs Registered)")
plt.xlabel("Hour of the Day")
plt.ylabel("Number of Rides")
plt.legend()
plt.grid(True)
st.pyplot(plt.gcf())

# Temperature group usage
st.subheader("Bike Usage Grouped by Temperature")
def temp_group(temp_value):
    if temp_value < 0.3:
        return 'Low'
    elif 0.3 <= temp_value < 0.6:
        return 'Medium'
    else:
        return 'High'

hour_df['temp_group'] = hour_df['temp'].apply(temp_group)
grouped_temp_usage = hour_df.groupby('temp_group').agg({
    'cnt': 'mean',
    'casual': 'mean',
    'registered': 'mean',
}).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(24, 6))
colors = ["#102C57", "#1679AB", "#83B4FF"]

sns.barplot(x='temp_group', y='cnt', data=grouped_temp_usage, palette=colors, ax=ax[0])
ax[0].set_title('Average Bike Usage by Temperature Group')
ax[0].set_ylabel('Average Usage Count')
ax[0].set_xlabel('Temperature Group')

sns.barplot(x='temp_group', y='casual', data=grouped_temp_usage, palette=colors, ax=ax[1])
ax[1].set_title('Average Casual User Usage by Temperature Group')
ax[1].set_ylabel('Average Casual Users')
ax[1].set_xlabel('Temperature Group')

sns.barplot(x='temp_group', y='registered', data=grouped_temp_usage, palette=colors, ax=ax[2])
ax[2].set_title('Average Registered User Usage by Temperature Group')
ax[2].set_ylabel('Average Registered Users')
ax[2].set_xlabel('Temperature Group')

plt.suptitle('Bike Usage Grouped by Temperature')
st.pyplot(plt.gcf())
