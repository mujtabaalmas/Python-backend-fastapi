from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"] #for specfic website or url to access our api endpoint
# origins = [*] for any website to acess our api endpoint 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message:" "hellooooo"}

# def find_posts(id):
#     for p in my_posts:
#         if p['id'] == id:
#            return p
        
# def find_index_posts(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i





