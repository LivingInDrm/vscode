from typing import List, Dict
from .models import AINews

class MemoryDatabase:
    def __init__(self):
        self.news: List[AINews] = []

    def add_news(self, news: AINews) -> AINews:
        self.news.append(news)
        return news

    def get_news(self) -> List[AINews]:
        return self.news

db = MemoryDatabase()
