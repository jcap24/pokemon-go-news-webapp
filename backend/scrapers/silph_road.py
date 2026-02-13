import requests
from bs4 import BeautifulSoup
from datetime import datetime


class SilphRoadScraper:
    """Scraper for The Silph Road news and research."""

    BASE_URL = "https://thesilphroad.com"
    NEWS_URL = f"{BASE_URL}/news"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_news(self):
        """Scrape news from The Silph Road."""
        try:
            response = self.session.get(self.NEWS_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news_items = []
            # The Silph Road uses different HTML structure - adjust as needed
            articles = soup.find_all('article', class_='news-article')[:15]

            if not articles:
                # Fallback to generic article selector
                articles = soup.find_all('article')[:15]

            for article in articles:
                try:
                    news_item = {}

                    # Extract title
                    title_elem = article.find('h2') or article.find('h3') or article.find('a', class_='title')
                    if title_elem:
                        news_item['title'] = title_elem.get_text(strip=True)

                    # Extract URL
                    link_elem = article.find('a')
                    if link_elem and link_elem.get('href'):
                        href = link_elem['href']
                        news_item['url'] = self.BASE_URL + href if href.startswith('/') else href

                    # Extract content/excerpt
                    content_elem = article.find('p', class_='excerpt') or article.find('p')
                    if content_elem:
                        news_item['content'] = content_elem.get_text(strip=True)[:1000]
                    else:
                        news_item['content'] = ""

                    # Extract date
                    date_elem = article.find('time') or article.find('span', class_='date')
                    if date_elem:
                        news_item['published_date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)

                    news_item['source'] = 'The Silph Road'

                    if 'title' in news_item and 'url' in news_item:
                        news_items.append(news_item)

                except Exception as e:
                    print(f"Error parsing Silph Road article: {e}")
                    continue

            print(f"Silph Road: Scraped {len(news_items)} news items")
            return news_items

        except Exception as e:
            print(f"Error scraping Silph Road news: {e}")
            return []

    def scrape_events(self):
        """Extract events from The Silph Road news."""
        try:
            news_items = self.scrape_news()
            events = []

            # Convert news items that are events into event format
            for news in news_items:
                if self._is_event_post(news['title']):
                    event = {
                        'title': news['title'],
                        'url': news['url'],
                        'description': news.get('content', ''),
                        'source': 'The Silph Road',
                        'event_type': self._infer_event_type(news['title'])
                    }
                    events.append(event)

            print(f"Silph Road: Extracted {len(events)} events from news")
            return events

        except Exception as e:
            print(f"Error extracting events from Silph Road: {e}")
            return []

    def _is_event_post(self, title):
        """Check if a news post is about an event."""
        event_keywords = [
            'community day', 'event', 'spotlight hour', 'raid',
            'research', 'special', 'celebration', 'GO Fest',
            'featured', 'bonus', 'challenge', 'season'
        ]
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in event_keywords)

    def _infer_event_type(self, title):
        """Infer event type from title."""
        title_lower = title.lower()
        if 'community day' in title_lower:
            return 'Community Day'
        elif 'spotlight hour' in title_lower:
            return 'Spotlight Hour'
        elif 'raid' in title_lower:
            return 'Raid Event'
        elif 'go battle' in title_lower or 'gbl' in title_lower:
            return 'GO Battle League'
        elif 'research' in title_lower:
            return 'Research Event'
        elif 'go fest' in title_lower:
            return 'GO Fest'
        elif 'season' in title_lower:
            return 'Season Event'
        else:
            return 'Special Event'
