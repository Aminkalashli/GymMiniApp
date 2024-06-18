import streamlit as st
from sqlalchemy import create_engine, text

# The functions used to connect to database which is usable from every pages

#fucntion for connection to database
def connect_db(dialect, username, password, host, dbname):
    try:
        engine = create_engine(f"{dialect}://{username}:{password}@{host}/{dbname}")
        conn = engine.connect()
        return conn
    except:
        return False
    

# the fuction for executing queries
def execute_query(connection, query):
    return connection.execute(text(query))


#Show numbers in a more compact form
def compact_format(num):
    num=float(num)
    if abs(num) >= 1e9:
        return "{:.2f}B".format(num / 1e9)
    elif abs(num) >= 1e6:
        return "{:.2f}M".format(num / 1e6)
    elif abs(num) >= 1e3:
        return "{:.2f}K".format(num / 1e3)
    else:
        return "{:.0f}".format(num)


def check_connection():
    # it is possible use database connection details predefined
    # dialect = "mysql+pymysql"
    # username = "root"
    # password = "mypassword"
    # host = "localhost"
    # dbname = "gym"

    # Here is you can put detail of the databese as input
    dialect = st.sidebar.text_input("dialect")
    username = st.sidebar.text_input("username")
    password = st.sidebar.text_input("password")
    host = st.sidebar.text_input("host")
    dbname = st.sidebar.text_input("database name")

    if "connection" not in st.session_state.keys():
        st.session_state["connection"]=False

    if st.sidebar.button("Connect to the Database"):
        myconnection=connect_db(dialect,username,password,host,dbname)
        if myconnection is not False:
            st.session_state["connection"]=myconnection

        else:
            st.session_state["connection"]=False
            st.sidebar.error("Error connecting to DB")

    if st.session_state["connection"]:
        st.sidebar.success("Connected to DB")
        return True