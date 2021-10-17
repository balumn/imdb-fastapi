from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import models, schemas
from database import engine
from auth import UserInDB, get_password_hash

def createMovie(db: Session, movie: schemas.ImdbBaseCreate):
    data = movie.dict()
    db_item = models.Imdb(**data)
    db.add(db_item)
    try:
        db.commit()
    except IntegrityError:
        return {"status": False, "message": "Movie already exists"}
    db.refresh(db_item)
    return getMovieDetails(db, db_item.name)

def getMovieDetails(db: Session, movie_name: str):
    return db.query(models.Imdb).filter(models.Imdb.name == movie_name).first()

def bulkCreateMovies(db: Session, data):
    try:
        # will raise error if any of data already exists in db
        db.bulk_insert_mappings(models.Imdb, data)
        db.commit()
    except IntegrityError as e:
        # will try one by one. takes time but works.
        # run as a seperate thread if performace is more important
        for item in data:
            db_item = models.Imdb(**item)
            db.add(db_item)
            try:
                db.commit()
            except:
                db.rollback()
    return {"status": "upload complete"}

def updateMovie(db: Session, pk, data: schemas.ImdbBaseUpdate):
    result = db.query(models.Imdb).filter(models.Imdb.id ==pk).update(data)
    if result == 1:
        db.commit()
        return {'status':True,'status_message':"Movie Updated successfully"}
    elif result == 0:
        return {'status':False,'status_message':"Movie not found"}
    return {'status':False,'status_message':"Something went wrong"}

def deleteMovie(db: Session, pk):
    result = db.query(models.Imdb).filter(models.Imdb.id ==pk).delete()
    if result == 1:
        db.commit()
        return {'status':True,'status_message':"Movie deleted successfully"}
    elif result == 0:
        return {'status':False,'status_message':"Movie not found"}
    return {'status':False,'status_message':"Something went wrong"}

def getUserDetails(db: Session, username: models.User.username):
    return db.query(models.User).filter(models.User.username == username).first()

def createUser(db: Session, user, user_type=models.UserType.user):
    data = user.dict()
    data['user_type'] = user_type
    data['hashed_password'] = get_password_hash(data.pop('password'))
    db_item = models.User(**data)
    db.add(db_item)
    try:
        db.commit()
    except IntegrityError:
        return {"status": False, "message": "User already exists"}
    db.refresh(db_item)
    return getUserDetails(db, db_item.username)