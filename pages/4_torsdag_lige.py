import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Torsdag lige", page_icon=":house:")
st.write("# Torsdag lige")
csv_file = 'data/torsdag_lige_merged.csv'

@st.cache_data
def load_data(data):
    data = pd.read_csv(data)
    #'''cast column "postnr" to string'''
    data['postnr'] = data['postnr'].astype(str)
    data = data.drop(columns=['tur'])
    #return_data = data.groupby(['gade', 'postnr', 'beholder'])['antal'].sum(numeric_only=True).reset_index()
    return_data = data
    # '''return data where antal is greater than 0'''
    #return_data = return_data[return_data['antal'] > 0]
    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)
    return return_data

def create_map(df):
    lat_avg = df.latitude.mean()
    lng_avg = df.longitude.mean()
    m = folium.Map(location=[lat_avg, lng_avg], zoom_start=17)
    for _, row in df.iterrows():
        folium.Marker(
            [row.latitude, row.longitude], popup=row.gade
        ).add_to(m)
    return m


# df = read_data()
# m = create_map(df)
# events = st_folium(m)


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
raw_data = load_data(csv_file)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

m = create_map(raw_data)

tab1, tab2 = st.tabs(['Kort', 'Info'])

with tab2:
    
    col1,col2 = st.columns([1,2])

    with col1:
        st.write('Tømninger:')
        antal = raw_data['antal'].sum()
        st.write(f'Antal: {antal}')
        #st.write(raw_data['antal'].sum())


        st.write('Fordelt på størrelser:')
        antal_type = raw_data.groupby(['type'])[["antal"]].sum(numeric_only=True).reset_index()

        antal_type = antal_type.set_index('type')
        st.write(antal_type.T)

        st.divider()

        st.write('Sække til ombytning:')
        antal_sække = raw_data[raw_data['sæk']].groupby(['gade', 'postnr', 'beholder', 'fremsætter'])['antal'].sum(numeric_only=True).reset_index()
        st.write(f' Antal: {raw_data["sæk"].sum()}')
        sække = raw_data[raw_data['sæk']]
        if st.checkbox('Vis Adresser'):
        #st.write(sække[['gade', 'postnr', 'antal', 'beholder', 'fremsætter']])
            st.write(antal_sække)

        st.divider()

        st.write('Fremsætninger:')
        antal_fremsætninger = raw_data[raw_data['fremsætter']].groupby(['gade', 'postnr', 'beholder'])['antal'].sum(numeric_only=True).reset_index()
        st.write(f' Antal: {raw_data["fremsætter"].sum()}')
        if st.checkbox('Vis Adresser_2'):
            st.write(antal_fremsætninger)





        if st.checkbox('Show raw data'):
            st.subheader('Raw data')
            st.write(raw_data)

with tab1:
    st.write('Kort over tømninger:')
    #m = create_map(raw_data)
    events = st_folium(m)
    #st.write(st_folium(m))