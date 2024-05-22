import streamlit as st 
import pandas as pd 

st.write(
    """
    # My first app
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


st.line_chart(wind_direction_df['percent'])