from pydantic import BaseModel, EmailStr
from datetime import datetime


#PostBase define what the user have to provide to the API request to create a post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # Optional for user to specify in the post request and it will default to true if not specified


class PostCreate(PostBase):
    pass


# Create a class for validation == schema validation - define what the response for post should look like
class Post(PostBase):
    id: str
    created_at: datetime
    class Config:
        orm_mode = True

# UserCreate schema will config what the user have to provide to create a post
class UserCreate(BaseModel):
    email: str
    password: str

# UserOut control what the user sees in the response to the API request
class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime
    class Config:
        orm_mode = True
    
