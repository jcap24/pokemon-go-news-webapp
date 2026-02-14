"""Smart Event Recommender using Claude AI."""
import os
from anthropic import Anthropic
from datetime import datetime
from models.database import Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class EventRecommender:
    """AI-powered event recommender for Pokemon GO."""

    def __init__(self):
        """Initialize the Anthropic client and database session."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-haiku-20240307"  # Using Haiku - fast and efficient

        # System prompt for event recommendation
        self.system_prompt = """You are an expert Pokemon GO event analyst and advisor. Your role is to analyze upcoming events and provide personalized recommendations based on player preferences.

When analyzing events, consider:
- Player's playstyle (casual, hardcore, competitive)
- Player's goals (shiny hunting, PvP, raiding, collecting, XP grinding, stardust farming)
- Time constraints (how much time they can play)
- Resource priorities (stardust, candy, XP, rare Pokemon)

For each recommended event, provide:
1. Why this event matches their goals
2. Optimal strategy for maximizing value
3. What to prioritize during the event
4. Time investment needed
5. Expected rewards/benefits

Be encouraging, practical, and specific. Tailor advice to their stated preferences."""

    def get_upcoming_events(self):
        """Fetch upcoming and active events from the database."""
        try:
            # Create database session
            db_path = os.getenv('DATABASE_URL', 'sqlite:///pokemon_go.db')
            engine = create_engine(db_path)
            Session = sessionmaker(bind=engine)
            session = Session()

            # Get events that haven't ended yet
            now = datetime.now()
            events = session.query(Event).filter(
                Event.end_date >= now
            ).order_by(Event.start_date).all()

            session.close()

            # Convert to dictionaries
            event_list = []
            for event in events:
                event_list.append({
                    'name': event.name,
                    'type': event.event_type,
                    'start_date': event.start_date.strftime('%Y-%m-%d %H:%M') if event.start_date else 'TBD',
                    'end_date': event.end_date.strftime('%Y-%m-%d %H:%M') if event.end_date else 'TBD',
                    'description': event.description or 'No description available',
                    'source': event.source
                })

            return event_list

        except Exception as e:
            print(f"Error fetching events: {e}")
            return []

    def get_recommendations(self, user_preferences):
        """
        Get personalized event recommendations based on user preferences.

        Args:
            user_preferences: Dictionary with keys:
                - playstyle: str (casual, moderate, hardcore)
                - goals: list of str (shiny_hunting, pvp, raids, collecting, xp, stardust)
                - time_available: str (limited, moderate, plenty)
                - additional_notes: str (optional)

        Returns:
            dict with 'success', 'recommendations', and optionally 'error'
        """
        try:
            # Fetch upcoming events
            events = self.get_upcoming_events()

            if not events:
                return {
                    'success': True,
                    'recommendations': "No upcoming events found at the moment. Check back soon!",
                    'events_analyzed': 0
                }

            # Build the user profile text
            playstyle = user_preferences.get('playstyle', 'moderate')
            goals = user_preferences.get('goals', [])
            time_available = user_preferences.get('time_available', 'moderate')
            additional_notes = user_preferences.get('additional_notes', '')

            goals_text = ', '.join(goals) if goals else 'general gameplay'

            user_profile = f"""Player Profile:
- Playstyle: {playstyle}
- Primary Goals: {goals_text}
- Time Available: {time_available}
{f'- Additional Notes: {additional_notes}' if additional_notes else ''}"""

            # Build the events text
            events_text = "\n\n".join([
                f"Event: {e['name']}\n"
                f"Type: {e['type']}\n"
                f"Dates: {e['start_date']} to {e['end_date']}\n"
                f"Description: {e['description']}"
                for e in events
            ])

            # Create the prompt
            prompt = f"""{user_profile}

Upcoming Events:
{events_text}

Please analyze these events and recommend which ones this player should prioritize. For each recommended event:

1. Explain why it matches their goals and playstyle
2. Provide an optimal strategy for participating
3. Suggest what to prioritize during the event
4. Estimate time investment needed
5. Describe expected rewards/benefits

Format your response as a numbered list of recommendations, starting with the most relevant events first. Be specific, encouraging, and practical."""

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,  # More tokens for detailed recommendations
                system=self.system_prompt,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract response text
            recommendations = response.content[0].text

            return {
                'success': True,
                'recommendations': recommendations,
                'events_analyzed': len(events),
                'model': self.model
            }

        except Exception as e:
            print(f"Error getting event recommendations: {e}")
            return {
                'success': False,
                'recommendations': "I'm having trouble analyzing events right now. Please try again in a moment!",
                'error': str(e)
            }
