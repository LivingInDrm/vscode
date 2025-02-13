from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from typing import List, Dict

from .market_data import get_daily_market_summary
from .email_service import send_ai_programming_news

async def daily_market_update():
    """Daily market update task that runs at 10 AM"""
    try:
        market_summary = await get_daily_market_summary()
        print(f"Market update completed at {datetime.now()}")
    except Exception as e:
        print(f"Error in daily market update: {str(e)}")

async def daily_programming_news():
    """Daily AI programming news update task that runs at 20:30"""
    try:
        # TODO: Implement AI programming news collection in next step
        news_summary = "AI编程动态将在下一步实现"
        
        # Send email notification
        subject = f"AI编程动态 - {datetime.now().strftime('%Y-%m-%d')}"
        await send_ai_programming_news(subject, news_summary)
        
        print(f"Programming news update completed at {datetime.now()}")
    except Exception as e:
        print(f"Error in programming news update: {str(e)}")

def init_scheduler():
    """Initialize the scheduler with all daily tasks"""
    scheduler = AsyncIOScheduler()
    
    # Schedule market update for 10 AM
    scheduler.add_job(
        daily_market_update,
        CronTrigger(
            hour='10',
            minute='0',
            second='0'
        ),
        id='daily_market_update',
        replace_existing=True
    )
    
    # Schedule programming news for 20:30
    scheduler.add_job(
        daily_programming_news,
        CronTrigger(
            hour='20',
            minute='30',
            second='0'
        ),
        id='daily_programming_news',
        replace_existing=True
    )
    
    return scheduler
