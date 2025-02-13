from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from typing import List, Dict
import pytz

from .market_data import get_daily_market_summary
from .models import AINews
from .services import db

async def daily_market_update():
    """Daily market update task that runs at 10 AM"""
    try:
        # Get market data summary
        market_summary = await get_daily_market_summary()
        
        # Create main market summary news
        market_news = AINews(
            title=f"AI市场每日总结 - {datetime.now().strftime('%Y-%m-%d')}",
            content=market_summary["analysis"],
            source="Market Analysis",
            published_date=datetime.now()
        )
        
        # Create individual stock summaries
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
        
        # Store all news items
        all_news = [market_news] + stock_details
        for news in all_news:
            db.add_news(news)
            
        print(f"Daily market update completed at {datetime.now()}")
    except Exception as e:
        print(f"Error in daily market update: {str(e)}")

def init_scheduler():
    """Initialize the scheduler with daily market update task"""
    scheduler = AsyncIOScheduler()
    
    # Schedule the task to run at 10 AM local time
    scheduler.add_job(
        daily_market_update,
        CronTrigger(
            year='*',        # Any year
            month='*',       # Any month
            day='*',         # Any day
            hour='10',       # At 10
            minute='0',      # At 0 minutes
            second='0'       # At 0 seconds
        ),
        id='daily_market_update',
        replace_existing=True
    )
    
    return scheduler
