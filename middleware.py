import time
from fastapi import FastAPI, Request


app = FastAPI()


@app.middleware("http")
def authentication(req: Request, call_next):
    print(req.cookies)