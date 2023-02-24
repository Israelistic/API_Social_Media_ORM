from pydantic import BaseModel
# Create a class for validation == schema validation - dfine what a post should look like



class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # Optional for user to specify in the post request and it will default to true if not speccified


class PostCreate(PostBase):
    pass

