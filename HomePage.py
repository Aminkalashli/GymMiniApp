import streamlit as st
import numpy as np
import pandas as pd
from utils.utils import *
if __name__ == "__main__":
    st.set_page_config(
        page_title="Gym Analytics",
        layout="wide",
        page_icon="🗂",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# *Introduction to Databases* course - Home Work 4"
        }
    )




        
    

    st.title("🏋 Gym App")

    col1, col2 = st.columns([3,2])

    
    # description of the Homework
    with col1:
        st.markdown("# :red[Gym Analytics] Mini App")
        st.markdown("## :blue[Homework 4] - Introduction To Database Course")
        st.markdown("### :green[Amin Kalashli] - 2024")

        


    with col2:
        st.image("images/polito_white.png")
        


    col11, col22 = st.columns(2)
    if not check_connection():
        st.warning("Please connect to database")
    else:
        with col11:
            query = "SELECT StartTime, COUNT(*) AS Courses FROM PROGRAM GROUP BY StartTime;"

            bar_data = execute_query(st.session_state['connection'], query=query)
            df_lesson = pd.DataFrame(bar_data)
            st.subheader("Number of courses in available time slots")
            st.bar_chart(df_lesson, x = "StartTime", y = "Courses")
        with col22:
            query2 = "SELECT Day, COUNT(*) AS NumberOfLessons FROM PROGRAM GROUP BY Day;"
            area_data = execute_query(st.session_state['connection'], query=query2)
            df_num = pd.DataFrame(area_data)
            st.subheader("Number of lessons in each day")
            st.area_chart(df_num, x = "Day", y = "NumberOfLessons")