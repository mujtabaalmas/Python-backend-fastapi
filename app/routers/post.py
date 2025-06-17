from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from typing import List
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
     prefix="/posts",
     tags=['Posts']
)

@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), Limit: int = 10, skip: int = 0, search: Optional[str]= "" ):

    # if we want to display one specific owner(user) posts then  ------
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() 

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                     models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    return posts
    # cursor.execute(""" Select * from post""")
    # posts = cursor.fetchall()
    # return {"data": posts}

@router.post("/" , status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):
     
    # , get_current_user: int = Depends(oauth2.get_current_user
    # cursor.execute("""INSERT INTO post (title, description, published) VALUES (%s,%s,%s) RETURNING * """, 
    # (post.title,post.description,post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    # -----------------------------------------------
    #  new_post= models.Post(title=post.title, 
    #                        description=post.description, published=post.published)

    try:
        new_post= models.Post(owner_id = current_user.id, **post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        print(current_user.email, "created a new post")

        return new_post
    except:
         raise HTTPException(status_code=status.HTTP_307_TEMPORARY_REDIRECT,
                             detail=(f"Unable to create a post !!!"))

@router.get("/{id}", response_model= schemas.PostOut)
def get_post(id: str, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * from post where id = %s """, (str(id),))
    # fetched_post = cursor.fetchone()

    fetched_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
                models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
                                models.Post.id == id).first()
    # post without vote --------------------------------------------------------
    # fetched_post = db.query(models.Post).filter(models.Post.id == id).first() 
    print(fetched_post)

    if not fetched_post:  
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=(f"post with id: {id} NOT FOUND !!!"))
    
    #if we want to get specific owner posts only thenn-----
    # if fetched_post.owner_id != current_user.id:
    #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail=f"Not Authorized to perform requested Action ")
    
    return fetched_post

        # ANOTHER METHOD FOR 404 ERROR MAKE VAR response IN get_post (id: int , response: response)
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} NOT FOUND !!!"}  

# my_posts = [{'title': 'florida beaches', 'description': 'these are good beaches',"id": 1},
#             {'title': 'florida pizza', 'description': 'very good pizaaaaaaaaaaa',"id": 2}]

@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):
    # index = find_index_posts(id)
    # cursor.execute("""DELETE from post where id = %s returning *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    
    if deleted_post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized to perform requested Action ")
    
    deleted_post_query.delete(synchronize_session=False)
    db.commit()

    # my_posts.pop(index)
    #return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int =
                  Depends(oauth2.get_current_user)):
    #    index = find_index_posts(id)
    #--------------------------------------
    # cursor.execute("""UPDATE post set title = %s,description = %s, published = %s
    #                where id = %s returning *""",(post.title,post.description,post.published, (str(id),)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} not found")
    
    if updated_post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Not Authorized to perform requested Action ")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    #    post_dict = post.dict()
    #    post_dict['id'] = id 
    #    my_posts[index] = post_dict
    return  post_query.first()