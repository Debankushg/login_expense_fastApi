from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.user import User
from app.schemas.user import UserRequestDto,UserResponseDto,UserUpdateDto
from app.schemas.api_response import ApiResponse
from app.core.security import get_password_hash

user_router=APIRouter(
    prefix="/user",
    tags=["user"]
)

# create user
@user_router.post("/" ,response_model=ApiResponse , status_code=status.HTTP_201_CREATED)
async def create_user(user_request:UserRequestDto,db:Session=Depends(get_db)):

    # check if email already exists
    user=db.query(User).filter(User.email==user_request.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
            )

    # check if username already exists
    user=db.query(User).filter(User.username==user_request.username).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
            )

    hashed_pwd = get_password_hash(user_request.password)

    new_user=User(
        username=user_request.username,
        email=user_request.email,
        password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return ApiResponse(
        status="success",
        message="User created successfully",
        data={
        "user":UserResponseDto.model_validate(new_user)
    })  

# get All users
@user_router.get("/",response_model=ApiResponse)
async def get_all_users(db:Session=Depends(get_db)):
    users=db.query(User).all()

    return ApiResponse(
        status="success",
        message="Users fetched successfully",
        data={
        "users":[UserResponseDto.model_validate(user) for user in users]
    })  


# get user by id
@user_router.get("/{id}",response_model=ApiResponse)
async def get_user_by_id(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )


    return ApiResponse(status="success",
                       message="User fetched successfully",
                       data={
        "user":UserResponseDto.model_validate(user)
    })


# update user
@user_router.put("/{id}",response_model=ApiResponse)
async def update_user_by_id(
    id:int,
    user_update:UserUpdateDto,
    db:Session=Depends(get_db)):


    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )


    # check unique constraints if field are updated
    if user_update.username and user.username != user_update.username:
        conflict_user=db.query(User).filter(User.username==user_update.username).first()
        if conflict_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
                )

    if user_update.email and user.email != user_update.email:
        conflict_email=db.query(User).filter(User.email==user_update.email).first()
        if conflict_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
                )

    if user_update.password:
        user.password=get_password_hash(user_update.password)


    user.username=user_update.username
    user.email=user_update.email
    user.password=user_update.password

    db.commit()
    db.refresh(user)

    return ApiResponse(status="success",
                       message="User updated successfully",
                       data={
        "user":UserResponseDto.model_validate(user)
    })

# delete User
@user_router.delete("/{id}",response_model=ApiResponse)
async def delete_user_by_id(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found"
                            )

    db.delete(user)
    db.commit()

    return ApiResponse(status="success",
                       message="User deleted successfully",
                       data={
        "user":UserResponseDto.model_validate(user)
    })