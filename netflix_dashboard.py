import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# Set page config - MUST be the first Streamlit command
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Title
st.title("Netflix Data Dashboard")

# Load Data
data = pd.read_csv('netflix_titles.csv')

# Sidebar Filters
st.sidebar.header("Filters")
selected_type = st.sidebar.selectbox("Select Type", ["All"] + list(data['type'].unique()))

# Data Preprocessing
data['date_added'] = pd.to_datetime(data['date_added'], format='mixed')
data['year_added'] = data['date_added'].dt.year
data['month_added'] = data['date_added'].dt.month

# Handle Missing Values
data.fillna({'director': 'Unknown', 'cast': 'Unknown', "country": 'Unknown', 'rating': 'Unknown', 'duration': 'Unknown'}, inplace=True)
data.dropna(inplace=True)

# Filter Data based on selection
if selected_type != "All":
    data = data[data['type'] == selected_type]

# Display Data
st.subheader("Netflix Data Preview")
st.dataframe(data.head(20))

# Type Distribution
st.subheader("Content Type Distribution")
data_type = data['type'].value_counts().reset_index()
fig1 = px.pie(data_type, values='count', names='type', title='Type Distribution', color_discrete_sequence=['grey', '#e50914'])
st.plotly_chart(fig1)

# Rating Distribution
st.subheader("Ratings Distribution")
data_rate = data['rating'].value_counts().reset_index()
fig2 = px.bar(data_rate, x='rating', y='count', title='Rating Counts', color_discrete_sequence=['grey', '#e50914'])
st.plotly_chart(fig2)

# Year Added Analysis
st.subheader("Year Content Was Added")
data_added_year = data['year_added'].value_counts().reset_index()
fig3 = px.bar(data_added_year, x='year_added', y='count', title='Year Added Counts', color_continuous_scale=['grey', '#e50914'])
st.plotly_chart(fig3)

# Country-wise Content
st.subheader("Top 10 Countries with Most Content")
data_country = data['country'].value_counts().reset_index().head(10)
fig4 = px.bar(data_country, x='country', y='count', title='Top 10 Countries', color_discrete_sequence=['grey', '#e50914'])
st.plotly_chart(fig4)

# Duration Analysis (Seasons & Minutes)
st.subheader("Content Duration Analysis")
filtered_seasons = data[data['duration'].str.contains('Season', case=False, na=False)]['duration'].value_counts().reset_index()
filtered_seasons = filtered_seasons.reset_index()  # Reset index to make it a column
fig5 = px.bar(filtered_seasons, x='index', y='count', title='Seasons Distribution', color_discrete_sequence=['grey', '#e50914'])
st.plotly_chart(fig5)

#minutes distributuon
filtered_minutes = data[data['duration'].str.contains('min', case=False, na=False)]['duration'].value_counts().reset_index()
filtered_minutes = filtered_minutes.reset_index()  # Ensure index is a column
fig6 = px.bar(filtered_minutes, x=filtered_minutes.index, y='duration', title='Minutes Distribution', color_discrete_sequence=['grey', '#e50914'])
st.plotly_chart(fig6)

# Movie vs TV Show Trend Analysis
st.subheader("Trend Analysis: Movie vs TV Shows")
type_data = data[['type', 'year_added']]
tv_shows = type_data[type_data['type'] == 'TV Show'].groupby('year_added')['type'].count()
movies = type_data[type_data['type'] == 'Movie'].groupby('year_added')['type'].count()

plt.figure(figsize=(15, 8))
plt.plot(tv_shows.index, tv_shows.values, label='TV Shows', color='white', linewidth=2)
plt.plot(movies.index, movies.values, label='Movies', color='red', linewidth=2)
plt.title('Movie vs TV Show Trend Over Years', fontsize=20, color='white')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.legend()
st.pyplot(plt)

st.write("### Netflix Dashboard Completed 🚀")
