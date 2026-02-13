from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()

class NewsItem(Base):
    __tablename__ = 'news_items'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    content = Column(Text)
    summary = Column(Text)
    source = Column(String(100), nullable=False)
    url = Column(String(1000), unique=True, nullable=False)
    published_date = Column(DateTime)
    scraped_date = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'summary': self.summary,
            'source': self.source,
            'url': self.url,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'scraped_date': self.scraped_date.isoformat() if self.scraped_date else None
        }


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    event_type = Column(String(100))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    summary = Column(Text)
    source = Column(String(100), nullable=False)
    url = Column(String(1000))
    scraped_date = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'event_type': self.event_type,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'description': self.description,
            'summary': self.summary,
            'source': self.source,
            'url': self.url,
            'scraped_date': self.scraped_date.isoformat() if self.scraped_date else None
        }


class RaidBoss(Base):
    __tablename__ = 'raid_bosses'
    __table_args__ = (Index('idx_raid_boss_name', 'name'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    pokemon_id = Column(Integer)
    tier = Column(String(20))
    cp_min = Column(Integer)
    cp_max = Column(Integer)
    cp_boosted_min = Column(Integer)
    cp_boosted_max = Column(Integer)
    types = Column(String(100))
    weaknesses = Column(String(200))
    weather_boost = Column(String(100))
    is_active = Column(Boolean, default=True)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    image_url = Column(String(500))
    scraped_date = Column(DateTime, default=datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    counters = relationship("RaidCounter", backref="raid_boss", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'pokemon_id': self.pokemon_id,
            'tier': self.tier,
            'cp_min': self.cp_min,
            'cp_max': self.cp_max,
            'cp_boosted_min': self.cp_boosted_min,
            'cp_boosted_max': self.cp_boosted_max,
            'types': self.types.split(',') if self.types else [],
            'weaknesses': self.weaknesses.split(',') if self.weaknesses else [],
            'weather_boost': self.weather_boost.split(',') if self.weather_boost else [],
            'is_active': self.is_active,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'image_url': self.image_url,
            'scraped_date': self.scraped_date.isoformat() if self.scraped_date else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }


class RaidCounter(Base):
    __tablename__ = 'raid_counters'
    __table_args__ = (
        Index('idx_raid_counter_boss_id', 'raid_boss_id'),
        Index('idx_raid_counter_rank', 'rank'),
    )

    id = Column(Integer, primary_key=True)
    raid_boss_id = Column(Integer, ForeignKey('raid_bosses.id'), nullable=False)
    pokemon_name = Column(String(100), nullable=False)
    rank = Column(Integer, nullable=False)
    fast_move = Column(String(50))
    charge_move = Column(String(50))
    pokemon_types = Column(String(100))
    dps = Column(Float)
    tdo = Column(Float)
    ttw = Column(Float)
    is_shadow = Column(Boolean, default=False)
    is_mega = Column(Boolean, default=False)
    is_legendary = Column(Boolean, default=False)
    scraped_date = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'raid_boss_id': self.raid_boss_id,
            'pokemon_name': self.pokemon_name,
            'rank': self.rank,
            'fast_move': self.fast_move,
            'charge_move': self.charge_move,
            'pokemon_types': self.pokemon_types.split(',') if self.pokemon_types else [],
            'dps': self.dps,
            'tdo': self.tdo,
            'ttw': self.ttw,
            'is_shadow': self.is_shadow,
            'is_mega': self.is_mega,
            'is_legendary': self.is_legendary,
            'scraped_date': self.scraped_date.isoformat() if self.scraped_date else None
        }


# Database setup
db_url = os.getenv('DATABASE_URL', 'sqlite:///pokemon_go_news.db')
engine = create_engine(db_url)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal


def init_db():
    """Initialize the database, creating all tables."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully!")


def get_db():
    """Get a database session."""
    session = SessionLocal()
    try:
        return session
    finally:
        pass  # Session will be closed by the caller
