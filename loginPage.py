# 1.connect to databse
# 2. add user


import os
from dotenv import load_dotenv
import psycopg2 as pg

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


def get_AllUsers():
    cursor.execute('SELECT * FROM Users') #so this gather the results

    data = cursor.fetchall() #this allows me to access the results within my code

    return data