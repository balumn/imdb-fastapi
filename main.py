from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Header, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional
import json

from config import Settings, AuthSettings, admin_user
from auth import get_current_active_user, authenticate_user, create_access_token, Token, User
import dboperations, models, schemas
from database import SessionLocal, engine


app = FastAPI()
settings = Settings()
auth = AuthSettings()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(admin_user, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/")
def upload_movies_in_bulk(upload_file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    
    json_data = json.load(upload_file.file)
    data = []
    for movie in json_data:
        data.append(
            dict(
                name      = movie['name'],
                imdb_score= movie['imdb_score'],
                director  = movie['director'],
                popularity= movie['99popularity'],
                genre     = (",").join(movie['genre'])
                )
            )
    return dboperations.bulkCreateMovies(db=db,data=data)

@app.post("/movie/")
def add_movie(movie: schemas.ImdbBaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return dboperations.createMovie(db=db, movie=movie)