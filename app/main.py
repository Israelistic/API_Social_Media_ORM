import sys
sys.path.insert(0, '/Users/hlerman/Documents/development/python/API_Social_Media_ORM/app')
# import config
import fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
# imports from local files
from . import models, schemas, utils, config
# import from database.py that contains the db connection setting
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# connection to the database.
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user= config.db_user, password= config.db_password, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        # with psycopg.connect("host=localhost dbname=fastapi user=postgres") as conn:
        #     with conn.cursor() as cur:       
        print("Database connection was succesfull!")       
        break
    except Exception as error:
        print("connection to database failed")
        print("Error:", error)
        time.sleep(2)
        

########### POINTERS TO ROUTES ###########
# This include_router will point to the routers/post.py, and look for routing match
app.include_router(post.router)
# This include_router will point to the routers/user.py, and look for routing match
app.include_router(user.router)
# root site
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}



