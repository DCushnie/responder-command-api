from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
import os
from fastapi import Depends,HTTPException
from fastapi.security import OAuth2PasswordBearer

KEY = os.getenv("JWT_SECRET")
MIN = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
ALG = os.getenv("ALGORITHM")
myoauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") #this is where users are able to get a token from

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=int(MIN))
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, KEY,algorithm=ALG)


def verify_token(token:str = Depends(myoauth2_scheme)):
    try:
        check_token = jwt.decode(token,KEY,algorithms=[ALG])

        username = check_token.get("sub")
        role = check_token.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            username: username,
            role: role
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or excpired token")


