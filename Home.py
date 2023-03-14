import streamlit as st
import streamlit_authenticator as sauth
import bcrypt
from deta import Deta
import os
from dotenv import load_dotenv

st.set_page_config(page_title="homepage", page_icon=":tada", layout="wide")

load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY2")

deta = Deta(DETA_KEY)

db = deta.Base("learnX_main_db")

def insert_user(username,name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username,"name":name, "password": password})


def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items

users = fetch_all_users()


usernames = ["pparker", "rmiller"]
names = ["Peter Parker", "Rebecca Miller"]
passwords = ["abc123", "def456"]
hashed_passwords = sauth.Hasher(passwords).generate()


for (username, name, hash_password) in zip(usernames, names, hashed_passwords):
    insert_user(username, name, hash_password)




usernames = [user["key"] for user in users]
names = [user["name"] for user in users]
hashed_passwords = [user["password"] for user in users]

authenticator = sauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

######################creating new user ####################################33

with st.sidebar:
    st.write (" # Happy to join LearnX")
    """
    Register As a New Student """
    name = st.text_input("Enter full name")
    username = st.text_input("Enter username")
    password = st.text_input("Enter password", type='password')
    confirm_password = st.text_input("Confirm password", type='password')

    if password != confirm_password:
        st.error("Passwords do not match")
    else:
        hashed_password = sauth.Hasher([password]).generate()[0]
        if st.button("sign up", key="signup"):

            insert_user(username, name, hashed_password)
            st.success("User registered successfully")





name, authentication_status, username = authenticator.login("Login", "main")



if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")


if authentication_status:
    st.write(""" 
    # LearnX
    ...your improvement is our goal
    """)
    
    # st.write('welcome'+ "   " +username)
    st.write("# Welcome to LearnX! 👋"+ "   "+username)
    st.write("---")
    st.markdown(
    """
    LearnX is a Learning Management System Built by Abubakar Emmanuella Faridat as a final year project. 
    The system is designed to improve the performance of students who enroll in our platform, to give them industry standrard AI driven test and an accurate breakdown of the performance asides the score of the test, detailing their areas of weakness and strength and also prooviding a visualized breakdown of your performance to enable you have a better understand the areas that needs to be improved on.
    
    **👈 Select a course from the sidebar, take your time to go through our materials and attempt the test ** 
    ### What are the Courses We offer at learnX?
    #### We offer three courses for computer science final year student as of now 
   
    - COM 423 Expert System    
    - COM 425 Modelling and Simulation   
    - GNS 425 Law of Contract    
    ### See more of my related works 
    - Follow ths link to see my portfolio [Notion](https://www.notion.so/abubakar-/Emmanuella-Abubakar-a39f3eeb3474436b8a93d95d569fe357 )
    - Behance Portfolio [Behance](https://www.behance.net/manuellabubakar)
""")
    authenticator.logout("logout", "sidebar")






