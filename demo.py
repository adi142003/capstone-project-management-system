import streamlit as st
import mysql.connector
import hashlib
import pandas as pd
from PIL import Image

# Connect to the MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="ab142003",
    database="capstone_db"
)
cursor = db.cursor()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_create_user_form' not in st.session_state:
    st.session_state.show_create_user_form = False
if 'pass_change_form' not in st.session_state:
    st.session_state.pass_change_form = False
if 'logged_in_user' not in st.session_state:
    st.session_state.logged_in_user = None
if 'srn' not in st.session_state:
    st.session_state.srn = None
if 'fid' not in st.session_state:
    st.session_state.fid = None
if 'view_grade' not in st.session_state:
    st.session_state.view_grade = False
if 'give_grade' not in st.session_state:
    st.session_state.give_grade = False


# Streamlit app
st.title("Capstone Database Management")

# Page selection
page = st.sidebar.selectbox("Select Page", ["Home", "Login", "Insert Project", "Dashboard"])

if page == "Home":
    st.subheader("Welcome to the Capstone Database Management System")
    image_ = Image.open("database.jpeg")
    st.image(image_,width=500)
    


elif page == "Login":
    st.header("Login")
    choice = st.selectbox("select user",["admin","student","teacher"])
    if choice == "admin":

        # User input for username and password
        username = st.text_input("Username:")
        password = st.text_input("Password:", type="password")

        #encrypting the password to check with DB
        enc_pass = hashlib.md5(password.encode()).hexdigest()

        # Check login credentials
        if st.button("Login"):
            cursor.execute(f"SELECT * FROM Users WHERE username='{username}' AND pass_word='{enc_pass}'")
            user_data = cursor.fetchone()

            if user_data:
                #login successful
                st.success("Login Successful!")
                st.sidebar.success(f"Logged in as {username}")
                st.session_state.logged_in = True
                st.session_state.logged_in_user = username
            else:
                st.error("Invalid username or password")
    elif choice == "student":
        # User input for username and password
        username = st.text_input("Username:")
        srn = st.text_input("srn")
        password = st.text_input("Password:", type="password")

        #encrypting the password to check with DB
        enc_pass = hashlib.md5(password.encode()).hexdigest()

        # Check login credentials
        if st.button("Login"):
            cursor.execute(f"SELECT * FROM Users WHERE username='{username}' AND pass_word='{enc_pass}'")
            user_data = cursor.fetchone()

            if user_data:
                st.success("Login Successful!")
                st.sidebar.success(f"Logged in as {username}")
                st.session_state.logged_in = True
                st.session_state.logged_in_user = username
                st.session_state.srn = srn
            else:
                st.error("Invalid username or password")

    elif choice == "teacher":
        # User input for username and password
        username = st.text_input("Username:")
        fid = st.text_input("FID:")
        password = st.text_input("Password:", type="password")

        #encrypting the password to check with DB
        enc_pass = hashlib.md5(password.encode()).hexdigest()

        # Check login credentials
        if st.button("Login"):
            cursor.execute(f"SELECT * FROM Users WHERE username='{username}' AND pass_word='{enc_pass}'")
            user_data = cursor.fetchone()

            if user_data:
                st.success("Login Successful!")
                st.sidebar.success(f"Logged in as {username}")
                st.session_state.logged_in = True
                st.session_state.logged_in_user = username
                st.session_state.fid = fid
            else:
                st.error("Invalid username or password")
    
    #button to change password
    if st.button("change password"):
        st.session_state.pass_change_form = not st.session_state.pass_change_form

    # Button to show/hide create user form
    if st.button("Create a New User"):
        st.session_state.show_create_user_form = not st.session_state.show_create_user_form

    if st.session_state.pass_change_form:
        with st.form("password change form"):
            st.subheader("change password")

            username = st.text_input("enter username")
            new_password = st.text_input("enter new password",type='password')
            change = st.form_submit_button("change")

            if change:
                try:
                    cursor.callproc("ChangeStudentPassword", (username,new_password))
                    db.commit()

                    data = next(cursor.stored_results())

                    row_count = cursor.rowcount
                    if row_count>0:
                        # for row in data.fetchall():
                        st.write(data.fetchall()[0][0])
                    else:
                        st.write("no rows found")

                except Exception as e:
                    st.error(f"Error: {e}")

    # Popup for creating a new user
    if st.session_state.show_create_user_form:
        with st.form("create_user_form"):
            st.subheader("Create a New User")

            new_username = st.text_input("New Username:")
            new_password = st.text_input("New Password:", type="password")
            create_user_button = st.form_submit_button("Create User")

            if create_user_button:
                try:
                    # Insert new user into the Users table
                    cursor.execute(f"INSERT INTO Users (username, pass_word) VALUES ('{new_username}','{new_password}') ")
                    db.commit()

                    st.success("User created successfully!")
                    st.session_state.show_create_user_form = False
                except Exception as e:
                    st.error(f"Error: {e}")

