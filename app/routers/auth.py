from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from app.schemas.user import LoginRequestDto,LoginResponseDto,UserResponseDto
from app.schemas.api_response import ApiResponse
from app.core.security import get_password_hash,verify_password
from app.core.jwt_helper import create_access_token


auth_router=APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@auth_router.post("/",response_model=LoginResponseDto)
def login_user(login_request:LoginRequestDto,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==login_request.email).first()
    if not user or not verify_password(user.password , login_request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials"
                            )

    access_token =create_access_token(data={
        "user_id":user.id,
        "email":user.email
    })

    return LoginResponseDto(
        access_token=access_token,
        token_type="bearer",
        user=UserResponseDto.model_validate(user)
    )