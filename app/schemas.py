from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# schema or pydantic model (defines the structure of a response/request)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass

# class UpdatePost(PostBase):
#     pass 

class UserReturn(BaseModel):
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# shape the response we send to the user
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserReturn

    # pydantic ORM mode will tell the Pydantic model to read data even if it's not in the dict format
    # but in any object format
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str



class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class VoteCreate(BaseModel):
    post_id: int
    dir: conint(le=1)

