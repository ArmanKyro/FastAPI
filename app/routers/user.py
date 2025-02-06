from fastapi import APIRouter
from fastapi import FastAPI, Depends, status, HTTPException
from app import database, schemas, models, oauth2
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()
get_db = database.get_db

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Creating user
@router.post('/user', response_model=schemas.User, tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # Adding HashedPassword
    h_Pass = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email, password=h_Pass)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get User data
@router.get('/user/{id}', response_model=schemas.ShowUser, tags=['User'])
def show(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    user.blog = db.query(models.Blog).filter(models.Blog.user_id == id).all()
    return user