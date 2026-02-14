from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import models and services
from models.database import init_db
from services.scheduler import setup_scheduler, scrape_all_sources
from routes import news_bp, events_bp, raids_bp, assistant_bp

# Create Flask app
app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(news_bp)
app.register_blueprint(events_bp)
app.register_blueprint(raids_bp)
app.register_blueprint(assistant_bp)


@app.route('/')
def index():
    """API root endpoint."""
    return jsonify({
        'message': 'Pokemon GO News API',
        'version': '1.0',
        'endpoints': {
            'news': '/api/news',
            'events': '/api/events',
            'calendar': '/api/events/calendar',
            'raids': '/api/raids',
            'assistant': '/api/assistant',
            'scrape': '/api/scrape'
        }
    })


@app.route('/api/scrape', methods=['POST'])
def manual_scrape():
    """Manually trigger scraping of all sources."""
    try:
        scrape_all_sources()
        return jsonify({
            'success': True,
            'message': 'Scraping completed successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Pokemon GO News API'
    })


def initialize_app():
    """Initialize database and scheduler."""
    print("Initializing database...")
    init_db()

    print("Setting up scheduler...")
    scheduler = setup_scheduler()

    # Run initial scrape
    print("Running initial scrape...")
    try:
        scrape_all_sources()
    except Exception as e:
        print(f"Initial scrape failed: {e}")

    return scheduler


if __name__ == '__main__':
    # Initialize
    scheduler = initialize_app()

    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True') == 'True'

    try:
        app.run(host='0.0.0.0', port=port, debug=debug)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("Shutting down...")
