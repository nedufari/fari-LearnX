from deta import Deta
import os
from dotenv import load_dotenv
import bcrypt



load_dotenv(".env")
DETA_KEY =os.getenv("DETA_KEY")


deta=Deta(DETA_KEY) # to initialize the key and deta 

#create a database connection 

db= deta.Base("learnX_user_db")

def insert_user(username, user_dict):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return db.put({"key":username, "name":user_dict["name"], "password":user_dict["password"]}) #the primary key is the username 


# to fetch all the users 

def db_fetch():
    res =db.fetch()
    return res.items
print (db_fetch())


# def update_user(username, updates):
#     return db.update(updates,username)

# update_user("ellafari", updates={"name":"laraba usman"})


# def delete(username):
#     return db.delete(username)
# delete("ellafari")