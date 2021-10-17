from sqlalchemy import Column, Numeric, Integer, String, Boolean
from database import Base


class Imdb(Base):
    __tablename__ = "imdb"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), index=True, unique=True)
    imdb_score = Column(Numeric(1,1), index=True)
    director = Column(String(100), index=True)
    genre = Column(String(1000), index=True)
    popularity = Column(Integer, index=True)

class UserType:
    admin = "admin"
    user  = "user"
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), index=True, unique=True)
    full_name = Column(String(100), index=True)
    email = Column(String(100), index=True)
    hashed_password = Column(String(1000))
    user_type = Column(String(10), default=UserType.user)
    disabled = Column(Boolean,default=False)
