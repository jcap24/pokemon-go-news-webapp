"""Test script to debug LeekDuck scraper."""
import sys
sys.path.insert(0, 'C:\\Users\\Josh\\pokemon-go-news-webapp\\backend')

from scrapers.leekduck import LeekDuckScraper

# Test the scraper
scraper = LeekDuckScraper()

print("=" * 60)
print("Testing LeekDuck News Scraper")
print("=" * 60)

print("\n1. Attempting to scrape news...")
news_items = scraper.scrape_news()

print(f"\n2. Results: Found {len(news_items)} news items")

if news_items:
    print("\n3. First 3 news items:")
    for i, item in enumerate(news_items[:3], 1):
        print(f"\n   Item {i}:")
        print(f"   - Title: {item.get('title', 'N/A')}")
        print(f"   - URL: {item.get('url', 'N/A')}")
        print(f"   - Content: {item.get('content', 'N/A')[:100]}...")
        print(f"   - Source: {item.get('source', 'N/A')}")
        print(f"   - Date: {item.get('published_date', 'N/A')}")
else:
    print("\n3. No news items found. Debugging...")

    # Try to fetch the page and inspect
    import requests
    from bs4 import BeautifulSoup

    try:
        response = scraper.session.get(scraper.BASE_URL, timeout=10)
        print(f"   - Status Code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for ol element
        news_list = soup.find('ol')
        print(f"   - Found <ol> element: {news_list is not None}")

        if news_list:
            list_items = news_list.find_all('li', recursive=False)
            print(f"   - Found {len(list_items)} <li> elements")

            if list_items:
                first_item = list_items[0]
                print(f"\n   First <li> structure:")
                print(f"   {first_item.prettify()[:500]}...")

                # Check for links
                links = first_item.find_all('a')
                print(f"\n   - Found {len(links)} <a> tags in first <li>")
                if links:
                    for j, link in enumerate(links[:3]):
                        print(f"     Link {j+1}: {link.get('href', 'no href')}")
        else:
            print("\n   Could not find <ol> element on page")
            print("   Page title:", soup.find('title').get_text() if soup.find('title') else 'N/A')

    except Exception as e:
        print(f"   Error during debug: {e}")

print("\n" + "=" * 60)
