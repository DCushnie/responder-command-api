from fastapi import FastAPI
from loginPage import get_AllUsers

app = FastAPI()
users = get_AllUsers()

@app.get("/new")
def new():
    return {"message":"hello there","data":users}