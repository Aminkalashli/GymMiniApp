import streamlit as st
from utils.utils import *
import pandas as pd


CON = st.session_state['connection']
# this will return the list of data related to given atrribute
def get_list(atr):
    query = f"SELECT DISTINCT {atr} FROM COURSES;"
    res = execute_query(st.session_state['connection'], query=query)
    res_list = []
    for row in res.mappings():
        res_list.append(row[atr])
    return res_list

#this will return the level for a given option (MAX or MIN)
def get_level(max_min):
    query = f"SELECT {max_min}(Level) AS res FROM COURSES"
    res = execute_query(st.session_state['connection'], query=query).mappings().first()
    return res['res']


#this funcction is design of expander
def start_expander(expander, Data):
    lcod = list()
    if Data.empty:
        expander.warning("No result has been found")
    else :
        with expander:
            for cod in Data['CodC']:
                cod = "'" + cod + "'"
                lcod.append(cod)
            query = 'SELECT Day, StartTime, Duration, CodC, Room FROM PROGRAM WHERE CodC IN (' + ','.join((l)for l in lcod) + ')'
            query_instructor = 'SELECT FisCode FROM PROGRAM WHERE CodC IN (' + ','.join((l)for l in lcod) + ') GROUP BY FisCode'

            ins_table = execute_query(CON, query=query_instructor)
            tempdf = pd.DataFrame(ins_table)
            fis_list = list()
            for row in tempdf['FisCode']:
                row = "'" + row + "'"
                fis_list.append(row)
            res_table = execute_query(CON, query=query)
            res_df = pd.DataFrame(res_table)
            st.dataframe(res_df, use_container_width=True)

            query_instructor_name = 'SELECT Name, Surname FROM INSTRUCTOR WHERE FisCode IN ('+ ','.join((l)for l in fis_list) +')'
            name_result = execute_query(CON, query_instructor_name)
            df_name = pd.DataFrame(name_result)
            st.dataframe(df_name, use_container_width=True)

            


# The page structure 
def course_page():
    col1, col2 = st.columns(2)


    q1 = "SELECT COUNT(DISTINCT CType) AS NCTYPE FROM COURSES;"
    res_dist = execute_query(st.session_state['connection'],q1).mappings().first()
    q2 = "SELECT COUNT(*) AS Total FROM COURSES;"
    res_tot = execute_query(st.session_state['connection'],q2).mappings().first()
    cours_type = get_list("CType")
    min_val = get_level("MIN")
    max_val = get_level("MAX")
    with col1:
        st.metric("# Course Types", value=res_dist['NCTYPE'])
        type = col1.selectbox("Course types ", cours_type)
        level = st.number_input("Select Level", min_value=min_val, max_value=max_val)
        base_q = f"SELECT * FROM COURSES;"
        serch_res = execute_query(st.session_state['connection'], base_q)
        df = pd.DataFrame(serch_res)
        if st.button("search", type="primary"):
            q_search = f"SELECT * FROM COURSES WHERE CType = '{type}' AND LEVEL = '{level}';"
            serch_res = execute_query(st.session_state['connection'], q_search)
            df = pd.DataFrame(serch_res)


    with col2:
        if df.empty:
            st.warning("No result found", icon="🚨")
        else:
            st.metric("# Total Courses", res_tot['Total'])
            st.dataframe(df, use_container_width=True)


    expander = st.expander("Lesson plans")
    start_expander(expander=expander, Data=df)




if __name__ == "__main__":
    st.title(":red[Courses]")


    if check_connection():
        course_page()
    else:
        st.warning("please connect to database")

       

