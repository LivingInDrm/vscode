import pytest
from datetime import datetime, timedelta
import pytz
from apscheduler.triggers.cron import CronTrigger
from app.scheduler import init_scheduler, daily_market_update

@pytest.mark.asyncio
async def test_scheduler_initialization():
    """Test scheduler initialization and job configuration"""
    scheduler = init_scheduler()
    
    # Verify scheduler is configured but not running
    assert not scheduler.running
    
    # Get the job
    job = scheduler.get_job('daily_market_update')
    assert job is not None
    
    # Verify job timing (10 AM)
    trigger = job.trigger
    assert isinstance(trigger, CronTrigger)
    
    # Find hour and minute fields
    hour_field = next(f for f in trigger.fields if f.name == 'hour')
    minute_field = next(f for f in trigger.fields if f.name == 'minute')
    
    # Verify 10 AM timing
    assert str(hour_field.expressions[0]) == '10'
    assert str(minute_field.expressions[0]) == '0'

@pytest.mark.asyncio
async def test_daily_market_update():
    """Test the daily market update function"""
    # Run the update function
    await daily_market_update()
    
    # Note: The actual verification of data is done in test_market_data.py
    # This test ensures the function runs without errors
    
    # In a real environment, we would:
    # 1. Mock the database
    # 2. Verify news items are created
    # 3. Check notification delivery
    # But since this is a demo, we just verify it doesn't raise exceptions
