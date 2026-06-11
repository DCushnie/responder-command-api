from fastapi import FastAPI
from loginPage import get_AllUsers,get_SpecificUser

app = FastAPI()
users = get_AllUsers()
 

@app.get("/allusers")
def new():
    return {"message":"hello there","data":users}

@app.get("/user/{username}")
def send_specificUser(username: str):
    u_data = get_SpecificUser(username)
    return {"message": "working on it","data": u_data}