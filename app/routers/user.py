from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils 

router = APIRouter(
     prefix="/users",
     tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
     #hash the password - user.password 
     hashed_password = utils.hash(user.password)
     user.password = hashed_password

     existing_user = db.query(models.User).filter(models.User.email == user.email).first()
     if existing_user:
         raise HTTPException(status_code=400, detail="User with this email already exists")
     
     new_user= models.User(**user.dict())
     db.add(new_user)
     db.commit()
     db.refresh(new_user)
     return new_user

@router.get("/{id}", status_code=status.HTTP_302_FOUND, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
     fetched_user = db.query(models.User).filter(models.User.id == id).first()

     if not fetched_user:  
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=(f"user with id: {id} NOT FOUND !!!"))
     return fetched_user