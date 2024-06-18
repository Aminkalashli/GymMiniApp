import streamlit as st
from utils.utils import *
from datetime import  time

# this function will check to our data shoud not be empty before committing
def check_info(insert_dict):
    for value in insert_dict.values():
        if value == "":
            return False
        
    return True


# this fuction will make a quury for a given dictionary 
# keys are attributes and values are our data
def insert_dictionary(data_dic):
    if check_info(data_dic):
        attributes = ",".join(data_dic.keys())
        values = tuple(data_dic.values())
        query = f"INSERT INTO PROGRAM ({attributes}) VALUES {values}"
        
        try :
            execute_query(st.session_state['connection'], query)
            st.session_state['connection'].commit()
        except Exception as e:
            st.error(e,icon="🚨")
            return False
        
        return True
    else:
        return False
    
        
# wrapper function
def get_info():
    return get_list("Room"), get_list("CodC"), get_list("FisCode")

# the function will be used to get data for a given attribute from database as a list
def get_list(attribute):
    query = f"SELECT DISTINCT {attribute} FROM PROGRAM;"
    result = execute_query(st.session_state['connection'], query=query)
    result_list = []
    for row in result.mappings():
        result_list.append(row[attribute])
    
    return result_list

# this function will create the body of the form
def create_form():
    # we need data from database to be our options in room, CodC and Fiscode 
    #so we use get info function as a wrapper function
    # which uses the get_list function to get the result from database
    rooms, cods, fisocdes = get_info()
    with st.form("New Program"):
        st.header(":blue[Add Program:]")
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        fiscode = st.selectbox("Fiscal Code", fisocdes)
        day = st.selectbox("Day", days)
        startime = st.slider("Start Time",value=time()) # we use time() as value so the givin data will be 00:00:00 then wh change to string to add to database
        duration = st.slider("Duration", 1, 60)
        room = st.selectbox("Room", rooms)
        codc = st.selectbox("Cod Course", cods)
        

        dat_dic= {"FisCode":fiscode, "Day":day,"StartTime":startime.strftime('%H:%M:%S'),"Duration":duration,"Room":room,"CodC":codc}

        submitted = st.form_submit_button("Submit", type="primary")

        if submitted:
            # after submission we check for the correctness of the commit
            if insert_dictionary(data_dic=dat_dic):
                st.success("You have added this Course : ", icon = "🔥")
                st.write(dat_dic)

            else:
                st.error("Unable to add Course.",icon='⚠️')



if __name__ == "__main__":
    st.title("🖊 Add Program")


    if check_connection():
        create_form()
    else:
        st.warning("please connect to database")
    
    
    