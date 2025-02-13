from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Schedule(BaseModel):
    id: Optional[str] = None
    title: str
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None

class AINews(BaseModel):
    id: Optional[str] = None
    title: str
    content: str
    source: str
    published_date: datetime

class ScheduleResponse(BaseModel):
    message: str
    schedule: Optional[Schedule] = None

class NewsResponse(BaseModel):
    message: str
    news: List[AINews] = []
