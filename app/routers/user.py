from .. import utils,schemas,models
from fastapi import FastAPI, HTTPException, Response,status,Depends,APIRouter
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db

#this router is responsible for our endpoints and prefix basically helps us avoid writing the prefix each time
router=APIRouter( prefix="/users",tags=["users"])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse) #"/users" without router prefix
def create_user(user:schemas.CreateUser,db:Session=Depends(get_db)):
    hashed_password = utils.hash(user.password) #get hashed password
    user.password = hashed_password # set the hased password as password in the pydantic schema

    new_user=models.User(**(user.model_dump()))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.scalars(select(models.User).where(models.User.id==id)).first()
    if(not user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User does not exist")
    return user
