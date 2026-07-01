
from datetime import timedelta

from fastapi import APIRouter,HTTPException,Response,status,Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas,models,utils,Oauth2


router=APIRouter( tags=["login"])

@router.post("/login",response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    #def login(use_credentials:schemas.UserLogin,db:Session=Depends(get_db)): 
    # this is using the pydantic schema instead of Oauth style maintians consistency in code and 
    # front end naturally sends data in json but we wont get the swagger ui functionality of authorize
    # so we will use the Oauthstyle here, Oauth syles has strict username and password format so change that 
    # even if its an email thats username but pydantic models will provide us flexibility there
    user=db.scalars(select(models.User).where(models.User.email==user_credentials.username)).first()
    if(not user):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    #user_password=utils.hash(use_credentials.password) this is the hashed user attempted pasword but the verify method does this for us
    allowed=utils.verify(user_credentials.password,user.password)
    if(not allowed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid credentials")
    
    access_token_expires = timedelta(minutes=Oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=Oauth2.create_access_token(data={"user_id":user.id},expires_delta=access_token_expires)
    return {"access_token":access_token,"token_type":"bearer"}