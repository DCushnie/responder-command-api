from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
import os
from dotenv import load_dotenv
from fastapi import Depends,HTTPException,Cookie
from typing import Optional

load_dotenv()

KEY = os.getenv("JWT_SECRET")
MIN = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
ALG = os.getenv("ALGORITHM")


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=MIN)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, KEY,algorithm=ALG)

def get_token_from_cookie(token: Optional[str] = Cookie(None)):
    """This func looks for the token inside my cookie"""
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="Not Authenticated, Must login first"
        )
    
    return token

def verify_token(token:str = Depends(get_token_from_cookie)):
    """This func checks that the token the user gave is mine and then gets the current user"""
    try:
        check_token = jwt.decode(token,KEY,algorithms=[ALG])

        username = check_token.get("sub")
        role = check_token.get("role")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return {
            'username': username,
            'user_role': role
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or excpired token")
    
