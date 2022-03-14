from .. import models
from ..utils import hash
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import UserCreate, UserReturn
from fastapi import Depends, status, HTTPException, APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


# generate a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserReturn)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=UserReturn)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found.")
    return user