import aiohttp
from datetime import datetime, timedelta
from typing import List, Dict
import json

class ProgrammingNewsCollector:
    def __init__(self):
        self.github_api = "https://api.github.com"
        self.stackoverflow_api = "https://api.stackexchange.com/2.3"
        
    async def fetch_github_trends(self) -> List[Dict]:
        """Fetch trending AI/ML repositories from GitHub"""
        async with aiohttp.ClientSession() as session:
            # Search for AI/ML repositories created in the last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            query = f"q=topic:artificial-intelligence+topic:machine-learning+created:>{yesterday}&sort=stars&order=desc"
            
            async with session.get(f"{self.github_api}/search/repositories?{query}") as response:
                if response.status == 200:
                    data = await response.json()
                    return [{
                        "title": repo["name"],
                        "description": repo["description"] or "",
                        "url": repo["html_url"],
                        "stars": repo["stargazers_count"],
                        "language": repo["language"] or "Unknown",
                        "created_at": repo["created_at"]
                    } for repo in data.get("items", [])[:5]]
                return []

    async def fetch_stackoverflow_questions(self) -> List[Dict]:
        """Fetch recent AI/ML questions from Stack Overflow"""
        async with aiohttp.ClientSession() as session:
            # Search for AI/ML questions from the last 24 hours
            params = {
                "site": "stackoverflow",
                "tagged": "artificial-intelligence;machine-learning",
                "sort": "votes",
                "order": "desc",
                "fromdate": int((datetime.now() - timedelta(days=1)).timestamp())
            }
            
            async with session.get(f"{self.stackoverflow_api}/questions", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{
                        "title": question["title"],
                        "url": question["link"],
                        "score": question["score"],
                        "tags": question["tags"],
                        "created_at": datetime.fromtimestamp(question["creation_date"]).isoformat()
                    } for question in data.get("items", [])[:5]]
                return []

    def format_news_summary(self, github_trends: List[Dict], stackoverflow_questions: List[Dict]) -> str:
        """Format collected news into a readable summary"""
        summary = ["<h2>AI编程最新动态</h2>"]
        
        # GitHub trends
        summary.append("<h3>GitHub热门AI项目</h3>")
        for repo in github_trends:
            summary.append(
                f"<p><strong>{repo['title']}</strong> ({repo['language']})<br>"
                f"描述：{repo['description']}<br>"
                f"⭐ {repo['stars']} | <a href='{repo['url']}'>查看项目</a></p>"
            )
        
        # Stack Overflow questions
        summary.append("<h3>Stack Overflow热门问题</h3>")
        for question in stackoverflow_questions:
            summary.append(
                f"<p><strong>{question['title']}</strong><br>"
                f"标签：{', '.join(question['tags'])}<br>"
                f"得分：{question['score']} | <a href='{question['url']}'>查看问题</a></p>"
            )
        
        return "\n".join(summary)

async def get_programming_news_summary() -> Dict:
    """Get daily programming news summary"""
    collector = ProgrammingNewsCollector()
    
    # Collect news from different sources
    github_trends = await collector.fetch_github_trends()
    stackoverflow_questions = await collector.fetch_stackoverflow_questions()
    
    # Format news summary
    summary = collector.format_news_summary(github_trends, stackoverflow_questions)
    
    return {
        "github_trends": github_trends,
        "stackoverflow_questions": stackoverflow_questions,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }
