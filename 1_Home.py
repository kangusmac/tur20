import pandas as pd
import folium
import streamlit as st
from streamlit_folium import st_folium


st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

st.write('Godmorgen, *Kolding!* :sunglasses:')

@st.cache_data
def read_data():
    df = pd.read_csv('geomu.csv')
    return df

def create_map(df):
    lat_avg = df.latitude.mean()
    lng_avg = df.longitude.mean()
    m = folium.Map(location=[lat_avg, lng_avg], zoom_start=17)
    for _, row in df.iterrows():
        folium.Marker(
            [row.latitude, row.longitude], popup=row.address
        ).add_to(m)
    return m


df = read_data()
m = create_map(df)
events = st_folium(m)