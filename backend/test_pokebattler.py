"""Test script to check Pokebattler scraper."""
import sys
sys.path.insert(0, 'C:\\Users\\Josh\\pokemon-go-news-webapp\\backend')

from scrapers.pokebattler import PokebattlerScraper

# Test scraping
scraper = PokebattlerScraper()

print("Testing Pokebattler scraper...")
print("=" * 50)

# Test scraping raid bosses
print("\n1. Scraping raid bosses...")
bosses = scraper.scrape_raid_bosses()
print(f"Found {len(bosses)} raid bosses")

if bosses:
    print("\nFirst 3 bosses:")
    for boss in bosses[:3]:
        print(f"  - {boss.get('name')} (Tier {boss.get('tier')})")
else:
    print("No bosses found. The HTML structure might have changed.")
    print("\nTrying to fetch the page to see what we get...")

    # Test basic HTTP request
    import requests
    response = scraper.session.get(scraper.RAIDS_URL, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Content Length: {len(response.content)} bytes")

    # Save HTML for inspection
    with open('pokebattler_debug.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("Saved response to pokebattler_debug.html for inspection")

print("\n" + "=" * 50)
