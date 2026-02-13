from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from dateutil import parser as date_parser
import os


def scrape_all_sources():
    """Background job to scrape all news sources."""
    from scrapers import (
        LeekDuckScraper,
        OfficialBlogScraper,
        SilphRoadScraper,
        SerebiiScraper,
        PokemonGoHubScraper
    )
    from models.database import get_db, NewsItem, Event
    from services.summarizer import AISummarizer

    print("Starting scheduled scraping...")

    db = get_db()
    summarizer = AISummarizer()

    # Initialize scrapers
    leekduck = LeekDuckScraper()
    official = OfficialBlogScraper()
    silph = SilphRoadScraper()
    serebii = SerebiiScraper()
    pokemongohub = PokemonGoHubScraper()

    # Scrape events
    all_events = []
    all_events.extend(leekduck.scrape_events())
    all_events.extend(official.scrape_events())
    all_events.extend(silph.scrape_events())
    all_events.extend(serebii.scrape_events())
    all_events.extend(pokemongohub.scrape_events())

    # Scrape news
    all_news = []
    all_news.extend(leekduck.scrape_news())
    all_news.extend(official.scrape_news())
    all_news.extend(silph.scrape_news())
    all_news.extend(serebii.scrape_news())
    all_news.extend(pokemongohub.scrape_news())

    # Save events to database
    new_events_count = 0
    for event_data in all_events:
        try:
            # Check if event already exists by URL
            existing = db.query(Event).filter_by(url=event_data.get('url')).first()
            if not existing:
                # Generate summary if not exists
                if not event_data.get('summary'):
                    event_data['summary'] = summarizer.summarize_event(
                        event_data.get('title', ''),
                        event_data.get('description', '')
                    )

                event = Event(**event_data)
                db.add(event)
                new_events_count += 1
        except Exception as e:
            print(f"Error saving event: {e}")
            continue

    # Save news to database
    new_news_count = 0
    for news_data in all_news:
        try:
            # Check if news already exists by URL
            existing = db.query(NewsItem).filter_by(url=news_data.get('url')).first()
            if not existing:
                # Generate summary if not exists
                if not news_data.get('summary'):
                    news_data['summary'] = summarizer.summarize_news(
                        news_data.get('title', ''),
                        news_data.get('content', '')
                    )

                # Parse published_date if it's a string
                if news_data.get('published_date') and isinstance(news_data['published_date'], str):
                    try:
                        news_data['published_date'] = date_parser.parse(news_data['published_date'])
                    except:
                        news_data['published_date'] = None

                news = NewsItem(**news_data)
                db.add(news)
                new_news_count += 1
        except Exception as e:
            print(f"Error saving news: {e}")
            continue

    db.commit()
    db.close()

    print(f"Scraping complete: {new_events_count} new events, {new_news_count} new news items")


def scrape_raid_data():
    """Background job to scrape Pokebattler raid data."""
    from scrapers.pokebattler import PokebattlerScraper
    from models.database import get_db, RaidBoss, RaidCounter
    from datetime import datetime

    print("Starting scheduled raid data scraping...")

    db = get_db()
    scraper = PokebattlerScraper()

    try:
        # Scrape all raids and counters
        raid_data = scraper.scrape_all_raids_and_counters()

        updated_count = 0
        added_count = 0

        # Process each raid boss and its counters
        for raid_entry in raid_data:
            boss_data = raid_entry.get('boss_data', {})
            counters_data = raid_entry.get('counters', [])

            if not boss_data.get('name'):
                continue

            # Check if raid boss already exists
            existing_boss = db.query(RaidBoss).filter_by(name=boss_data['name']).first()

            if existing_boss:
                # Update existing boss
                for key, value in boss_data.items():
                    if hasattr(existing_boss, key) and key != 'id':
                        setattr(existing_boss, key, value)
                existing_boss.last_updated = datetime.utcnow()
                raid_boss = existing_boss
                updated_count += 1
            else:
                # Create new boss
                raid_boss = RaidBoss(**boss_data)
                db.add(raid_boss)
                db.flush()  # Get the ID
                added_count += 1

            # Delete old counters for this boss
            db.query(RaidCounter).filter_by(raid_boss_id=raid_boss.id).delete()

            # Add new counters
            for counter_data in counters_data:
                counter_data['raid_boss_id'] = raid_boss.id
                counter = RaidCounter(**counter_data)
                db.add(counter)

        db.commit()
        print(f"Raid scraping complete: {added_count} added, {updated_count} updated")

    except Exception as e:
        print(f"Error scraping raid data: {e}")
        db.rollback()
    finally:
        db.close()


def setup_scheduler():
    """Set up the background scheduler for periodic scraping."""
    scheduler = BackgroundScheduler()

    # Get scraping interval from environment (default 30 minutes)
    interval_minutes = int(os.getenv('SCRAPE_INTERVAL', 30))

    # Schedule scraping job for news and events
    scheduler.add_job(
        func=scrape_all_sources,
        trigger=IntervalTrigger(minutes=interval_minutes),
        id='scrape_pokemon_go_news',
        name='Scrape Pokemon GO news and events',
        replace_existing=True
    )

    # Get raid scraping interval from environment (default 6 hours)
    raid_interval_hours = int(os.getenv('RAID_SCRAPE_INTERVAL', 6))

    # Schedule raid scraping job
    scheduler.add_job(
        func=scrape_raid_data,
        trigger=IntervalTrigger(hours=raid_interval_hours),
        id='scrape_raid_counters',
        name='Scrape Pokebattler raid counters',
        replace_existing=True
    )

    scheduler.start()
    print(f"Scheduler started: Will scrape news every {interval_minutes} minutes and raids every {raid_interval_hours} hours")

    return scheduler
