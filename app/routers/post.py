from .. import schemas,models,Oauth2
from fastapi import FastAPI, HTTPException, Response,status,Depends,APIRouter
from sqlalchemy import case, desc, func, select
from sqlalchemy.orm import Session
from ..database import get_db
router=APIRouter(prefix="/posts",tags=["Posts"])



@router.get("/",response_model=list[schemas.PostStatsResponse])
def get_posts(db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user),limit:int=10,skip:int |None=None,search:str=""):
    # with conn.cursor() as cur:
        # cur.execute("SELECT * FROM posts;")
        # data=cur.fetchall()
        # conn.commit()
    posts=db.execute(select(models.Post,func.count(case((models.Like.direction==1,1))).label("likes"),func.count(case((models.Like.direction==-1,1))).label("dislikes")).join(models.Like,models.Post.id==models.Like.post_id,isouter=True).group_by(models.Post.id).where(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip)).all()
    return [row._mapping for row in posts]


#3 WAYS TO GET
# # 1. Run the query
# result = db.execute(select(models.Post).where(models.Post.id == id))
# # 2. Extract the actual Python object out of the database wrapper rows
# post = result.scalars().first()

#OR
# # This does db.execute() AND extracts the scalars all in one single step!
# post = db.scalars(select(models.Post).where(models.Post.id == id)).first()

#OR this only works when getting a single element using primary key
#post=db.get(models.Post,id)

# post is just any random variable Post is the class name used as type hints here define the fields
#since according to conventions we must return status code 201 if we have successfully created smtg we change the status code
@router.post("/",response_model=schemas.PostResponse,status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost,db:Session=Depends(get_db),user_id :int=Depends(Oauth2.get_current_user)):
    #with conn.cursor() as cur:
        # #we dont use f strings to execute this query as its vulnarebale to sql injection attack as if you use f string the person
        # #  may enter a sql command and that will break your system rather u use placeholders that convert anythign into a string
        # cur.execute("INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *;",(post.title,post.content,post.published))
        # data= cur.fetchone()

    new_post1=models.Post(
        title=post.title,
        content=post.content,
        published=post.published
        )# you could do it this way but the problem is what if there are 50 fields and we dont want type so much we unpack the dict 
    
    new_post=models.Post(user_id=user_id,**post.model_dump()) #standard method
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    #print(new_post.user_info)
    return new_post


@router.get("/latest",response_model=schemas.PostResponse)
def get_latest(db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user)):
    #if this function were to be placed below @app.get("/posts/{id}") we would get an error why?
    #  cuz it will think latest is a path parameter and will try to validate it
    # with conn.cursor() as cur:
    #     cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;")
    #     post=cur.fetchone()
    post=db.scalars(select(models.Post).order_by(desc(models.Post.created_at))).first()
        #OR you can use .limit(1)
    return post

@router.get("/my_posts",response_model=list[schemas.PostResponse])
def my_posts(db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user)):
    posts=db.scalars(select(models.Post).where(models.Post.user_id==user_id)).all()
    if(not posts):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No posts available")
    return posts

@router.get("/{id}",response_model=schemas.PostStatsResponse)
def get_post(id:int,db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user)):
    #fastAPI will extract the id from the url and give it to our function
    # with conn.cursor() as cur:
    #     cur.execute(f"SELECT * FROM posts WHERE id=({id})") # we can use f strign here as id is type hinted as a int so no sql queries
    #     post=cur.fetchone()
    post=db.execute(select(models.Post,func.count(case((models.Like.direction==1,1))).label("likes"),func.count(case((models.Like.direction==-1,1))).label("dislikes")).join(models.Like,models.Post.id==models.Like.post_id,isouter=True).where(models.Post.id==id).group_by(models.Post.id)).first() # will not give a list unlike .all() so change the response model accordingly
    #OR 
    post_alt=db.get(models.Post,id) # this is made for finding using primary key a shortcut this will no return a list so make sure to change the response model
    if not post:# .all() will give out an empty list,.first() will give out None
        # Response.status_code=status.HTTP_404_NOT_FOUND
        # return {"message":f"post with {id} not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} not found")
        
    return post._mapping

# @app.get("/recent/latest")
# def get_latest():
#     #this is another way in which you could get the recent posts by changing the url so that no collision happens



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_posts(id:int,db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user)):
    # with conn.cursor() as cur:
    #     cur.execute("DELETE FROM posts WHERE id = %s RETURNING * ;",(str(id),))
    #     deleted_post=cur.fetchone()
    # conn.commit()
    deleted_post=db.get(models.Post,id)
    if(deleted_post==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    if(deleted_post.user_id!=user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    # return {"message":f"Post {id} deleted"} you will not recieve this msg cuz accordign to fastapi if ur deleting smtg 
    # there shouldnt be any data coming back so 204 status code doest send anything
    db.delete(deleted_post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # not necessary to put but a good practice

@router.put("/{id}",response_model=schemas.PostResponse)
def put_post(id:int,post:schemas.CreatePost,db:Session=Depends(get_db),user_id:int=Depends(Oauth2.get_current_user)):
    # with conn.cursor() as cur:
    #     cur.execute("SELECT * FROM posts WHERE id=%s;",(str(id),))
    #     old_post=cur.fetchone()
    #     if(old_post==None):
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    #     cur.execute("UPDATE posts SET title=%s , content=%s , published=%s WHERE id=%s RETURNING * ;",(post.title,post.content,post.published,str(id)))
    #     new_post=cur.fetchone()
    #     conn.commit()
    post_update=db.get(models.Post,id)
    if(post_update==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    if(post_update.user_id!=user_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform the requested action")
    for k,v in post.model_dump().items():
        setattr(post_update,k,v)
    post_update.user_id=user_id
    db.commit()
    db.refresh(post_update)

    #ALTERNATE WAY TO UPDATE
    # stmt = update(models.Post).where(models.Post.id == 1).values(**payload)
    # db.execute(stmt)
    # db.expire_all()
    return post_update