from sqlalchemy import Column, Numeric, Integer, String
from database import Base


class Imdb(Base):
    __tablename__ = "imdb"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True, unique=True)
    imdb_score = Column(Numeric(1,1), index=True)
    director = Column(String(100), index=True)
    genre = Column(String(1000), index=True)
    popularity = Column(Integer, index=True)
