from sqlalchemy import Boolean, Column, Numeric, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from database import Base


class Imdb(Base):
    __tablename__ = "imdb"

    name = Column(String(100), index=True, primary_key=True)
    imdb_score = Column(Numeric(1,1), index=True)
    director = Column(String(100), index=True)
    genre = Column(String(1000), index=True)
    popularity = Column(Integer, index=True)
