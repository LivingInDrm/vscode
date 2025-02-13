from datetime import datetime
import json
from typing import List, Dict
from .models import Schedule, AINews

class MemoryDatabase:
    def __init__(self):
        self.schedules: Dict[str, Schedule] = {}
        self.news: List[AINews] = []

    def add_schedule(self, schedule: Schedule) -> Schedule:
        schedule.id = str(len(self.schedules) + 1)
        self.schedules[schedule.id] = schedule
        return schedule

    def get_schedules(self) -> List[Schedule]:
        return list(self.schedules.values())

    def add_news(self, news: AINews) -> AINews:
        news.id = str(len(self.news) + 1)
        self.news.append(news)
        return news

    def get_news(self) -> List[AINews]:
        return self.news

db = MemoryDatabase()
