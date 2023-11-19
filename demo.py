import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import hashlib

#connecting to database
try:
    conn = mysql.connector.connect(
        host= 'localhost',
        user = 'root',
        password = 'ab142003',
        database = 'capstone_db'
    )
    if conn.is_connected():
            print(f"Connected to MySQL database: {conn.get_server_info()}")
except mysql.connector.Error as e:
        print(f"Error: {e}")

#cursor
cur = conn.cursor()

#function to execute queries
def execute_query(connection,query):
    try:
        cur.execute(query)
        connection.commit()
        print("Query executed successfully")
        return True

    except Error as e:
        print(f"Error: {e}")

#user auth
def login(username, password):
    #checking against database
    enc_pass = hashlib.md5(password.encode()).hexdigest()
    check_user = f"SELECT * FROM Users WHERE username = '{username}' AND pass_word = '{enc_pass}'"
    
    cur.execute(check_user)
    user = cur.fetchone()
    # print(user)
    if user:
        return True
    else:
        return False

#adding new users
def sign_up(username, password):
    if username and password:
        #checking against database
        insert_user = f"INSERT INTO Users (username, pass_word) VALUES ('{username}', '{password}')"
        res = execute_query(conn,insert_user)
        conn.commit()
        if res:
            return True
        else:
            st.warning('some DB error')
            return False
    else:
        return False


def main():
    st.title(":blue[CAPSTONE MANAGEMENT SYSTEM]")
    menu = ["Home","Login","Signup"]
    choice = st.sidebar.selectbox("Menu",menu)
    st.session_state.is_logged_in = False
    if choice=="Home":
        st.header("Home")   
        
    if choice=="Login":
        st.sidebar.write("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        submitted = st.sidebar.checkbox("login/logout")
        if submitted:
            if login(username, password):
                st.success("Logged in!")
                st.session_state.is_logged_in =True
            else:
                st.error("Invalid username or password")
        if st.session_state.is_logged_in == True:
            action = st.selectbox("Actions",["view teams","view projects"])
            if action == "view teams":
                cur.execute("select * from team")
                data = cur.fetchall()
                df = pd.DataFrame(data,columns=["team_id","no_of_girls","no_of_boys","phase1_grade","phase2_grade","phase3_grade","project_id","faculty_id"])
                st.dataframe(df)
            if action == "view projects":
                cur.execute("select * from project")
                data = cur.fetchall()
                df = pd.DataFrame(data,columns=['project_id', 'problem statement', 'description', 'start_date', 'submission_date', 'phase1', 'phase 2', "phase 3"])
                st.dataframe(df)

    if choice=="Signup":
         st.subheader("dont have an account? Sign-up")  
         with st.form("signup_form",clear_on_submit=True):
                st.write("Sign up")
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")

                submitted = st.form_submit_button("Submit")
                if submitted:
                    if sign_up(username, password):
                        st.success("account created")
                    else:
                        st.error("Invalid username or password")   



if __name__ == "__main__":
    main()



