from fastapi import FastAPI,Request,Response
from loginPage import get_AllUsers,get_SpecificUser,check_User
from authHandler import verify_token

app = FastAPI()
users = get_AllUsers()
 

@app.get("/allusers")
def new():
    return {"message":"hello there","data":users}

@app.get("/user/{username}")
def send_specificUser(username: str):
    u_data = get_SpecificUser(username)
    return {"message": "working on it","data": u_data}




@app.post("/auth/login")
def login(req:Request,username,password, res: Response):
    token = check_User(username,password)

    return res.set_cookie("token",token,httponly=True,samesite="lax",secure=False)

