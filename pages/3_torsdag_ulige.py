import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Torsdag ulige", page_icon=":house:")
st.write("# Torsdag ulige")
csv_file = 'data/torsdag_ulige_merged.csv'

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


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
raw_data = load_data(csv_file)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

col1,col2 = st.columns([1,2])

with col1:
    st.write('Tømninger:')
    antal = raw_data['antal'].sum()
    st.write(f'Antal: {antal}')
    #st.write(raw_data['antal'].sum())


st.write('Fordelt på typer:')
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


# Antal = raw_data['antal'].sum()
# st.write(f'Antal: {Antal}')
# #st.write(raw_data['type'].unique())
# antal_type = raw_data.groupby(['type'])[["antal"]].sum(numeric_only=True)
# #antal_type = antal_type['antal']
# st.write('Fordelt på type:')
# #st.write(raw_data['type'].unique())
# st.write(antal_type)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(raw_data)
