"""AI-powered Pokemon GO assistant using Claude."""
import os
from anthropic import Anthropic


class PokemonAssistant:
    """AI assistant for Pokemon GO questions and advice."""

    def __init__(self):
        """Initialize the Anthropic client."""
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-haiku-20240307"  # Using Haiku - fast and efficient

        # System prompt with Pokemon GO expertise
        self.system_prompt = """You are an expert Pokemon GO assistant with deep knowledge of:
- Game mechanics and features
- Pokemon stats, types, and movesets
- Raid battles and counters
- PvP (GO Battle League) strategies
- Events, Community Days, and special features
- Resource management (Stardust, Candy, items)
- Evolution strategies and timing
- Trading and friendship systems
- Team building and optimization

Provide helpful, accurate, and concise advice. When giving recommendations:
- Consider the current meta and game state
- Prioritize accessible options for casual and F2P players
- Explain your reasoning briefly
- Be encouraging and positive

If you don't know something specific or if information might be outdated, acknowledge it.
Keep responses conversational and friendly, but informative."""

    def ask(self, question, conversation_history=None):
        """
        Ask the assistant a question.

        Args:
            question: The user's question
            conversation_history: Optional list of previous messages [{"role": "user/assistant", "content": "..."}]

        Returns:
            dict with 'response' and 'success' keys
        """
        try:
            # Build messages array
            messages = []

            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history)

            # Add current question
            messages.append({
                "role": "user",
                "content": question
            })

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system_prompt,
                messages=messages
            )

            # Extract response text
            assistant_response = response.content[0].text

            return {
                'success': True,
                'response': assistant_response,
                'model': self.model
            }

        except Exception as e:
            print(f"Error getting AI response: {e}")
            return {
                'success': False,
                'response': "I'm having trouble connecting right now. Please try again in a moment!",
                'error': str(e)
            }

    def get_quick_answer(self, question):
        """
        Get a quick answer without conversation history.
        Useful for one-off questions.
        """
        return self.ask(question, conversation_history=None)
