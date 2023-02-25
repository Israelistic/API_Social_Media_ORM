from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. database import get_db

from .. import models, schemas

router = APIRouter(
    prefix = '/posts', # for routes with id it will do /posts/{id}
    tags=['Posts']
)


########### PATH OPERATION FOR POSTS/ ROUTE ###########
# GET ALL the posts from the database
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    '''
    Traditinal sql:
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    '''
    posts = db.query(models.Post).all()
    return posts

# CREATE a post. # and commit the changes to the database.
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
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
# @router.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return post

#GET POST BY ID --the id in the route is path parameter
@router.get("/{id}", response_model=schemas.Post)
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
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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
@router.put("/{id}", response_model=schemas.Post)
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
