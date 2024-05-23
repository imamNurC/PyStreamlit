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



###==========================================


data_Winspeed ={
   'year': [2013]*24,
    'month': [3]*24,
    'day': [1]*24,
    'hour': list(range(24)),
    'WSPM': [4.4, 4.7, 5.6, 3.1, 2.0, 3.7, 2.5, 3.8, 4.1, 2.6, 3.6, 3.7, 5.1, 4.3, 4.4, 2.8, 3.9, 2.8, 2.1, 2.8, 2.1, 0.8, 1.8, 1.4],
    'time': [f'{i:02}:00' for i in range(24)]
}


hour_df = pd.DataFrame(data_Winspeed)
st.write(hour_df)

# Create a line chart using Altair
line_chart = alt.Chart(hour_df).mark_line(point=True).encode(
    x=alt.X('time', title='Time (Hour)'),
    y=alt.Y('WSPM', title='Wind Speed (m/s)'),
    tooltip=['time', 'WSPM']
).properties(
    title='Wind Speed over 24 Hours',
    width=600,
    height=400
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=18
)

# Display the line chart
st.altair_chart(line_chart, use_container_width=True)