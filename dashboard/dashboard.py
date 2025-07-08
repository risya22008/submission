import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
day_df = pd.read_csv("https://raw.githubusercontent.com/risya22008/submission/refs/heads/main/data/day.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/risya22008/submission/refs/heads/main/data/hour.csv")

# Preprocessing
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
day_df['year'] = day_df['yr'].map({0: 2011, 1: 2012})
day_df['season_name'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

# Setup UI
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")
st.title("🚴‍♀️ Bike Sharing Analysis Dashboard")

# Sidebar filter
st.sidebar.header("Filter Data")
year_filter = st.sidebar.multiselect("Select Year", options=day_df['year'].unique(), default=day_df['year'].unique())
season_filter = st.sidebar.multiselect("Select Season", options=day_df['season_name'].unique(), default=day_df['season_name'].unique())

filtered_data = day_df[(day_df['year'].isin(year_filter)) & (day_df['season_name'].isin(season_filter))]

# Data preview
st.subheader("🗂️ Preview Filtered Data")
st.dataframe(filtered_data.head())
st.markdown("---")

# Monthly Usage
st.subheader("📆 Monthly Bike Usage")
monthly_usage = filtered_data.groupby(['year', 'mnth'])['cnt'].sum().reset_index()
monthly_usage['month'] = monthly_usage['mnth']
monthly_usage['date'] = pd.to_datetime(monthly_usage[['year', 'month']].assign(day=1))

plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly_usage, x='date', y='cnt', marker="o", color="#3E8E7E")
plt.title('Total Monthly Bike Usage')
plt.xlabel('Month')
plt.ylabel('Total Usage')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt.gcf())
st.markdown("---")

# Season Usage
st.subheader("🌤️ Usage by Season")
season_df = filtered_data.groupby("season_name")[["casual", "registered"]].sum().reset_index()
season_df = pd.melt(season_df, id_vars="season_name", var_name="user_type", value_name="ride_count")

plt.figure(figsize=(8, 5))
sns.barplot(x="season_name", y="ride_count", hue="user_type", data=season_df, palette="Set2")
plt.title("Bike Usage per Season by User Type")
plt.xlabel("Season")
plt.ylabel("Ride Count")
st.pyplot(plt.gcf())
st.markdown("---")

# Clustering by Hour
st.subheader("⏱️ Hourly Usage Grouped")
hour_df['hour_range'] = pd.cut(hour_df['hr'], bins=[-1, 6, 11, 16, 21, 24],
                               labels=["Midnight", "Morning", "Afternoon", "Evening", "Night"])
hour_grouped = hour_df.groupby("hour_range")[["casual", "registered", "cnt"]].mean().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
hour_grouped.plot(kind='bar', x='hour_range', y=['casual', 'registered'], ax=ax, color=["#f4a261", "#2a9d8f"])
plt.title("Average Usage by Hour Group")
plt.xlabel("Time of Day")
plt.ylabel("Average Usage")
plt.grid(True)
st.pyplot(fig)
st.markdown("---")

# Clustering by Temp Group (Binning)
st.subheader("🌡️ Usage by Temperature Group")

def temp_group(temp_value):
    if temp_value < 0.3:
        return 'Low'
    elif temp_value < 0.6:
        return 'Medium'
    else:
        return 'High'

hour_df['temp_group'] = hour_df['temp'].apply(temp_group)
grouped_temp = hour_df.groupby('temp_group')[['casual', 'registered', 'cnt']].mean().reset_index()

fig, axs = plt.subplots(1, 3, figsize=(24, 5))
colors = ["#457b9d", "#1d3557", "#a8dadc"]

sns.barplot(x='temp_group', y='cnt', data=grouped_temp, ax=axs[0], palette=colors)
axs[0].set_title("Avg Total Usage")
axs[0].set_ylabel("Average")

sns.barplot(x='temp_group', y='casual', data=grouped_temp, ax=axs[1], palette=colors)
axs[1].set_title("Avg Casual Usage")
axs[1].set_ylabel("Average")

sns.barplot(x='temp_group', y='registered', data=grouped_temp, ax=axs[2], palette=colors)
axs[2].set_title("Avg Registered Usage")
axs[2].set_ylabel("Average")

plt.suptitle("Bike Usage by Temperature Group")
st.pyplot(fig)
