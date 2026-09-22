from fastapi import APIRouter,Depends,HTTPException,status,Request
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.jwt_helper import verify_token
from app.models.user import User


security_scheme = HTTPBearer()

def get_current_user(request:Request,db:Session=Depends(get_db),credentials:HTTPAuthorizationCredentials=Depends(security_scheme)):

    try:
        token=credentials.credentials
        payload=verify_token(token)
        user_id=payload.get("user_id")
        email=payload.get("email")
        if user_id is None:
            raise HTTPException(
                detail="Invalid authentication credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        user=db.query(User).filter(User.id==user_id).first()
        if user is None:
            raise HTTPException(
                detail="Invalid authentication credentials",
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        request.state.user=user
        return user

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )



