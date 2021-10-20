from os import name
from pydantic import BaseModel, Field, EmailStr


class MenuSchema(BaseModel):
    id: int = Field(default=None)
    name: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "cheez",
            }
        }

class UserSchema(BaseModel):
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "username": "asdf",
                "password": "asdf" #harusnya hash yg disimpen
            }
        }

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "abdulazeez@x.com",
                "password": "weakpassword"
            }
        }