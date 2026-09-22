from datetime import datetime

from pydantic import BaseModel, Field

class UserRequestDto(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Username of the user"
    )
    email: str = Field(
        ...,
        description="Email of the user"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password of the user"
    )

class UserResponseDto(BaseModel):
    id: int = Field(
        ...,
        description="User ID"
    )
    username: str = Field(
        ...,
        description="Username of the user"
    )
    email: str = Field(
        ...,
        description="Email of the user"
    )
    is_active: bool = True
    created_at: datetime
    model_config = {
        "from_attributes": True
    }

class UserUpdateDto(BaseModel):
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Username of the user"
    )
    email: str = Field(
        ...,
        description="Email of the user"
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password of the user"
    )


    # authentication response

class LoginRequestDto(BaseModel):
        email: str = Field(
            ...,
            description="Email of the user"
        )
        password: str = Field(
            ...,
            min_length=8,
            description="Password of the user"
        )

class LoginResponseDto(BaseModel):
    access_token: str
    token_type: str
    user: UserResponseDto