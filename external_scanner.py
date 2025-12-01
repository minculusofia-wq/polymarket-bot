import requests
from newsapi import NewsApiClient
import config
from datetime import datetime, timedelta

class ExternalScanner:
    def __init__(self):
        self.news_api = None
        if config.NEWS_API_KEY:
            try:
                self.news_api = NewsApiClient(api_key=config.NEWS_API_KEY)
                print("✅ NewsAPI Client initialized")
            except Exception as e:
                print(f"❌ Failed to init NewsAPI: {e}")
        
        # Reddit placeholder (disabled for now)
        self.reddit = None

    def get_crypto_news(self):
        """Fetch top crypto and market news."""
        if not self.news_api:
            return []
            
        try:
            # Fetch news about crypto, polymarket, election
            articles = self.news_api.get_everything(
                q='crypto OR bitcoin OR polymarket OR election',
                language='en',
                sort_by='publishedAt',
                page_size=5
            )
            
            news_items = []
            for article in articles.get('articles', []):
                news_items.append({
                    "source": article['source']['name'],
                    "title": article['title'],
                    "url": article['url'],
                    "published_at": article['publishedAt'],
                    "type": "news"
                })
            return news_items
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []

    def scan_all(self):
        """Scan all external sources."""
        return {
            "news": self.get_crypto_news(),
            "reddit": [] # Placeholder
        }

# Global instance
external_scanner = ExternalScanner()
