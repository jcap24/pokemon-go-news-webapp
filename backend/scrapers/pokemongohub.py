import requests
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
import html


class PokemonGoHubScraper:
    """Scraper for Pokemon GO Hub news."""

    BASE_URL = "https://pokemongohub.net"
    NEWS_URL = f"{BASE_URL}/post/news/"
    RSS_URL = f"{BASE_URL}/feed/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_news(self):
        """Scrape news from Pokemon GO Hub."""
        # Try RSS feed first
        news_items = self._try_rss_feed()
        if not news_items:
            news_items = self._scrape_html()

        print(f"Pokemon GO Hub: Scraped {len(news_items)} news items")
        return news_items

    def _clean_html_content(self, content):
        """Remove HTML tags and decode HTML entities."""
        if not content:
            return ""
        # Parse HTML and extract text
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        # Decode HTML entities
        text = html.unescape(text)
        return text

    def _try_rss_feed(self):
        """Try to parse RSS feed."""
        try:
            feed = feedparser.parse(self.RSS_URL)
            news_items = []

            for entry in feed.entries[:15]:
                # Clean the content
                raw_content = entry.get('summary', '')
                clean_content = self._clean_html_content(raw_content)[:1000]

                news_item = {
                    'title': html.unescape(entry.get('title', '')),
                    'url': entry.get('link', ''),
                    'content': clean_content,
                    'published_date': entry.get('published', ''),
                    'source': 'Pokemon GO Hub'
                }
                if news_item['title'] and news_item['url']:
                    news_items.append(news_item)

            return news_items

        except Exception as e:
            print(f"Error parsing Pokemon GO Hub RSS: {e}")
            return []

    def _scrape_html(self):
        """Scrape news from HTML."""
        try:
            response = self.session.get(self.NEWS_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news_items = []

            # Look for article elements
            articles = soup.find_all('article', class_='post')[:15]

            for article in articles:
                try:
                    news_item = {}

                    # Extract title
                    title_elem = article.find('h2', class_='entry-title') or article.find('h3')
                    if title_elem:
                        link = title_elem.find('a')
                        if link:
                            news_item['title'] = html.unescape(link.get_text(strip=True))
                            news_item['url'] = link.get('href', '')

                    # Extract content
                    content_elem = article.find('div', class_='entry-content') or article.find('div', class_='excerpt')
                    if content_elem:
                        clean_content = self._clean_html_content(str(content_elem))
                        news_item['content'] = clean_content[:1000]

                    # Extract date
                    date_elem = article.find('time') or article.find('span', class_='date')
                    if date_elem:
                        news_item['published_date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)

                    news_item['source'] = 'Pokemon GO Hub'

                    if 'title' in news_item and 'url' in news_item:
                        news_items.append(news_item)

                except Exception as e:
                    print(f"Error parsing Pokemon GO Hub article: {e}")
                    continue

            return news_items

        except Exception as e:
            print(f"Error scraping Pokemon GO Hub HTML: {e}")
            return []

    def scrape_events(self):
        """Extract events from Pokemon GO Hub news."""
        try:
            news_items = self.scrape_news()
            events = []

            for news in news_items:
                if self._is_event_post(news.get('title', '')):
                    event = {
                        'title': news['title'],
                        'url': news['url'],
                        'description': news.get('content', ''),
                        'source': 'Pokemon GO Hub',
                        'event_type': self._infer_event_type(news['title'])
                    }
                    events.append(event)

            print(f"Pokemon GO Hub: Extracted {len(events)} events from news")
            return events

        except Exception as e:
            print(f"Error extracting events from Pokemon GO Hub: {e}")
            return []

    def _is_event_post(self, title):
        """Check if a news post is about an event."""
        event_keywords = [
            'community day', 'event', 'spotlight hour', 'raid',
            'research', 'special', 'celebration', 'GO Fest',
            'featured', 'bonus', 'challenge', 'announced'
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
        else:
            return 'Special Event'
