from fastapi import FastAPI,Request,Response,Depends,APIRouter, HTTPException
from userHandler import get_AllUsers,get_SpecificUser,check_User,create_User,get_responders_only,get_dispatcher_and_responders_only
from fastapi.responses import JSONResponse
from authHandler import verify_token

app = FastAPI()
router = APIRouter()
users = get_AllUsers()
 

@app.get("/allusers")
async def new(current_usr_data = Depends(verify_token)):
    print()
    role = current_usr_data['user_role']

    if role == 'admin':
        return {"message":"hello there","data":users}
    elif role == 'dispatcher':
        u_data = get_dispatcher_and_responders_only()
        return {"message": "Attreval successful", "data": u_data}
    else:
        raise HTTPException(status_code=401,detail="Only authorised personnel can see this page")
        
@app.get("/user/{username}")
def send_specificUser(username: str, current_usr_data = Depends(verify_token)):

    role = current_usr_data['user_role']

    if role == 'admin':
        u_data = get_SpecificUser(username)
    elif role == 'responder':
        u_data = get_responders_only(username)
    elif role == 'dispatcher':
        u_data = get_dispatcher_and_responders_only(username)
    else:
        raise HTTPException(status_code=401,detail="Only admins can see this page")

    return {"message": "Attreval successful", "data": u_data}
    


@app.post("/auth/login")
def login(req:Request,username,password, res: Response):
    token = check_User(username,password)

    return res.set_cookie("token",token,httponly=True,samesite="lax",secure=False)

@app.post("/admin/createuser")
def creation(username,password,role):
    response = create_User(username,password,role)

    print(response)

    return JSONResponse(content="user created sucessfully",status_code=200)


