import streamlit as st
from utils.utils import *
import pandas as pd
import datetime

# this function will be the body of the page
def instructor_page():
    col1, col2 = st.columns([2,3])
    # we make a base query since there is no search yet we show all instructors
    query_base = "SELECT * FROM INSTRUCTOR;"
    init_data = execute_query(st.session_state['connection'], query_base)
    df_base = pd.DataFrame(init_data)
    

    with col1:
        last_name = st.text_input("Instructor last name :")
        birth_date = st.date_input("Instructor birth date :")
        
        show = st.button("show", type="primary")
        if show:
            query_base = f"Select * FROM INSTRUCTOR WHERE Surname LIKE '{last_name}%' OR BirthDate = '{birth_date}'"
            init_data = execute_query(st.session_state['connection'], query_base)
            df_base = pd.DataFrame(init_data)
        

    with col2:
        # we show the result of a search as string not a table
        for index, row in df_base.iterrows():
            st.write(" 🤼 | Name : ", row["Name"],"| LastName : ", row["Surname"],"| Email : ", row["Email"],"| Tel Number : ", row["Telephone"])
            st.write("--------------------------")
            if row.empty:
                st.warning("No result has been found")
            

            

if __name__ == "__main__":
    st.title(":red[Instrocturs]")


    if check_connection():
        instructor_page()
    else:
        st.warning("please connect to database")

       
