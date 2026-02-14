from flask import Blueprint, jsonify, request
from services.pokemon_assistant import PokemonAssistant
from services.event_recommender import EventRecommender

assistant_bp = Blueprint('assistant', __name__, url_prefix='/api/assistant')


@assistant_bp.route('/ask', methods=['POST'])
def ask_question():
    """
    Ask the AI assistant a question.

    Request body:
    {
        "question": "Should I evolve my Eevee now?",
        "conversation_history": [...]  # Optional
    }
    """
    try:
        data = request.get_json()

        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'Question is required'
            }), 400

        question = data['question'].strip()

        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400

        # Get conversation history if provided
        conversation_history = data.get('conversation_history', None)

        # Initialize assistant and get response
        assistant = PokemonAssistant()
        result = assistant.ask(question, conversation_history)

        if result['success']:
            return jsonify({
                'success': True,
                'response': result['response'],
                'model': result.get('model', 'unknown')
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'response': result.get('response', 'Sorry, I encountered an error.')
            }), 500

    except Exception as e:
        print(f"Error in ask_question endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'response': 'Sorry, something went wrong. Please try again!'
        }), 500


@assistant_bp.route('/suggestions', methods=['GET'])
def get_suggestions():
    """Get example questions users can ask."""
    suggestions = [
        "Should I power up my Mewtwo for raids or PvP?",
        "What's the best moveset for Garchomp?",
        "When should I use a Lucky Egg?",
        "How do I get more Stardust quickly?",
        "What are the best counters for Dialga raids?",
        "Should I evolve my shiny Eevee or wait?",
        "How does the friendship system work?",
        "What Pokemon should I prioritize for Community Day?",
        "Is it worth raiding for this boss?",
        "How can I improve my GO Battle League team?",
    ]

    return jsonify({
        'success': True,
        'suggestions': suggestions
    })


@assistant_bp.route('/recommend-events', methods=['POST'])
def recommend_events():
    """
    Get personalized event recommendations based on user preferences.

    Request body:
    {
        "playstyle": "casual|moderate|hardcore",
        "goals": ["shiny_hunting", "pvp", "raids", "collecting", "xp", "stardust"],
        "time_available": "limited|moderate|plenty",
        "additional_notes": "Optional notes about preferences"
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'Request body is required'
            }), 400

        # Validate required fields
        playstyle = data.get('playstyle', 'moderate')
        goals = data.get('goals', [])
        time_available = data.get('time_available', 'moderate')
        additional_notes = data.get('additional_notes', '')

        # Build user preferences
        user_preferences = {
            'playstyle': playstyle,
            'goals': goals,
            'time_available': time_available,
            'additional_notes': additional_notes
        }

        # Initialize recommender and get recommendations
        recommender = EventRecommender()
        result = recommender.get_recommendations(user_preferences)

        if result['success']:
            return jsonify({
                'success': True,
                'recommendations': result['recommendations'],
                'events_analyzed': result.get('events_analyzed', 0),
                'model': result.get('model', 'unknown')
            })
        else:
            return jsonify({
                'success': False,
                'error': result.get('error', 'Unknown error'),
                'recommendations': result.get('recommendations', 'Sorry, I encountered an error.')
            }), 500

    except Exception as e:
        print(f"Error in recommend_events endpoint: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'recommendations': 'Sorry, something went wrong. Please try again!'
        }), 500


@assistant_bp.route('/health', methods=['GET'])
def health_check():
    """Check if the assistant service is available."""
    try:
        assistant = PokemonAssistant()
        return jsonify({
            'success': True,
            'status': 'ready',
            'model': assistant.model
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e)
        }), 500