elif page == "Insert Project":
    if not st.session_state.logged_in:
        st.warning("Please login to access this page.")
    else:
        st.header("Insert Project Details")
        cursor.execute("select count(*) from project")
        min_proj = cursor.fetchone()[0]+1
        # User input for project details
        project_id = st.number_input("Project ID:",step=1,min_value=min_proj)
        problem_statement = st.text_area("Problem Statement:")
        description = st.text_area("Description:")
        start_date = st.date_input("Start Date:")
        submission_date = st.date_input("Submission Date:")

        if st.button("Insert Project"):
            try:
                # Insert project details into the database
                cursor.execute("""
                    INSERT INTO Project (project_id, problem_statement, description, start_date, submission_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (project_id, problem_statement, description, start_date, submission_date))

                # Commit the changes to the database
                db.commit()

                st.success("Project details inserted successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

elif page == "Dashboard":
    if not st.session_state.logged_in:
        st.warning("Please login to access this page.")
    else:
        st.header("View Tables")

        logged_in_user = st.session_state.logged_in_user

        if logged_in_user.startswith("fac"):
            # Display all tables for user starting with "fac"
            tables = ["my projects", "my teams", "Department","Grades","My interests","view teams performance"]
        
        elif logged_in_user.startswith("stu"):
            # Display specific tables for user starting with "stu"
            tables = ["search team", "my project", "my team","my grade","my interests","project faculty","update description"]
        
        elif logged_in_user.startswith("admin"):
            tables = ["Users"]
        else:
            st.warning("Table access not specified for this user.")

        if tables:
            table_name = st.selectbox("Select Table", tables)

            #faculty related functions 
            if table_name == "my projects":
                cursor.execute(f"""SELECT project_id, problem_statement, description
                                    FROM Project
                                    WHERE project_id IN (
                                        SELECT project_id
                                        FROM Faculty_tracks_project
                                        WHERE faculty_id = '{st.session_state.fid}'
                                    )""")
                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.table(data)

            elif table_name == "my teams":
                cursor.execute(f"""SELECT
                        Team.team_id,
                        Team.no_of_girls,
                        Team.no_of_boys,
                        GROUP_CONCAT(CONCAT(Student.fname, ' ', Student.lname) SEPARATOR ', ') AS team_members
                        FROM Team
                        JOIN Project ON Team.project_id = Project.project_id
                        JOIN Faculty_tracks_project ON Project.project_id = Faculty_tracks_project.project_id
                        JOIN Student ON Team.team_id = Student.team_id
                        WHERE Faculty_tracks_project.faculty_id = '{st.session_state.fid}'
                        GROUP BY Team.team_id;
                        """)
                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.table(data)
            
            elif table_name == "Department":
                cursor.execute(f"""SELECT
                            Faculty.fname AS faculty_name,
                            Project.project_id,
                            Project.problem_statement,
                            Project.description,
                            Project.start_date,
                            Project.submission_date
                            FROM Faculty
                        JOIN Faculty_tracks_project ON Faculty.faculty_id = Faculty_tracks_project.faculty_id
                        JOIN Project ON Faculty_tracks_project.project_id = Project.project_id
                        WHERE Faculty.faculty_id != '{st.session_state.fid}'
                        AND 
                        Faculty.department = 
                        (SELECT department FROM Faculty WHERE faculty_id = '{st.session_state.fid}')""")

                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.table(data)
            
            elif table_name == "Grades":
                phase = st.selectbox("select phase",["phase1","phase2","phase3"])
                team = st.text_input("enter team id")
                project = st.text_input("enter project id")
                grade = st.text_input("write grade in capital letter")
                givegrade = st.button("give grade")
                if givegrade:
                    st.session_state.give_grade = not st.session_state.give_grade

                if st.button("view grades"):
                    st.session_state.view_grade = True
                    
                if givegrade and phase == "phase1":
                    cursor.execute(f"insert into grade (team_id,project_id,{phase}) values ({team},{project},'{grade}')")
                    db.commit()
                elif givegrade and phase == "phase2" or phase == "phase3":
                    cursor.execute(f"update grade set {phase}='{grade}' where team_id={team}")
                    db.commit()
                    st.session_state.give_grade = False
                
                if st.session_state.view_grade == True:
                    cursor.execute(f"select * from grade where team_id = {team}")
                    data = cursor.fetchall()
                    st.table(pd.DataFrame(data,columns=[i[0] for i in cursor.description]))

            elif table_name == "view teams performance":
                cursor.execute(f"""SELECT
                            f.faculty_id,
                            f.fname,
                            f.lname,
                            t.team_id,
                            g.project_id,
                            g.phase1,
                            g.phase2,
                            g.phase3
                        FROM
                            Faculty f
                        JOIN
                            Team t ON f.faculty_id = t.faculty_id
                        JOIN
                            grade g ON t.team_id = g.team_id;
                        """)
                st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))
                if st.checkbox("show best team"):
                    cursor.execute(f"""SELECT
                        team_id,
                        MAX(phase1) AS highest_phase1,
                        MAX(phase2) AS highest_phase2,
                        MAX(phase3) AS highest_phase3
                    FROM
                        grade
                    GROUP BY
                        team_id
                    ORDER BY
                        highest_phase1 DESC, highest_phase2 DESC, highest_phase3 DESC
                    LIMIT 1""")
                    st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))
               

            #students related functions
            if table_name == "search team":
                cursor.execute("select count(team_id) from team")
                max_teams = cursor.fetchone()
                max_teams = max_teams[0]
                team_id = st.number_input("",step=1,min_value=1,max_value=max_teams)
                cursor.execute(f"select * from student where team_id = {team_id}")
                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.dataframe(data)

            elif table_name == "my project":
                cursor.execute(f"""SELECT
                            Team.team_id,
                            Project.project_id,
                            Project.problem_statement,
                            Project.description,
                            Project.start_date,
                            Project.submission_date
                            FROM
                                Student
                            JOIN
                                Team ON Student.team_id = Team.team_id
                            JOIN
                                Project ON Team.project_id = Project.project_id
                            WHERE
                                Student.SRN = '{st.session_state.srn}'""")
                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.table(data)
            
            elif table_name == "my team":
                cursor.execute(f"""SELECT team_id,SRN,fname,lname,email
                                    FROM Student
                                    WHERE team_id = (
                                            SELECT team_id
                                            FROM Student
                                            WHERE SRN = '{st.session_state.srn}')""")
                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.table(data)
            
            elif table_name == "my interests":
                cursor.execute(f"""select interests 
                               from student join student_interests 
                               on student.srn = student_interests.srn 
                               and student.srn='{st.session_state.srn}'""")
                data = cursor.fetchall()
                data = pd.DataFrame(data,columns=[i[0] for i in cursor.description])
                st.table(data)

            elif table_name == "project faculty":
                proj_id = st.text_input("enter project id")
                show = st.button("enter")

                if show:
                    cursor.callproc("GetProjectFaculty", (proj_id,))
                    db.commit()

                    data = next(cursor.stored_results())

                    row_count = cursor.rowcount
                    if row_count>0:
                        # for row in data.fetchall():
                        st.table(pd.DataFrame(data.fetchall(),columns=[i[0] for i in data.description]))
                    else:
                        st.write("no rows found")

            elif table_name == "update description":
                your_project_id = st.text_input("enter project id")
                your_desc = st.text_input("enter description")
                if st.button("submit"):
                    cursor.execute(f"select UpdateProjectDescription({your_project_id},'{your_desc}')")
                    data = cursor.fetchone()[0]
                    if data:
                        st.write(data)
                    else:
                        st.error("no data")
                if st.button("show update"):
                    cursor.execute(f"select * from project where project_id={your_project_id}") 
                    st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))

            elif table_name == "My interests" and logged_in_user.startswith("fac"):
                cursor.execute(f"""SELECT
                            ffi.field_of_interest
                        FROM
                            Faculty f
                        JOIN
                            Faculty_field_of_interest ffi ON f.faculty_id = ffi.faculty_id
                        WHERE
                            f.faculty_id = {st.session_state.fid}""")
                st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))
                
            elif table_name == "my grade":
                cursor.execute(f"""select fname, lname, phase1,phase2,phase3 
                               from student s, grade g where s.team_id = g.team_id and srn={st.session_state.srn}""")
                st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))

            #admin functions
            if table_name == "Users":
                user = st.text_input("enter user name")
                cursor.execute("select * from users")
                st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))
                if st.button("delete user"):
                    cursor.execute(f"delete from users where username='{user}'")
                    db.commit()

                    cursor.execute("select * from users")
                    st.table(pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description]))


                
# Close the database connection
db.close()
