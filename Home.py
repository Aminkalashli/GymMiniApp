import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="My App",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://dbdmg.polito.it/',
        'Report a bug': "https://dbdmg.polito.it/",
        'About': "# *Introduction to Databases* course"
    }
)
st.title("📈 My App")