from typing import List
from fastapi import APIRouter
from app import schemas, database, models, oauth2
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import joinedload

router = APIRouter()

get_db = database.get_db

@router.get('/blog', response_model=List [schemas.ShowBlog], tags=[ 'blogs' ])
def all(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/blog', tags=['Blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id = 1)
    # Now, here adding an oject to database is taken care by ORM
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# GETTING DATA TO THE DATABASE
@router.get('/blog', response_model=List[schemas.ShowBlog], tags=['Blogs'])
def all(db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    # blogs = db.query(models.Blog).all()
    blogs = db.query(models.Blog).options(joinedload(models.Blog.creator).joinedload(models.User.blogs)).all()
    return blogs

@router.get('/blog/{id}', response_model=schemas.ShowBlog, tags=['Blogs'])
def show(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    # blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    blog = db.query(models.Blog).options(joinedload(models.Blog.creator).joinedload(models.User.blogs)).filter(models.Blog.id == id).first()
    return blog


# DELETING DATA TO THE DATABASE
@router.delete('/blog/{id}', tags=['Blogs'])
def destroy(id, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")

    blog.delete(synchronize_session = False)
    db.commit()
    return {"status" : "Deleted Successfully."}


# UPDATING DATA ONTO THE DATABASE
@router.put('/blog/{id}', tags=['Blogs'])
def update(id, request : schemas.Blog, db: Session = Depends(get_db), get_current_user: schemas.User = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    # blog.update(blog)
    blog.update(request.dict())
    db.commit()
    return {"status" : "Updated Successfully."}