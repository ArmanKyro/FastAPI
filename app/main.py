import sys
import os


from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


@app.get("/")
async def home():
    return {"message": "FastAPI app running on Vercel!"}



