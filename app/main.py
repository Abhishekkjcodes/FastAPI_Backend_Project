from fastapi import FastAPI
from .database import engine
from . import models
from .routers import post,user,auth,like
from fastapi.middleware.cors import CORSMiddleware


#models.Base.metadata.create_all(bind=engine) we will not need this when we use alembic as this was used to create tables when the sql alchemy started up but now alembic handles that
#app can be named anything you like but follow conventions
app = FastAPI()
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
    
app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)
app.include_router(router=like.router)

#1.this is know as a path function or a route in some frameworks
#2.async is for async process and rest is a normal function, root is the name of our 
# function ,could be anything accordign to the functionality try to make it descriptive 
@app.get("/")
async def root():
    return {"message": "well this is fast api with bind mounts"}
#------------------------------------------------------------------------------------------
