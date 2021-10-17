from fastapi import FastAPI, HTTPException, Depends, Request, File, UploadFile, Header, status
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from datetime import datetime, timedelta
from functools import lru_cache
from typing import Optional
import json

from config import Settings, AuthSettings
from auth import get_current_active_user, authenticate_user, create_access_token, Token, User, UserCreate, AdminCreate, admin_user
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
    user = authenticate_user(form_data.username, form_data.password)
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

@app.get("/ping")
async def root():
    return {"message": "Hello World"}

@app.post("/upload/")
def upload_movies_in_bulk(upload_file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(admin_user)):
    
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
def add_movie(movie: schemas.ImdbBaseCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_user)):
    return dboperations.createMovie(db=db, movie=movie)

@app.patch("/movie/{id}", response_model=schemas.Response)
async def update_item(id: str, movie: schemas.Imdb, db: Session = Depends(get_db), current_user: User = Depends(admin_user)):
    update_data = movie.dict(exclude_unset=True)
    return dboperations.updateMovie(db=db, pk=id, data=update_data)

@app.delete("/movie/{id}", response_model=schemas.Response)
async def delete_movie(id: str, db: Session = Depends(get_db), current_user: User = Depends(admin_user)):
    return dboperations.deleteMovie(db=db, pk=id)

@app.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    result = dboperations.createUser(db=db,user=user)
    if type(result) == dict:
        return result
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/admin/")
def create_admin(user: AdminCreate, db: Session = Depends(get_db)):
    """
    You need to have a SUPERUSER Password to create the admin users
    """
    if user.superuser_password != settings.SUPER_USER_PASSWORD:
        return {"status": False, "message": "Super User password is wrong"}
    del user.superuser_password
    result = dboperations.createUser(db=db,user=user,user_type=models.UserType.admin)
    if type(result) == dict:
        return result
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/")
async def search_movies(search: str = "", db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """
    Search for Movie name, Movie genre and director name
    only single params is needed for all three fields
    """
    print(search)
    return dboperations.searchMovie(db=db,search=search)