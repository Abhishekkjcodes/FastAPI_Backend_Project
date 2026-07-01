from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr

class PostsBase(BaseModel):
    title: str
    content: str
    published: bool =True
    #rating : int | None=None

class CreatePost(PostsBase):
    pass

#see we may create multiple schemas one for update ,
# one for response and try to inherit only when it makes sense dont force it

class PostResponse(PostsBase):
    id:int
    published: bool
    created_at: datetime
    user_id:int
    user_info:UserResponse
    #you can select what you wanna sent to the user using pydantic model

    model_config = ConfigDict(from_attributes=True)

class PostStatsResponse(BaseModel):
    Post:PostResponse
    likes:int
    dislikes:int
    model_config = ConfigDict(from_attributes=True)
#-----------------------------------------------------------------------------------------------

class CreateUser(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

#---------------------------------------------------------------------------------------------
class UserLogin(BaseModel):
    email:EmailStr
    password:str

#--------------------------------------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id:int |None=None

#---------------------------------------------------------------------------------------------------
class CreateLike(BaseModel):
    post_id:int
    direction:Literal[-1,1]