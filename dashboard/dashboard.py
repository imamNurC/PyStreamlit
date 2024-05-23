import streamlit as st 
import pandas as pd 
import altair as alt

st.write(
    """
    # Analisis Kecenderungan Arah dan Kecepatan Udara Pada kota Wanliu di tahun 2013
    Hello, para calon praktisi data masa depan!
    """
)


data = pd.read_csv("./data/PRSA_Data_Wanliu_20130301-20170228.csv")

df = data.drop(['station'], axis=1)
df.fillna(method = "ffill", inplace=True)



df["wind_direction"]= df["wd"]
wind_direction_df = df[['wind_direction', 'wd']].copy()
wind_direction_df = wind_direction_df.groupby(by="wind_direction").agg({"wd": "count"}).sort_values(by="wd", ascending=False).reset_index()
wind_direction_df = wind_direction_df.rename(columns = {'wd' : 'jumlah'})
wind_direction_df['percent'] = round((wind_direction_df['jumlah'] / wind_direction_df['jumlah'].sum()) * 100, 2)


st.write(pd.DataFrame({
    'wind_direction': wind_direction_df['wind_direction'],
    'description': [
        'North East', 'South West', 'East North East', 'North North East', 'North',
        'West South West', 'South South West', 'North North West', 'West', 'East',
        'North West', 'South', 'West North West', 'South East', 'South South East', 'East South East'
    ],
    'jumlah': wind_direction_df['jumlah'],
    'persen': wind_direction_df['percent'],
}))

st.title(" Data Kecenderungan arah udara di kota winliu")

# Create a bar chart using Altair
bar_chart = alt.Chart(wind_direction_df).mark_bar().encode(
    x=alt.X('wind_direction', sort=None, title='Wind Direction'),
    y=alt.Y('percent', title='Percentage (%)'),
    tooltip=['wind_direction', 'percent']
).properties(
    title='Persentase Arah Angin',
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=18
)

# Display the bar chart
st.altair_chart(bar_chart, use_container_width=True)

# Linechart
st.line_chart(wind_direction_df.set_index('wind_direction')['percent'])




####----------------==============================
from datetime import datetime

# Define initial data for one day
initial_wind_speed = [4.4, 4.7, 5.6, 3.1, 2.0, 3.7, 2.5, 3.8, 4.1, 2.6, 3.6, 3.7, 5.1, 4.3, 4.4, 2.8, 3.9, 2.8, 2.1, 2.8, 2.1, 0.8, 1.8, 1.4]

# Generate data for 30 days with different wind speeds
all_days_data = []
for day in range(1, 31):
    wind_speeds = [speed + (day * 0.1) for speed in initial_wind_speed]  # Modify wind speed values for each day
    day_data = {
        'year': [2013] * 24,
        'month': [3] * 24,
        'day': [day] * 24,
        'hour': list(range(24)),
        'WSPM': wind_speeds,
        'time': [f'{i:02}:00' for i in range(24)],
        'date': [f'2013-03-{day:02} {hour:02}:00' for hour in range(24)]
    }
    all_days_data.append(pd.DataFrame(day_data))

# Concatenate all days data into a single DataFrame
month_df = pd.concat(all_days_data).reset_index(drop=True)

# Convert 'date' to datetime format for proper plotting
month_df['date'] = pd.to_datetime(month_df['date'])

# Aggregate data to get mean wind speed for each day
wind_speed_day = month_df.groupby(['year', 'month', 'day']).agg({
    'WSPM': 'mean'
}).sort_values(by=['year', 'month', 'day'], ascending=True).reset_index()

wind_speed_day['time'] = wind_speed_day["year"].astype(str) + "-" + wind_speed_day["month"].astype(str) + "-" + wind_speed_day["day"].astype(str)

# Streamlit app starts here
st.title(" Data Kecepatan angin bulan maret 2013 di kota winliu")

# Add a date selector
selected_date = st.date_input("Select a date:", datetime(2013, 3, 1), min_value=datetime(2013, 3, 1), max_value=datetime(2013, 3, 30))

# Filter data based on the selected date
filtered_df = month_df[month_df['date'].dt.date == selected_date]

# Plot the filtered data using Altair
line_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
    x=alt.X('time', title='Time (Hour)'),
    y=alt.Y('WSPM', title='Wind Speed (m/s)'),
    tooltip=['time', 'WSPM']
).properties(
    title=f'Wind Speed on {selected_date.strftime("%Y-%m-%d")}',
    width=800,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=18
)

# Display the line chart
st.altair_chart(line_chart, use_container_width=True)