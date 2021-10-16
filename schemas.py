from typing import List, Optional
from pydantic import BaseModel
import datetime


class ImdbBase(BaseModel):
    name : str = "Iron Man (2008)"
    imdb_score : float = 8.6
    director : str = 'Robert Browny Jr.'
    genre    : str = "action,comedy,thriller,sci-fi"
    popularity : int = 84

class ImdbBaseCreate(ImdbBase):
    pass

class Imdb(ImdbBase):
    class Config:
        orm_mode = True