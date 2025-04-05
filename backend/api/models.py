from pydantic import BaseModel
from typing import Optional, List

class Article(BaseModel):
    title: str
    published_date: str
    source: str 