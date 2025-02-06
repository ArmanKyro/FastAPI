from pydantic import BaseModel
from typing import List, Optional

class Blog(BaseModel):
    title: str
    body: str
    class Config():
        from_attributes = True

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUser(BaseModel):
    name: str
    email: str
    blog: List[Blog] = [] 

    class Config:
        from_attributes = True

class ShowUserNoPass(BaseModel):
    name: str
    email: str

    class Config:
        from_attributes = True

class ShowBlog(BaseModel):
    title: str
    body: str
    creator: ShowUserNoPass
    
    class Config:
        from_attributes = True

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


