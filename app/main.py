import sys
sys.path.insert(0, '/Users/hlerman/Documents/development/python/API_Social_Media_ORM/app')
import config
import fastapi
from fastapi import FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

# from psycopg2.extras import RealDictCursor
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
        

########### PATH OPERATION / ROUTE ###########

# root site
@app.get("/")
def root():
    return {"message": "Welcome to my API!!"}

# GET ALL the posts from the database
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    '''
    Traditinal sql:
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    '''
    posts = db.query(models.Post).all()
    return posts

# CREATE a post. # and commit the changes to the database.
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    '''
    Traditinal sql:
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) # the %s prevents sql injection
    new_post = cursor.fetchone() 
    conn.commit() # commit the changes to the database
    '''
    new_post = models.Post(**post.dict()) # unpacking dictionary
    db.add(new_post)
    db.commit() # commit the changes to the database
    db.refresh(new_post)
    return new_post

# The order of the routes matter. If the lastest path was under the post{id}-rotute it will be confuesd by a different route
@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post

#GET POST BY ID --the id in the route is path parameter
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    '''
    cursor.execute("""SELECT * FROM posts WHERE id= %s """, (str(id)))
    post = cursor.fetchone()  
    '''     
    post = db.query(models.Post).filter(models.Post.id == id).first()  
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return post

# DELETE POST BY ID
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone() # saved the deleted post
    # conn.commit() # commit the changes to the database
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit() # commit the changes
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# UPDATE POST BY ID
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title= %s, content= %s, published = %s WHERE id = %s RETURNING*""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit() # commit the changes to the database
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit() # commit the changes to the database
    return post_query.first()
