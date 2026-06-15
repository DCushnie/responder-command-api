# 1.connect to databse
# 2. add user


import os
from dotenv import load_dotenv
import psycopg2 as pg
from psycopg2.errors import UniqueViolation
from fastapi import HTTPException
from passlib.hash import bcrypt
from authHandler import create_access_token
from typing import Optional



load_dotenv()

try:
    conn = pg.connect(
        dbname= os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("HOST")
    )
except:
    print("Failed to connect to database")

cursor = conn.cursor()

def check_User(username,passwrd):

    try:
        user_info = get_SpecificUser(username)
        user_pass = user_info[2]
    except:
        raise HTTPException(304, detail="User does not exist")

    result = bcrypt.verify(passwrd,user_pass)

    if result == True:
        token = create_access_token({
        "sub":str(user_info[0]),
        "role": user_info[3]
        })
    else:
        raise HTTPException(304,detail="not authorised")

    return token

    

def get_AllUsers():
    query = 'SELECT * FROM Users'
    cursor.execute(query) #so this gather the results

    data = cursor.fetchall() #this allows me to access the results within my code

    return data

def get_SpecificUser(usrnm):
    
    specific_userquery = "SELECT * FROM Users WHERE username = %s"

    cursor.execute(specific_userquery,(usrnm,))
    userdetails = cursor.fetchone()

    if userdetails:
        return userdetails
    else:
        print("Error: Could not find user")
        return
    
def protectPassword(password):

    hash_passwrd = bcrypt.using(rounds=12).hash(password)
    return hash_passwrd



def create_User(usrnm,passwrd,rl):
    new_pass = protectPassword(passwrd)

    query = """
            INSERT INTO Users(username, user_pass,user_role)
            VALUES(%s,%s,%s)
            """

    try:
        cursor.execute(query, (usrnm,new_pass,rl))
    except UniqueViolation:
        conn.rollback() #stops the databsefrom getting stuck
        print("There is already a user with that username")
        raise HTTPException(status_code=500, detail="There is already a user with that username")
    
    conn.commit()
    
    data = get_SpecificUser(usrnm)

    
    return data
    

def delete_User(userid,usrnm):

    delete_query =  """
        DELETE FROM Users WHERE userid = %s
        """

    cursor.execute(delete_query,(userid,)) 
    # the placeholdervalue section must always be a tuple
    

    conn.commit()
    
    check_userData = get_SpecificUser(usrnm)
    
    if check_userData:
        print("Error: Failed to delete user")
    else:
        print("✅ succesfully Deleted User")



def get_responders_only(usrname: Optional[str]):


    if usrname is None:
        responder_query = """
        SELECT * FROM users
        WHERE user_role = 'responder'
            """
        cursor.execute(responder_query)
    else:
        responder_query = """
        SELECT * FROM users
        WHERE user_role = 'responder' and username = %s
            """
        cursor.execute(responder_query,(usrname,))

    data = cursor.fetchall()

    if not data:
        raise HTTPException(status_code=404,detail="USER NOT FOUND")
    else:
        response_data = data[0]

        return{
            'username': response_data[1],
            'user_role': response_data[3]
        }


def get_dispatcher_and_responders_only(usrname: Optional[str] = None):
    
    if usrname is None:
        responder_query = """
        SELECT username,user_role FROM users
        WHERE user_role != 'admin'
            """
        cursor.execute(responder_query)
    else:
        responder_query = """
        SELECT username,user_role FROM users
        WHERE user_role != 'admin' and username = %s
            """
        cursor.execute(responder_query,(usrname,))

    data = cursor.fetchall()

    if not data:
        raise HTTPException(status_code=404,detail="USER NOT FOUND")
    else:
        response_data = data[0]

        # return{
        #     'username': response_data[1],
        #     'user_role': response_data[3]
        # }

        return data


