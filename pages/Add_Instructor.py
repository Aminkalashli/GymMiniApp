import streamlit as st
from utils.utils import *


# this function will check to our data shoud not be empty before committing
def check_info(insert_dict):
    for key in insert_dict.keys():
        # if our attribute is key we are allowed to have empty data since it is optional
        if key == "Telephone":
            pass
        elif insert_dict[key] == "":
            return False
        
        
    return True

# this fuction will make a quury for a given dictionary 
# keys are attributes and values are our data
def insert_dictionary(data_dic):
    if check_info(data_dic):
        attributes = ",".join(data_dic.keys())
        values = tuple(data_dic.values())
        query = f"INSERT INTO INSTRUCTOR ({attributes}) VALUES {values};"
        
        try :
            execute_query(st.session_state['connection'], query)
            st.session_state['connection'].commit()
        except Exception as err:
            st.error(err)
            return False
        
        return True
    else:
        return False
    
        
# this function will create the body of the form
def create_form():
    with st.form("New Instructor"):
        st.header(":blue[Add Instructor:]")
        
        FisCode = st.text_input("Fiscale Code")
        name = st.text_input("Name")
        surname = st.text_input("Surname")
        birthDate = st.date_input("Birth Date")
        email = st.text_input("Email", placeholder="example@mail.it")
        telephone = st.text_input("Telephone")

        # we put our data in a dictionary in such that our keys are attributes of our database table and values are our new data which will be committed
        insert_dict= {"FisCode":FisCode, "Name":name,"Surname":surname,"BirthDate":birthDate.isoformat(),"Email":email,"Telephone":telephone}

        submitted = st.form_submit_button("Submit", type="primary")

        if submitted:
            if insert_dictionary(insert_dict):
                st.success("Instructor has been added", icon='🔥')
                st.write(insert_dict)

            else:
                st.error("Unable to add instructor.",icon='⚠️')



if __name__ == "__main__":
    st.title("🖊 Add Instructor")
    if check_connection():
        create_form()
    else:
        st.warning("please connect to database")



    
    
    