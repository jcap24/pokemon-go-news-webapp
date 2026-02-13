import requests
from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
import html


class OfficialBlogScraper:
    """Scraper for official Pokemon GO blog."""

    BASE_URL = "https://pokemongolive.com"
    BLOG_URL = f"{BASE_URL}/en/news/"
    RSS_URL = "https://pokemongolive.com/en/rss"  # If available

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_news(self):
        """Scrape news from official Pokemon GO blog."""
        # Try RSS feed first, fall back to HTML scraping
        news_items = self._try_rss_feed()
        if not news_items:
            news_items = self._scrape_html()

        print(f"Official Blog: Scraped {len(news_items)} news items")
        return news_items

    def _clean_html_content(self, content):
        """Remove HTML tags and decode HTML entities."""
        if not content:
            return ""
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        text = html.unescape(text)
        return text

    def _try_rss_feed(self):
        """Try to parse RSS feed if available."""
        try:
            feed = feedparser.parse(self.RSS_URL)
            news_items = []

            for entry in feed.entries[:15]:  # Limit to 15 most recent
                raw_content = entry.get('summary', '')
                clean_content = self._clean_html_content(raw_content)[:1000]

                news_item = {
                    'title': html.unescape(entry.get('title', '')),
                    'url': entry.get('link', ''),
                    'content': clean_content,
                    'published_date': entry.get('published', ''),
                    'source': 'Official Blog'
                }
                if news_item['title'] and news_item['url']:
                    news_items.append(news_item)

            return news_items

        except Exception as e:
            print(f"Error parsing RSS feed: {e}")
            return []

    def _scrape_html(self):
        """Scrape news from HTML if RSS is unavailable."""
        try:
            response = self.session.get(self.BLOG_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news_items = []
            # Look for article elements
            articles = soup.find_all('article')[:15] or soup.find_all('div', class_='news-item')[:15]

            for article in articles:
                try:
                    news_item = {}

                    # Extract title
                    title_elem = article.find('h2') or article.find('h3') or article.find('h1')
                    if title_elem:
                        news_item['title'] = title_elem.get_text(strip=True)

                    # Extract URL
                    link_elem = article.find('a')
                    if link_elem and link_elem.get('href'):
                        href = link_elem['href']
                        news_item['url'] = self.BASE_URL + href if href.startswith('/') else href

                    # Extract content
                    content_elem = article.find('p') or article.find('div', class_='excerpt')
                    if content_elem:
                        news_item['content'] = content_elem.get_text(strip=True)[:1000]

                    # Extract date
                    date_elem = article.find('time') or article.find('span', class_='date')
                    if date_elem:
                        news_item['published_date'] = date_elem.get('datetime') or date_elem.get_text(strip=True)

                    news_item['source'] = 'Official Blog'

                    if 'title' in news_item and 'url' in news_item:
                        news_items.append(news_item)

                except Exception as e:
                    print(f"Error parsing official blog article: {e}")
                    continue

            return news_items

        except Exception as e:
            print(f"Error scraping official blog HTML: {e}")
            return []

    def scrape_events(self):
        """Scrape events from official blog (events are usually in news posts)."""
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
                        'source': 'Official Blog',
                        'event_type': self._infer_event_type(news['title'])
                    }
                    events.append(event)

            print(f"Official Blog: Extracted {len(events)} events from news")
            return events

        except Exception as e:
            print(f"Error extracting events from official blog: {e}")
            return []

    def _is_event_post(self, title):
        """Check if a news post is about an event."""
        event_keywords = [
            'community day', 'event', 'spotlight hour', 'raid',
            'research', 'special', 'celebration', 'GO Fest',
            'featured', 'bonus', 'challenge'
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
