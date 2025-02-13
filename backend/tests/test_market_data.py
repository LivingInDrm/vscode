import pytest
from datetime import datetime
import pytz
from app.market_data import MarketDataCollector, get_daily_market_summary

@pytest.mark.asyncio
async def test_fetch_stock_data():
    """Test real stock data fetching"""
    collector = MarketDataCollector()
    stock_data = await collector.fetch_stock_data()
    
    # Verify we get data for all companies
    assert len(stock_data) == len(collector.ai_companies)
    
    # Check data structure and types
    for company, data in stock_data.items():
        assert isinstance(data["price"], float)
        assert isinstance(data["change"], float)
        assert isinstance(data["volume"], int)
        assert isinstance(data["market_cap"], (int, float))
        assert data["currency"] == "USD"

@pytest.mark.asyncio
async def test_market_summary():
    """Test complete market data summary"""
    summary = await get_daily_market_summary()
    
    # Check all required fields
    assert "stock_data" in summary
    assert "news" in summary
    assert "analysis" in summary
    assert "timestamp" in summary
    
    # Verify analysis content
    assert "AI市场分析" in summary["analysis"]
    assert "市场领导者" in summary["analysis"]
    assert "市场动能" in summary["analysis"]

@pytest.mark.asyncio
async def test_company_news():
    """Test company news fetching"""
    collector = MarketDataCollector()
    news = await collector.fetch_company_news()
    
    # Verify we get news items
    assert isinstance(news, list)
    
    # Check news item structure if any news exists
    if news:
        for item in news:
            assert "title" in item
            assert "content" in item
            assert "source" in item
            assert "published_date" in item
