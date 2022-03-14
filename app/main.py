from . import models
from .routers import post, user, auth, vote
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from .database import engine, get_db
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# usingg alembic we don't need sqlalchemy to create tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# specify which domains will be able to access our API
origins = ["*"]

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

# path operation
@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"message": "Hello World!!"} # fastapi automatically converts it to json before sending to user
