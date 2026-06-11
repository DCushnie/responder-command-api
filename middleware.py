import time
from fastapi import Depends,HTTPException
from jose import JWTError,jwt

# def authenticate(token: str = Depends(oauth2_scheme))