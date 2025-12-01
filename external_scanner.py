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

    def get_coinstats_news(self):
        """Fetch news from CoinStats (Free, No Key)."""
        try:
            url = "https://api.coinstats.app/public/v1/news/latest?skip=0&limit=10"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                news_items = []
                for item in data.get('news', []):
                    news_items.append({
                        "source": item.get('source'),
                        "title": item.get('title'),
                        "url": item.get('link'),
                        "published_at": datetime.fromtimestamp(item.get('feedDate')/1000).isoformat(),
                        "type": "news"
                    })
                return news_items
            return []
        except Exception as e:
            print(f"Error fetching CoinStats news: {e}")
            return []

    def get_reddit_posts(self):
        """Fetch latest posts from r/CryptoCurrency via JSON (No Key)."""
        try:
            url = "https://www.reddit.com/r/CryptoCurrency/new.json?limit=10"
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                posts = []
                for child in data['data']['children']:
                    post = child['data']
                    posts.append({
                        "source": f"r/{post.get('subreddit')}",
                        "title": post.get('title'),
                        "url": f"https://reddit.com{post.get('permalink')}",
                        "published_at": datetime.fromtimestamp(post.get('created_utc')).isoformat(),
                        "score": post.get('score'),
                        "comments": post.get('num_comments'),
                        "type": "social"
                    })
                return posts
            return []
        except Exception as e:
            print(f"Error fetching Reddit posts: {e}")
            return []

    def get_coingecko_events(self):
        """Fetch upcoming events from CoinGecko."""
        try:
            url = "https://api.coingecko.com/api/v3/events"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                events = []
                for event in data.get('data', [])[:5]:
                    events.append({
                        "title": event.get('title'),
                        "description": event.get('description'),
                        "url": event.get('website'),
                        "date": event.get('start_date'),
                        "type": "event"
                    })
                return events
            return []
        except Exception as e:
            print(f"Error fetching CoinGecko events: {e}")
            return []

    def get_lunarcrush_sentiment(self):
        """Fetch social sentiment for top coins via LunarCrush."""
        if not config.LUNARCRUSH_API_KEY:
            return []
            
        try:
            # Fetching data for Bitcoin and Ethereum as a baseline
            url = f"https://lunarcrush.com/api3/coins/global?key={config.LUNARCRUSH_API_KEY}" 
            # Note: LunarCrush V3 endpoint might differ, using a generic approach or specific coin endpoint
            # Let's try listing top coins
            url = f"https://lunarcrush.com/api3/coins?limit=5&sort=galaxy_score&key={config.LUNARCRUSH_API_KEY}"
            
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                items = []
                for coin in data.get('data', []):
                    items.append({
                        "symbol": coin.get('symbol'),
                        "name": coin.get('name'),
                        "galaxy_score": coin.get('galaxy_score'),
                        "sentiment": coin.get('sentiment_relative'), # bullish/bearish
                        "url": f"https://lunarcrush.com/coins/{coin.get('symbol').lower()}",
                        "type": "sentiment"
                    })
                return items
            return []
        except Exception as e:
            print(f"Error fetching LunarCrush: {e}")
            return []

    def get_youtube_videos(self):
        """Fetch latest crypto videos via SerpAPI."""
        if not config.SERPAPI_KEY:
            return []
            
        try:
            params = {
                "engine": "youtube",
                "search_query": "crypto polymarket prediction",
                "api_key": config.SERPAPI_KEY,
                "num": 3
            }
            url = "https://serpapi.com/search.json"
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                videos = []
                for result in data.get('video_results', []):
                    videos.append({
                        "title": result.get('title'),
                        "link": result.get('link'),
                        "channel": result.get('channel', {}).get('name'),
                        "published": result.get('published_date'),
                        "thumbnail": result.get('thumbnail', {}).get('static'),
                        "type": "video"
                    })
                return videos
            return []
        except Exception as e:
            print(f"Error fetching YouTube: {e}")
            return []

    def scan_all(self):
        """Scan all external sources."""
        # Prioritize CoinStats for news if NewsAPI is not set or fails, but here we combine or select.
        # Let's combine NewsAPI (if available) and CoinStats.
        
        news = self.get_crypto_news() # NewsAPI
        coinstats_news = self.get_coinstats_news()
        
        # Merge and sort by date
        all_news = news + coinstats_news
        all_news.sort(key=lambda x: x['published_at'], reverse=True)
        
        return {
            "news": all_news[:10],
            "reddit": self.get_reddit_posts(),
            "events": self.get_coingecko_events(),
            "sentiment": self.get_lunarcrush_sentiment(),
            "videos": self.get_youtube_videos()
        }

# Global instance
external_scanner = ExternalScanner()
