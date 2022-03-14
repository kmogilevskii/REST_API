from .. import models
from typing import List, Optional
from ..database import get_db
from sqlalchemy.orm import Session
from ..schemas import CreatePost, Post, PostOut
from ..oath2 import get_current_user
from fastapi import Depends, status, Response, HTTPException, APIRouter
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(get_current_user), 
                                            limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
 
    return posts 


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post) # why int?
def create_posts(post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostOut) 
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)): # casting to int - user can't fill in incorrect value
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
            models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} wasn't found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found.")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your post.")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=Post)
def update_post(id: int, post: CreatePost, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_for_update = post_query.first()
    if not post_for_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if post_for_update.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="It's not your post.")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()