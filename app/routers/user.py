

########### PATH OPERATION FOR USERS/ ROUTE ###########
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

from .. import models, schemas, utils

router = APIRouter(
    prefix = '/users', # for routes with id it will do /users/{id}
    tags = ['Users']
)

# USER CREATE
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict()) #  **user.dict()unpacking dictionary
    db.add(new_user)
    db.commit() # commit the changes to the database
    db.refresh(new_user)
    
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int,  db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User  with id {id} does not exist")

    return user