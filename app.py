import pandas as pd
import streamlit as st
import os
import base64

import streamlit.components.v1 as components
from pygwalker.api.streamlit import init_streamlit_comm, get_streamlit_html
from src.keboola_storage_api.connection import add_keboola_table_selection

st.set_page_config(layout='wide')

image_path = os.path.dirname(os.path.abspath(__file__))

logo_image = image_path+"/static/keboola_logo.png"
logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 150px; margin-left: -10px;"></div>'
st.markdown(f"{logo_html}", unsafe_allow_html=True)

st.title('🐷+🐙=💙')

def get_uploaded_file(upload_option):
    if upload_option == 'Connect to Keboola Storage':
        add_keboola_table_selection()
        st.session_state.setdefault('uploaded_file', None)
    elif upload_option == 'Use Demo Dataset':
        file = image_path + "/data/sample_data.csv"
        st.session_state['uploaded_file'] = file
    return st.session_state['uploaded_file']

@st.cache_resource
def get_pyg_html(df: pd.DataFrame) -> str:
    # When you need to publish your application, you need set `debug=False`,prevent other users to write your config file.
    # If you want to use feature of saving chart config, set `debug=True`
    html = get_streamlit_html(df, spec="./gw0.json", use_kernel_calc=True, debug=False)
    return html

def get_df(uploaded_file) -> pd.DataFrame:
    return pd.read_csv(uploaded_file)


# Initialize pygwalker communication
def app():
    if 'uploaded_file' not in st.session_state:
        st.session_state['uploaded_file'] = None

    init_streamlit_comm()

    upload_option = st.sidebar.selectbox('Select an upload option:', 
                                ['Connect to Keboola Storage',
                                'Use Demo Dataset'])

    uploaded_file = get_uploaded_file(upload_option)
    
    if uploaded_file is not None:
        df = get_df(uploaded_file=uploaded_file)

        components.html(get_pyg_html(df), width=1300, height=1000, scrolling=True)

    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

app()
