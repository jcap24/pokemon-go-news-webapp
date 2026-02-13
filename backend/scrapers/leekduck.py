import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re


class LeekDuckScraper:
    """Scraper for LeekDuck Pokemon GO event calendar and news."""

    BASE_URL = "https://leekduck.com"
    EVENTS_URL = f"{BASE_URL}/events/"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape_events(self):
        """Scrape events from LeekDuck's event calendar."""
        try:
            response = self.session.get(self.EVENTS_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            events = []
            # LeekDuck uses event-item-wrapper class for event listings
            event_items = soup.find_all('div', class_='event-item-wrapper')

            for item in event_items:
                try:
                    event = self._parse_event_item(item)
                    if event:
                        events.append(event)
                except Exception as e:
                    print(f"Error parsing LeekDuck event: {e}")
                    continue

            print(f"LeekDuck: Scraped {len(events)} events")
            return events

        except Exception as e:
            print(f"Error scraping LeekDuck events: {e}")
            return []

    def _parse_event_item(self, item):
        """Parse individual event item from LeekDuck."""
        event = {}

        # Extract title
        title_elem = item.find('h2') or item.find('h3') or item.find('a', class_='event-item-link')
        if title_elem:
            event['title'] = title_elem.get_text(strip=True)
        else:
            return None

        # Extract URL
        link_elem = item.find('a', class_='event-item-link')
        if link_elem and link_elem.get('href'):
            event['url'] = self.BASE_URL + link_elem['href'] if link_elem['href'].startswith('/') else link_elem['href']
        else:
            event['url'] = self.EVENTS_URL

        # Extract event type
        type_elem = item.find('span', class_='event-type') or item.find('div', class_='event-type')
        if type_elem:
            event['event_type'] = type_elem.get_text(strip=True)
        else:
            event['event_type'] = self._infer_event_type(event['title'])

        # Extract dates
        date_elem = item.find('div', class_='event-date') or item.find('span', class_='event-date')
        if date_elem:
            date_text = date_elem.get_text(strip=True)
            dates = self._parse_date_range(date_text)
            event['start_date'] = dates.get('start')
            event['end_date'] = dates.get('end')

        # Extract description
        desc_elem = item.find('p', class_='event-description') or item.find('div', class_='event-description')
        if desc_elem:
            event['description'] = desc_elem.get_text(strip=True)
        else:
            event['description'] = ""

        event['source'] = 'LeekDuck'

        return event

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
        elif 'special' in title_lower or 'event' in title_lower:
            return 'Special Event'
        else:
            return 'General Event'

    def _parse_date_range(self, date_text):
        """Parse date range from text."""
        # This is a simplified parser - you may need to enhance it
        # Example formats: "Jan 15 - Jan 17", "February 10, 2024"
        dates = {'start': None, 'end': None}

        try:
            # Try to extract year, month, day
            # For now, return None - you can implement proper date parsing
            # using dateutil.parser or custom regex patterns
            pass
        except Exception:
            pass

        return dates

    def scrape_news(self):
        """Scrape latest news from LeekDuck."""
        try:
            # News posts are on the main page, not /news/
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news_items = []

            # LeekDuck uses <ol> with <li> items for news posts
            news_list = soup.find('ol')
            if not news_list:
                print("LeekDuck: Could not find news list")
                return []

            list_items = news_list.find_all('li', recursive=False)[:10]  # Limit to 10 most recent

            for item in list_items:
                try:
                    news_item = {}

                    # Find the post card
                    post_card = item.find('div', class_='post-card')
                    if not post_card:
                        continue

                    # Find the link element
                    link_elem = post_card.find('a', href=re.compile(r'/posts/'))
                    if not link_elem:
                        continue

                    # Extract URL
                    href = link_elem.get('href', '')
                    news_item['url'] = self.BASE_URL + href if href.startswith('/') else href

                    # Extract title from alt attribute or aria-label
                    title = link_elem.get('alt') or link_elem.get('aria-label')
                    if title:
                        news_item['title'] = title.strip()
                    else:
                        # Try to find h3 or h2 in the post card
                        title_elem = post_card.find(['h3', 'h2', 'h4'])
                        if title_elem:
                            news_item['title'] = title_elem.get_text(strip=True)
                        else:
                            continue

                    # Extract category/tags from post-card-body
                    post_body = post_card.find('div', class_='post-card-body')
                    if post_body:
                        tag_elem = post_body.find('a', class_='tag')
                        if tag_elem:
                            news_item['content'] = tag_elem.get_text(strip=True)
                        else:
                            news_item['content'] = ""
                    else:
                        news_item['content'] = ""

                    # Extract date from data attributes if available
                    if item.get('data-resource-updated-date'):
                        news_item['published_date'] = item.get('data-resource-updated-date')

                    news_item['source'] = 'LeekDuck'

                    if 'title' in news_item and 'url' in news_item:
                        news_items.append(news_item)

                except Exception as e:
                    print(f"Error parsing LeekDuck news item: {e}")
                    continue

            print(f"LeekDuck: Scraped {len(news_items)} news items")
            return news_items

        except Exception as e:
            print(f"Error scraping LeekDuck news: {e}")
            return []
