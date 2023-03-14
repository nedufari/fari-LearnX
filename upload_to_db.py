import streamlit_authenticator as stauth

import database as db

usernames =["ellafari","nedu","fred","eniola"]
names=["abubakar emmanuella", "anolue francis ", "sylva fred","eniola"]
password =["fari123","nedu123","fred123","eniola123"]

hash_passwords =stauth.Hasher(password).generate()

for (username, name, hash_password) in zip(usernames,names,hash_passwords ):
    db.insert_user(username,name,hash_password)