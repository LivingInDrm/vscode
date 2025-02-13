from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
import os
from datetime import datetime

from .models import Schedule, AINews, ScheduleResponse, NewsResponse
from .services import db
from .market_data import get_daily_market_summary
from .scheduler import init_scheduler
from .config import get_settings

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize and start the scheduler on app startup"""
    scheduler = init_scheduler()
    scheduler.start()

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/news/", response_model=List[AINews])
async def get_news():
    try:
        # Get real market data summary
        market_summary = await get_daily_market_summary()
        
        # Create news items from market data
        market_news = AINews(
            title=f"AI市场每日总结 - {datetime.now().strftime('%Y-%m-%d')}",
            content=market_summary["analysis"],
            source="Market Analysis",
            published_date=datetime.now()
        )
        
        # Add detailed stock data as additional news items
        stock_details = []
        for company, data in market_summary["stock_data"].items():
            change_direction = "上涨" if data["change"] > 0 else "下跌"
            content = (
                f"{company}股票分析：\n"
                f"- 当前价格：{data['price']:.2f} {data['currency']}\n"
                f"- 价格变动：{change_direction} {abs(data['change']):.2f}%\n"
                f"- 交易量：{data['volume']:,}\n"
                f"- 市值：{data['market_cap']/1e9:.1f}B {data['currency']}"
            )
            stock_details.append(AINews(
                title=f"{company}市场表现",
                content=content,
                source="Stock Analysis",
                published_date=datetime.now()
            ))
        
        # Combine all news
        all_news = [market_news] + stock_details
        
        # Store in database
        for news in all_news:
            db.add_news(news)
        
        return all_news
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching market data: {str(e)}"
        )
