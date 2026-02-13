import os
from anthropic import Anthropic


class AISummarizer:
    """AI-powered summarization service for Pokemon GO news and events."""

    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")
        self.client = Anthropic(api_key=api_key)
        # Use Claude 3 Haiku - cheaper and more widely available
        self.model = "claude-3-haiku-20240307"

    def summarize_event(self, title, description=""):
        """Generate a player-friendly summary for a Pokemon GO event."""
        prompt = f"""Summarize this Pokemon GO event in 2-3 sentences for players.
Focus on:
- Event dates (if mentioned)
- Featured Pokemon
- Special bonuses or rewards
- Key activities or what players should do

Event Title: {title}
Event Description: {description}

Provide a clear, concise summary that helps players quickly understand what this event is about and what they should know."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            summary = message.content[0].text.strip()
            return summary

        except Exception as e:
            print(f"Error generating summary: {e}")
            return self._generate_fallback_summary(title, description)

    def summarize_news(self, title, content=""):
        """Generate a summary for a Pokemon GO news article."""
        prompt = f"""Summarize this Pokemon GO news in 2-3 sentences.
Focus on the key information that players need to know.

Title: {title}
Content: {content[:500]}

Provide a clear, concise summary."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            summary = message.content[0].text.strip()
            return summary

        except Exception as e:
            print(f"Error generating news summary: {e}")
            return self._generate_fallback_summary(title, content)

    def identify_event_type(self, title, description=""):
        """Use AI to identify the type of Pokemon GO event."""
        prompt = f"""What type of Pokemon GO event is this? Choose ONE from:
- Community Day
- Spotlight Hour
- Raid Event
- GO Battle League
- Research Event
- GO Fest
- Season Event
- Special Event

Title: {title}
Description: {description[:200]}

Respond with only the event type name."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=50,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            event_type = message.content[0].text.strip()
            return event_type

        except Exception as e:
            print(f"Error identifying event type: {e}")
            return "Special Event"

    def _generate_fallback_summary(self, title, content):
        """Generate a simple fallback summary without AI."""
        if content:
            # Take first 150 characters of content as summary
            summary = content[:150].strip()
            if len(content) > 150:
                # Find the last complete sentence within 150 chars
                last_period = summary.rfind('.')
                if last_period > 50:  # If there's a sentence, use it
                    summary = summary[:last_period + 1]
                else:
                    summary += "..."
            return summary
        else:
            return f"Check out: {title}"

    def extract_dates_from_text(self, text):
        """Use AI to extract event dates from text."""
        prompt = f"""Extract the start and end dates from this Pokemon GO event text.
If only one date is mentioned, use it for both start and end.
Return in format: START_DATE | END_DATE (use YYYY-MM-DD format if year is mentioned, otherwise MM-DD)

Text: {text[:500]}

If no dates found, return: NONE"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response = message.content[0].text.strip()
            if response != "NONE" and "|" in response:
                start, end = response.split("|")
                return {
                    'start': start.strip(),
                    'end': end.strip()
                }
            return None

        except Exception as e:
            print(f"Error extracting dates: {e}")
            return None
