import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import asyncio
import json

class MarketDataCollector:
    def __init__(self):
        self.ai_companies = {
            "NVDA": "NVIDIA",
            "MSFT": "Microsoft",
            "GOOGL": "Google",
            "META": "Meta",
            "AMZN": "Amazon",
            "IBM": "IBM",
            "INTC": "Intel",
            "AMD": "AMD"
        }
    
    async def fetch_stock_data(self) -> Dict:
        """Fetch real-time stock data for AI companies"""
        stock_data = {}
        for symbol, name in self.ai_companies.items():
            try:
                # Get historical data for today
                end_date = datetime.now()
                start_date = end_date - timedelta(days=2)  # Get 2 days for comparison
                hist = yf.download(symbol, start=start_date, end=end_date, progress=False)
                
                if not hist.empty:
                    latest = hist.iloc[-1]
                    prev_close = hist.iloc[-2]['Close'] if len(hist) > 1 else latest['Close']
                    price = float(latest['Close'])
                    prev_close = float(prev_close)
                    change = ((price - prev_close) / prev_close) * 100
                    
                    stock = yf.Ticker(symbol)
                    info = stock.info
                    
                    stock_data[name] = {
                        "price": price,
                        "change": change,
                        "volume": int(latest['Volume'].iloc[0]),
                        "market_cap": info.get("marketCap", 0),
                        "currency": info.get("currency", "USD")
                    }
            except Exception as e:
                print(f"Error fetching data for {name}: {e}")
                # Add placeholder data
                stock_data[name] = {
                    "price": 0,
                    "change": 0,
                    "volume": 0,
                    "market_cap": 0,
                    "currency": "USD"
                }
        return stock_data

    async def fetch_company_news(self) -> List[Dict]:
        """Fetch latest news for AI companies"""
        all_news = []
        for symbol, name in self.ai_companies.items():
            try:
                stock = yf.Ticker(symbol)
                news = stock.news
                if news:
                    for item in news[:2]:  # Get latest 2 news items per company
                        all_news.append({
                            "title": item.get("title", ""),
                            "content": item.get("summary", ""),
                            "source": item.get("publisher", "Yahoo Finance"),
                            "published_date": datetime.fromtimestamp(
                                item.get("providerPublishTime", datetime.now().timestamp())
                            ).isoformat()
                        })
            except Exception as e:
                print(f"Error fetching news for {name}: {e}")
        return all_news

    async def analyze_market_trends(self, stock_data: Dict) -> str:
        """Analyze market trends from real stock data"""
        analysis = ["AI市场分析："]
        
        # Analyze market leaders
        sorted_by_cap = sorted(
            stock_data.items(),
            key=lambda x: x[1]["market_cap"],
            reverse=True
        )
        
        # Market leaders
        analysis.append("\n市场领导者：")
        for name, data in sorted_by_cap[:3]:
            change = data["change"]
            direction = "上涨" if change > 0 else "下跌"
            analysis.append(
                f"- {name}: 市值 {data['market_cap']/1e9:.1f}B, "
                f"股价 {direction} {abs(change):.1f}%"
            )
        
        # Market momentum
        gainers = [name for name, data in stock_data.items() if data["change"] > 0]
        analysis.append(f"\n市场动能：")
        analysis.append(f"- {len(gainers)}/{len(stock_data)} 的AI相关公司股价上涨")
        
        return "\n".join(analysis)

async def get_daily_market_summary() -> Dict:
    """Get daily market summary for AI industry"""
    collector = MarketDataCollector()
    stock_data = await collector.fetch_stock_data()
    news_data = await collector.fetch_company_news()
    analysis = await collector.analyze_market_trends(stock_data)
    
    return {
        "stock_data": stock_data,
        "news": news_data,
        "analysis": analysis,
        "timestamp": datetime.now().isoformat()
    }

# Test function
async def test_market_data():
    """Test market data collection"""
    summary = await get_daily_market_summary()
    print(json.dumps(summary, indent=2))
    return summary

if __name__ == "__main__":
    asyncio.run(test_market_data())
