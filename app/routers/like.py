from fastapi import FastAPI, HTTPException, Response,status,Depends,APIRouter,Response
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..database import get_db
from .. import Oauth2,models, schemas
router=APIRouter(prefix="/likes",tags=["Likes"])

@router.post("/")
def create_like(like:schemas.CreateLike,db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user)):
    post=db.scalars(select(models.Post).where(models.Post.id==like.post_id)).first()
    if(not post):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    like_info=db.scalars(select(models.Like).where(models.Like.post_id==like.post_id, models.Like.user_id==user_id)).first()
    reaction = "liked" if like.direction == 1 else "disliked"
    if(not like_info):
        new_like=models.Like(user_id=user_id,**like.model_dump())
        db.add(new_like)
        db.commit()
        return {
            "message": f"You {reaction} the post"
        }
        
    elif(like_info.direction==like.direction):
        db.delete(like_info)
        db.commit()
        return {
            "message": f"Your reaction was removed from the post"
        }
    else:
        like_info.direction=like.direction
        db.commit()
        db.refresh(like_info)
        return {
            "message": f"You {reaction} the post"
        }
    
