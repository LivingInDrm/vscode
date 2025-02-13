import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.scheduler import daily_programming_news

async def test_email_notification():
    """Test sending email notification with programming news"""
    await daily_programming_news()

if __name__ == "__main__":
    asyncio.run(test_email_notification())
