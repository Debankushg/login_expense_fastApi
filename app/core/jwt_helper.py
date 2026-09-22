# function that help use to perform jwt operations like encoding and decoding
from datetime import datetime, timedelta,timezone
from typing import Union
from fastapi import HTTPException, status
from jose import JWTError, jwt


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


# create access token

def create_access_token(data:dict,expires_delta:Union[timedelta,None]=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(tz=timezone.utc)+expires_delta
    else:
        expire=datetime.now(tz=timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload
        return username
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )

# create refresh token

def create_refresh_token(data:dict,expires_delta:Union[timedelta,None]=None):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(tz=timezone.utc)+expires_delta
    else:
        expire=datetime.now(tz=timezone.utc)+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp":expire,"type":"refresh"})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def verify_refresh_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get("type")!="refresh":
            raise JWTError("Not a refresh token")
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate":"Bearer"},
        )



if __name__=="__main__":
    token=create_access_token({"name":"mohamed"})
    print(token)

    payload =verify_token(token)
    print("token verified succesfully")
    print(payload)