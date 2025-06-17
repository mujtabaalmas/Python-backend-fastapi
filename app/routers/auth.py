from fastapi import FastAPI , Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

 
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    User = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not User:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=(f"INVALID CREDENTIALS !!!"))
    
    if not utils.verify(user_credentials.password, User.password):
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=(f"INVALID CREDENTIALS !!!"))
    
    access_token = oauth2.create_access_token(data = {"user_id": User.id})
    return {"access_token": access_token, "token_type": "bearer"}












