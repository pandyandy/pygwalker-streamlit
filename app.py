import pandas as pd
import streamlit as st
from pygwalker.api.streamlit import StreamlitRenderer

LOGO_URL = 'https://assets-global.website-files.com/5e21dc6f4c5acf29c35bb32c/5e21e66410e34945f7f25add_Keboola_logo.svg'

st.set_page_config(layout="wide")

st.markdown(
    f'''
    <div style="text-align: left;">
        <img src="{LOGO_URL}" alt="Logo" width="200">
    </div>
    ''',
    unsafe_allow_html=True
)

def app():
    df = pd.read_csv('sample_data.csv')

    pyg_app = StreamlitRenderer(df)
    
    pyg_app.explorer()

app()