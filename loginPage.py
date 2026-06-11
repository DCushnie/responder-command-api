# 1.connect to databse
# 2. add user


import os
from dotenv import load_dotenv
import psycopg2 as pg
from psycopg2.errors import UniqueViolation
from fastapi import HTTPException
from passlib.hash import bcrypt


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

# def check_User(username,passwrd):
#     user_info = get_SpecificUser(username)
#     user_pass = user_info[2]

#     entered_pass_byte = passwrd.encode('utf-8')
#     salt = gensalt(10)
#     hash = hashpw(entered_pass_byte,salt)

#     result = checkpw(entered_pass_byte,hash)

#     print(user_pass)
#     print(result)

    

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

    print(data)
    

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


get_SpecificUser('Thor')