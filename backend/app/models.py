from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AINews(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    source: str
    published_date: datetime

class NewsResponse(BaseModel):
    message: str
    news: Optional[AINews] = None
