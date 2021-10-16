from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import models, schemas

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
