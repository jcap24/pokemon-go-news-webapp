import requests
from bs4 import BeautifulSoup
from datetime import datetime


class SerebiiScraper:
    """Scraper for Serebii Pokemon GO news."""

    BASE_URL = "https://www.serebii.net"
    NEWS_URL = f"{BASE_URL}/pokemongo/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_news(self):
        """Scrape news from Serebii Pokemon GO section."""
        try:
            response = self.session.get(self.NEWS_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news_items = []

            # Serebii typically has news in a specific content div
            content = soup.find('div', class_='content') or soup.find('td', class_='content')

            if content:
                # Look for news entries (typically in tables or divs)
                news_tables = content.find_all('table', class_='news')[:10]

                for table in news_tables:
                    try:
                        news_item = {}

                        # Extract title and link
                        title_link = table.find('a')
                        if title_link:
                            news_item['title'] = title_link.get_text(strip=True)
                            href = title_link.get('href', '')
                            news_item['url'] = self.BASE_URL + href if href.startswith('/') else href

                        # Extract content
                        content_text = table.get_text(strip=True)
                        if content_text:
                            news_item['content'] = content_text[:1000]

                        # Extract date if available
                        date_elem = table.find('span', class_='date')
                        if date_elem:
                            news_item['published_date'] = date_elem.get_text(strip=True)

                        news_item['source'] = 'Serebii'

                        if 'title' in news_item and 'url' in news_item:
                            news_items.append(news_item)

                    except Exception as e:
                        print(f"Error parsing Serebii news item: {e}")
                        continue

            print(f"Serebii: Scraped {len(news_items)} news items")
            return news_items

        except Exception as e:
            print(f"Error scraping Serebii news: {e}")
            return []

    def scrape_events(self):
        """Extract events from Serebii news."""
        try:
            news_items = self.scrape_news()
            events = []

            for news in news_items:
                if self._is_event_post(news.get('title', '')):
                    event = {
                        'title': news['title'],
                        'url': news['url'],
                        'description': news.get('content', ''),
                        'source': 'Serebii',
                        'event_type': self._infer_event_type(news['title'])
                    }
                    events.append(event)

            print(f"Serebii: Extracted {len(events)} events from news")
            return events

        except Exception as e:
            print(f"Error extracting events from Serebii: {e}")
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
        else:
            return 'Special Event'
